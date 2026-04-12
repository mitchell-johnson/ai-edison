# AI Edison — Maze Challenge Project

## What This Is

A workshop project where **non-programmers** use AI (GitHub Copilot or Claude) to control
an Edison V3 robot through a maze. Participants describe what they want in plain English,
the AI writes the code, and it gets deployed to the robot automatically.

## Project Structure

```
ai-edison/
├── CLAUDE.md              ← You are here (project guide for AI assistants)
├── README.md              ← Workshop setup guide for facilitators
├── .github/
│   └── copilot-instructions.md  ← AI behavior instructions (Copilot skill)
├── .vscode/
│   ├── settings.json      ← Editor config + Copilot settings
│   └── tasks.json         ← Build/flash/check tasks
├── apps/
│   └── maze_runner/
│       └── main.py        ← THE robot program (AI edits this file)
├── docs/
│   ├── CHALLENGE.md       ← Challenge description for participants
│   └── edison-api-reference.md  ← Edison V3 API reference
├── lore/                  ← LORE toolchain (auto-installed on first run)
└── scripts/
    ├── run.py             ← Build & deploy wrapper script
    └── setup.sh           ← First-time setup script
```

## How It Works

### The Toolchain: LORE
We use [LORE](https://github.com/dgpc/LORE) (Low Overhead Robotics Explorer) to compile
and flash programs to the Edison V3 via USB. LORE is auto-installed on first use by `scripts/run.py`.

- `python scripts/run.py build` — Compiles `apps/maze_runner/main.py` to Edison bytecode
- `python scripts/run.py flash` — Sends the compiled program to the robot via USB
- `python scripts/run.py build-and-flash` — Both steps in one command
- `python scripts/run.py check` — Checks if the robot is connected

### The AI Workflow
1. Participant describes what they want in chat
2. AI writes/edits `apps/maze_runner/main.py`
3. AI runs the build-and-flash VS Code task
4. Participant tests on the real maze
5. Participant describes what to change → repeat

### Edison V3 Programming Rules
- All robot commands use the `Ed.` prefix (built-in, no imports needed)
- **No imports, classes, try/except, or decorators** — EdPy is a Python subset
- Functions (`def`), loops (`while`, `for`), and conditionals (`if/elif/else`) all work
- Must set `Ed.EdisonVersion = Ed.V3` at the top of every program
- Sensors must be explicitly enabled before reading (e.g., `Ed.ObstacleDetectionBeam(Ed.ON)`)

### USB Connection
- Edison V3 uses USB-A (use a USB-C adapter if needed)
- USB Vendor ID: `0x16D0`, Product ID: `0x1207`
- Requires `pyusb` library and appropriate USB permissions
- On Linux, may need a udev rule for non-root access

## Key Files to Edit

**`apps/maze_runner/main.py`** — This is THE file. The AI should edit this file in response
to participant requests. Always keep the setup block at the top:

```python
import Ed

Ed.EdisonVersion = Ed.V3
Ed.DistanceUnits = Ed.CM
Ed.Tempo = Ed.TEMPO_MEDIUM
```

## Common Patterns

### Wall-following maze solver
```python
import Ed

Ed.EdisonVersion = Ed.V3
Ed.DistanceUnits = Ed.CM
Ed.ObstacleDetectionBeam(Ed.ON)

while True:
    Ed.Drive(Ed.FORWARD, Ed.SPEED_5, Ed.DISTANCE_UNLIMITED)
    obstacle = Ed.ReadObstacleDetection()
    if obstacle != Ed.OBSTACLE_NONE:
        Ed.Drive(Ed.STOP, Ed.SPEED_1, 0)
        Ed.Drive(Ed.BACKWARD, Ed.SPEED_3, 2)
        Ed.Drive(Ed.SPIN_RIGHT, Ed.SPEED_3, 90)
    if Ed.ReadKeypad() == Ed.KEYPAD_ROUND:
        Ed.Drive(Ed.STOP, Ed.SPEED_1, 0)
        break
```

### Line-following
```python
import Ed

Ed.EdisonVersion = Ed.V3
Ed.LineTrackerLed(Ed.ON)

while True:
    line = Ed.ReadLineState()
    if line == Ed.LINE_ON_BLACK:
        Ed.Drive(Ed.FORWARD, Ed.SPEED_3, 1)
    elif line == Ed.LINE_LEFT_ON_BLACK:
        Ed.Drive(Ed.SPIN_LEFT, Ed.SPEED_2, 10)
    elif line == Ed.LINE_RIGHT_ON_BLACK:
        Ed.Drive(Ed.SPIN_RIGHT, Ed.SPEED_2, 10)
    else:
        Ed.Drive(Ed.SPIN_RIGHT, Ed.SPEED_2, 15)
```

## Troubleshooting

### Build failures
- Check for unsupported Python features (imports, classes, try/except)
- Check for typos in `Ed.` commands (see docs/edison-api-reference.md)
- Try remote compile: `python scripts/run.py build --remote`

### Robot not found
- Check USB cable connection
- Check robot is turned on
- On Linux: may need `sudo` or udev rule for USB access
- On macOS: should work out of the box with pyusb + libusb

### Robot does nothing after flash
- Press the ▶ (triangle/play) button on the robot
- Check the program has a `while True` loop
- Check sensors are enabled before reading them

### Obstacle detection unreliable
- Avoid direct sunlight (confuses IR sensor)
- Walls must be opaque and at least as tall as the robot
- Obstacles must not be too dark (very dark surfaces absorb IR)

## The "start" Command

When a user types **"start"** in the chat, this kicks off the full guided experience:
1. Welcome message explaining the challenge
2. Automatic robot connection check (`python scripts/run.py check`)
3. Guided brainstorm conversation
4. Plan presentation and approval
5. Code generation, build, and flash
6. Test and iterate loop

The AI should handle everything — the user never needs to touch code, run commands,
or understand what's happening behind the scenes.

## Workshop Setup Checklist

1. Clone this repo to each participant's machine
2. Run `bash scripts/setup.sh` to install dependencies
3. Open the folder in VS Code
4. Connect Edison V3 via USB
5. Test with `python scripts/run.py check`
6. Tell participants: "Type **start** in the Copilot Chat to begin!"
