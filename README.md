# LearningToRideABike
In this project, our goal is to use reinforcement learning to balance a bicycle that moves with constant speed. More specifically, we only look at the lean angel of the bicycle and try to keep it balanced by steering the handlebars, while it moves with a constant speed. For the reinforcement learning method, we chose to use *fitted value iteration (FVI)*. 

## How to use
Download the repository and run main.py (it works with python3.6, at least)
```bash
$ python main.py
```
Then, it prints logs while it is learning to ride! It does at least 10 iterations of *FVI* and the average change in state values should get less than 1.

After that, it asks to pick the initial value for theta and theta_dot from the provided lists. The simulation starts after entering these values and it stops after 50 seconds of simulation or when the lean angle of bike gets too high. After stopping the simulation, it asks for the initial values for theta and theta_dot again to start simulation with the new initial values.

## Details

Specifications of the components of the algorithm are as below:
- States: We define each state S as s := (θ,θ ̇) which correspond to the leaning angle and the angular velocity about the z-axis. We constrained and discretized these values to be 17 equally spaced values in range of [−12,+12] for θ and 17 equally spaced values in range of [−3,+3] for θ ̇.
- Actions: Actions are defined to be the steering angles which are also constrained and discretized. We have defined them to be a ∈ −6, −3, 0, +3, +6 degrees.
- Rewards: We defined the reward for state s = {θ,θ ̇} to be R(s) = c2 −θ2 −(0.1)θ ̇2. c is a constant set to 0.5 in our code.
- Gamma: The constant γ is set to be 0.9 in our code.

## Authors

* [**Saeid Naderiparizi**](https://github.com/saeidnp)
* [**Setareh Cohan**](https://github.com/setarehc)
