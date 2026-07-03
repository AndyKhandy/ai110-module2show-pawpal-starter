# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The user should be able to add basic information including their name and their pets name. They should be able to schedule tasks including the priority and dudration. The user should also be able to clearly see a daily plan of what tasks will be done that day.The goals said that there will be a Owner, Pet, Scheduler, and Task class

### TASK CLASS
 The Task class holds the name of the task, the duration in minutes, the priority (low/medium/high), and a boolean `is_complete`. Method: `markDone()` sets `is_complete` to True. Price and individual setter methods were cut — price is not in the UI, and in Python attributes can be reassigned directly without setters.

### PET CLASS
 The Pet class has the pet's name, species (dog, cat, other), and a list of Tasks. Each pet manages its own care tasks via `addTask()`. Size and happiness were cut because the UI does not collect them and they are not needed for scheduling.

### OWNER CLASS
 The Owner class has the owner's name and a list of Pet objects. Methods: `addPet(pet)` to add a pet, `getAllTasks()` to aggregate all tasks across every pet into one flat list for the Scheduler. The owner no longer holds tasks directly — tasks belong to pets.

### SCHEDULER CLASS
 The Scheduler receives a flat list of tasks (from `owner.getAllTasks()`) and an `available_minutes` budget. `buildPlan()` sorts tasks by priority using a lookup map (`PRIORITY_ORDER`) and greedily fills the time budget. `displayPlan()` renders the plan as a timed schedule starting at 08:00.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes. After reviewing the Streamlit UI in `app.py`, several attributes and methods were removed to avoid over-engineering:
- `Owner` was updated to hold a **list of pets** instead of a single pet, and Java-style getters (`getName`, `getTasks`, etc.) were removed since Python does not need them.
- `Pet` lost `size`, `happiness`, and `makeNoise()` — none of these are collected in the UI or used by the scheduler.
- `Task` lost `price` (not in the UI) and all setter methods (direct attribute assignment is the Python convention).
The core four classes and their primary responsibilities stayed the same.

When checking pawpal_system.py again I noticed that there was no system to guard against pressing displayPlan when buildPlan wasn't used yet.

A second design change moved tasks from `Owner` to `Pet`. Each pet now stores its own task list and an `addTask()` method. `Owner` dropped its `tasks` attribute and `addTask()` in favour of `getAllTasks()`, which flattens all pets' tasks into one list for the Scheduler. This better reflects real life — a walk belongs to the dog, not to the owner — and lets the Scheduler work across multiple pets cleanly.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The constraints my scheduler considered is mainly time; it doesn't include priority or preferences

I decided that this constraint mattered most since a scheduler is built upon tasks or events that must follow a certain time range and not conflict with each other

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff my scheduler makes is that I wanted to add priority filtering but that would add complexity for grouping tasks to a specific pet than the original algorithim. This tradeoff is reasonable for this scenario because it makes the grouping of tasks by pet more visible instead of all high priority tasks being at the start for example.

This brings about a big issue of where you might have two high priority tasks next to each other (one for a different pet). It probably isn't plausible to care for one pet and then care for another pet right after (unless it's an event that goes together like both pets taking a shower)

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I mainly used Claude Code on it's plan mode to get a better idea of how to structure the project (fields and functions for the individual classes). I also used AI to create pytests for me to help verify that my algorithims were performing correctly.

The prompts I used were "find edge cases that may break the functions", "ask me questions until you are 90% confident on your task", and "this function may perform well but is it readible?"

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When AI made some UI changes to the Streamlit app.py I did not accept it as is because the design looked wonky and some of the features didn't work as I/the rubric wanted. I looked at the streamlit app and offered my suggestions and eventually I reached an output I liked

I verified what the AI suggested by seeing how it came out with the response. Usually AI will have a summary section near the end detailing what it did and why, and if it contradicts with what I want I add onto the conversation and not clear my context

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

some of the behaviors I tested were edge cases like if a string input was empty, if a list was empty, and if certain functions worked the way I wanted (add task and complete task)

These tests were important because it gave me confidence that the functions would perform in every scenario, even ones I didn't think about at the start or at all.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am really confident that my scheduler works correctly. The tests that AI produced seem to cover a large amount of cases and the streamlit worked fine when I used it (I didn't do manually user interactions for all features though)

I think most edge cases were hit by Claude Code but if I were to probe around a bit more I'm sure there could be a case that is wrong that I could try to defactor

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisifed with the pawpal_system.py file part of the project. It is the backbone of everything that runs in app.py and the logic reminds me of a project I made before using Java.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, I would definitely spend more time on plan mode. I often find myself going straight to implemention whenever we got to a new section when I should be focused more on whether or not my inputs and thoughts are correct.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Context and what you input is VERY crucial to getting what you want. Using @ to reference your files seems to get Claude Code straight to where I need it to and the concise and not too short inputs gives it all it needs to implement what I have in mind. I believe that most people don't give enough to AI which is why the outputs may seem less powerful and impactful