from intents import detect_intent, intent_detector
import actions
import logging
from typing import Tuple

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TaskAgent:
    """Enhanced AI Task Agent with multiple capabilities"""
    
    def __init__(self):
        self.conversation_history = []
        self.context = {}
    
    def process_input(self, user_input: str) -> str:
        """Process user input and return appropriate response"""
        try:
            # Detect intent with confidence
            intent, confidence = intent_detector.detect_intent(user_input)
            
            # Log the interaction
            logger.info(f"Intent: {intent}, Confidence: {confidence:.2f}, Input: {user_input}")
            
            # Store in conversation history
            self.conversation_history.append({
                "user": user_input,
                "intent": intent,
                "confidence": confidence
            })
            
            # Route to appropriate handler
            response = self._route_intent(intent, user_input, confidence)
            
            # Add response to history
            self.conversation_history[-1]["response"] = response
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing input: {e}")
            return "Sorry, I encountered an error processing your request. Please try again."
    
    def _route_intent(self, intent: str, user_input: str, confidence: float) -> str:
        """Route intent to appropriate handler"""
        
        # Check confidence threshold
        if confidence < 0.3 and intent != "unknown":
            return f"I'm not very confident about understanding '{user_input}'. Could you rephrase that?"
        
        # Route to handlers
        if intent == "weather":
            return actions.handle_weather(user_input)
        elif intent == "add_note":
            return actions.handle_add_note(user_input)
        elif intent == "show_notes":
            return actions.handle_show_notes()
        elif intent == "calculator":
            return actions.handle_calculator(user_input)
        elif intent == "reminder":
            return actions.handle_reminder(user_input)
        elif intent == "web_search":
            return actions.handle_web_search(user_input)
        elif intent == "file_operation":
            return actions.handle_file_operation(user_input)
        else:
            return actions.handle_unknown(user_input)
    
    def get_help(self) -> str:
        """Get help information about available commands"""
        help_text = """
🤖 AI Task Agent - Available Commands:

🌤️  Weather:
   - "What's the weather in London?"
   - "Weather forecast for New York"
   - "How's the weather today?"

📝 Notes:
   - "Add note: Buy groceries"
   - "Remember: Call mom tomorrow"
   - "Show my notes"

🧮 Calculator:
   - "What is 15 + 27?"
   - "Calculate 100 / 4"
   - "2 * 3 + 5"

⏰ Reminders:
   - "Remind me to check email"
   - "Set reminder: Doctor appointment"
   - "Show reminders"

🔍 Web Search:
   - "Search for Python tutorials"
   - "Find information about AI"
   - "Look up machine learning"

📁 File Operations:
   - "Create file: notes.txt"
   - "Read file: config.json"

Type 'help' for this message, 'exit' to quit.
        """
        return help_text.strip()
    
    def get_status(self) -> str:
        """Get agent status and statistics"""
        total_interactions = len(self.conversation_history)
        recent_intents = [h["intent"] for h in self.conversation_history[-5:]]
        
        status = f"""
📊 Agent Status:
   - Total interactions: {total_interactions}
   - Recent intents: {', '.join(recent_intents) if recent_intents else 'None'}
   - Data directory: {actions.data_manager.data_dir}
   - Notes saved: {len(actions.data_manager.notes)}
   - Reminders active: {len([r for r in actions.data_manager.reminders if not r['completed']])}
        """
        return status.strip()

def main():
    """Main application loop"""
    agent = TaskAgent()
    
    print("🤖 Enhanced AI Task Agent Ready!")
    print("Type 'help' for available commands, 'status' for agent info, or 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("👋 Goodbye! Thanks for using the AI Task Agent!")
                break
            elif user_input.lower() == "help":
                print(agent.get_help())
            elif user_input.lower() == "status":
                print(agent.get_status())
            else:
                response = agent.process_input(user_input)
                print(f"Agent: {response}")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Thanks for using the AI Task Agent!")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
            print("Sorry, an unexpected error occurred. Please try again.")

if __name__ == "__main__":
    main()
