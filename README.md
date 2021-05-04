# Using Q-Learning to Learn How To Play Tic-Tac-Toe

<img src="./images/tictactoe.png" width="250">

test the game: [tictactoe](https://tictactoereinforcementlearning.herokuapp.com/)

## Overview
This project follows the description of the Q Learning table described in Playing Tic-Tac-Toe with Reinforcement Learning.

## Installation Dependencies:
* Python 2.7 or 3
* Flask 1.1.2
* pandas 1.1.5
* jupyter 

## What is Q learning?
Q-learning is a model-free reinforcement learning algorithm to learn the value of an action in a particular state. It does not require a model of the environment (hence "model-free"), and it can handle problems with stochastic transitions and rewards without requiring adaptations.

The core of the algorithm is a Bellman equation as a simple value iteration update, using the weighted average of the old value and the new information:

<img src="./images/equation.png" width="1000">


## A brief exemplo of how the algorithm work



2. Modify `deep_q_network.py`'s parameter as follow:
```python
OBSERVE = 10000
EXPLORE = 3000000
FINAL_EPSILON = 0.0001
INITIAL_EPSILON = 0.1
```

