# ntu-ai-2015-spring
NTU Introduction to AI 2015 spring Final Project

## Coding Style

We are mainly using Python, and Python cares the coding style very much. So
let's follow [PEP8](https://www.python.org/dev/peps/pep-0008/).

## Git Workflow

It would be better if we all follow [git-flow](http://nvie.com/posts/a-successful-git-branching-model/), but it might not be that easy for git beginner.
Instead, here are some basic and easy instruction for all team members:

- Work on your own branch.
  ```
  git checkout -b your-new-feature
  ```
- Before coding, please update master and rebase/merge your branch against to
  master.
  ```
  # suppose you're now at branch-1
  # make sure you've committed all your changes
  git checkout master
  git pull -u origin master
  git checkout branch-1

  # then merge
  git merge master
  # or better -- rebase
  git rebase -i master
  ```
- Commit message should be clear and concise.
