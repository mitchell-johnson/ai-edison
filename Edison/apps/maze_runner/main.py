# Edison V3 - Maze Runner
# ========================
# This is your robot's program! Tell the AI what you want the robot to do
# and it will write the code here for you.
#
# The robot can:
#   - Drive forward, backward, turn left, turn right
#   - Detect obstacles in front of it
#   - Follow lines on the ground
#   - Flash LEDs and make sounds
#   - Read light levels
#
# To get started, tell the AI something like:
#   "Make the robot drive forward until it sees a wall, then turn right"

# --- Setup (don't change this) ---
import Ed

Ed.EdisonVersion = Ed.V3
Ed.DistanceUnits = Ed.CM
Ed.Tempo = Ed.TEMPO_MEDIUM

# --- Your program starts here ---

# Tell the AI what you want the robot to do!
# Example: "I want the robot to drive forward slowly"
Ed.Drive(Ed.FORWARD, Ed.SPEED_5, 10)
