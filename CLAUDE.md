# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**PawPal+** is a Streamlit pet care planning app built as an AI110 Module 2 project. The backend (`pawpal_system.py`), the Streamlit UI (`app.py`), and the test suite (`tests/test_pawpal.py`) are all implemented — task scheduling, sorting, filtering, recurring tasks, and conflict detection are done. `main.py` is a small CLI demo script that exercises the backend directly (useful for quick manual checks without launching Streamlit).

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
pytest tests/test_pawpal.py

# Run the CLI demo script
python main.py
```

## Architecture

All logic lives in `pawpal_system.py`. Four dataclasses, defined in this order (each depends on the one above it):

- **`Task`** — `name`, `duration` (minutes), `priority` ("low"/"medium"/"high"), `petName`, `time` ("HH:MM" start), `is_complete`, `recurrence` ("none"/"daily"/"weekly"), `due_date` (defaults to today). `markDone()` sets `is_complete = True`; if `recurrence` is `"daily"` or `"weekly"`, it also returns a new `Task` for the next occurrence with `due_date` advanced via `timedelta` (module-level `RECURRENCE_DELTA` maps recurrence → `timedelta`). Returns `None` for non-recurring tasks.
- **`Pet`** — `name`, `species`, `tasks: list[Task]`; `addTask()` appends to its own task list
- **`Owner`** — `name`, `pets: list[Pet]`; `addPet()` adds a pet, `getAllTasks()` flattens all pets' tasks into one list
- **`Scheduler`** — requires `tasks: list[Task]` and `available_minutes: int`:
  - `compute_priority_score(task, today=None)` scores a task using `PRIORITY_ORDER` × `PRIORITY_WEIGHT` plus a due-date urgency term (`URGENCY_WEIGHT`, capped at `URGENCY_CAP_DAYS`) — priority dominates but urgency can bump a due-today task above a less urgent higher-priority one
  - `buildPlan(today=None)` ranks tasks by `compute_priority_score()` (descending) and greedily fills the time budget
  - `sort_by_time()` sorts `self.tasks` in place by `"HH:MM"` start time
  - `filter_tasks(pet_name=None, is_complete=None)` returns tasks matching either/both optional filters
  - `detect_conflicts()` sorts tasks by `(due_date, time)` and returns a list of warning strings for any two tasks (same pet or different pets) whose time windows overlap on the same day
  - `displayPlan()` renders the built plan, grouped by pet, using each task's own start time

**Key design decision:** tasks belong to `Pet`, not `Owner`. The owner aggregates via `getAllTasks()` and passes the result to `Scheduler`. The typical call sequence is:

```python
scheduler = Scheduler(tasks=owner.getAllTasks(), available_minutes=120)
scheduler.buildPlan()
print(scheduler.displayPlan())
```

`PRIORITY_ORDER = {"low": 1, "medium": 2, "high": 3}` is a module-level constant used by `compute_priority_score()` for weighting; `PRIORITY_WEIGHT`, `URGENCY_WEIGHT`, and `URGENCY_CAP_DAYS` tune how strongly priority vs. due-date urgency affect that score.

**Completed features:** sorting by time, filtering by pet/status, recurring tasks (daily/weekly), conflict detection, and weighted prioritization are all implemented — see `sort_by_time()`, `filter_tasks()`, `Task.markDone()`, `detect_conflicts()`, and `compute_priority_score()` above.

## Key Files

| File | Purpose |
|------|---------|
| `app.py` | Streamlit UI — pet/task entry, recurrence selection, mark-complete flow, schedule generation |
| `main.py` | CLI demo script exercising the backend directly (sorting, filtering, conflicts) |
| `diagrams/uml.mmd` | Mermaid class diagram — keep updated to match implementation |
| `reflection.md` | Design journal — student fills this in during development |
| `ai_interactions.md` | Log for stretch features involving AI agent/prompt experiments |
| `requirements.txt` | `streamlit>=1.30`, `pytest>=7.0` |

## Integration Pattern

Backend classes are wired into `app.py`'s "Add pet", "Add task", "Mark complete", and "Generate schedule" buttons. Note: `st.selectbox()` does not reliably return the same live object reference across reruns for options that are custom dataclass instances (e.g. `Task`) — select by index into a freshly computed list instead, then dereference the real object at click time (see the "Mark a task complete" flow in `app.py` for the pattern).

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