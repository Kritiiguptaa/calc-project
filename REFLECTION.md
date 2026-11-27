# Reflection: Creating and Resolving a Merge Conflict

**Course:** UCS 745 Cloud and DevOps
**Assignment:** Q1, Git and GitHub workflow
**Repository:** https://github.com/Kritiiguptaa/calc-project

## What the task was

For this assignment I built a small Python command line calculator with four
operations and division by zero handling, but the calculator itself was not really
the point. The actual exercise was the Git workflow around it: initialising a local
repository, pushing it to GitHub, making two branches that change the same code in
different ways, and then merging them so that a conflict happens and I have to fix
it myself. I had seen merge conflicts before in a group project and my reaction had
mostly been to panic and ask someone else to deal with it, so doing one on purpose
and having to read it carefully was useful.

## What caused the conflict

Both of my branches started from the same commit. After the first commit on `main`
(`eacb1d9`) I created `feature-a` and changed two things: the title line of
`README.md`, and the body of the `add()` function so that it validates its inputs
with `isinstance()` and raises a `TypeError` if it gets something that is not a
number. I committed that and pushed it.

Then I went back to `main` before creating `feature-b`. This step turned out to be
the one that matters. If I had created `feature-b` while still standing on
`feature-a`, the new branch would have already contained feature-a's commit and
there would have been nothing to disagree about, because one change would simply
have come after the other in a straight line. Branching from `main` instead meant
both branches had `eacb1d9` as their common ancestor and neither knew anything
about the other. On `feature-b` I changed the same README title line to something
else, and rewrote the same lines of `add()` to log its arguments with
`logging.info()` instead of validating them.

Merging `feature-a` into `main` was clean. Git did not even make a merge commit for
it, it just reported `Fast-forward` and moved the `main` pointer up to feature-a's
commit, because `main` had nothing of its own since the common ancestor. I did not
expect that at first and had to look it up: a fast forward is not really a merge at
all, it is Git noticing that the target branch is strictly behind and sliding the
label forward.

Merging `feature-b` was where it broke:

```
Auto-merging README.md
CONFLICT (content): Merge conflict in README.md
Auto-merging calc.py
CONFLICT (content): Merge conflict in calc.py
Automatic merge failed; fix conflicts and then commit the result.
```

The reason is that Git merges by comparing both branches against their common
ancestor, a three way merge. For any region of a file that only one side changed,
it can safely take that change, and it does so without telling you. The clearest
example in my own diff was the `import logging` line. Only `feature-b` added it and
`feature-a` never touched that part of the file, so Git merged it silently and it
appeared in the diff with a single `+`, outside the conflict markers. But the
README title line and the lines inside `add()` were changed by both branches, to
different things, starting from the same original. There is no information anywhere
in the repository that would let Git decide whether validation or logging is the
correct outcome. Both are valid edits by the same author. So it stopped and asked
me.

## The exact steps I took to resolve it

First I ran `git status`, which told me the repository was in a paused state:

```
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
        both modified:   README.md
        both modified:   calc.py
```

The phrase "both modified" is a precise description of what went wrong, and
`git merge --abort` being offered right there was reassuring, because it meant I
could get back to a clean `main` at any point if I made a mess of the resolution.
No commit had been created yet and `HEAD` had not moved.

Then I ran `git diff` to see the conflicted regions. Git had rewritten the
conflicting parts of both files in place, wrapped in three markers:

```
<<<<<<< HEAD
# Calculator Project - Input Validation Edition
=======
# Calculator Project - Logging Edition
>>>>>>> feature-b
```

Once I understood what the three markers are, they stopped looking like damage to
the file. `<<<<<<< HEAD` opens the version from the branch I am currently on, which
was `main` and therefore contained feature-a's work. `=======` is just the divider.
`>>>>>>> feature-b` closes the version coming in from the branch being merged, and
it is helpfully labelled with that branch name. The whole block is only text that
Git has inserted into my working file. It is not in any commit and it is not a
special file format; it is a question written into the file for me to answer by
deleting the parts that should not survive.

I resolved both files by opening them in the editor and editing them by hand. VS
Code offered me "Accept Current Change", "Accept Incoming Change" and "Accept Both
Changes" buttons directly above the conflict, and I deliberately did not use them,
partly because the assignment required a manual resolution and partly because
"Accept Both" would have given me nonsense here anyway. It would have pasted
feature-a's `def add(a, b):` and feature-b's `def add(a, b):` one after the other
and produced a file that does not even run.

