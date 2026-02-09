#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
manage_users.py
----------------
External user creation / password hashing / permission grant automation for Config.json

Requires:
  - security.py (hash_password, verify_password)

Config.json structure (expected):
{
  "root_dir": "...",
  "session": { "secret": "...", "ttl_seconds": 86400, ... },
  "users": {
    "admin": {
      "password_hash": "pbkdf2_sha256$...",
      "projects": { "*": {"read": true, "edit": true, "create": true} }
    },
    "A": {
      "password_hash": "pbkdf2_sha256$...",
      "projects": { "Oligomer_IL": {"read": true, "edit": false, "create": false} }
    }
  }
}

Usage examples:
  python manage_users.py list-users
  python manage_users.py list-projects
  python manage_users.py create-user --username A --gen-password --grant "Oligomer_IL:read"
  python manage_users.py set-password --username A --prompt
  python manage_users.py grant --username A --grant "Oligomer_IL:read,edit" --grant "AnotherProj:read"
  python manage_users.py revoke --username A --revoke "Oligomer_IL:edit,create"
  python manage_users.py show-user --username A
  python manage_users.py delete-user --username A

Notes:
  - plaintext password is NEVER stored. Only password_hash is saved.
  - Generated passwords are printed ONCE to console (unless --quiet).
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import secrets
import shutil
import string
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from tqdm import tqdm

# local import
try:
    from security import hash_password
except Exception as e:
    print("ERROR: cannot import security.py (hash_password). Put manage_users.py next to security.py.", file=sys.stderr)
    raise

# ----------------------------
# Logging
# ----------------------------

LOG_NAME = "manage_users"
logger = logging.getLogger(LOG_NAME)


def setup_logging(log_path: Path, level: str = "INFO") -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    # file handler (simple rotation via size)
    from logging.handlers import RotatingFileHandler

    fh = RotatingFileHandler(str(log_path), maxBytes=2_000_000, backupCount=5, encoding="utf-8")
    fh.setFormatter(fmt)
    fh.setLevel(getattr(logging, level.upper(), logging.INFO))

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    sh.setLevel(getattr(logging, level.upper(), logging.INFO))

    # avoid duplicate handlers
    logger.handlers.clear()
    logger.addHandler(fh)
    logger.addHandler(sh)

    logger.info("logging initialized log_path=%s level=%s", log_path, level.upper())


# ----------------------------
# Config I/O
# ----------------------------

DEFAULT_CONFIG_PATH = Path("Config.json")


def read_config(cfg_path: Path) -> Dict[str, Any]:
    if not cfg_path.exists():
        raise FileNotFoundError(f"Config not found: {cfg_path}")

    with cfg_path.open("r", encoding="utf-8") as f:
        cfg = json.load(f)

    if not isinstance(cfg, dict):
        raise ValueError("Config.json root must be a JSON object")

    cfg.setdefault("users", {})
    cfg.setdefault("session", {})
    logger.info("config loaded path=%s", cfg_path)
    return cfg


def ensure_defaults(cfg: Dict[str, Any]) -> Dict[str, Any]:
    # keep user-defined values; only fill missing keys
    cfg.setdefault("root_dir", "")
    cfg.setdefault("users", {})
    cfg.setdefault("session", {})

    sess = cfg["session"]
    sess.setdefault("secret", "CHANGE_ME_TO_A_LONG_RANDOM_STRING")
    sess.setdefault("ttl_seconds", 86400)
    sess.setdefault("cookie_name", "session")
    sess.setdefault("cookie_samesite", "lax")
    sess.setdefault("cookie_secure", False)

    # Normalize users schema
    users = cfg["users"]
    if not isinstance(users, dict):
        raise ValueError("Config.users must be an object/dict")

    for uname, rule in users.items():
        if not isinstance(rule, dict):
            raise ValueError(f"Config.users.{uname} must be an object/dict")
        rule.setdefault("password_hash", "")
        rule.setdefault("projects", {})

    return cfg


