from dronekit import Vehicle, LocationGlobalRelative
import time, sys

WAIT_TIMEOUT = 30

LOG_PREVIOUSLINE = '\033[F'
_summarize_out_msgs = []
_summarize_out_time_between = 0.1

class VehicleWrapper:

    def __init__(self, vehicle: Vehicle):
        self.vehicle = vehicle
        self.timeout = WAIT_TIMEOUT

    def close(self) -> None:
        pass

    '''
    Summarize the data of interest to output.
    '''
    def flash_info(self) -> None:
        global _summarize_out_msgs
        for i in range(len(_summarize_out_msgs)):
            sys.stdout.write(LOG_PREVIOUSLINE)

        _summarize_out_msgs = []

        def msg(msg):
            _summarize_out_msgs.append(msg)
        
        vehicle = self.vehicle
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
    

    def guided(self):
        print("Setting guided mode...")
        self.vehicle.wait_for_mode("GUIDED", timeout=self.timeout)
        print("Guided mode set.")
    
    def is_landed(self):
        return (not self.vehicle.armed) and (self.vehicle.location.global_relative_frame.alt <= 1)
    
    def is_in_flight(self):
        return self.vehicle.armed and (self.vehicle.location.global_relative_frame.alt > 1);

    def land(self):
        if not self.vehicle.armed:
            print("Can't land when vehicle is not armed!")
            return
        
        # get location
        curr = self.vehicle.location.global_relative_frame
        print(curr)

        # create destination to altitude=0
        new = LocationGlobalRelative(curr.lat, curr.lon, 0)

        # set the destination
        self.vehicle.simple_goto(new)

        # wait
        print("Waiting for landing...")
        def landed():
            return self.vehicle.location.global_relative_frame.alt < 1
        self.vehicle.wait_for(landed, timeout=self.timeout)
    
    def takeoff(self, targetAlt = 10):
        if not self.vehicle.armed:
            print("Can't takeoff when vehicle is not armed!")
        self.vehicle.simple_takeoff(targetAlt)
    
    def wait_altitude(self, targetAlt):
        while True:
            print(" Altitude: ", self.vehicle.location.global_relative_frame.alt, end='\r')
            print()
            #Break and return from function just below target altitude.
            if self.vehicle.location.global_relative_frame.alt >= targetAlt*0.95:
                print("Reached target altitude")
                break
            time.sleep(1)
    
    def wait_arm(self):
        print("Waiting for ready to arm...")
        self.vehicle.wait_for_armable(self.timeout)
        print("Armable!")

    def arm(self):
        if self.vehicle.armed:
            print("Can't arm a vehicle that is already armed already!")
            return
        self.vehicle.arm(self.timeout)
    
    def disarm(self):
        if not self.vehicle.armed:
            print("Can't disarm when already disarmed!")
            return
        print("Disarming")
        self.vehicle.armed = False
        def whilearmed():
            return self.vehicle.armed
        self.vehicle.wait_for(whilearmed, timeout=self.timeout)
        print("Disarmed")
    
    '''
    Routine: Resets the drone to the ground if its armed/flying.
    '''
    def routine_reset(self):
        if not self.vehicle.armed:
            print("No need to safe reset, not armed!")
            return
        
        self.guided()
        self.land()
        self.disarm()
        
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

    def routine_preflight(self):
        if self.is_in_flight():
            print("Resetting drone...")
            self.routine_reset()
            print("Reset!")
        self.disarm()
    

    '''
    Routine: Land
    '''
    def routine_takeoff(self, targetAlt = 10):
        if self.is_in_flight():
            print("Can't takeoff, already armed and in-flight!")
            return
        
        print("Takeoff!")
        self.guided()
        self.wait_arm()
        self.arm()

        self.takeoff(targetAlt=targetAlt)
        self.wait_altitude(targetAlt=targetAlt)
