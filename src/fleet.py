from src.vehicle import VehicleWrapper

class Fleet:
    def __init__(self):
        self._vehicles: list[VehicleWrapper] = []

    def fleet_add(self, vehicle_wrapper: VehicleWrapper) -> None:
        self._vehicles.append(vehicle_wrapper)

    def takeoff(self, targetAlt = 10) -> None:
        for vehicle in self._vehicles:
            vehicle.takeoff(10)

    def tick(self) -> bool:
        pass

    def run(self) -> None:
        while True:
            if self.tick():
                break