For `README.md` I did not pick a side at all. Picking one would have thrown away
real work, so I wrote a third version of the line that names both changes:

```markdown
# Calculator Project - Input Validation and Logging Edition
```

For `calc.py` I had to actually think about what the combined function should do
rather than just stacking the two versions. I kept both the validation and the
logging, but I put the `logging.info()` call before the `isinstance()` check on
purpose, so that a bad call still gets recorded in the log rather than disappearing
into an exception. I also added a `logging.error()` line on the failure path, which
was in neither branch, because once the two features live in the same function it
would be strange for the error case to be the one thing that is not logged. Then I
rewrote the comment above the function, since the comments from both branches had
become inaccurate descriptions of what the merged code actually does.

After that I deleted every remaining marker line, searched the files to make sure
none were left, and checked that the file still compiled before going any further.

Finally:

```
git add README.md calc.py
git commit -m "Resolve merge conflict between feature-a and feature-b"
git push origin main
```

I had not realised before this that `git add` is what signals the resolution. The
status message changed from "You have unmerged paths" to "All conflicts fixed but
you are still merging", which made it clear that staging the file is me telling Git
that I have dealt with it. Git does not check my work, it simply trusts that
whatever is in the file now is what I meant, which is slightly alarming and also
exactly why committing a file with the markers still in it is such a common
mistake.

The resulting history, from `git log --oneline --graph --all`, shows the shape of
the whole thing:

```
*   693bb81 (HEAD -> main, origin/main) Resolve merge conflict between feature-a and feature-b
|\
| * 797cd0f (origin/feature-b, feature-b) feature-b: add logging to add() and update README title
* | 8d28085 (origin/feature-a, feature-a) feature-a: add input validation to add() and update README title
|/
* eacb1d9 Initial commit: Python CLI calculator with README
```

I then ran the calculator again to confirm the merged code works. Adding 7 and 5
printed `INFO: add() called with a=7.0, b=5.0` followed by `Result: 12.0`, so
feature-b's logging survived, and dividing by zero still returned the error message
rather than crashing.

## What I learned about distributed version control

The thing that landed hardest is the difference between my local repository and the
remote one. After `git commit` the commit exists only on my laptop, in
`.git`, and GitHub knows nothing about it until I push. That is what "distributed"
means in practice: every clone is a complete repository with the full history, not
a thin view of a server. GitHub is not special to Git, it is just another copy that
my repository happens to call `origin` and that everyone has agreed to treat as the
shared one. It also explains why both `git push` and `git pull` exist at all. In a
centralised system you would just save; here, syncing is an explicit action in each
direction, and `git pull` reporting "Already up to date" was a reminder that local
and remote drift apart silently until you make them talk.

I also understand branches better now. A branch is not a copy of the project, it is
a movable label pointing at one commit, which is why making one is instant and why
`git checkout -b` costs nothing. That also made the fast forward merge make sense.
`main` had not moved since the common ancestor, so merging feature-a was just a
matter of moving the label, with no new commit needed. The merge commit for
feature-b is the opposite case: it is the one commit in my history with two parents,
which is how the branching is recorded permanently rather than being flattened away.

Most of all I stopped seeing conflicts as errors. A conflict is not Git failing, it
is Git succeeding at detecting that two people made incompatible decisions about
the same lines and then refusing to guess. It can diff, it can see that the base
said one thing and the two branches say two different things, but it has no idea
whether input validation or logging is more important to this project, and any rule
it invented for choosing would quietly destroy somebody's work. Escalating to the
human is the correct behaviour. The fact that I had to actually combine the two
features, reorder the log call, add an error log and rewrite the comment is proof of
that, because none of those decisions are derivable from the diff. No automatic
strategy would have produced the file I ended up with.

The practical lessons I am taking away are to branch from an up to date `main`
rather than from whatever branch I happen to be standing on, to pull before starting
work and merge often so that branches do not drift far enough apart to make
conflicts large, to read `git status` instead of guessing when something is wrong,
and to always run the code after resolving a conflict. A merge that produces a file
with no conflict markers is not the same thing as a merge that produces a file that
works, and Git only guarantees the first one.
