# AGENTS.md

## Project Context
- Project: ForeTheMoney, a golf pool web app based on PGA Tour earnings.
- Primary backend: FastAPI + Pydantic + SQLAlchemy.
- Database: PostgreSQL (psycopg2-binary), with Alembic for migrations.
- Main app entrypoint: backend/app/main.py.

## Default Working Style
- Prefer small, focused changes that preserve current behavior.
- Avoid broad refactors unless explicitly requested.
- Keep code readable and consistent with nearby style.
- Provide comprehensive code commenting per language standards (i.e. if I code in Java, use Javadoc standard)
- Add type hints for new Python code where practical.

## Implementation Rules
- Do not change API contracts or database schema without calling it out.
- If assumptions are needed, state them clearly in the final summary.
- Update docs when behavior, setup, or workflows change.
- Keep changes scoped to the task and avoid unrelated edits.

## Validation Checklist
From backend directory:
1. Install dependencies: pip install -r requirements.txt
2. Run app locally: uvicorn app.main:app --reload
3. Run tests if present: pytest
4. Run migrations if needed: alembic upgrade head

If a command is not available or setup is incomplete, report what blocked validation.

## Definition Of Done
- Requested behavior is implemented.
- No known regressions introduced by the change.
- Relevant checks or run steps were executed (or blockers reported).
- Final summary includes changed files, validation status, and any risks.

## Communication Preferences For Agent Responses
- Start with what changed and why.
- Keep summaries concise and concrete.
- For reviews, prioritize bugs, regressions, and missing tests.

## Maintenance
- Review this file every 2 to 4 weeks or after major project changes.
- Keep entries short, actionable, and specific to this repository.
- Remove outdated guidance when workflows or architecture change.

### Update Checklist
- Confirm project context still matches current architecture and stack.
- Verify validation commands still run and reflect current tooling.
- Add any new conventions that repeat across multiple tasks.
- Record new guardrails only when they prevent real regressions.

## Context Retention Policy
- Do not store full chat transcripts in the repository.
- Persist only durable decisions, conventions, and workflow changes.
- Capture architecture-impacting choices and recurring implementation patterns.
- Skip one-off experiments, temporary debugging notes, and brainstorming chatter.
- When a task changes process or standards, update this file and any relevant docs.
- Keep retained context concise so future guidance stays easy to trust.