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
        print("Pre-flight...")
        veh = self._vehicles[0]
        veh.routine_preflight()

        input('Preflight complete, take off (enter)')
        try:
            print("Arming and taking off...")
            veh.routine_takeoff(20)
            while True:
                veh.flash_info()
        except KeyboardInterrupt:
            print("Exiting info!")
        return False

    def run(self) -> None:
        while True:
            if self.tick():
                break
