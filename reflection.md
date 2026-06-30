# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The user should be able to add basic information including their name and their pets name. They should be able to schedule tasks including the priority and dudration. The user should also be able to clearly see a daily plan of what tasks will be done that day.The goals said that there will be a Owner, Pet, Scheduler, and Task class

### OWNER CLASS
 The Owner class has the owner's name, a list of Pet objects (so an owner can have more than one pet), and a list of Tasks. Methods: `addPet(pet)` to add a pet, `addTask(task)` to add a task. Python attributes are accessed directly, so separate getter methods like `getName()` are not needed.

### PET CLASS
 The Pet class has the pet's name and species (dog, cat, other). Size and happiness were cut because the UI does not collect them and they are not needed for scheduling.

### TASKS CLASS
 The Task class holds the name of the task, the duration in minutes, the priority (low/medium/high), and a boolean `is_complete`. Method: `markDone()` sets `is_complete` to True. Price and individual setter methods were cut — price is not in the UI, and in Python attributes can be reassigned directly without setters.

### SCHEDULER CLASS
 The Scheduler has the list of tasks to consider and a `daily_plan` list that stores the built schedule. Methods: `buildPlan()` constructs and returns the ordered schedule, `displayPlan()` formats it as a string for the UI.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes. After reviewing the Streamlit UI in `app.py`, several attributes and methods were removed to avoid over-engineering:
- `Owner` was updated to hold a **list of pets** instead of a single pet, and Java-style getters (`getName`, `getTasks`, etc.) were removed since Python does not need them.
- `Pet` lost `size`, `happiness`, and `makeNoise()` — none of these are collected in the UI or used by the scheduler.
- `Task` lost `price` (not in the UI) and all setter methods (direct attribute assignment is the Python convention).
The core four classes and their primary responsibilities stayed the same.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
