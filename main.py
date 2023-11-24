# Simple PyMavLink Proof of Concept
# Connects and reads data from MavLink

from pymavlink import mavutil
import time

MAVLINK_PROTOCOL = 'udp'
# Mission Planner over VPN
MAVLINK_ADDRESS = '10.1.2.3:14550'


# Start a connection listening on a UDP port
connection_to = f'{MAVLINK_PROTOCOL}:{MAVLINK_ADDRESS}'
print(f"Making MAVLink connection: {connection_to}")
the_connection = mavutil.mavlink_connection(connection_to)

# Once connected, use 'the_connection' to get and send messages
handlers = {
    "GPS_RAW_INT": lambda v : print(f"GPS:\n\tLONG: {v.lon}; LATI: {v.lat}; ALT: {v.alt}; SATS: {v.satellites_visible}"),
    "SYSTEM_TIME": lambda v : print(f"SYSTEM_TIME: UNIX_USEC: {v.time_unix_usec}; RUNTIME: {v.time_boot_ms}"),
    "TIMESYNC": lambda v : print(f"TIME: {v.ts1}"),
    #"SIMSTATE": lambda v: print(f"SIMUALTOR: {v}"),
    "BATTERY_STATUS": lambda v: print(f"BATTERY:\n\tREMAINING: {v.battery_remaining}\n\tCURRENT: {v.current_battery}\n\tTIME_LEFT: {v.time_remaining}\n\tTEMPERATURE: {v.temperature}\n\tVOLTAGES: {v.voltages}")
    #"": lambda v: print
}
def print_summary(msgs):
    unsupported = []
    for key in msgs:
        if key in handlers:
            handlers[key](msgs[key])
        else:
            unsupported.append(key)
    print(f"\nUnsupported data: {len(unsupported)}\n\t{unsupported}")

# Wait for the first heartbeat 
#   This sets the system and component ID of remote system for the link
print("Waiting for heartbeat...")
the_connection.wait_heartbeat()
print("First heartbeat from system (system %u component %u)\n\n" % (the_connection.target_system, the_connection.target_component))
print("Keys found:", end='\n\t')
print(the_connection.messages.keys(), end='\n\n\n')
print_summary(the_connection.messages)

while True:
    the_connection.wait_heartbeat()
    print("Heartbeat (system %u component %u)" % (the_connection.target_system, the_connection.target_component))
    print_summary(the_connection.messages)
    #for key in the_connection.messages:
    #    print(f"{key}: {type(the_connection.messages[key])}")
    #    
    print("\n\n\n")
