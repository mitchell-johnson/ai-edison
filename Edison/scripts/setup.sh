#!/usr/bin/env bash
# ============================================================
# Edison V3 Maze Challenge — Setup Script
# ============================================================
# Run this once on each participant's computer before the workshop.
# It installs all the tools needed to compile and send programs
# to the Edison V3 robot.
#
# Usage:  bash scripts/setup.sh
# ============================================================

set -e

echo ""
echo "  🤖  Edison V3 Maze Challenge — Setup"
echo "  ====================================="
echo ""

# Check we're in the right directory
if [ ! -f "CLAUDE.md" ]; then
    echo "  ❌  Please run this script from the project root directory."
    echo "      cd ai-edison && bash scripts/setup.sh"
    exit 1
fi

# --- Step 1: Check Python ---
echo "  [1/5] Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON=python3
    echo "        ✅ Found $(python3 --version)"
elif command -v python &> /dev/null; then
    PYTHON=python
    echo "        ✅ Found $(python --version)"
else
    echo "        ❌ Python not found!"
    echo "           Please install Python 3.8+ from https://python.org"
    exit 1
fi

# --- Step 2: Check Git ---
echo "  [2/5] Checking Git..."
if command -v git &> /dev/null; then
    echo "        ✅ Found $(git --version)"
else
    echo "        ❌ Git not found!"
    echo "           Please install Git from https://git-scm.com"
    exit 1
fi

# --- Step 3: Check C Compiler ---
echo "  [3/5] Checking C compiler..."
if command -v gcc &> /dev/null; then
    echo "        ✅ Found $(gcc --version | head -1)"
elif command -v cc &> /dev/null; then
    echo "        ✅ Found a C compiler"
elif command -v clang &> /dev/null; then
    echo "        ✅ Found $(clang --version | head -1)"
else
    echo "        ⚠️  No C compiler found."
    echo "           The remote compiler will be used as a fallback."
    echo "           To install locally: sudo apt install build-essential (Linux)"
    echo "                              xcode-select --install (macOS)"
fi

# --- Step 4: Install LORE ---
echo "  [4/5] Installing Edison V3 toolchain (LORE)..."
if [ -d "lore" ]; then
    echo "        Already installed, updating..."
    cd lore && git pull 2>/dev/null || true && cd ..
else
    git clone https://github.com/dgpc/LORE.git lore
fi

# Create venv and install dependencies
if [ ! -d "lore/.venv" ]; then
    $PYTHON -m venv lore/.venv
fi
lore/.venv/bin/pip install -q pyusb requests lark

# Build mpy-cross
echo "        Building MicroPython compiler..."
if command -v make &> /dev/null; then
    cd lore && make 2>/dev/null && cd .. && echo "        ✅ Local compiler ready" || {
        cd ..
        echo "        ⚠️  Local compiler build failed — will use remote compiler"
    }
else
    echo "        ⚠️  make not found — will use remote compiler"
fi

# Link apps directory
if [ -d "lore/apps" ] && [ ! -L "lore/apps" ]; then
    # Move example apps to our apps directory
    for dir in lore/apps/*/; do
        name=$(basename "$dir")
        if [ ! -d "apps/$name" ]; then
            cp -r "$dir" "apps/$name"
        fi
    done
    rm -rf lore/apps
fi
if [ ! -e "lore/apps" ]; then
    ln -s "$(pwd)/apps" lore/apps
fi

# --- Step 5: USB Permissions (Linux only) ---
echo "  [5/5] Checking USB permissions..."
if [[ "$OSTYPE" == "linux"* ]]; then
    UDEV_RULE='SUBSYSTEM=="usb", ATTR{idVendor}=="16d0", ATTR{idProduct}=="1207", MODE="0666", GROUP="plugdev"'
    UDEV_FILE="/etc/udev/rules.d/99-edison.rules"

    if [ -f "$UDEV_FILE" ]; then
        echo "        ✅ USB permissions already configured"
    else
        echo "        Setting up USB permissions for Edison V3..."
        echo "        (This requires sudo — enter your password if prompted)"
        echo "$UDEV_RULE" | sudo tee "$UDEV_FILE" > /dev/null 2>&1 && {
            sudo udevadm control --reload-rules 2>/dev/null
            sudo udevadm trigger 2>/dev/null
            echo "        ✅ USB permissions configured"
        } || {
            echo "        ⚠️  Could not set USB permissions automatically."
            echo "           You may need to run flash commands with sudo."
            echo "           Or ask your facilitator to add this udev rule:"
            echo "           $UDEV_RULE"
        }
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "        ✅ macOS — USB permissions should work automatically"
else
    echo "        ⚠️  Unknown OS — USB permissions may need manual setup"
fi

echo ""
echo "  ============================================"
echo "  ✅  Setup complete!"
echo "  ============================================"
echo ""
echo "  Next steps:"
echo "    1. Open this folder in VS Code"
echo "    2. Connect your Edison V3 robot via USB"
echo "    3. Test: python scripts/run.py check"
echo "    4. Open Copilot Chat and start describing what you want!"
echo ""
echo "  📖  Read docs/CHALLENGE.md for the maze challenge rules"
echo ""
