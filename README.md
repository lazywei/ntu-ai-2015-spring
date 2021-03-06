# ntu-ai-2015-spring
NTU Introduction to AI 2015 spring Final Project

## Author list

1. B00201015 洪仲言
2. B00201037 張志瑋     Skype :jrweizhang
3. R03922125 賴洋
4. R03922134 鍾文藍
5. R03944030 羅國宣     Skype :tonylo2ooo

## Requirement

1. install [redis] (http://redis.io/topics/quickstart)
2. install python redis `pip install redis`

## Usage

1. redis-server
2. python supervisor.py
3. python animation_interactive/interactive.py

## Reference
We haven't refer any lib or rep, yet.

## Pseudo-code

```
class Supervisor:
  state = new State
  cars = state.getCars()

  for car in cars:
    nextAction = AI.nextStep(car.id, state)
    state = state.getStateByAction(car.id, nextAction)
    Drawer.draw(state)

class State
  - map: a static or dynamic matrix indicating the world
  - cars: including cars position

  def getMap()
    return current map matrix

  def getCars()
    return all cars

  def getSucc(carId)
    return possible actions

  def getStateByAction(carId, action)
    move carId according to the action
    # dynamics happen here
    return a new State


class Drawer
  def draw(state)
    draw according to
      - state.getMap()
      - state.getCars()

class AI
  def getNextAction(carId, state)
    actions = state.getSucc(carId)

    for action in actions:
      nextState = state.getStateByAction(carId, action)

    return next action according to certain Algorithm

```

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