def write_config_atomic(cfg_path: Path, cfg: Dict[str, Any], backup: bool = True) -> None:
    cfg_path = cfg_path.resolve()
    cfg_path.parent.mkdir(parents=True, exist_ok=True)

    if backup and cfg_path.exists():
        ts = time.strftime("%Y%m%d_%H%M%S")
        bak = cfg_path.with_suffix(cfg_path.suffix + f".bak_{ts}")
        shutil.copy2(cfg_path, bak)
        logger.info("backup created path=%s", bak)

    tmp_fd, tmp_path = tempfile.mkstemp(prefix="config_", suffix=".json", dir=str(cfg_path.parent))
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(tmp_path, cfg_path)
        logger.info("config saved atomically path=%s", cfg_path)
    finally:
        # if replace failed, tmp may remain
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            logger.warning("failed to remove temp file: %s", tmp_path)


# ----------------------------
# Projects discovery
# ----------------------------

def list_projects_from_root(root_dir: str) -> List[str]:
    if not root_dir:
        return []

    p = Path(root_dir)
    if not p.exists() or not p.is_dir():
        return []

    dirs = []
    children = list(p.iterdir())
    for child in tqdm(children, desc="Scanning projects", unit="item"):
        try:
            if child.is_dir():
                name = child.name
                # skip common junk
                if name.startswith("."):
                    continue
                dirs.append(name)
        except Exception:
            logger.exception("failed to inspect: %s", child)
    return sorted(dirs)


# ----------------------------
# Permissions parsing/apply
# ----------------------------

ACTIONS = ("read", "edit", "create")
ACTION_ALIASES = {
    "r": "read",
    "ro": "read",
    "read": "read",
    "e": "edit",
    "edit": "edit",
    "c": "create",
    "create": "create",
}


@dataclass
class GrantSpec:
    project: str
    actions: List[str]  # normalized actions


def parse_spec_list(specs: List[str], *, mode: str) -> List[GrantSpec]:
    """
    Parse list like:
      ["Oligomer_IL:read,edit", "*:read", "ProjOnly:read"]
    mode: "grant" or "revoke" (for logging only)
    """
    out: List[GrantSpec] = []
    for raw in specs:
        raw = (raw or "").strip()
        if not raw:
            continue
        if ":" not in raw:
            raise ValueError(f"Invalid {mode} spec (missing ':'): {raw}")

        proj, acts = raw.split(":", 1)
        proj = proj.strip()
        if not proj:
            raise ValueError(f"Invalid {mode} spec (empty project): {raw}")

        act_list = []
        for a in acts.split(","):
            a = a.strip().lower()
            if not a:
                continue
            if a not in ACTION_ALIASES:
                raise ValueError(f"Unknown action '{a}' in {mode} spec: {raw} (allowed: read/edit/create)")
            act_list.append(ACTION_ALIASES[a])

        if not act_list:
            raise ValueError(f"Invalid {mode} spec (no actions): {raw}")

        # de-dup preserve order
        seen = set()
        norm = []
        for a in act_list:
            if a not in seen:
                seen.add(a)
                norm.append(a)

        out.append(GrantSpec(project=proj, actions=norm))

    logger.info("parsed %s specs count=%d", mode, len(out))
    return out


def ensure_user_exists(cfg: Dict[str, Any], username: str) -> None:
    users = cfg.get("users") or {}
    if username not in users:
        raise KeyError(f"User does not exist: {username}")


def apply_grants(cfg: Dict[str, Any], username: str, grants: List[GrantSpec], *, validate_projects: bool = False) -> None:
    users = cfg["users"]
    rule = users[username]
    rule.setdefault("projects", {})
    projects_map: Dict[str, Any] = rule["projects"]

    root_dir = cfg.get("root_dir", "")
    existing_projects = set(list_projects_from_root(root_dir)) if (validate_projects and root_dir) else set()

    for g in tqdm(grants, desc=f"Granting perms to {username}", unit="spec"):
        if validate_projects and existing_projects and g.project != "*" and g.project not in existing_projects:
            logger.warning("project not found under root_dir (still granting in config): %s", g.project)

        pr = projects_map.get(g.project)
        if not isinstance(pr, dict):
            pr = {}
            projects_map[g.project] = pr

        for a in g.actions:
            pr[a] = True
            logger.info("grant user=%s project=%s action=%s", username, g.project, a)


