# Git Steps Log

Every Git command run for UCS 745 Cloud and DevOps, Assignment Q1, in the order it
was run, with its output. Repository: https://github.com/Kritiiguptaa/calc-project

Environment: Windows 11, Git Bash, git 2.45.2, GitHub CLI 2.106.0, Python 3.10.0

---

## Stage 0: Setup

The GitHub CLI was not installed on the machine, so it was installed first.

```
$ winget install --id GitHub.cli
Found GitHub CLI [GitHub.cli] Version 2.106.0
Downloading https://github.com/cli/cli/releases/download/v2.106.0/gh_2.106.0_windows_amd64.msi
Successfully verified installer hash
Starting package install...
Successfully installed

$ export PATH="$PATH:/c/Program Files/GitHub CLI"

$ gh --version
gh version 2.106.0 (2026-11-25)
https://github.com/cli/cli/releases/tag/v2.106.0
```

---

## Stage 1: Initialise the repository and make the first commit on main

```
$ git init -b main
Initialized empty Git repository in C:/Users/kriti/Desktop/devops assign/calc-project/.git/

$ git add calc.py README.md

$ git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   README.md
        new file:   calc.py

$ git commit -m "Initial commit: Python CLI calculator with README"
[main (root-commit) eacb1d9] Initial commit: Python CLI calculator with README
 2 files changed, 106 insertions(+)
 create mode 100644 README.md
 create mode 100644 calc.py
```

---

## Stage 2: Create the public GitHub repo with the gh CLI and push main

```
$ gh auth login
? How would you like to authenticate GitHub CLI? Login with a web browser
? What is your preferred protocol for Git operations on this host? HTTPS
? Authenticate Git with your GitHub credentials? Yes
! One-time code (847D-82F7) copied to clipboard
Press Enter to open https://github.com/login/device in your browser...
Congratulations, you're all set! Your device is now connected.

$ gh repo create calc-project --public --source=. --remote=origin --push

$ git remote -v
origin  https://github.com/Kritiiguptaa/calc-project.git (fetch)
origin  https://github.com/Kritiiguptaa/calc-project.git (push)

$ git branch -a
* main
  remotes/origin/main
```

At this point the local repository and the remote repository both have one commit,
`eacb1d9`, and `main` tracks `origin/main`.

---

## Stage 3: Create feature-a from main and change the README title and add()

```
$ git checkout -b feature-a
Switched to a new branch 'feature-a'
```

Changes made on `feature-a`:

- `README.md` line 1: `# Calculator Project` became
  `# Calculator Project - Input Validation Edition`
- `calc.py`: the body and the comment of `add()` were changed so that the function
  validates its arguments with `isinstance()` and raises a `TypeError` if either
  argument is not an `int` or a `float`.

```
$ git add README.md calc.py

$ git status --short
M  README.md
M  calc.py

$ git commit -m "feature-a: add input validation to add() and update README title"
[feature-a 8d28085] feature-a: add input validation to add() and update README title
 2 files changed, 7 insertions(+), 3 deletions(-)

$ git push -u origin feature-a
Enumerating objects: 7, done.
Counting objects: 100% (7/7), done.
Delta compression using up to 12 threads
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 665 bytes | 665.00 KiB/s, done.
Total 4 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
remote:
remote: Create a pull request for 'feature-a' on GitHub by visiting:
remote:      https://github.com/Kritiiguptaa/calc-project/pull/new/feature-a
remote:
To https://github.com/Kritiiguptaa/calc-project.git
 * [new branch]      feature-a -> feature-a
branch 'feature-a' set up to track 'origin/feature-a'.
```

---

## Stage 4: Go back to main and create feature-b from main (not from feature-a)

Going back to `main` first is the important part here. If `feature-b` had been
branched off `feature-a`, it would already contain feature-a's commit and the two
branches would not have a conflicting common base.

```
$ git checkout main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.

$ git checkout -b feature-b
Switched to a new branch 'feature-b'

$ git log --oneline -1
eacb1d9 Initial commit: Python CLI calculator with README
```

That last command confirms `feature-b` starts from `eacb1d9`, the same commit
`feature-a` started from.

Changes made on `feature-b`, on the same lines as `feature-a`:

- `README.md` line 1: `# Calculator Project` became
  `# Calculator Project - Logging Edition`
- `calc.py`: `import logging` and a `logging.basicConfig(...)` call were added, and
  the body and comment of `add()` were changed so the function logs both operands
  with `logging.info()` before doing the addition.

