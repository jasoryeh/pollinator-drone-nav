
RUN_SIMULATOR = False

import dronekit_sitl
sitl = None
connection_string = None

if RUN_SIMULATOR:
    print("Start simulator (SITL)")
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()
else:
    connection_string = "udpin:10.1.2.3:14550"

import time, sys
# Import DroneKit-Python
from dronekit import connect, Vehicle, VehicleMode, LocationGlobalRelative, LocationGlobal

_READY_ATTRIBUTES = ['gps_0', 'armed', 'mode', 'attitude'] # modified for MissionPlanner simulator

# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (connection_string,))
def makeVehicle(handler):
    instance = Vehicle(handler)
    print("Created Vehicle instance")
    instance._default_ready_attrs = _READY_ATTRIBUTES
    return instance

veh = connect(connection_string, baud=4800, wait_ready=True, vehicle_class=makeVehicle)
print("Connected.")

LOG_PREVIOUSLINE = '\033[F'
_summarize_out_msgs = []
_summarize_out_time_between = 0.1
'''
Summarize the data of interest to output.
'''
def summarize_out(vehicle):
    global _summarize_out_msgs
    for i in range(len(_summarize_out_msgs)):
        sys.stdout.write(LOG_PREVIOUSLINE)

    _summarize_out_msgs = []

    def msg(msg):
        _summarize_out_msgs.append(msg)

    # Get some vehicle attributes (state)
    msg("VEHICLE:")
    msg(" GPS: {vehicle.gps_0}")
    msg(" Battery: {vehicle.battery}")
    msg(" Last Heartbeat: {vehicle.last_heartbeat}")
    msg(" Is Armable?: {vehicle.is_armable}")
    msg(" System status: {vehicle.system_status.state}")
    msg(" Mode: {vehicle.mode.name}")  # settable
    msg(f" Position: {str(vehicle.location.global_frame)}")  # lat lon alt

    for m in _summarize_out_msgs:
        print(str(m))
    time.sleep(_summarize_out_time_between)

def arm_and_takeoff(vehicle, aTargetAltitude):
    print("Setting guided mode")
    vehicle.wait_for_mode("GUIDED", 30) # guided required for arming and flying
    print("Waiting for vehicle ready")
    vehicle.wait_for_armable(30)
    vehicle.arm(timeout=30)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt, end='\r')
        print()
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude*0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

def pre_arm(vehicle):
    if vehicle.armed:
        print("Vehicle is armed.")
        print("Configuring guided mode...")
        vehicle.wait_for_mode("GUIDED", timeout=30)
        print("Guided set, landing...")
        curr = vehicle.location.global_relative_frame
        print(curr)
        new = LocationGlobalRelative(curr.lat, curr.lon, 0)
        vehicle.simple_goto(new)
        print("Waiting for landing...")
        def landed():
            return vehicle.location.global_relative_frame.alt < 1
        vehicle.wait_for(landed, timeout=60)
        print("Disarming")
        vehicle.armed = False
        def whilearmed():
            return vehicle.arm
        vehicle.wait_for(whilearmed, 30)
        # TODO: Force Disarm - Drone does not disarm?
        #vehicle._master.mav.command_long_send(
        #        0,  # target_system
        #        0,
        #        mavlink.MAV_CMD_COMPONENT_ARM_DISARM, # command
        #        0, # confirmation
        #        0, # param1 (0 to indicate disarm)
        #        21196, # param2 (21196=force) (all other params meaningless)
        #        0, # param3
        #        0, # param4
        #        0, # param5
        #        0, # param6
        #        0) # param7
        print()
        print("Disarmed")
        print(vehicle.armed)


def vehicle_loop(vehicle):
    print("Pre-flight...")
    pre_arm(vehicle)
    input('Preflight complete, take off (enter)')
    try:
        print("Arming and taking off...")
        arm_and_takeoff(vehicle, 20)
        while True:
            summarize_out(vehicle)
    except KeyboardInterrupt:
        print("Exiting info!")


vehicle_loop(veh)

# Close vehicle object before exiting script
veh.close()

# Shut down simulator
if RUN_SIMULATOR:
    sitl.stop()
print("Completed")