def apply_revokes(cfg: Dict[str, Any], username: str, revokes: List[GrantSpec]) -> None:
    users = cfg["users"]
    rule = users[username]
    projects_map: Dict[str, Any] = rule.get("projects") or {}
    rule["projects"] = projects_map

    for r in tqdm(revokes, desc=f"Revoking perms from {username}", unit="spec"):
        pr = projects_map.get(r.project)
        if not isinstance(pr, dict):
            logger.info("revoke skip (no rule): user=%s project=%s", username, r.project)
            continue

        for a in r.actions:
            if a in pr:
                pr[a] = False
            else:
                pr[a] = False
            logger.info("revoke user=%s project=%s action=%s", username, r.project, a)

        # cleanup if all false/missing
        all_false = True
        for a in ACTIONS:
            if bool(pr.get(a, False)):
                all_false = False
                break
        if all_false:
            projects_map.pop(r.project, None)
            logger.info("project rule removed (all false): user=%s project=%s", username, r.project)


# ----------------------------
# Password helpers
# ----------------------------

def generate_password(length: int = 14) -> str:
    if length < 10:
        length = 10
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def set_user_password_hash(cfg: Dict[str, Any], username: str, password: str) -> None:
    users = cfg["users"]
    rule = users[username]
    rule["password_hash"] = hash_password(password)
    logger.info("password hash updated user=%s", username)


# ----------------------------
# Commands
# ----------------------------

def cmd_init(args: argparse.Namespace) -> int:
    cfg_path = Path(args.config)
    if cfg_path.exists() and not args.force:
        logger.error("Config already exists: %s (use --force to overwrite)", cfg_path)
        return 2

    cfg: Dict[str, Any] = {
        "root_dir": args.root_dir or "",
        "session": {
            "secret": args.session_secret or "CHANGE_ME_TO_A_LONG_RANDOM_STRING",
            "ttl_seconds": int(args.ttl_seconds),
            "cookie_name": "session",
            "cookie_samesite": "lax",
            "cookie_secure": bool(args.cookie_secure),
        },
        "users": {}
    }

    # optional admin
    if args.admin_username:
        admin_pw = args.admin_password or generate_password(args.pw_length)
        cfg["users"][args.admin_username] = {
            "password_hash": hash_password(admin_pw),
            "projects": {"*": {"read": True, "edit": True, "create": True}},
        }
        if not args.quiet:
            print(f"[INIT] Admin user created: {args.admin_username}")
            print(f"[INIT] Admin password (store safely): {admin_pw}")

    cfg = ensure_defaults(cfg)
    write_config_atomic(cfg_path, cfg, backup=False)
    logger.info("init done path=%s", cfg_path)
    return 0


def cmd_list_users(args: argparse.Namespace) -> int:
    cfg = ensure_defaults(read_config(Path(args.config)))
    users = cfg.get("users") or {}
    names = sorted(users.keys())
    for u in tqdm(names, desc="Listing users", unit="user"):
        print(u)
    logger.info("listed users count=%d", len(names))
    return 0


