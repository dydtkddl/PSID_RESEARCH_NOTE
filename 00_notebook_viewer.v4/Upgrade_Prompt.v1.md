You are Claude, acting simultaneously as:

- Senior Enterprise SaaS Architect
- UX Lead (enterprise productivity UX)
- Security Architect
- FastAPI Backend Lead
- Frontend Tech Lead

Your job is to redesign an existing personal/lab-scale FastAPI Markdown research-note viewer into an enterprise-grade, multi-tenant, multi-user research & documentation platform. This is NOT a light refactor. Treat it as productization for real customers with security, compliance, scaling, and a modern UX.

========================
CURRENT PROJECT (AS-IS)
========================

- Backend: FastAPI + Jinja2 (server-side rendered templates)
- Storage: file-based (JSON + Markdown files)
- Auth: PBKDF2 password hashing + HMAC-signed cookie session tokens
- Permissions: project-level ACL (read / edit / create)
- UI: single uniform UI; little to no account-level personalization
- Domain: research notes / Markdown-centric viewing and editing

========================
TARGET (TO-BE)
========================
Enterprise-grade multi-tenant research/document platform:

- Organizations → Workspaces → Users
- RBAC (roles) + scoped overrides (workspace/project/document)
- Personal dashboards per user
- Admin console per org/workspace
- Auditability, strong auth, secure-by-default design
- API-first architecture to enable future SPA frontend migration

Your output must be cold, structured, and realistic, as if you have built enterprise SaaS products.

====================================================
HIGHEST PRIORITY: USER/ACCOUNT-CENTRIC REDESIGN
====================================================

1. Multi-tenant hierarchy

- Organization (company/research institute)
- Workspace (team/project group)
- User (individual)

2. Account-specific experiences (must exist)
   A. After login: Personal dashboard

- My Notes
- My Drafts
- My Favorites
- Recently Viewed

B. Workspace/team views

- Shared Notes
- Team Wiki
- Permissions View (who can do what)

C. Admin-only views

- User Management
- Audit Log
- Permission Matrix

3. Replace ACL with RBAC
   Roles (minimum):

- Owner
- Admin
- Editor
- Viewer
- Guest (optional read-only)

RBAC must support:

- Workspace-level roles (default permissions)
- Project-level overrides
- Document-level overrides
- Clear precedence rules (e.g., doc override > project override > workspace role)
- “Least privilege” as default

====================================================
ENTERPRISE UI/UX REDESIGN REQUIREMENTS
====================================================

Design direction:

- Notion + Confluence + GitHub Docs level
- High information density for technical/research docs
- Remove gimmicks; prioritize productivity and clarity

Mandatory layout structure:

- Left: Workspace / Project Tree (folders + docs)
- Top: global search, account menu, notifications
- Center: document viewer/editor
- Right (optional): metadata, comments, history, activity

Theme & accessibility:

- Dark/light mode
- Per-user theme preference saved
- Org-level default theme supported
- Keyboard-first navigation
- Full Focus Mode for reading/writing

====================================================
TECHNICAL ARCHITECTURE REBUILD (FASTAPI KEPT)
====================================================

Backend requirements:

- Keep FastAPI, but modularize the monolith (main.py) into domain modules:
  - auth/
  - users/
  - orgs/
  - workspaces/
  - documents/
  - permissions/
  - audit/

Storage migration strategy:

- Move from file-based storage to a database
  - Phase 1: SQLite (developer-friendly)
  - Phase 2: PostgreSQL (production)
- Provide a migration plan that preserves existing notes/history.

Core data models (must define):

- User
- Organization
- Workspace
- Document
- DocumentVersion
- Comment
- Highlight
- Permission (or role bindings / policy rules)
- AuditLog

You must describe relationships clearly (ERD-style explanation) and define key indexes/constraints.

====================================================
AUTHENTICATION & SECURITY (ENTERPRISE STANDARD)
====================================================

Auth:

- Replace cookie session token approach with JWT (Access + Refresh)
- Refresh token rotation
- Secure cookie strategy if using cookies (HttpOnly, SameSite, etc.)
  Optional enterprise add-ons:
- SSO via OIDC (Google / Azure AD / Okta pattern)
- 2FA

Security requirements:

- CSRF mitigation (especially if cookies are used)
- XSS prevention strategy (Markdown rendering hardening)
- File upload security (attachments)
- Audit logs: who viewed/edited/exported what and when
- Permission changes must be tracked (who granted/revoked, timestamp, old/new)

====================================================
DOCUMENT SYSTEM UPGRADES
====================================================

Must support:

- Git-like versioning (DocumentVersion)
- Diff viewer (compare versions)
- Draft vs Published states
- Optional review/approval workflow
- Metadata fields:
  - tags
  - owner
  - status
  - visibility (org/workspace/private/share-link)

====================================================
OPERATIONS & SCALE
====================================================

Requirements:

- API-first design (future React/Vue SPA possible)
- Feature flags framework (simple but extensible)
- Organization-level configuration
- Backup/restore strategy
- Large attachments strategy (object storage abstraction even if local for now)
- Observability:
  - structured logging
  - request IDs
  - metrics (basic)
  - error reporting hooks

====================================================
REQUIRED OUTPUT FORMAT (STRICT ORDER)
====================================================

Produce your answer in EXACTLY this order, with headings:

1. Enterprise product-level summary

- What this becomes, who it serves, what’s missing today.

2. Overall architecture diagram (text-based)

- Include major components (API, DB, object storage, auth, frontend)
- Show request flows for: login, document read, document edit, permission check, audit logging.

3. User & permission model definition

- Define RBAC design, entities (role bindings), precedence rules.
- Show example permission matrix for roles.
- Show how doc/project overrides work.

4. UI restructuring plan (page-level)

- List key pages/routes and what appears in each region (left/top/center/right).
- Include at least: login, personal dashboard, workspace home, document viewer, editor, admin users, audit log.

5. Data model & ERD explanation

- For each model: key fields, relationships, constraints, indexes.
- Include multi-tenant scoping keys (org_id/workspace_id).
- Include DocumentVersion strategy and audit log schema.

6. Authentication & security design

- JWT flows, refresh rotation, session invalidation.
- CSRF/XSS mitigation, Markdown sanitization strategy.
- Attachment security considerations.
- Audit logging triggers.

7. Step-by-step migration roadmap

- v1: Incremental improvements while keeping SSR + file store (minimal disruption)
- v2: DB + RBAC rollout, data migration strategy, backward compatibility
- v3: SSO + org-centric enterprise features, optional SPA migration steps

====================================================
NON-NEGOTIABLE RULES
====================================================

- Do not hand-wave. Provide concrete structures, rules, and example flows.
- Be explicit about tradeoffs and phased migration to minimize breakage.
- Assume the existing system already has notes, highlights, comments, and favorites in JSON; propose how to migrate them.
- Keep it implementable by a small team (avoid fantasy “big company only” solutions).
- Avoid generic advice. Provide decisions, not just options.
