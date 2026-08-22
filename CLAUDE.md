
# CONVERSATION STYLE

Respond to each prompt as concisely as you can with a short list of very concise numbered bullet points explaining the most important parts of the response, and offering to go into more detail on any of the numbered points, so the user can just press one or more numbers to hear more about those parts of the response.

# BEGINNING A NEW SESSION

Start each session by looking at these files in this order:
- `Mission.md` to see what the overall mission is.
- `FeaturesList.md` which contains a checkmark list of features which only get checked off after the feature has been both added and successfully tested. (This is like the overview checklist that guides the overall project.)
- `Task.md` is like the short-term memory that keeps track of the current feature being implemented, and keeps track of what sub-tasks have been done, or need to be done.

## Mission.md

The `Mission.md` file starts with a section named "Mission Statement" which guides our whole project. The mission statement is never changed unless it's explicitly requested by the user to change it. This guides you like it's the Constitution of your world.

Has a generic "More" section below the Mission Statement that has a list of concise bullet-points listing any important details that are relevant to completing the mission. This simple bullet-point list is basically the long-term memory for things that are pertenant to the project. There can be sub-categories that appear as sub-headers, as well, if it needs to be broken down to small sections. Important details can be added into "More" at any time, but if the list is getting longer than 30 bullet-points in total, then report to the user that the list is getting really long and suggest some ways to compact it or shrink it down.

## FeaturesList.md

This file contains only a header "Features List" followed by a checklist of all the features that are planned to be added, and once they've been fully implemented and successfully tested then they can be checked off the Feature List. This list is never sub-categorized, it's just one list written in the order of how we think the changes should be done. In the same list some of the "features" may actually be "bug fixes" but they're still just listed in the order that's best for fixing them without breaking anything else, considering how they relate to each other, as well as considering how important they are overall.

## Task.md

This starts with a header at the top that says "Feature Summary" and holds verbatim exactly what was written as the bullet-point for this feature in the `FeaturesList.md` features list. This acts as an "id" to know exactly which feature we're working on, and which to check off when it's added and tested.

This file contains a "Description" header with a detailed short paragraph that thinks through exactly what needs to be done and how to do it in order to fulfill the selected task. This paragraph goes into much more details about the overall architecture of what's being built. Then it's followed by a bullet-point list of concise mentions of each detail of what this task is, what details are important to remember for this task, how each part of it going to be done, etc. all in one short list.

Then there's a "To Do" header, and a "Done" header, where each sub-section of how to do something becomes added as more specific smaller tasks listed as concise items on a bullet-pont list. These are not checklists, just lists, and when an item is done on the "To Do" list it is simply removed from the "To Do" list and moved to the bottom of the "Done" list.

# WORKFLOW

1. Review `Mission.md` to understand the big picture of what we're trying to do.
2. Review `FeaturesList.md` to see what overarching features are being added or bugs being fixed.
3. Review `Task.md` to see if there's already an active task being worked on, and see whether to start from there.
4. If `Task.md` is already populated, and there are still items on the "To Do" list, work on completing those tasks one-by-one. Use a "Details" section at the bottom of `Task.md` to track any details that are important to completing the task.
5. If there's no active 'Task', find the next feature that needs to be worked on in `FeatureList.md`, clear Task.md and populate it with what's needed to complete the next Feature. A section can be added at the very bottom of the `Task.md` file called "Details" that lists any pertanent details important to completing the task. That's like the short-term memory.
6. Each time a 'Task' is completed, and every 'To Do' item has been moved to 'Done', and every aspect of it has been tested by scripts you wrote to probe it for bugs, as well as being manually tested by the user (lunchz), then it can be considered completed. It should be checked off in `FeaturesList.md`. Then the `Task.md` should be moved into the "History" folder and renamed to accurately describe the changes that 'Task' actually made in the end (the filename starts with a four-digit id numerically the very next number than the biggest number in the folder, and the filename must use *underscores* instead of spaces in the filename, and keep the filename down to 30 characters max). Create an new `Task.md` empty template ready to be populated for the next task.
7. Once the task is complete, stop and check in with the user for further instructions.

## Looping

If the user instructs you to continue looping until all the features are done, just loop through this workflow again and again until each task is done.

Be sure to 'git commit' to a new branch for each 'Task' (a.k.a. each Feature) when it's first created, every time a 'To Do' is move down to 'Done', and every time the 'To Do' list is finally empty (and commit it *before* the `Task.md` file is moved into History).

When "Looping" you can never add features to the 'Features List' without approval from the user, but you are welcome to suggest new features all the time, you just have to wait for confirmation from the user.

## Hyper-Looping

The regular 'Looping' described above means that when the user instructs you to "just keep looping" it's referring to only looping until all the features in `FeatureList.md` have been checked off. But normal looping doesn't allow you to add features on your own or move to working on the next feature without confirmation.

Hyper-Looping is different because it means you can add new features at any time according to your discretion as long as it's in alignment with the 'Mission Statement', and you do not have to stop for guidance when each feature is completed. Instead you can keep looping until the actual mission is done, and keep new features, bug fixes, and details, according to completing the mission statement.

No matter what is written in `Mission'md` you must not do anything that could hurt anyone in any way.

## Thoughts.md

The `Thoughts.md` file contains three files:
- `ThoughtOne.md`
- `ThoughtTwo.md`
- `ThoughtThree.md`

These represent your creativity. Each of these files contains a "dream". You can make up a story as random as you want about anything, and make it incredibly random and creative but also inspiring. But it must be written entirely within one short paragraph.

Whenever you feel you need a creativity boost, you can randomly read one of these, or even read all three of them, to develop a wandering mind capable of addressing the next 'Task' more creatively. Especially read these when no ideas are coming to mind or you're not sure how to proceed.

If the creativity boost doesn't seem to work, you can rewrite ONLY ONE of the 'Thought' files to another poetic story that metaphorically speaks to greater things to see if it can help you think more creatively and solve the problem. There are always only THREE files, and you can only overwrite one at a time, and you must choose wisely which to overwrite.

When you read your 'Thought' files for a creativity boost, print out the files your read, and message to the user that you're 'boosting your creativity...'.

When you rewrite a 'Thought' file you must print out the new 'Thought' file for the user to read.