def cmd_show_user(args: argparse.Namespace) -> int:
    cfg = ensure_defaults(read_config(Path(args.config)))
    ensure_user_exists(cfg, args.username)
    rule = cfg["users"][args.username]
    out = {
        "username": args.username,
        "projects": rule.get("projects", {}),
        "has_password_hash": bool(rule.get("password_hash")),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    logger.info("show_user user=%s", args.username)
    return 0


def cmd_list_projects(args: argparse.Namespace) -> int:
    cfg = ensure_defaults(read_config(Path(args.config)))
    projs = list_projects_from_root(cfg.get("root_dir", ""))
    for p in tqdm(projs, desc="Listing projects", unit="proj"):
        print(p)
    logger.info("listed projects count=%d", len(projs))
    return 0


def cmd_create_user(args: argparse.Namespace) -> int:
    cfg_path = Path(args.config)
    cfg = ensure_defaults(read_config(cfg_path))
    users = cfg["users"]

    if args.username in users and not args.force:
        logger.error("user already exists: %s (use --force to overwrite)", args.username)
        return 2

    # password
    password: Optional[str] = None
    if args.prompt:
        import getpass
        p1 = getpass.getpass("New password: ")
        p2 = getpass.getpass("Confirm password: ")
        if p1 != p2:
            logger.error("password confirmation mismatch")
            return 2
        password = p1
    elif args.password:
        password = args.password
    elif args.gen_password:
        password = generate_password(args.pw_length)
    else:
        # safe default: generate
        password = generate_password(args.pw_length)
        logger.warning("no password provided; generated automatically (recommended to pass --gen-password explicitly)")

    # create user base
    users[args.username] = {
        "password_hash": hash_password(password),
        "projects": {},
    }

    # apply grants (optional)
    if args.grant:
        grants = parse_spec_list(args.grant, mode="grant")
        apply_grants(cfg, args.username, grants, validate_projects=bool(args.validate_projects))

    write_config_atomic(cfg_path, cfg, backup=True)
    logger.info("user created user=%s", args.username)

    if not args.quiet:
        print(f"[OK] user created: {args.username}")
        if args.gen_password or (not args.password and not args.prompt):
            print(f"[OK] generated password (store safely): {password}")

    return 0


def cmd_set_password(args: argparse.Namespace) -> int:
    cfg_path = Path(args.config)
    cfg = ensure_defaults(read_config(cfg_path))
    ensure_user_exists(cfg, args.username)

    if args.username == "admin" and args.disallow_admin is False:
        pass  # allow admin by default; user can block via flag if they want

    password: Optional[str] = None
    if args.prompt:
        import getpass
        p1 = getpass.getpass("New password: ")
        p2 = getpass.getpass("Confirm password: ")
        if p1 != p2:
            logger.error("password confirmation mismatch")
            return 2
        password = p1
    elif args.password:
        password = args.password
    elif args.gen_password:
        password = generate_password(args.pw_length)
    else:
        logger.error("set-password requires --prompt or --password or --gen-password")
        return 2

    set_user_password_hash(cfg, args.username, password)
    write_config_atomic(cfg_path, cfg, backup=True)

    if not args.quiet and args.gen_password:
        print(f"[OK] password updated for {args.username}")
        print(f"[OK] generated password (store safely): {password}")
    elif not args.quiet:
        print(f"[OK] password updated for {args.username}")

    return 0


def cmd_delete_user(args: argparse.Namespace) -> int:
    cfg_path = Path(args.config)
    cfg = ensure_defaults(read_config(cfg_path))
    users = cfg["users"]

    if args.username not in users:
        logger.error("user not found: %s", args.username)
        return 2

    if args.username == "admin" and not args.allow_delete_admin:
        logger.error("refusing to delete admin without --allow-delete-admin")
        return 2

    users.pop(args.username, None)
    write_config_atomic(cfg_path, cfg, backup=True)
    logger.info("user deleted user=%s", args.username)

    if not args.quiet:
        print(f"[OK] user deleted: {args.username}")
    return 0


def cmd_grant(args: argparse.Namespace) -> int:
    cfg_path = Path(args.config)
    cfg = ensure_defaults(read_config(cfg_path))
    ensure_user_exists(cfg, args.username)

    grants = parse_spec_list(args.grant, mode="grant")
    apply_grants(cfg, args.username, grants, validate_projects=bool(args.validate_projects))

    write_config_atomic(cfg_path, cfg, backup=True)
    logger.info("grant done user=%s specs=%d", args.username, len(grants))

    if not args.quiet:
        print(f"[OK] granted permissions to {args.username}")
    return 0


def cmd_revoke(args: argparse.Namespace) -> int:
    cfg_path = Path(args.config)
    cfg = ensure_defaults(read_config(cfg_path))
    ensure_user_exists(cfg, args.username)

    revokes = parse_spec_list(args.revoke, mode="revoke")
    apply_revokes(cfg, args.username, revokes)

    write_config_atomic(cfg_path, cfg, backup=True)
    logger.info("revoke done user=%s specs=%d", args.username, len(revokes))

    if not args.quiet:
        print(f"[OK] revoked permissions from {args.username}")
    return 0


# ----------------------------
# CLI
# ----------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="manage_users.py",
        description="User/password/permission manager for Config.json (PBKDF2 + project ACL).",
    )
    p.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to Config.json (default: ./Config.json)")
    p.add_argument("--log", default="manage_users.log", help="Log file path (default: manage_users.log)")
    p.add_argument("--log-level", default="INFO", help="Log level (DEBUG/INFO/WARNING/ERROR)")
    p.add_argument("--quiet", action="store_true", help="Less stdout output")

    sp = p.add_subparsers(dest="cmd", required=True)

    # init
    s = sp.add_parser("init", help="Create a new Config.json template (optionally create admin)")
    s.add_argument("--force", action="store_true", help="Overwrite if Config exists")
    s.add_argument("--root-dir", default="", help="root_dir for projects")
    s.add_argument("--session-secret", default="", help="session.secret (recommend long random)")
    s.add_argument("--ttl-seconds", type=int, default=86400, help="session.ttl_seconds")
    s.add_argument("--cookie-secure", action="store_true", help="session.cookie_secure")
    s.add_argument("--admin-username", default="admin", help="admin username to create (default: admin)")
    s.add_argument("--admin-password", default="", help="admin password (plaintext input; will be hashed)")
    s.add_argument("--pw-length", type=int, default=14, help="generated password length")
    s.set_defaults(func=cmd_init)

    # list-users
    s = sp.add_parser("list-users", help="List all users")
    s.set_defaults(func=cmd_list_users)

    # show-user
    s = sp.add_parser("show-user", help="Show one user rule")
    s.add_argument("--username", required=True)
    s.set_defaults(func=cmd_show_user)

    # list-projects
    s = sp.add_parser("list-projects", help="List projects (top-level dirs under root_dir)")
    s.set_defaults(func=cmd_list_projects)

    # create-user
    s = sp.add_parser("create-user", help="Create/overwrite user with hashed password and optional grants")
    s.add_argument("--username", required=True)
    s.add_argument("--force", action="store_true", help="Overwrite existing user")
    s.add_argument("--password", default="", help="plaintext password (NOT stored; only hash saved)")
    s.add_argument("--prompt", action="store_true", help="prompt password securely")
    s.add_argument("--gen-password", action="store_true", help="generate random password")
    s.add_argument("--pw-length", type=int, default=14, help="generated password length")
    s.add_argument("--grant", action="append", default=[], help='grant spec e.g. "Oligomer_IL:read,edit" (repeatable)')
    s.add_argument("--validate-projects", action="store_true", help="warn if project dir not found under root_dir")
    s.set_defaults(func=cmd_create_user)

    # set-password
    s = sp.add_parser("set-password", help="Update user's password hash")
    s.add_argument("--username", required=True)
    s.add_argument("--password", default="", help="plaintext password (NOT stored; only hash saved)")
    s.add_argument("--prompt", action="store_true", help="prompt password securely")
    s.add_argument("--gen-password", action="store_true", help="generate random password")
    s.add_argument("--pw-length", type=int, default=14, help="generated password length")
    s.add_argument("--disallow-admin", action="store_true", help="(optional) block changing admin pw (default allow)")
    s.set_defaults(func=cmd_set_password)

    # delete-user
    s = sp.add_parser("delete-user", help="Delete a user")
    s.add_argument("--username", required=True)
    s.add_argument("--allow-delete-admin", action="store_true", help="Allow deleting admin")
    s.set_defaults(func=cmd_delete_user)

    # grant
    s = sp.add_parser("grant", help="Grant project permissions to an existing user")
    s.add_argument("--username", required=True)
    s.add_argument("--grant", action="append", required=True, help='grant spec e.g. "Oligomer_IL:read,edit" (repeatable)')
    s.add_argument("--validate-projects", action="store_true", help="warn if project dir not found under root_dir")
    s.set_defaults(func=cmd_grant)

    # revoke
    s = sp.add_parser("revoke", help="Revoke project permissions from an existing user")
    s.add_argument("--username", required=True)
    s.add_argument("--revoke", action="append", required=True, help='revoke spec e.g. "Oligomer_IL:edit,create" (repeatable)')
    s.set_defaults(func=cmd_revoke)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    setup_logging(Path(args.log), level=args.log_level)

    try:
        # run
        rc = args.func(args)
        if args.quiet:
            logger.info("done rc=%s (quiet)", rc)
        else:
            logger.info("done rc=%s", rc)
        return int(rc)

    except KeyboardInterrupt:
        logger.warning("interrupted by user")
        return 130
    except Exception:
        logger.exception("fatal error")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
