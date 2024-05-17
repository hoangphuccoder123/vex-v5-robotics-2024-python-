from vex import *
import time

# Brain should be defined by default
brain = Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
left_motor_a = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)    
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = DriveTrain(
    left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)
rollerintake = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)
nangha = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)
lift = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)


# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")


# define variables used for controlling motors based on controller inputs
rollerintake_status = True
nangha_status = True
nangha_status_b = True
nangha_status_a = True
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False
lift_status = True
# define a task that will handle monitoring inputs from controller_1


def opcontrol():
    global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, lift_status, remote_control_code_enabled, nangha_status, rollerintake_status
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:

            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3 + axis1
            # right = axis3 - axis1
            drivetrain_left_side_speed = controller_1.axis3.position()
            drivetrain_right_side_speed = controller_1.axis2.position()

            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller_1:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller_1 = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller_1:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller_1 = True

            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(
                    drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(
                    drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
            # Change rollerintake to x and b button
            if controller_1.buttonR1.pressing():
              #  rollerintake.set_max_torque(100, PERCENT)
              #  rollerintake.set_velocity(250, PERCENT)
                rollerintake.spin(FORWARD)
                rollerintake_status = False
                print(rollerintake_status)
            elif controller_1.buttonR2.pressing():
               # rollerintake.set_max_torque(100, PERCENT)
               # rollerintake.set_velocity(100, PERCENT)
                rollerintake.spin(REVERSE)
                rollerintake_status = False
                print(rollerintake_status)
            elif not rollerintake_status:
                rollerintake.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                rollerintake_status = True
               # Change nangha_motor_a to r1 r2 and motor_b to l1 l2 button
            if controller_1.buttonL1.pressing():
                nangha.set_max_torque(100, PERCENT)
                nangha.set_velocity(250, PERCENT)
                nangha.spin(FORWARD)
                nangha_status = False
            elif controller_1.buttonL2.pressing():
                nangha.set_max_torque(100, PERCENT)
                nangha.set_velocity(250, PERCENT)
                nangha.spin(REVERSE)
                nangha_status = False
            elif not nangha_status:
                nangha.stop()
# set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                nangha_status = True


            if controller_1.buttonLeft.pressing():
                lift.set_max_torque(100, PERCENT)
                lift.set_velocity(250, PERCENT)
                lift.spin(FORWARD)
                lift_status = False
            elif controller_1.buttonRight.pressing():
                lift.set_max_torque(100, PERCENT)
                lift.set_velocity(250, PERCENT)
                lift.spin(REVERSE)
                lift_status = False
            elif not lift_status:
                lift.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                lift_status = True
        # wait before repeating the process
        wait(20, MSEC)


# define variable for remote controller enable/disable
remote_control_code_enabled = True

def lay_bong():
    nangha.spin(FORWARD, 250)
    time.sleep(0.5)
    nangha.stop()

def nha_bong():
    nangha.spin(REVERSE, 250)
    time.sleep(0.5)
    nangha.stop()

def nang_khung():
    rollerintake.spin(REVERSE,250)
    time.sleep(0.5)
    rollerintake.stop()
    
def ha_khung():
    rollerintake.spin(FORWARD,150)
    time.sleep(0.5)
    rollerintake.stop()

def drivetrain_auto():
    nang_khung()
    nangha.spin(FORWARD)
    drivetrain.drive_for(FORWARD,170, DistanceUnits.CM, 88, PERCENT)
    drivetrain.turn_for( RIGHT, 170, DEGREES, 70, PERCENT)
    nha_bong()
    ha_khung()
    drivetrain.drive_for(REVERSE, 30, DistanceUnits.CM, 80, PERCENT)
    drivetrain.drive_for(FORWARD, 70, DistanceUnits.CM, 100, PERCENT)
    drivetrain.drive_for(REVERSE, 80, DistanceUnits.CM, 80, PERCENT)
    drivetrain.turn_for(RIGHT, 90 , DEGREES, 70, PERCENT)
    drivetrain.drive_for(FORWARD, 150, DistanceUnits.CM, 80, PERCENT)
    drivetrain.turn_for( RIGHT, 90, DEGREES, 80, PERCENT)
    drivetrain.drive_for(FORWARD,50, DistanceUnits.CM, 80, PERCENT)
def go_auto():
    # Start the autonomous control tasks
    auton_task_2 = Thread(drivetrain_auto)
    # wait for the driver control period to end
    while (competition.is_autonomous() and competition.is_enabled()):
        # wait 10 milliseconds before checking again
        wait(10, MSEC)
    # Stop the autonomous control tasks
    auton_task_2.stop()


def go_driver():
    # Start the driver control tasks
    driver_control_task = Thread(opcontrol)

    # wait for the driver control period to end
    while (competition.is_driver_control() and competition.is_enabled()):
        # wait 10 milliseconds before checking again
        wait(10, MSEC)
    # Stop the driver control tasks
    driver_control_task.stop()


# register the competition functions
competition = Competition(go_driver, go_auto)