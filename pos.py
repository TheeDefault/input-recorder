from collections import deque
import threading
import time

from pynput import keyboard, mouse
import pyautogui

from display import run_display

click_positions = []
recent_events = deque(maxlen=5)
recent_events_lock = threading.Lock()
recording_state_lock = threading.Lock()
event_number = 0
last_event_monotonic = None
recording_started = False


def record_event(action, x=None, y=None):
    global event_number, last_event_monotonic

    event_number += 1
    monotonic_now = time.perf_counter()
    elapsed = (
        "N/A"
        if last_event_monotonic is None
        else f"{monotonic_now - last_event_monotonic:.3f} s"
    )
    x_coord = "Null" if x is None else x
    y_coord = "Null" if y is None else y
    event_row = (
        f"{event_number:>4} | {action:<12} | {x_coord:>6} | {y_coord:>6} | {elapsed}"
    )
    with recent_events_lock:
        recent_events.append(event_row)
    print(event_row)
    last_event_monotonic = monotonic_now


def on_click(x, y, button, pressed):
    with recording_state_lock:
        is_recording = recording_started
    if pressed and is_recording:
        record_event("click", x, y)
        click_positions.append((x, y))


def start_recording():
    global recording_started

    with recording_state_lock:
        if recording_started:
            return
        recording_started = True
    print("\nRecording started.")


hotkey = keyboard.HotKey(keyboard.HotKey.parse("<ctrl>+r"), start_recording)


def on_press(key):
    with recording_state_lock:
        was_recording = recording_started
    hotkey.press(keyboard_listener.canonical(key))
    if not was_recording:
        return

    key_name = getattr(key, "char", None) or str(key)
    record_event(key_name)


def on_release(key):
    hotkey.release(keyboard_listener.canonical(key))


def get_recent_events():
    with recent_events_lock:
        return list(recent_events)


def get_mouse_position():
    return pyautogui.position()


def get_recording_status():
    with recording_state_lock:
        return "Recording" if recording_started else "Not recording"


listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)


def main():
    print("S no | Action / key | X coord | Y coord | Time since last event")
    listener.start()
    keyboard_listener.start()
    print("Press Ctrl+R to start recording. Press Ctrl+C to stop.")

    try:
        run_display(get_recent_events, get_mouse_position, get_recording_status)
    except KeyboardInterrupt:
        pass
    finally:
        listener.stop()
        keyboard_listener.stop()
        print("\nStopped.")
        print("Recorded click positions:", click_positions)


if __name__ == "__main__":
    main()
