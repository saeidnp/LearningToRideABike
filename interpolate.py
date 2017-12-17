from state_entry import StateEntry
import constants as consts

def interpolateValue(next_state, theta_options, theta_dot_options, Q):
    theta = next_state[0]
    theta_dot = next_state[1]

    if(abs(theta) > consts.theta_max):
        return -1000000

    nearest_theta_idx = findNearest(theta, theta_options)
    nearest_theta_dot_idx = findNearest(theta_dot, theta_dot_options)

    return Q[nearest_theta_dot_idx][nearest_theta_idx].value


def interpolateAction(next_state, theta_options, theta_dot_options, Q):
    theta = next_state[0]
    theta_dot = next_state[1]

    nearest_theta_idx = findNearest(theta, theta_options)
    nearest_theta_dot_idx = findNearest(theta_dot, theta_dot_options)

    nearest_theta_idx2 = nearest_theta_idx
    nearest_theta_dot_idx2 = nearest_theta_dot_idx

    if(theta < theta_options[nearest_theta_idx]):
        if(nearest_theta_idx - 1 >= 0):
            nearest_theta_idx2 = nearest_theta_idx - 1
    else:
        if(nearest_theta_idx + 1 < len(theta_options)):
            nearest_theta_idx2 = nearest_theta_idx + 1

    if(theta_dot < theta_dot_options[nearest_theta_dot_idx]):
        if(nearest_theta_dot_idx - 1 >= 0):
            nearest_theta_dot_idx2 = nearest_theta_dot_idx - 1
    else:
        if(nearest_theta_dot_idx + 1 < len(theta_dot_options)):
            nearest_theta_dot_idx2 = nearest_theta_dot_idx + 1

    action1 = _interpolate(theta,\
                    theta_options[nearest_theta_idx], Q[nearest_theta_dot_idx][nearest_theta_idx].best_action,\
                    theta_options[nearest_theta_idx2], Q[nearest_theta_dot_idx][nearest_theta_idx2].best_action)

    action2 = _interpolate(theta,\
                    theta_options[nearest_theta_idx], Q[nearest_theta_dot_idx2][nearest_theta_idx].best_action,\
                    theta_options[nearest_theta_idx2], Q[nearest_theta_dot_idx2][nearest_theta_idx2].best_action)

    return _interpolate(theta_dot,\
                theta_dot_options[nearest_theta_dot_idx], action1,\
                theta_dot_options[nearest_theta_dot_idx2], action2)


def findNearest(val, list):
    res = 0
    min_val = abs(list[0] - val)
    for i in range(len(list)):
        distance = abs(list[i] - val)
        if distance < min_val:
            min_val = distance
            res = i
    return res

def _interpolate(val, point1, point1_val, point2, point2_val):
    if(point1 == point2):
        return point1_val
    return (abs(val - point2) * point1_val + abs(val - point1) * point2_val) / abs(point2 - point1)