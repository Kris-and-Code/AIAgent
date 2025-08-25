from intents import detect_intent
import actions

def task_agent(user_input: str) -> str:
    intent = detect_intent(user_input)

    if intent == "weather":
        return actions.handle_weather()
    elif intent == "add_note":
        return actions.handle_add_note(user_input)
    elif intent == "show_notes":
        return actions.handle_show_notes()
    else:
        return "Sorry, I didn't understand that."

if __name__ == "__main__":
    print("Task Agent ready! Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = task_agent(user_input)
        print("Agent:", response)
