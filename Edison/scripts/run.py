#!/usr/bin/env python3
"""
Edison V3 Build & Deploy Script
================================
Wraps LORE to build and flash Edison V3 programs.
Provides friendly error messages for non-programmers.

Usage:
    python scripts/run.py build          - Compile the maze_runner program
    python scripts/run.py flash          - Send program to the robot
    python scripts/run.py build-and-flash - Compile and send in one step
    python scripts/run.py check          - Check if robot is connected
"""

import subprocess
import sys
import os
import time
import shutil

# --- Configuration ---
APP_NAME = "maze_runner"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LORE_DIR = os.path.join(PROJECT_ROOT, "lore")
LORE_BIN = os.path.join(LORE_DIR, "lore")
APP_SOURCE = os.path.join(PROJECT_ROOT, "apps", APP_NAME, "main.py")


def print_status(emoji, message):
    """Print a friendly status message."""
    print(f"\n  {emoji}  {message}\n")


def print_step(step, message):
    """Print a numbered step."""
    print(f"  [{step}] {message}")


def check_lore_installed():
    """Check if LORE is available, offer to install if not."""
    if os.path.exists(LORE_BIN):
        return True

    print_status("📦", "Setting up the Edison V3 toolchain (first time only)...")
    print("  This downloads the tools needed to send programs to your robot.")
    print("  It may take a minute or two.\n")

    try:
        # Clone LORE
        print_step(1, "Downloading Edison V3 tools...")
        subprocess.run(
            ["git", "clone", "https://github.com/dgpc/LORE.git", LORE_DIR],
            check=True,
            capture_output=True,
            text=True,
        )

        # Set up virtual environment inside LORE
        print_step(2, "Setting up Python environment...")
        subprocess.run(
            [sys.executable, "-m", "venv", os.path.join(LORE_DIR, ".venv")],
            check=True,
            capture_output=True,
            text=True,
        )

        venv_pip = os.path.join(LORE_DIR, ".venv", "bin", "pip")
        subprocess.run(
            [venv_pip, "install", "pyusb", "requests", "lark"],
            check=True,
            capture_output=True,
            text=True,
        )

        # Build mpy-cross
        print_step(3, "Building compiler (this takes a moment)...")
        result = subprocess.run(
            ["make"],
            cwd=LORE_DIR,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print_status("⚠️", "Compiler build had issues. Trying remote compile mode instead.")
            # Remote compile will still work

        # Symlink apps directory into LORE
        lore_apps = os.path.join(LORE_DIR, "apps")
        project_apps = os.path.join(PROJECT_ROOT, "apps")
        if os.path.exists(lore_apps) and not os.path.islink(lore_apps):
            # Move any existing example apps
            for item in os.listdir(lore_apps):
                src = os.path.join(lore_apps, item)
                dst = os.path.join(project_apps, item)
                if not os.path.exists(dst):
                    shutil.move(src, dst)
            shutil.rmtree(lore_apps)
        if not os.path.exists(lore_apps):
            os.symlink(project_apps, lore_apps)

        print_step(4, "Done!")
        print_status("✅", "Edison V3 tools are ready!")
        return True

    except subprocess.CalledProcessError as e:
        print_status("❌", "Something went wrong during setup.")
        print(f"  Error: {e.stderr if e.stderr else str(e)}")
        print("\n  Please ask your workshop facilitator for help.")
        return False
    except Exception as e:
        print_status("❌", f"Setup failed: {e}")
        print("\n  Please ask your workshop facilitator for help.")
        return False


def sync_app():
    """Make sure the app source is available in LORE's apps directory."""
    lore_app_dir = os.path.join(LORE_DIR, "apps", APP_NAME)
    if not os.path.exists(lore_app_dir):
        # The symlink should handle this, but just in case
        os.makedirs(lore_app_dir, exist_ok=True)
        shutil.copy2(APP_SOURCE, os.path.join(lore_app_dir, "main.py"))


def run_lore(command, app_name=APP_NAME, extra_args=None):
    """Run a LORE command with friendly error handling."""
    venv_python = os.path.join(LORE_DIR, ".venv", "bin", "python")
    cmd = [venv_python, LORE_BIN, command, app_name]
    if extra_args:
        cmd.extend(extra_args)

    try:
        result = subprocess.run(
            cmd,
            cwd=LORE_DIR,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result
    except subprocess.TimeoutExpired:
        print_status("⏰", "The command took too long. The robot might not be responding.")
        print("  Try unplugging and replugging the USB cable.")
        return None
    except FileNotFoundError:
        print_status("❌", "Can't find the Edison tools. Try running setup again.")
        return None


def do_build():
    """Compile the maze runner program."""
    print_status("🔨", "Compiling your robot program...")

    # Use remote compile by default (faster and doesn't need mpy-cross)
    result = run_lore("build", extra_args=["--remote-compile"])

    if result and result.returncode == 0:
        print_status("✅", "Program compiled successfully (using online compiler)!")
        return True

    # Parse common errors
    error_output = (result.stderr if result else "") + (result.stdout if result else "")

    if "SyntaxError" in error_output:
        print_status("❌", "There's a problem with the program code.")
        print("  Don't worry — tell the AI what went wrong and it will fix it.")
    elif "unsupported" in error_output.lower():
        print_status("❌", "The program uses a feature the robot doesn't support.")
        print("  The AI will need to rewrite that part differently.")
    else:
        print_status("❌", "Something went wrong during compilation.")
        print(f"  Details: {error_output[:200]}")

    return False


def do_flash():
    """Send the compiled program to the robot."""
    print_status("📡", "Sending program to your robot...")

    result = run_lore("flash")

    if result is None:
        return False

    if result.returncode == 0:
        print_status("✅", "Program sent to the robot!")
        print("  Press the ▶ (triangle/play) button on your robot to start it.")
        return True

    error_output = (result.stderr if result else "") + (result.stdout if result else "")

    if "usb" in error_output.lower() or "device" in error_output.lower() or "no backend" in error_output.lower():
        print_status("🔌", "Can't find your robot!")
        print("  Please check:")
        print("    1. Is the USB cable plugged into the robot and your computer?")
        print("    2. Is the robot turned on?")
        print("    3. Try unplugging the cable and plugging it back in")
        print()

        input("  Press Enter when you're ready to try again...")
        print()

        # Retry once
        print_status("📡", "Trying again...")
        result = run_lore("flash")
        if result and result.returncode == 0:
            print_status("✅", "Program sent to the robot!")
            print("  Press the ▶ (triangle/play) button on your robot to start it.")
            return True
        else:
            print_status("❌", "Still can't connect. Ask your workshop facilitator for help.")
            return False

    elif "permission" in error_output.lower():
        print_status("🔒", "Your computer won't let me talk to the robot.")
        print("  This is a permissions issue — ask your workshop facilitator for help.")
        print("  (They may need to add a udev rule or run with elevated permissions.)")
        return False

    else:
        print_status("❌", "Something went wrong sending the program.")
        print(f"  Details: {error_output[:200]}")
        return False


def do_check():
    """Check if the robot is connected."""
    print_status("🔍", "Looking for your Edison V3 robot...")

    try:
        # Try to find the USB device
        result = subprocess.run(
            ["lsusb"],
            capture_output=True,
            text=True,
        )
        if "16d0:1207" in result.stdout.lower() or "mcs" in result.stdout.lower():
            print_status("✅", "Robot found! It's connected and ready.")
            return True
        else:
            print_status("🔌", "Can't find the robot.")
            print("  Make sure:")
            print("    1. The USB cable is plugged in at both ends")
            print("    2. The robot is turned on")
            print("    3. You're using a USB data cable (not just a charging cable)")
            return False
    except FileNotFoundError:
        # lsusb not available, try the flash command as a probe
        print("  (Can't check directly — try 'Build & Run' to test the connection)")
        return False


def main():
    if len(sys.argv) < 2:
        print("Edison V3 Maze Challenge — Robot Control")
        print("=========================================")
        print()
        print("Commands:")
        print("  python scripts/run.py build          - Compile your program")
        print("  python scripts/run.py flash          - Send program to robot")
        print("  python scripts/run.py build-and-flash - Compile and send (recommended)")
        print("  python scripts/run.py check          - Check robot connection")
        sys.exit(0)

    command = sys.argv[1].lower()

    # Make sure LORE is set up
    if not check_lore_installed():
        sys.exit(1)

    if command == "build":
        success = do_build()
        sys.exit(0 if success else 1)

    elif command == "flash":
        success = do_flash()
        sys.exit(0 if success else 1)

    elif command == "build-and-flash":
        if do_build():
            do_flash()
        else:
            print_status("⏸️", "Fix the build errors first, then try again.")
            sys.exit(1)

    elif command == "check":
        do_check()

    else:
        print(f"Unknown command: {command}")
        print("Use: build, flash, build-and-flash, or check")
        sys.exit(1)


if __name__ == "__main__":
    main()
