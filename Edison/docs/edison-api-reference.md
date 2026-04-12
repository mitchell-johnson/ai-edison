# Edison V3 API Quick Reference

This is the complete list of commands the Edison V3 robot understands.
All commands start with `Ed.` — the AI knows how to use all of these.

## Movement

| Command | What it does |
|---------|-------------|
| `Ed.Drive(direction, speed, distance)` | Move the whole robot |
| `Ed.DriveLeftMotor(speed, distance)` | Move just the left wheel |
| `Ed.DriveRightMotor(speed, distance)` | Move just the right wheel |

**Directions:** `Ed.FORWARD`, `Ed.BACKWARD`, `Ed.SPIN_LEFT`, `Ed.SPIN_RIGHT`, `Ed.STOP`

**Speeds:** `Ed.SPEED_1` (slowest) through `Ed.SPEED_10` (fastest)

**Distance:** Number in cm (or inches if you change units). Use `Ed.DISTANCE_UNLIMITED` to keep going forever.

## Sensors

| Command | What it returns |
|---------|----------------|
| `Ed.ReadObstacleDetection()` | What's in front: `Ed.OBSTACLE_AHEAD`, `Ed.OBSTACLE_LEFT`, `Ed.OBSTACLE_RIGHT`, `Ed.OBSTACLE_NONE` |
| `Ed.ReadLineState()` | Line position: `Ed.LINE_ON_BLACK`, `Ed.LINE_ON_WHITE`, `Ed.LINE_LEFT_ON_BLACK`, `Ed.LINE_RIGHT_ON_BLACK` |
| `Ed.ReadLineTracker()` | Raw line sensor value (number) |
| `Ed.ReadLeftLightLevel()` | Left light sensor (0-1000) |
| `Ed.ReadRightLightLevel()` | Right light sensor (0-1000) |
| `Ed.ReadKeypad()` | Button pressed: `Ed.KEYPAD_ROUND`, `Ed.KEYPAD_TRIANGLE`, `Ed.KEYPAD_NONE` |
| `Ed.ReadClapSensor()` | Clap detected: `Ed.CLAP_DETECTED` or `Ed.CLAP_NOT_DETECTED` |
| `Ed.ReadDistance()` | Distance travelled since last reset (in cm) |
| `Ed.ReadRemote()` | Remote control button pressed |

## Lights & Sound

| Command | What it does |
|---------|-------------|
| `Ed.LeftLed(state)` | Left LED on/off: `Ed.ON` or `Ed.OFF` |
| `Ed.RightLed(state)` | Right LED on/off: `Ed.ON` or `Ed.OFF` |
| `Ed.PlayBeep()` | Play a short beep |
| `Ed.PlayTone(frequency, duration)` | Play a specific tone |

## Timing

| Command | What it does |
|---------|-------------|
| `Ed.TimeWait(duration, unit)` | Pause the program |

**Time units:** `Ed.TIME_SECONDS`, `Ed.TIME_MILLISECONDS`

## Setup Commands (use at the top of your program)

```python
import Ed                          # REQUIRED — must be the first line

Ed.EdisonVersion = Ed.V3          # Always use this for V3 robots
Ed.DistanceUnits = Ed.CM          # or Ed.INCH
Ed.Tempo = Ed.TEMPO_MEDIUM        # Music speed
Ed.ObstacleDetectionBeam(Ed.ON)   # Turn on obstacle sensor
Ed.LineTrackerLed(Ed.ON)          # Turn on line tracker
Ed.ResetDistance()                 # Zero the distance counter
```

## Important Rules

1. **`import Ed` is required** — Must be the first line of every program
2. **No classes** — Edison doesn't support Python classes
3. **No try/except** — Error handling isn't supported
4. **Simple types only** — Use numbers, strings, lists, and basic variables
5. **Functions are OK** — You can define functions with `def`
6. **Loops are OK** — `while` and `for` loops work fine
7. **If/else works** — Conditional logic is fully supported
