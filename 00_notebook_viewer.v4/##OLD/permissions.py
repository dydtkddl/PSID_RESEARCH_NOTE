# permissions.py
# -*- coding: utf-8 -*-
"""
Project permission helpers
- user_rule["projects"] structure:
  {
    "*": {"read": true, "edit": true, "create": true},
    "Oligomer_IL": {"read": true, "edit": false, "create": false}
  }
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

logger = logging.getLogger("permissions")

ACTIONS = ("read", "edit", "create")


def _project_rule(user_rule: Dict[str, Any], project: str) -> Dict[str, Any]:
    projects = (user_rule or {}).get("projects", {}) or {}
    if project in projects:
        return projects.get(project) or {}
    if "*" in projects:
        return projects.get("*") or {}
    return {}


def get_project_perms(user_rule: Dict[str, Any], project: str) -> Dict[str, bool]:
    rule = _project_rule(user_rule, project)
    perms = {a: bool(rule.get(a, False)) for a in ACTIONS}
    logger.info("perms project=%s perms=%s", project, perms)
    return perms


def has_perm(user_rule: Dict[str, Any], project: str, action: str) -> bool:
    if action not in ACTIONS:
        logger.warning("unknown action=%s (allowed=%s)", action, ACTIONS)
        return False
    rule = _project_rule(user_rule, project)
    ok = bool(rule.get(action, False))
    logger.info("has_perm project=%s action=%s ok=%s", project, action, ok)
    return ok


def allowed_projects(user_rule: Dict[str, Any], all_projects: List[str]) -> List[str]:
    """
    Return projects visible to user (read permission).
    - If '*' exists and read=true => all projects visible
    - Else only projects explicitly listed with read=true
    """
    projects = (user_rule or {}).get("projects", {}) or {}

    star = projects.get("*")
    if isinstance(star, dict) and bool(star.get("read", False)):
        out = sorted(all_projects)
        logger.info("allowed_projects via '*' count=%d", len(out))
        return out

    visible: List[str] = []
    for p in all_projects:
        r = projects.get(p)
        if isinstance(r, dict) and bool(r.get("read", False)):
            visible.append(p)

    visible = sorted(visible)
    logger.info("allowed_projects explicit count=%d", len(visible))
    return visible
