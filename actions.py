import json
import os
import re
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataManager:
    """Handles data persistence for notes and reminders"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.notes_file = os.path.join(data_dir, "notes.json")
        self.reminders_file = os.path.join(data_dir, "reminders.json")
        self.config_file = os.path.join(data_dir, "config.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Load existing data
        self.notes = self._load_notes()
        self.reminders = self._load_reminders()
        self.config = self._load_config()
    
    def _load_notes(self) -> List[Dict[str, Any]]:
        """Load notes from JSON file"""
        try:
            if os.path.exists(self.notes_file):
                with open(self.notes_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading notes: {e}")
        return []
    
    def _load_reminders(self) -> List[Dict[str, Any]]:
        """Load reminders from JSON file"""
        try:
            if os.path.exists(self.reminders_file):
                with open(self.reminders_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading reminders: {e}")
        return []
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
        return {"weather_api_key": "", "default_city": "London"}
    
    def save_notes(self):
        """Save notes to JSON file"""
        try:
            with open(self.notes_file, 'w') as f:
                json.dump(self.notes, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving notes: {e}")
    
    def save_reminders(self):
        """Save reminders to JSON file"""
        try:
            with open(self.reminders_file, 'w') as f:
                json.dump(self.reminders, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving reminders: {e}")
    
    def save_config(self):
        """Save configuration to JSON file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving config: {e}")

# Global data manager instance
data_manager = DataManager()

class WeatherService:
    """Handles weather-related operations"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or data_manager.config.get("weather_api_key", "")
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def get_weather(self, city: str) -> str:
        """Get weather information for a city"""
        if not self.api_key:
            return "Weather API key not configured. Please set your OpenWeatherMap API key."
        
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            
            return f"Weather in {city}: {description.title()}, {temp}°C, Humidity: {humidity}%, Wind: {wind_speed} m/s"
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Weather API error: {e}")
            return f"Sorry, I couldn't get weather data for {city}. Please check the city name and try again."
        except Exception as e:
            logger.error(f"Unexpected error getting weather: {e}")
            return "Sorry, there was an error getting weather information."

class Calculator:
    """Handles mathematical calculations"""
    
    def calculate(self, expression: str) -> str:
        """Safely evaluate mathematical expressions"""
        try:
            # Clean the expression - only allow numbers, operators, and parentheses
            cleaned = re.sub(r'[^0-9+\-*/().\s]', '', expression)
            if not cleaned.strip():
                return "Please provide a valid mathematical expression."
            
            # Use eval with restricted globals for safety
            result = eval(cleaned, {"__builtins__": {}}, {})
            return f"{expression} = {result}"
            
        except ZeroDivisionError:
            return "Error: Division by zero is not allowed."
        except Exception as e:
            logger.error(f"Calculation error: {e}")
            return "Sorry, I couldn't calculate that expression. Please check your input."

class ReminderManager:
    """Handles reminder functionality"""
    
    def add_reminder(self, text: str, time_str: str = None) -> str:
        """Add a new reminder"""
        reminder = {
            "id": len(data_manager.reminders) + 1,
            "text": text,
            "created_at": datetime.now().isoformat(),
            "time": time_str,
            "completed": False
        }
        data_manager.reminders.append(reminder)
        data_manager.save_reminders()
        return f"Reminder added: '{text}'"
    
    def get_reminders(self) -> str:
        """Get all active reminders"""
        if not data_manager.reminders:
            return "No reminders set."
        
        active_reminders = [r for r in data_manager.reminders if not r["completed"]]
        if not active_reminders:
            return "No active reminders."
        
        reminder_list = []
        for reminder in active_reminders:
            status = f" (Due: {reminder['time']})" if reminder['time'] else ""
            reminder_list.append(f"- {reminder['text']}{status}")
        
        return "Active reminders:\n" + "\n".join(reminder_list)

# Initialize services
weather_service = WeatherService()
calculator = Calculator()
reminder_manager = ReminderManager()

# Action handlers
def handle_weather(user_input: str = None) -> str:
    """Handle weather requests"""
    if not user_input or user_input.strip() == "":
        default_city = data_manager.config.get("default_city", "London")
        return f"Getting weather for {default_city}...\n{weather_service.get_weather(default_city)}"
    
    # Extract city from input
    city = user_input.strip()
    return weather_service.get_weather(city)

def handle_add_note(user_input: str) -> str:
    """Handle adding notes"""
    # Extract note content
    note_content = user_input.lower()
    for trigger in ["add note", "note", "remember", "save"]:
        note_content = note_content.replace(trigger, "").strip()
    
    if not note_content:
        return "Please provide the note content."
    
    note = {
        "id": len(data_manager.notes) + 1,
        "content": note_content,
        "created_at": datetime.now().isoformat()
    }
    data_manager.notes.append(note)
    data_manager.save_notes()
    return f"Note saved: '{note_content}'"

def handle_show_notes() -> str:
    """Handle showing notes"""
    if not data_manager.notes:
        return "No notes saved yet."
    
    note_list = []
    for note in data_manager.notes[-10:]:  # Show last 10 notes
        created = datetime.fromisoformat(note["created_at"]).strftime("%Y-%m-%d %H:%M")
        note_list.append(f"- {note['content']} (Added: {created})")
    
    return "Recent notes:\n" + "\n".join(note_list)

def handle_calculator(user_input: str) -> str:
    """Handle calculator requests"""
    # Extract mathematical expression
    expression = user_input.strip()
    for trigger in ["calculate", "compute", "what is", "how much is"]:
        expression = expression.replace(trigger, "").strip()
    
    return calculator.calculate(expression)

def handle_reminder(user_input: str) -> str:
    """Handle reminder requests"""
    if "show" in user_input.lower() or "list" in user_input.lower():
        return reminder_manager.get_reminders()
    
    # Extract reminder text
    reminder_text = user_input.lower()
    for trigger in ["remind me", "set reminder", "reminder"]:
        reminder_text = reminder_text.replace(trigger, "").strip()
    
    if not reminder_text:
        return "Please provide the reminder text."
    
    return reminder_manager.add_reminder(reminder_text)

def handle_web_search(user_input: str) -> str:
    """Handle web search requests (placeholder)"""
    search_query = user_input.strip()
    for trigger in ["search for", "find", "look up", "what is"]:
        search_query = search_query.replace(trigger, "").strip()
    
    return f"I would search for '{search_query}' on the web. (Web search integration coming soon!)"

def handle_file_operation(user_input: str) -> str:
    """Handle file operations (placeholder)"""
    return "File operations are not yet implemented. This feature is coming soon!"

def handle_unknown(user_input: str) -> str:
    """Handle unknown intents"""
    return f"I'm not sure how to help with '{user_input}'. Try asking about weather, notes, calculations, or reminders!"
