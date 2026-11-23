import tkinter as tk


def run_display(get_recent_events, get_mouse_position, get_recording_status):
    root = tk.Tk()
    root.title("Recent inputs")
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.8)
    root.protocol("WM_DELETE_WINDOW", root.quit)

    recording_status_label = tk.Label(
        root,
        text="Not recording",
        font=("Consolas", 10, "bold"),
        anchor="w",
    )
    recording_status_label.pack(fill="x", padx=10, pady=(10, 2))

    mouse_position_label = tk.Label(root, font=("Consolas", 10), anchor="w")
    mouse_position_label.pack(fill="x", padx=10, pady=(2, 4))

    events_display = tk.Text(
        root, height=6, width=74, state="disabled", font=("Consolas", 10)
    )
    events_display.pack(fill="both", expand=True, padx=10, pady=(4, 10))

    def refresh_display():
        recording_status = get_recording_status()
        status_color = "red" if recording_status == "Recording" else "gray"
        recording_status_label.config(
            text=f"Recording status: {recording_status}",
            foreground=status_color,
        )

        x, y = get_mouse_position()
        mouse_position_label.config(text=f"Mouse position: ({x}, {y})")

        events = get_recent_events()
        events_display.config(state="normal")
        events_display.delete("1.0", tk.END)
        events_display.insert(
            tk.END, "\n".join(events) if events else "Waiting for input..."
        )
        events_display.config(state="disabled")
        root.after(100, refresh_display)

    try:
        refresh_display()
        root.mainloop()
    finally:
        root.destroy()
