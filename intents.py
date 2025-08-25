def detect_intent(user_input: str) -> str:
    text = user_input.lower()

    if "weather" in text or "temperature" in text or "forecast" in text:
        return "weather"
    elif "add note" in text or "note" in text:
        return "add_note"
    elif "show notes" in text or "list notes" in text:
        return "show_notes"
    else:
        return "unknown"
