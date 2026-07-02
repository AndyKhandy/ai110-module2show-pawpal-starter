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

All logic lives in `pawpal_system.py`. Four dataclasses, defined in this order (each depends on the one above it):

- **`Task`** — `name`, `duration` (minutes), `priority` ("low"/"medium"/"high"), `is_complete`; `markDone()` sets completion
- **`Pet`** — `name`, `species`, `tasks: list[Task]`; `addTask()` appends to its own task list
- **`Owner`** — `name`, `pets: list[Pet]`; `addPet()` adds a pet, `getAllTasks()` flattens all pets' tasks into one list
- **`Scheduler`** — requires `tasks: list[Task]` and `available_minutes: int`; `buildPlan()` sorts by `PRIORITY_ORDER` and greedily fills the time budget, `displayPlan()` renders the plan starting at 08:00

**Key design decision:** tasks belong to `Pet`, not `Owner`. The owner aggregates via `getAllTasks()` and passes the result to `Scheduler`. The typical call sequence is:

```python
scheduler = Scheduler(tasks=owner.getAllTasks(), available_minutes=120)
scheduler.buildPlan()
print(scheduler.displayPlan())
```

`PRIORITY_ORDER = {"low": 1, "medium": 2, "high": 3}` is a module-level constant used by `buildPlan()` for sorting.

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

### FUTURE TASKS TO COMPLETE
 You will implement logic for sorting tasks by time, filtering by pet/status, handling recurring tasks, and basic conflict detection .