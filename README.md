# Autonomous Pollinators Ground Software
Code for ground software.

## Initializing the repo
1. Clone the repo
2. Execute `source init.sh`
3. Run with `python main.py`

## Connecting to Mission Planner
In `main.py` find the line with `connection_string = "udpin:10.1.2.3:14550"` and 
change the IP address and port to one where your Mission Planner is mirroring/proxying
the MavLink connection.

# Model Data
Available on Roboflow: https://universe.roboflow.com/drone-dbsja/flower_dataset-podcd
