#!/usr/bin/env python3
"""Full-screen animation that repaints as fast as X allows (no vsync).

Covers one monitor, changes every pixel on each frame and shows its own
paint rate, so it can be compared with the rate triggerdm reports.
The window asks the compositor to bypass it (_NET_WM_BYPASS_COMPOSITOR),
otherwise mutter would cap updates at its own 60 Hz frame clock.

Usage: fpstest.py [OUTPUT] [--seconds N] [--geometry WxH+X+Y]
Esc or q quits.
"""
import argparse
import colorsys
import re
import subprocess
import sys
import time
import tkinter as tk


def output_geometry(name):
    out = subprocess.run(["xrandr"], capture_output=True, text=True).stdout
    m = re.search(rf"^{re.escape(name)} connected (?:primary )?(\d+)x(\d+)\+(\d+)\+(\d+)", out, re.M)
    if not m:
        sys.exit(f"output {name} not found or not active")
    return tuple(map(int, m.groups()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("output", nargs="?", default="DVI-I-1-1")
    ap.add_argument("--seconds", type=float, default=0, help="quit after N seconds (0 = never)")
    ap.add_argument("--geometry", help="WxH+X+Y instead of covering OUTPUT (windowed)")
    args = ap.parse_args()

    if args.geometry:
        w, h, x, y = map(int, re.match(r"(\d+)x(\d+)\+(\d+)\+(\d+)$", args.geometry).groups())
        fullscreen = False
    else:
        w, h, x, y = output_geometry(args.output)
        fullscreen = True

    root = tk.Tk()
    root.withdraw()
    root.geometry(f"{w}x{h}+{x}+{y}")
    root.update_idletasks()
    frame_id = int(root.wm_frame(), 16)
    subprocess.run(["xprop", "-id", str(frame_id), "-f", "_NET_WM_BYPASS_COMPOSITOR", "32c",
                    "-set", "_NET_WM_BYPASS_COMPOSITOR", "1"], check=False)
    root.deiconify()
    if fullscreen:
        root.attributes("-fullscreen", True)

    canvas = tk.Canvas(root, width=w, height=h, highlightthickness=0, bg="black")
    canvas.pack(fill="both", expand=True)
    bg = canvas.create_rectangle(0, 0, w, h, width=0)
    bar = canvas.create_rectangle(0, 0, w // 20, h, width=0, fill="white")
    label = canvas.create_text(w // 2, h // 2, fill="white", font=("Sans", max(12, h // 12), "bold"))

    for key in ("<Escape>", "q"):
        root.bind(key, lambda e: root.destroy())

    state = {"frame": 0, "t0": time.monotonic(), "count": 0, "rate": 0.0, "start": time.monotonic()}

    def tick():
        now = time.monotonic()
        if args.seconds and now - state["start"] >= args.seconds:
            print(f"last measured paint rate: {state['rate']:.1f} fps")
            root.destroy()
            return
        f = state["frame"]
        r, g, b = colorsys.hsv_to_rgb((f % 360) / 360, 0.8, 0.6)
        canvas.itemconfigure(bg, fill=f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}")
        bx = (f * 13) % w
        canvas.coords(bar, bx, 0, bx + w // 20, h)
        canvas.itemconfigure(label, text=f"{state['rate']:.0f} fps\nframe {f}")
        root.update_idletasks()
        state["frame"] += 1
        state["count"] += 1
        if now - state["t0"] >= 1.0:
            state["rate"] = state["count"] / (now - state["t0"])
            print(f"paint rate: {state['rate']:.1f} fps", flush=True)
            state["t0"], state["count"] = now, 0
        root.after(1, tick)

    root.after(100, tick)
    root.mainloop()


if __name__ == "__main__":
    main()
