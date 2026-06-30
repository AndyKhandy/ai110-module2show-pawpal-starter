# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The user should be able to add basic information including their name and their pets name. They should be able to schedule tasks including the priority and dudration. The user should also be able to clearly see a daily plan of what tasks will be done that day.The goals said that there will be a Owner, Pet, Scheduler, and Task class

### OWNER CLASS
 The Owner class will most likely have the owner's name, a list containing all the Tasks, and a Pet object that will hold the owner's Pet. For the methods it will likely have a getName, getPetName, getTasks, something like that and methods to add tasks, change the Pet object (if the owner gets a new one), and more

### PET CLASS
 The Pet class will likely include the name of the pet, the size of the pet, the type of the pet (dog, cat,etc), and possible an attribute that holds it's Owner object. It might also have a happy attribute or love attribute. The Pet could have a function to perform an animal noise like sneeze or poof 
 
 ### TASKS CLASS
 The Tasks class will hold the name of the task, the duration of the task, the priority of the task, the price of the task, if the task is complete, and more. The class should have methods to edit the fields and a method to set done to True

 ### SCHEDULER CLASS
 This class will likely contain a list of the Tasks of the owner (already an attribute of the owner), a display of the daily plan, and any other actions needed to build out a daily plan that the owner can view

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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
