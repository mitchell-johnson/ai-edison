# The Maze Challenge

## Your Mission

Get your Edison V3 robot from the start of the maze to the finish — using only your words.

You won't write any code yourself. Instead, you'll talk to an AI assistant (GitHub Copilot)
and describe what you want the robot to do. The AI writes the code, sends it to the robot,
and you test it on the real maze.

## How It Works

1. **Open the chat** — In VS Code, open the Copilot Chat panel (click the chat icon on the left sidebar)
2. **Describe your idea** — Tell the AI what you want the robot to do, like:
   - "Make the robot drive forward until it sees a wall, then turn right"
   - "I want it to follow the left wall through the maze"
   - "Can it beep every time it turns?"
3. **Review the plan** — The AI will describe what the robot will do in plain English. Say if you want changes.
4. **Send it to the robot** — The AI will compile the code and send it to your robot.
5. **Test it!** — Put your robot at the start of the maze and press the play button (▶).
6. **Iterate** — Tell the AI what happened and what to change. Keep improving!

## Tips for Talking to the AI

You don't need to know anything about programming. Just describe what you want
like you're giving directions to a person.

**Good prompts:**
- "Make the robot go forward slowly and stop when it sees something in front of it"
- "When the robot reaches a wall, I want it to back up a little, then turn left"
- "Can you make the lights flash when it's turning?"
- "It's turning too far — can you make it turn less?"
- "The robot keeps hitting the right wall. Can it check for walls on the right too?"

**Getting unstuck:**
- "What can the robot sense?" — The AI will tell you what sensors are available
- "What strategies could work for solving a maze?" — Ask for ideas!
- "It's not working, here's what happened..." — Describe what the robot did and the AI will help fix it

## The Maze

The maze is built with walls that the robot can detect using its infrared sensor.
The robot can only see obstacles directly ahead, to the left, or to the right.

**Key constraints:**
- The passages are wide enough for the robot to drive through
- Walls are opaque and tall enough for the sensor to detect
- Avoid direct sunlight on the maze (it confuses the infrared sensor)

## Scoring (optional)

If you're competing, here's how you'll be scored:

| Category | Points | Description |
|----------|--------|-------------|
| **Completion** | 50 | Robot reaches the end of the maze |
| **Speed** | 20 | Faster completion = more points |
| **Style** | 15 | Bonus features: sounds, lights, smooth turns |
| **Creativity** | 15 | Unique approach to solving the maze |

## Strategies to Try

Here are some classic maze-solving approaches you can describe to the AI:

**Wall Follower** — "Always keep the right wall next to you." The robot hugs one wall and
eventually finds the exit. Simple and reliable for most mazes.

**Scan and Turn** — "Drive forward, and when you hit a wall, look left and right to see
which way is open." Good for mazes with lots of dead ends.

**Cautious Explorer** — "Go slowly, check for walls often, and back up if you get stuck."
Safer but slower.

## Need Help?

- **Robot won't move?** Make sure the USB cable is plugged in and the robot is turned on.
  Press the triangle (play) button after the program is sent.
- **Robot runs into walls?** Tell the AI: "The robot is hitting walls, can you make it
  check for obstacles more often?"
- **Robot goes in circles?** Tell the AI: "It's going in circles, can we try a different strategy?"
- **Totally stuck?** Ask your facilitator — they're here to help!