```
$ git add README.md calc.py

$ git status --short
M  README.md
M  calc.py

$ git commit -m "feature-b: add logging to add() and update README title"
[feature-b 797cd0f] feature-b: add logging to add() and update README title
 2 files changed, 11 insertions(+), 3 deletions(-)

$ git push -u origin feature-b
Enumerating objects: 7, done.
Counting objects: 100% (7/7), done.
Delta compression using up to 12 threads
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 708 bytes | 708.00 KiB/s, done.
Total 4 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
remote:
remote: Create a pull request for 'feature-b' on GitHub by visiting:
remote:      https://github.com/Kritiiguptaa/calc-project/pull/new/feature-b
remote:
To https://github.com/Kritiiguptaa/calc-project.git
 * [new branch]      feature-b -> feature-b
branch 'feature-b' set up to track 'origin/feature-b'.
```

---

## Stage 5: Merge feature-a into main (clean fast-forward) and push

```
$ git checkout main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.

$ git merge feature-a
Updating eacb1d9..8d28085
Fast-forward
 README.md | 2 +-
 calc.py   | 8 ++++++--
 2 files changed, 7 insertions(+), 3 deletions(-)

$ git push origin main
Total 0 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To https://github.com/Kritiiguptaa/calc-project.git
   eacb1d9..8d28085  main -> main
```

This merge was a fast-forward: `main` had no commits of its own after `eacb1d9`, so
Git simply moved the `main` pointer forward to `8d28085`. No merge commit was
created and there was nothing to conflict with.

---

## Stage 6: Merge feature-b into main - CONFLICT (Screenshot 1)

```
$ git merge feature-b
Auto-merging README.md
CONFLICT (content): Merge conflict in README.md
Auto-merging calc.py
CONFLICT (content): Merge conflict in calc.py
Automatic merge failed; fix conflicts and then commit the result.
```

Both files conflicted, because both branches edited the same lines of both files
starting from the same base commit.

---

## Stage 7: Inspect the conflict (Screenshot 2)

```
$ git status
On branch main
Your branch is up to date with 'origin/main'.

You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   README.md
        both modified:   calc.py

no changes added to commit (use "git add" and/or "git commit -a")

$ git diff
diff --cc README.md
index f3d347f,92781ee..0000000
--- a/README.md
+++ b/README.md
@@@ -1,4 -1,4 +1,8 @@@
++<<<<<<< HEAD
 +# Calculator Project - Input Validation Edition
++=======
+ # Calculator Project - Logging Edition
++>>>>>>> feature-b

  A small command-line calculator written in Python for the UCS 745 Cloud and DevOps
  lab assignment. The point of the project is to practise the Git and GitHub
  workflow: branching, pushing, merging and resolving a merge conflict by hand.
diff --cc calc.py
index 0d22324,ffba0da..0000000
--- a/calc.py
+++ b/calc.py
@@@ -1,13 -1,17 +1,27 @@@
  """Simple command-line calculator for UCS 745 Cloud and DevOps, Assignment Q1."""

+ import logging

++<<<<<<< HEAD
 +# add: returns the sum of two numbers, after validating that both really are numbers.
 +# How it works: isinstance() checks each argument against int and float, and a
 +# TypeError is raised for anything else so the bad value is caught early instead
 +# of producing a nonsense result; valid values are then added with the + operator.
 +def add(a, b):
 +    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
 +        raise TypeError("add() expects two numbers")
++=======
+ # Send log messages to the console with the level and the message shown.
+ logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
+
+
+ # add: returns the sum of two numbers and records the call in the log.
+ # How it works: logging.info() writes both operands to the log before the work is
+ # done, which makes it possible to trace what the calculator was asked to do;
+ # the two values are then added with the + operator.
+ def add(a, b):
+     logging.info("add() called with a=%s, b=%s", a, b)
++>>>>>>> feature-b
      return a + b
```

### What the conflict markers mean

Git writes three markers into the file around every region it could not merge:

| Marker | Meaning |
| --- | --- |
| `<<<<<<< HEAD` | Start of the version on the current branch. `HEAD` here is `main`, which already contains feature-a's work. |
| `=======` | The divider between the two versions. Everything above it is "ours", everything below is "theirs". |
| `>>>>>>> feature-b` | End of the incoming version, labelled with the branch being merged in. |

