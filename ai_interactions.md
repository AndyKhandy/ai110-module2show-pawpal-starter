# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I gave the agent a task to implement weighted prioritization by combining task priority and due-date urgency

**What did the agent do?**

The agent looked at the different files like CLAUDE.md, app.py and pawpal_system.py in plan mode to figure out how to implement the feature. The agent then made a score formula that used priority as the most dominant factor. To implement this it made changes in pawpal_system.py first, then applied the changes to main.py to test it out in the CLI, then added the logic to the UI in app.py

The AI then updated the README.md and CLAUDE.md file to update phrases and blocks of writting that go against what was just made

**What did you have to verify or fix manually?**

<!-- After reviewing the diff and running `pytest` / `python main.py` / the Streamlit app, note here anything you changed — e.g. tweaked weight constants, adjusted wording, or caught an edge case the agent missed. -->

The things that I had to fix manualy were the tests and the redundancy that the code produced, but other than that it performed really well with the task I gave it 

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
