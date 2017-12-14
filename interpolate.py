from state_entry import StateEntry

def interpolate(next_state, theta_options, theta_dot_options, Q):
    return Q[0][0].value