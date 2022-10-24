

def model(cached_normalized_and_scaled_landmarks):
    cache_size = len(cached_normalized_and_scaled_landmarks)
    lms = normalized_and_scaled_landmarks

    ## take subset of landmarks x[t] = (head, left hand, right hand, left knee, right knee)
    ## take (x,y,z) of each of them.
    ## relative velocity (x[t][left_hand] - x[t][right_hand]) - (x[t-1][left_hand] - x[t-1][right_hand])
    ## quantities: for each pair of limps one gets a relative velocity (so with 5 points there will be 10 relative velocities)
    ## sum up the relative velocities.
    

