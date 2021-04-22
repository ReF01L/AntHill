# Commit instruction
*The basic syntax fro a Smart Commit message is*:
```
<ignored text> <ISSUE_KEY> <ignored text> #<COMMAND> <optional COMMAND_ARGUMENTS>
```
Any text between the ISSUE_KEY and the command is ignored.
There are three commands you can use in your Smart Commit messages:
- `comment`

- `time`

- `transition`

## 1. Comment
### Description
Adds a comment to a Jira Software issue.
### Syntax
`<ignored text> <ISSUE_KEY> <ignored text> #comment <comment_string>`
### Example
`JRA-34 #comment corrected indent issue`
### Notes
The email address of committer  must match the email address of a single Jira Software user with permission to comment on issues in that particular project.

## 2. Time
### Description
Records time tracking information against an issue.
### Syntax
`<ignored text> <ISSUE_KEY> <ignored text> #time <value>w <value>d <value>h <value>m <comment_string>`
### Example
`JRA-34 #time 1w 2d 4h 30m Total work logged`
### Notes
This example records 1 week, 2 days, 4 hours and 30 minutes against the issue, and adds the comment 'Total work logged' in the Work Log tab of the issue.

- The values for w, d, h and m can be decimal numbers.

- The comment is added automatically without needing to use the #comment command.

## 3. Workflow transitions
### Description
Transitions a Jira Software issue to a particular workflow state.
### Syntax
`<ignored text> <ISSUE_KEY> <ignored text> #<transition_name> #comment <comment_string>`
### Example
`JRA-090 #close #comment Fixed this today`
### Notes
This example executes the close issue workflow transition for the issue and adds the comment `Fixed this today` to the issue.
You can see the custom commands available for use with Smart Commits by visiting the Jira Software issue and looking at its available workflow transitions:
1. Open an issue in the project.
2. Click View Workflow (near the issue's Status).

The Smart Commit only considers the part of a transition name before the first space. So, for a transition name such as finish work, then specifying #finish is sufficient. You must use hyphens to replace spaces when ambiguity can arise over transition names, for example: #finish-work.
