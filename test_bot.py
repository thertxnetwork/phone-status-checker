#!/usr/bin/env python3
"""
Simple test script to validate bot components without running the full bot.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required imports work."""
    print("Testing imports...")
    try:
        from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
        from telegram.ext import Application, CommandHandler, CallbackQueryHandler
        import requests
        from dotenv import load_dotenv
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_env_loading():
    """Test environment variable loading."""
    print("\nTesting environment configuration...")
    from dotenv import load_dotenv
    
    load_dotenv()
    
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    api_key = os.getenv('SMS_API_KEY')
    
    if not token:
        print("⚠️  TELEGRAM_BOT_TOKEN not set (expected for first run)")
    else:
        print(f"✅ TELEGRAM_BOT_TOKEN is set (length: {len(token)})")
    
    if not api_key:
        print("⚠️  SMS_API_KEY not set (expected for first run)")
    else:
        print(f"✅ SMS_API_KEY is set (length: {len(api_key)})")
    
    return True


def test_phone_number_parsing():
    """Test phone number parsing logic."""
    print("\nTesting phone number parsing...")
    
    test_data = """
    +351303527488
    +351934014201
    # This is a comment
    +351934014202
    invalid_number
    +123456789
    """
    
    phone_numbers = []
    for line in test_data.splitlines():
        line = line.strip()
        if line and line.startswith('+') and not line.startswith('#'):
            phone_numbers.append(line)
    
    print(f"Parsed {len(phone_numbers)} valid numbers:")
    for phone in phone_numbers:
        print(f"  - {phone}")
    
    expected = 4  # All numbers starting with + are parsed
    if len(phone_numbers) == expected:
        print(f"✅ Correctly parsed {expected} phone numbers")
        return True
    else:
        print(f"❌ Expected {expected} numbers, got {len(phone_numbers)}")
        return False


def test_api_functions_syntax():
    """Test that API functions are properly defined."""
    print("\nTesting API function definitions...")
    
    try:
        # Import the bot module to check function definitions
        import bot
        
        # Check if functions exist
        assert hasattr(bot, 'send_sms'), "send_sms function not found"
        assert hasattr(bot, 'check_sms_status'), "check_sms_status function not found"
        assert hasattr(bot, 'process_phone_numbers'), "process_phone_numbers function not found"
        
        print("✅ All API functions are properly defined")
        return True
    except Exception as e:
        print(f"❌ Error checking functions: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Phone Status Checker Bot - Component Tests")
    print("=" * 60)
    
    results = []
    
    results.append(("Import Test", test_imports()))
    results.append(("Environment Test", test_env_loading()))
    results.append(("Phone Parsing Test", test_phone_number_parsing()))
    results.append(("API Functions Test", test_api_functions_syntax()))
    
    print("\n" + "=" * 60)
    print("Test Results Summary:")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed! Bot is ready to run.")
        print("\nNext steps:")
        print("1. Copy .env.example to .env")
        print("2. Add your API credentials to .env")
        print("3. Run: python bot.py")
    else:
        print("❌ Some tests failed. Please install dependencies:")
        print("   pip install -r requirements.txt")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
