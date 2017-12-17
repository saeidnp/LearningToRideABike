# LearningToRideABike
CPSC 526 final project - fall 2017

## How to use
Download the repository and run main.py (it works with python3.6, at least)
```bash
$ python main.py
```
Then, it pring buch of logs while it is learning to ride! It does at least 10 iterations of FVI and the average change in state values should get less than 1.

After that, it asks to pick the initial value for theta and theta_dot from the provided lists. The simulation starts, after entering them and it stops after 50 seconds of simulation or when the lean angle of bike gets too high. After stopping simulation, it asks for the initial values for theta and theta_dot again to start simulation with the new initial values.
