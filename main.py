
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
import src.vehicle as vehicle_handler

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

wrapper = vehicle_handler.VehicleWrapper(veh)


def pre_arm(wrapper):
    if wrapper.is_in_flight():
        print("Resetting drone...")
        wrapper.routine_reset()
        print("Reset!")
    wrapper.disarm()


def vehicle_loop(vehicle):
    print("Pre-flight...")
    pre_arm(wrapper)

    input('Preflight complete, take off (enter)')
    try:
        print("Arming and taking off...")
        wrapper.routine_takeoff(20)
        while True:
            wrapper.flash_info()
    except KeyboardInterrupt:
        print("Exiting info!")


vehicle_loop(veh)

# Close vehicle object before exiting script
veh.close()

# Shut down simulator
if RUN_SIMULATOR:
    sitl.stop()
print("Completed")