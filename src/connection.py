import dronekit_sitl

class ConnectionManager:
    def __init__(self):
        self.sitl = None
        self.connection_string = None

    def start_sim(self) -> None:
        print("Start simulator (SITL)...")
        self.sitl = dronekit_sitl.start_default()
        self.connection_string = sitl.connection_string()
        print("Simulator started.")

    def to(self, to) -> None:
        self.sitl = None
        self.connection_string = to

