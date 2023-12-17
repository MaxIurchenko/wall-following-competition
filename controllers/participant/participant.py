"""Sample Webots controller for the wall following benchmark."""

from controller import Robot


def getDistance(sensor):
    
    return ((1000 - sensor.getValue()) / 1000) * 5


# Maximum speed for the velocity value of the wheels.
# Don't change this value.
MAX_SPEED = 6.28

# Get pointer to the robot.
robot = Robot()

# Get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# Get pointer to the robot wheels motors.
leftWheel = robot.getDevice('left wheel')
rightWheel = robot.getDevice('right wheel')

# We will use the velocity parameter of the wheels, so we need to
# set the target position to infinity.
leftWheel.setPosition(float('inf'))
rightWheel.setPosition(float('inf'))

# Get and enable the distance sensors.
frontSensor = robot.getDevice("so3")
frontSensor.enable(timestep)
sideSensor = robot.getDevice("so0")
sideSensor.enable(timestep)

# Move forward until we are 50 cm away from the wall.
leftWheel.setVelocity(MAX_SPEED)
rightWheel.setVelocity(MAX_SPEED)
while robot.step(timestep) != -1:
    if getDistance(frontSensor) < 0.1:
        break

# Rotate clockwise until the wall is to our left.
leftWheel.setVelocity(MAX_SPEED * 0.7)
rightWheel.setVelocity(-MAX_SPEED * 0.7)
while robot.step(timestep) != -1:
    # Rotate until there is a wall to our left, and nothing in front of us.
    if getDistance(sideSensor) < 1:
        break

# Main loop.
while robot.step(timestep) != -1:

    # Too close to the wall, we need to turn right.
    if getDistance(sideSensor) < 0.1:
        leftWheel.setVelocity(MAX_SPEED)
        rightWheel.setVelocity(MAX_SPEED * 0.5)
        print(getDistance(sideSensor))
        
    elif getDistance(frontSensor) < 0.2:
        leftWheel.setVelocity(MAX_SPEED)
        rightWheel.setVelocity(-MAX_SPEED)
        robot.step(300)
        print(getDistance(frontSensor))

    # Too far from the wall, we need to turn left.
    elif getDistance(sideSensor) > 0.2:
        leftWheel.setVelocity(MAX_SPEED * 0.5)
        rightWheel.setVelocity(MAX_SPEED)
        print(getDistance(sideSensor))

    # We are in the right direction.
    else:
        leftWheel.setVelocity(MAX_SPEED)
        rightWheel.setVelocity(MAX_SPEED)

# Stop the robot when we are done.
leftWheel.setVelocity(0)
rightWheel.setVelocity(0)
