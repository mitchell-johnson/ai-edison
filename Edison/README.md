# AI Edison — Maze Challenge

Use AI to control an Edison V3 robot through a maze, **without writing any code**.

Participants describe what they want in plain English. The AI writes the code, sends it to the robot, and participants test it on a real maze. No programming experience needed.

## Quick Start (Participants)

1. Open this folder in VS Code
2. Plug in your Edison V3 robot via USB
3. Open Copilot Chat (click the chat icon in the sidebar)
4. Type **`start`** and the AI will walk you through everything!

Read [`docs/CHALLENGE.md`](docs/CHALLENGE.md) for the full challenge rules and tips.

## Workshop Setup (Facilitators)

### Prerequisites per machine

- **VS Code** with GitHub Copilot extension (needs Copilot subscription)
- **Python 3.8+**
- **Git**
- **USB-A port** (or USB-C adapter) for the Edison V3 cable
- **C compiler** (optional — falls back to remote compiler without it)
  - macOS: `xcode-select --install`
  - Linux: `sudo apt install build-essential`
  - Windows: Visual Studio Build Tools

### Setup steps

```bash
# 1. Clone the project
git clone https://github.com/mitchell-johnson/ai-edison.git
cd ai-edison

# 2. Run the setup script (installs the Edison toolchain)
bash scripts/setup.sh

# 3. Connect a robot and test
python scripts/run.py check
```

### Maze construction

- Use cardboard, foam board, or wood to build walls
- Walls should be **opaque** and **at least as tall as the Edison robot** (~5cm)
- Passages should be **at least 15cm wide** (the robot is about 9cm wide)
- **Avoid direct sunlight** on the maze — it confuses the infrared obstacle sensor
- Mark a clear start and finish position

### On the day

1. Each participant gets a laptop + Edison V3 robot + USB cable
2. Open VS Code in the ai-edison folder
3. Make sure the robot is connected (green light when plugged in)
4. Point them to the Copilot Chat panel
5. Tell them: *"Type 'start' in the chat and the AI will guide you from there"*

## How It Works

```
Participant ──(plain English)──▶ AI (Copilot) ──(Python code)──▶ Edison V3
     ▲                                                              │
     └──────────── (observes robot, describes changes) ◀────────────┘
```

The project uses [LORE](https://github.com/dgpc/LORE) to compile EdPy (MicroPython) programs and flash them to the Edison V3 over USB. The AI is guided by instructions in `.github/copilot-instructions.md` that tell it to:

- Use simple, non-technical language
- Never ask participants to write code
- Automatically handle errors and debugging
- Walk through a brainstorm → plan → build → test → iterate cycle

## Project Structure

| Path | Purpose |
|------|---------|
| `apps/maze_runner/main.py` | The robot program (AI edits this) |
| `.github/copilot-instructions.md` | AI behavior instructions |
| `scripts/run.py` | Build & deploy wrapper |
| `scripts/setup.sh` | First-time setup |
| `docs/CHALLENGE.md` | Challenge rules for participants |
| `docs/edison-api-reference.md` | Edison V3 API reference |
| `CLAUDE.md` | Project context for AI assistants |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Robot not detected | Check USB cable, ensure robot is on, try different port |
| Build fails | The AI should auto-fix — if not, check `apps/maze_runner/main.py` for unsupported Python features |
| Robot does nothing | Press the ▶ (triangle) button on the robot |
| Obstacle detection unreliable | Move away from sunlight, check walls are opaque and tall enough |
| USB permission denied (Linux) | Run `bash scripts/setup.sh` again or use `sudo` |

## License

MIT
