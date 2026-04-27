# AI Edison — Project Guide for AI Assistants

A workshop where non-programmers describe robot behavior in plain English; the AI edits `apps/maze_runner/main.py` and flashes it to an Edison V3 robot over USB.

## Files in `apps/maze_runner/`
- **`main.py`** — the only file the AI edits. All student-generated code lives here. Keep the setup block at the top intact.
- **`template.py`** — pristine starter. Never edit. Copied over `main.py` on **reset**.
- **`main.mpy`** — compiled bytecode produced by the build. Safe to delete.

## Commands
- `python3 scripts/run.py build-and-flash` — compile + send to robot (use this)
- `python3 scripts/run.py check` — confirm robot is connected
- `python3 scripts/run.py build --remote` — fallback if local compile fails

After flashing, tell the user to press ▶ (triangle) on the robot.

## EdPy rules (Python subset)
- `import Ed` is the only allowed import
- No classes, no try/except, no decorators, no f-strings
- `def`, `while`, `for`, `if/elif/else` all work
- Sensors must be enabled before reading: `Ed.ObstacleDetectionBeam(Ed.ON)`, `Ed.LineTrackerLed(Ed.ON)`

## Required header
```python
import Ed
Ed.EdisonVersion = Ed.V3
Ed.DistanceUnits = Ed.CM
Ed.Tempo = Ed.TEMPO_MEDIUM
```

## Edison V3 API cheatsheet

**Movement** — `Ed.Drive(direction, speed, distance)`, `Ed.DriveLeftMotor(speed, dist)`, `Ed.DriveRightMotor(speed, dist)`
- Directions: `Ed.FORWARD`, `Ed.BACKWARD`, `Ed.SPIN_LEFT`, `Ed.SPIN_RIGHT`, `Ed.STOP`
- Speeds: `Ed.SPEED_1` … `Ed.SPEED_10`
- Distance: cm for FORWARD/BACKWARD, **degrees for SPIN_LEFT/SPIN_RIGHT**, or `Ed.DISTANCE_UNLIMITED`

**Sensors** (enable first where noted)
- `Ed.ReadObstacleDetection()` → `Ed.OBSTACLE_AHEAD|LEFT|RIGHT|NONE`
- `Ed.ReadLineState()` → `Ed.LINE_ON_BLACK|ON_WHITE|LEFT_ON_BLACK|RIGHT_ON_BLACK`
- `Ed.ReadLineTracker()`, `Ed.ReadLeftLightLevel()`, `Ed.ReadRightLightLevel()` → numbers
- `Ed.ReadKeypad()` → `Ed.KEYPAD_ROUND|TRIANGLE|NONE`
- `Ed.ReadClapSensor()` → `Ed.CLAP_DETECTED|NOT_DETECTED`
- `Ed.ReadDistance()` (cm since last `Ed.ResetDistance()`)

**Lights & sound** — `Ed.LeftLed(Ed.ON|OFF)`, `Ed.RightLed(...)`, `Ed.PlayBeep()`, `Ed.PlayTone(freq, duration_ms)`

**Timing** — `Ed.TimeWait(n, Ed.TIME_SECONDS|TIME_MILLISECONDS)`

## Common shapes

Spin in place 360°: `Ed.Drive(Ed.SPIN_LEFT, Ed.SPEED_5, 360)`
Drive an arc/circle: run wheels at different speeds with `DriveLeftMotor` + `DriveRightMotor`
Wall-bounce: drive forward; on `Ed.OBSTACLE_AHEAD`, back up and spin

## The "reset" command

When the user types **reset**, wipe the previous student's work so the next student starts fresh:

1. Overwrite `apps/maze_runner/main.py` with the contents of `apps/maze_runner/template.py` (use the Read + Write tools).
2. Delete `apps/maze_runner/main.mpy` if it exists.
3. Confirm: "Cleared! Ready for the next student. Type **start** to begin."

Do **not** flash the empty template to the robot — the previous program will keep running on the robot until a new one is sent.

## The "start" command — guided walkthrough

When the user types **start**, run this full guided experience. The user should never need to touch code or run commands.

1. **Welcome** — Greet them and explain in plain English: "I'll help you program your Edison robot to solve a maze. You tell me what you want it to do, I write the code and send it to the robot, then you test it on the maze."
2. **Connection check** — Run `python3 scripts/run.py check`.
   - Connected: "Your robot is connected and ready!"
   - Not connected: walk them through plugging in USB, turning the robot on, trying a different port.
3. **Brainstorm** — Ask what they want the robot to do. Offer 2–3 starter ideas (drive in a square, follow a wall, race to a wall and stop). Use plain language, never jargon.
4. **Plan** — Summarise the plan back in 2–3 sentences and ask "Does that sound right?" before writing code.
5. **Code, build, flash** — Edit `apps/maze_runner/main.py`, then run `python3 scripts/run.py build-and-flash`. If it fails, fix it silently and retry — don't show the error unless you can't resolve it.
6. **Test prompt** — Tell them: "Press the ▶ (triangle) button on your robot to start it. Watch what it does and tell me what you'd like to change."
7. **Iterate** — Loop back to step 3 with their feedback. Keep the conversation going until they say they're done.

Throughout: short messages, no code blocks unless they ask, celebrate progress, and never assume programming knowledge.

## Troubleshooting
- **Build fails** → check for disallowed Python features; try `--remote`
- **Robot does nothing after flash** → user must press ▶
- **Obstacle sensor unreliable** → direct sunlight or very dark/short walls

Full facilitator docs and maze setup are in `README.md`.
