from vehicle import VehicleWrapper
class Fleet:
    def __init__(self):
        self._vehicles: list[VehicleWrapper] = []

    def fleet_add(self, vehicle_wrapper: VehicleWrapper):
        self._vehicles.append(vehicle_wrapper)

    def takeoff(self, targetAlt = 10):
        for vehicle in self._vehicles:
            vehicle.takeoff(10)
