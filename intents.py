import re
from typing import Dict, List, Tuple

class IntentDetector:
    def __init__(self):
        # Define intent patterns with confidence scoring
        self.intent_patterns = {
            "weather": {
                "keywords": ["weather", "temperature", "forecast", "rain", "sunny", "cloudy", "hot", "cold", "humidity"],
                "phrases": ["what's the weather", "how's the weather", "weather today", "weather forecast"],
                "confidence": 0.8
            },
            "add_note": {
                "keywords": ["note", "remember", "save", "write down", "jot down"],
                "phrases": ["add note", "create note", "save note", "remember that"],
                "confidence": 0.7
            },
            "show_notes": {
                "keywords": ["show", "list", "display", "view", "notes"],
                "phrases": ["show notes", "list notes", "display notes", "view notes", "my notes"],
                "confidence": 0.8
            },
            "calculator": {
                "keywords": ["calculate", "compute", "math", "add", "subtract", "multiply", "divide", "+", "-", "*", "/"],
                "phrases": ["what is", "how much is", "calculate", "compute"],
                "confidence": 0.6
            },
            "reminder": {
                "keywords": ["remind", "reminder", "alarm", "schedule", "later", "tomorrow"],
                "phrases": ["remind me", "set reminder", "schedule", "alarm"],
                "confidence": 0.7
            },
            "web_search": {
                "keywords": ["search", "find", "look up", "google", "information about"],
                "phrases": ["search for", "find information", "look up", "what is"],
                "confidence": 0.6
            },
            "file_operation": {
                "keywords": ["file", "create", "read", "write", "delete", "folder", "directory"],
                "phrases": ["create file", "read file", "write to file", "delete file"],
                "confidence": 0.7
            }
        }
    
    def detect_intent(self, user_input: str) -> Tuple[str, float]:
        """
        Detect intent with confidence scoring
        Returns: (intent_name, confidence_score)
        """
        text = user_input.lower().strip()
        
        # Check for exact phrase matches first (highest confidence)
        for intent, config in self.intent_patterns.items():
            for phrase in config["phrases"]:
                if phrase in text:
                    return intent, config["confidence"]
        
        # Check for keyword matches
        best_intent = "unknown"
        best_score = 0.0
        
        for intent, config in self.intent_patterns.items():
            score = 0.0
            keyword_count = 0
            
            for keyword in config["keywords"]:
                if keyword in text:
                    keyword_count += 1
                    score += 0.1  # Each keyword adds 0.1 to score
            
            # Normalize score based on number of keywords found
            if keyword_count > 0:
                score = min(score, config["confidence"])
                if score > best_score:
                    best_score = score
                    best_intent = intent
        
        # Special case: if no keywords found but contains numbers and operators, likely calculator
        if best_intent == "unknown" and re.search(r'[\d\+\-\*\/\(\)]', text):
            return "calculator", 0.5
        
        return best_intent, best_score
    
    def get_intent_confidence(self, user_input: str) -> float:
        """Get confidence score for intent detection"""
        _, confidence = self.detect_intent(user_input)
        return confidence

# Create global instance
intent_detector = IntentDetector()

def detect_intent(user_input: str) -> str:
    """Legacy function for backward compatibility"""
    intent, _ = intent_detector.detect_intent(user_input)
    return intent
