#!/usr/bin/env python3
"""
Configuration setup script for AI Task Agent
"""

import json
import os
from actions import data_manager

def setup_weather_api():
    """Setup weather API configuration"""
    print("🌤️  Weather API Setup")
    print("=" * 50)
    print("To get weather information, you need an OpenWeatherMap API key.")
    print("1. Go to https://openweathermap.org/api")
    print("2. Sign up for a free account")
    print("3. Get your API key from the dashboard")
    print()
    
    api_key = input("Enter your OpenWeatherMap API key (or press Enter to skip): ").strip()
    
    if api_key:
        data_manager.config["weather_api_key"] = api_key
        data_manager.save_config()
        print("✅ Weather API key saved successfully!")
    else:
        print("⚠️  Weather API key not set. Weather features will be limited.")
    
    print()

def setup_default_city():
    """Setup default city for weather"""
    print("🏙️  Default City Setup")
    print("=" * 50)
    
    current_city = data_manager.config.get("default_city", "London")
    print(f"Current default city: {current_city}")
    
    new_city = input("Enter your default city (or press Enter to keep current): ").strip()
    
    if new_city:
        data_manager.config["default_city"] = new_city
        data_manager.save_config()
        print(f"✅ Default city set to: {new_city}")
    else:
        print(f"✅ Keeping current default city: {current_city}")
    
    print()

def show_current_config():
    """Show current configuration"""
    print("📋 Current Configuration")
    print("=" * 50)
    print(f"Data directory: {data_manager.data_dir}")
    print(f"Weather API key: {'Set' if data_manager.config.get('weather_api_key') else 'Not set'}")
    print(f"Default city: {data_manager.config.get('default_city', 'London')}")
    print(f"Notes saved: {len(data_manager.notes)}")
    print(f"Reminders active: {len([r for r in data_manager.reminders if not r['completed']])}")
    print()

def main():
    """Main setup function"""
    print("🤖 AI Task Agent - Configuration Setup")
    print("=" * 50)
    print()
    
    while True:
        print("Choose an option:")
        print("1. Setup Weather API")
        print("2. Setup Default City")
        print("3. Show Current Configuration")
        print("4. Exit")
        print()
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            setup_weather_api()
        elif choice == "2":
            setup_default_city()
        elif choice == "3":
            show_current_config()
        elif choice == "4":
            print("👋 Setup complete! Run 'python main_agent.py' to start the agent.")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")
            print()

if __name__ == "__main__":
    main()
