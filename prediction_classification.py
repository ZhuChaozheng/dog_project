




























# define some useful global variant, which we don't need to modify them in the blew functions.

initial_sensor_data = -3
# pose status variant
running = 0
stand_up = 1
sit_down = 2
lay = 3


# we should modified the variant value in below functions, so set variant as global.
# default, we think the initial pose is stand up,
last_pose = stand_up
current_pose = stand_up


# this function is used to calculate the offset value between two angles.
# angle1 is 0~180, -180~-0, angle2 is 0~180, -180~-0
def offset_angle(angle1, angle2):
    if (math.fabs(angle1 - angle2) > 180):
        angle = 360 - (math.fabs(angle1) + math.fabs(angle2))
    else:
        angle = math.fabs(angle1) - math.fabs(angle2)
    return math.fabs(angle)


# this function try to predict the current pose, mainly depend on two conditions,
# the last pose and current action. Specifically, the last pose include those
# states, which are stand up, sit down, lay, and running. For current action, it
# includes those actions, which are accelerated_velocity, angluar_velocity, angle
# offset. In order to calibrate the initial pose, we should command the dog to run
# as soon as possible. when the angluar_velocity is greater than 1, it must be
# running.

# sensor_data: accelerated_velocity, angular_velocity, pitch

def predictions_decision_tree(sensor_data):
    # since we will modify those variants value in the next steps
    global last_pose
    global current_pose
    # accelerated_velocity is used to classificate the pose of stand up or lay
    # when the last time is sit down
    accelerated_velocity = sensor_data[0]
    # angluar_velocity is used to classificate the pose of running
    angular_velocity = sensor_data[1]

    # initial_sensor_data[2] default is -3, now the pose is stand up or lay
    angle_offset = offset_angle(sensor_data[2], initial_sensor_data)

    # now, let us definite a thing that must happen when the angular_velocity
    # is greater than 1. it must be running. So, in order to initial our
    # system, when should command the dog to run as soon as possible.
    if angular_velocity > 1:
        current_pose = running
        print("running")

    else:

        # last_pose is stand_up, then the current_pose could among sit_down,
        # stand_up, and running. When the angular_velocity is bigger than 1, it
        # must be running. When the angle_offset is greater than 40, it must be
        # sit_down. Or it shoule be keep the same pose. However, when the sensor data
        # enter this function, it immediately hanle the variant of angular_velocity.
        # if it is greater than 1, it must be running.
        if last_pose == stand_up:
            elif angle_offset > 40:
                current_pose = sit_down
                print("sit_down")
            elif accelerated_velocity > 10:
                current_pose = lay
                print("lay")
            else:
                current_pose = stand_up
                print("stand_up")

        # last_pose is running, then the current_pose must between running and
        # stand_up. When the angular_velocity is greater than 1, it must be keep
        # running. Or it shoule be stand_up. However, when the sensor data
        # enter this function, it immediately hanle the variant of angular_velocity.
        # if it is greater than 1, it must be running.
        elif last_pose == running:
            current_pose = stand_up
            print("stand_up")

        # last_pose is sit_down, then the current_pose could among stand_up,
        # sit_down and lay. When comparing initial_sensor_data value(stand up),
        # the angle_offset is greater than 40, it must be sit_down. When the
        # accelerated_velocity is greater than 10, it must
        # be lay, since we place the sensor(only an IMU) on the front back of
        # dog. Or it shoule be stand_up, as the sensor's accelerated_velocity
        # keep in a stable range. this range must less than 10.

        elif last_pose == sit_down:
            if angle_offset > 40:
                current_pose = sit_down
                print("sit_down")
            elif accelerated_velocity > 10:
                current_pose = lay
                print("lay")
            else:
                current_pose = stand_up
                print("stand_up")

        # last_pose is lay, then the current_pose could between lay and sit_down.
        # When the accelerated_velocity is greater than 10, or angle_offset is
        # greater than 40, it must be sit_down. Or current_pose should keep lay.
        elif last_pose == lay:
            if accelerated_velocity > 10:
                current_pose = stand_up
                print("stand_up")
            elif accelerated_velocity > 10 and angle_offset > 40:
                current_pose = sit_down
                print("sit_down")
            else:
                current_pose == lay
                print("lay")

    last_pose = current_pose
