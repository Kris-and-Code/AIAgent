notes = []

def handle_weather():
    return "Sure! Tell me the city you want weather for."

def handle_add_note(user_input: str):
    note = user_input.replace("add note", "").strip()
    notes.append(note)
    return f"Got it, I saved your note: '{note}'"

def handle_show_notes():
    return f"Your notes: {notes}" if notes else "No notes yet."
