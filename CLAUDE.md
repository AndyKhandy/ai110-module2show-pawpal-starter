# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**PawPal+** is a Streamlit pet care planning app built as an AI110 Module 2 project. The starter scaffold is intentionally thin — `app.py` has a working UI shell but no scheduling logic. The student's job is to design classes, implement a scheduler, connect it to the UI, and write tests.

## Commands

```bash
# Setup
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py

# Run all tests
pytest

# Run tests with coverage
pytest --cov

# Run a single test file
pytest tests/test_scheduler.py
```

## Architecture

The intended design (from `reflection.md`) has four classes:

- **`Task`** — `name`, `duration` (minutes), `priority` (low/medium/high), `is_complete`; method `markDone()` flips completion
- **`Pet`** — `name`, `species` (dog/cat/other)
- **`Owner`** — `name`, `pets` (list of `Pet`), `tasks` (list of `Task`); methods `addPet()` and `addTask()`
- **`Scheduler`** — `tasks` (list), `daily_plan` (list); methods `buildPlan()` constructs the schedule, `displayPlan()` formats it for the UI

These classes do not exist yet — they need to be implemented (likely in a new module such as `pawpal_system.py`, since a compiled `.pyc` for that name exists in `__pycache__`).

## Key Files

| File | Purpose |
|------|---------|
| `app.py` | Streamlit UI shell — connect scheduler output here |
| `diagrams/uml.mmd` | Mermaid class diagram — keep updated to match implementation |
| `reflection.md` | Design journal — student fills this in during development |
| `ai_interactions.md` | Log for stretch features involving AI agent/prompt experiments |
| `requirements.txt` | `streamlit>=1.30`, `pytest>=7.0` |

## Integration Pattern

Once the backend classes exist, wire them into `app.py` at the "Generate schedule" button (line 76). The UI already collects `owner_name`, `pet_name`, `species`, and a `tasks` list in `st.session_state`.

## UML

`diagrams/uml.mmd` uses Mermaid `classDiagram` syntax. Keep it in sync with the actual Python classes — this is checked during grading.

## Git Conventions

Use **Conventional Commits** style for all commit messages:

```
<type>(<optional scope>): <short description>
```

Common types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

Examples:
- `feat(scheduler): implement priority-based buildPlan logic`
- `docs(uml): update class diagram to reflect final implementation`
- `fix(task): correct markDone to set is_complete to True`
