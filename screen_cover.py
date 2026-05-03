"""Slay the Spire 2 — screen cover prank.

Serpentines the cursor across the whole screen so the in-game draw mechanic
paints over everything but your character.

Two modes — try F8 first; if the game ignores synthetic right-click, use F9.

Hotkeys:
    F8   FULL AUTO   — script holds right-click and sweeps
    F9   ASSIST MODE — you physically hold right-click, script only moves
    F8/F9 again while running   abort
    ESC  quit
"""

import ctypes
import threading
import time

import keyboard
import pydirectinput

pydirectinput.PAUSE = 0
pydirectinput.FAILSAFE = False

# Tune if coverage is patchy or sweep is too slow:
LINE_SPACING = 8        # px between horizontal sweeps (smaller = denser)
STEP_PX = 4             # px per relative-motion tick during a sweep
TICK_SLEEP = 0.001      # seconds between ticks (lets game's input poll catch up)
START_DELAY = 0.4       # seconds before the sweep starts after hotkey

_running = False
_abort = False


def _screen_size():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


def _do_sweep(hold_rmb: bool):
    global _running, _abort
    try:
        time.sleep(START_DELAY)
        width, height = _screen_size()

        # snap to bottom-right — top-left is a dead zone for StS2's draw mechanic
        pydirectinput.moveTo(width - 1, height - 1)
        time.sleep(0.02)

        if hold_rmb:
            pydirectinput.mouseDown(button="right")

        x = width - 1
        y = height - 1
        direction = -1  # start sweeping leftward
        while y > 0 and not _abort:
            target_x = 0 if direction < 0 else width - 1
            step_dir = -1 if direction < 0 else 1
            remaining = abs(target_x - x)
            while remaining > 0 and not _abort:
                step = min(STEP_PX, remaining)
                pydirectinput.moveRel(step * step_dir, 0, relative=True)
                remaining -= step
                time.sleep(TICK_SLEEP)
            x = target_x

            if y - LINE_SPACING > 0:
                pydirectinput.moveRel(0, -LINE_SPACING, relative=True)
            y -= LINE_SPACING
            direction *= -1
    finally:
        if hold_rmb:
            pydirectinput.mouseUp(button="right")
        _running = False
        _abort = False


def _trigger(hold_rmb: bool):
    global _running, _abort
    if _running:
        _abort = True
        return
    _running = True
    threading.Thread(target=_do_sweep, args=(hold_rmb,), daemon=True).start()


def main():
    bar = "=" * 60
    print(bar)
    print(" Slay the Spire 2 — Screen Cover Prank")
    print(bar)
    print()
    print("  F8   FULL AUTO   — script holds right-click and sweeps")
    print("  F9   ASSIST MODE — YOU hold right-click, script just moves")
    print("       (try F9 if F8 doesn't draw — many games filter")
    print("        synthetic right-click but accept synthetic motion)")
    print()
    print("  Press F8/F9 again while running to abort.")
    print("  ESC quits.")
    print()
    print("Tab into the game, then press your hotkey. Have fun.")
    print()

    keyboard.add_hotkey("f8", lambda: _trigger(hold_rmb=True))
    keyboard.add_hotkey("f9", lambda: _trigger(hold_rmb=False))
    keyboard.wait("esc")


if __name__ == "__main__":
    main()
