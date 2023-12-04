import asyncio
# Import SITL
# Import DroneKit-Python
from dronekit import connect, Vehicle
# Import our classes
import src.connection as connection_handler
import src.vehicle as vehicle_handler
import src.fleet as fleet_handler

RUN_SIMULATOR = False
def get_connection() -> connection_handler.ConnectionManager:
    connection = connection_handler.ConnectionManager()
    if RUN_SIMULATOR:
        print("Start simulator (SITL)")
        connection.start_sim()
    else:
        connection.to("udpin:10.1.2.3:14550")
    return connection



_READY_ATTRIBUTES = ['gps_0', 'armed', 'mode', 'attitude'] # modified for MissionPlanner simulator
def make_vehicle(connection: connection_handler.ConnectionManager) -> Vehicle:
    # Connect to the Vehicle.
    print("Connecting to vehicle on: %s" % (connection.connection_string,))

    def makeVehicle(handler):
        instance = Vehicle(handler)
        print("Created Vehicle instance")
        instance._default_ready_attrs = _READY_ATTRIBUTES
        return instance

    return connect(connection.connection_string, baud=4800, wait_ready=True, vehicle_class=makeVehicle)


async def main():
    print("Starting up...")
    fleet = fleet_handler.Fleet()

    print("Connecting vehicle(s)...")
    connection_details = get_connection()
    vehicle = make_vehicle(connection_details)
    wrapper = vehicle_handler.VehicleWrapper(vehicle)
    wrapper.routine_preflight() # reset vehicle if flying with preflight routine
    fleet.fleet_add(wrapper)
    print("Connected.")

    print("Running fleet!")
    fleet.run()
    print("Fleet closed.")

    wrapper.close()
    if connection_details.sitl is not None:
        connection_details.sitl.stop()
    print("Completed")

asyncio.run(main())

print("Completed!")