Git performs a three-way merge: it compares each branch against the common ancestor
`eacb1d9`. Where only one side changed a region, Git takes that change silently.
`import logging` is an example of this in the diff above, it appears with a single
`+` and sits outside the markers because only `feature-b` touched that area. Where
both sides changed the same region to different things, Git has no rule for
deciding which one is correct, so it writes both into the file and stops.

The `diff --cc` header means "combined diff", the format Git uses to show a
conflicted file against both parents at once.

---

## Stage 8: Resolve the conflict by hand (Screenshot 3)

The conflicts were resolved by editing both files in the editor and deleting every
marker line manually. No `-X ours`, no `-X theirs`, and none of VS Code's
"Accept Current / Accept Incoming / Accept Both" buttons were used.

`README.md` was given a title that names both changes rather than keeping one and
throwing away the other:

```markdown
# Calculator Project - Input Validation and Logging Edition
```

`calc.py` was resolved so the final `add()` keeps both the validation and the
logging, with the comment rewritten to describe the merged behaviour:

```python
import logging

# Send log messages to the console with the level and the message shown.
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# add: returns the sum of two numbers, after validating both and logging the call.
# How it works: the call is first recorded with logging.info() so the run can be
# traced; isinstance() then checks each argument against int and float and raises
# a TypeError for anything else, which is logged as an error before it is raised
# so a bad call is visible in the log too; valid values are added with the +
# operator. This keeps feature-a's validation and feature-b's logging together.
def add(a, b):
    logging.info("add() called with a=%s, b=%s", a, b)
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        logging.error("add() got a non-numeric argument: a=%r, b=%r", a, b)
        raise TypeError("add() expects two numbers")
    return a + b
```

The log call was deliberately placed before the validation check so that a bad call
still shows up in the log, and the failure path got its own `logging.error()` line.

---

## Stage 9: Stage the resolved files, commit the merge and push

```
$ git add README.md calc.py

$ git status
On branch main
Your branch is up to date with 'origin/main'.

All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)

Changes to be committed:
        modified:   README.md
        modified:   calc.py

$ git commit -m "Resolve merge conflict between feature-a and feature-b"

$ git push origin main
```

`git add` on a conflicted file is what tells Git the conflict has been resolved;
the status message changes from "You have unmerged paths" to "All conflicts fixed
but you are still merging".

---

## Stage 10: git pull and the history graph (Screenshot 4)

```
$ git pull
Already up to date.

$ git log --oneline --graph --all
*   693bb81 (HEAD -> main, origin/main) Resolve merge conflict between feature-a and feature-b
|\
| * 797cd0f (origin/feature-b, feature-b) feature-b: add logging to add() and update README title
* | 8d28085 (origin/feature-a, feature-a) feature-a: add input validation to add() and update README title
|/
* eacb1d9 Initial commit: Python CLI calculator with README
```

`git pull` reports "Already up to date" because the local `main` and `origin/main`
point at the same commit. The graph shows the shape of the whole exercise: both
feature branches fork from `eacb1d9`, and the merge commit `693bb81` has two
parents and joins them back together.

---

## Stage 11: Confirm the merged program still runs

```
$ printf '1\n7\n5\n4\n9\n0\n5\n' | python calc.py

--- Calculator ---
1. Add
2. Subtract
3. Multiply
4. Divide
5. Exit
Choose an option (1-5): Enter the first number: Enter the second number: INFO: add() called with a=7.0, b=5.0
Result: 12.0

--- Calculator ---
1. Add
2. Subtract
3. Multiply
4. Divide
5. Exit
Choose an option (1-5): Enter the first number: Enter the second number: Result: Error: cannot divide by zero

--- Calculator ---
1. Add
2. Subtract
3. Multiply
4. Divide
5. Exit
Choose an option (1-5): Goodbye!
```

Both merged features are visible in this run: the `INFO: add() called with ...`
line comes from feature-b's logging, and `7 + 5 = 12.0` is correct. Divide by zero
returns the error message instead of crashing. Feature-a's validation only fires
when `add()` is called with something that is not a number, which the menu itself
prevents, so it acts as a guard for any code that imports and calls `add()`
directly.

---

## Summary of commits

| Commit | Branch | Description |
| --- | --- | --- |
| `eacb1d9` | main | Initial commit: calculator and README |
| `8d28085` | feature-a | Input validation in `add()`, README title changed |
| `797cd0f` | feature-b | Logging in `add()`, README title changed differently |
| `693bb81` | main | Merge commit resolving the conflict between the two |
