#!/usr/bin/env python3
"""
Telegram bot for checking phone status using SMS API.
"""

import os
import logging
import time
import asyncio
from typing import List, Dict
from dotenv import load_dotenv
import requests

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration from environment
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
SMS_API_URL = os.getenv('SMS_API_URL', 'https://illyvoip.com/my/api.php')
SMS_API_KEY = os.getenv('SMS_API_KEY')
SMS_API_SESSION = os.getenv('SMS_API_SESSION')
SMS_FROM_NAME = os.getenv('SMS_FROM_NAME', 'RABBI RTX')

# Store user data temporarily
user_data_store = {}


def send_sms(phone_numbers: List[str], message: str) -> Dict:
    """Send SMS to one or multiple phone numbers."""
    url = f"{SMS_API_URL}?action=sms_api&subaction=send"
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': SMS_API_KEY,
        'Cookie': f'PHPSESSID={SMS_API_SESSION}'
    }
    data = {
        'from': SMS_FROM_NAME,
        'to': phone_numbers,
        'message': message
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error sending SMS: {e}")
        return {'status': 'error', 'message': str(e)}


def check_sms_status(message_id: str) -> Dict:
    """Check the status of a sent SMS."""
    url = f"{SMS_API_URL}?action=sms_api&subaction=status&message_id={message_id}"
    headers = {
        'X-API-KEY': SMS_API_KEY,
        'Cookie': f'PHPSESSID={SMS_API_SESSION}'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error checking SMS status: {e}")
        return {'status': 'error', 'message': str(e)}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler - shows main menu."""
    keyboard = [
        [InlineKeyboardButton("📤 Upload Phone Numbers File", callback_data='upload_file')],
        [InlineKeyboardButton("📱 Check Single Number", callback_data='check_single')],
        [InlineKeyboardButton("ℹ️ Help", callback_data='help')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = (
        "👋 Welcome to Phone Status Checker Bot!\n\n"
        "This bot helps you check if phone numbers are switched on or off by sending SMS.\n\n"
        "Choose an option below to get started:"
    )
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'upload_file':
        await query.edit_message_text(
            "📤 Please upload a text file containing phone numbers.\n\n"
            "Format: One phone number per line\n"
            "Example:\n"
            "+351303527488\n"
            "+351934014201\n"
            "+351934014202"
        )
    elif query.data == 'check_single':
        await query.edit_message_text(
            "📱 Please send a phone number to check.\n\n"
            "Format: +[country_code][phone_number]\n"
            "Example: +351303527488"
        )
        # Store state for this user
        user_data_store[query.from_user.id] = {'state': 'waiting_single_number'}
    elif query.data == 'help':
        help_text = (
            "ℹ️ *How to use this bot:*\n\n"
            "1️⃣ *Upload Phone Numbers File*\n"
            "   Upload a .txt file with phone numbers (one per line)\n\n"
            "2️⃣ *Check Single Number*\n"
            "   Send a single phone number to check its status\n\n"
            "📊 *Status Meanings:*\n"
            "• ✅ *Delivered* - Phone is switched ON\n"
            "• ⏳ *Sent* - Phone is switched OFF\n"
            "• ❌ *Failed* - Invalid number or error\n\n"
            "Use /start to return to the main menu."
        )
        keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(help_text, parse_mode='Markdown', reply_markup=reply_markup)
    elif query.data == 'back_to_menu':
        keyboard = [
            [InlineKeyboardButton("📤 Upload Phone Numbers File", callback_data='upload_file')],
            [InlineKeyboardButton("📱 Check Single Number", callback_data='check_single')],
            [InlineKeyboardButton("ℹ️ Help", callback_data='help')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        welcome_message = (
            "👋 Welcome to Phone Status Checker Bot!\n\n"
            "This bot helps you check if phone numbers are switched on or off by sending SMS.\n\n"
            "Choose an option below to get started:"
        )
        await query.edit_message_text(welcome_message, reply_markup=reply_markup)


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle uploaded document (text file with phone numbers)."""
    document = update.message.document
    
    # Check if it's a text file
    if not document.file_name.endswith('.txt'):
        await update.message.reply_text(
            "❌ Please upload a .txt file containing phone numbers."
        )
        return
    
    await update.message.reply_text("📥 Processing your file...")
    
    # Download the file
    file = await context.bot.get_file(document.file_id)
    file_content = await file.download_as_bytearray()
    
    # Parse phone numbers
    phone_numbers = []
    for line in file_content.decode('utf-8').splitlines():
        line = line.strip()
        if line and line.startswith('+'):
            phone_numbers.append(line)
    
    if not phone_numbers:
        await update.message.reply_text(
            "❌ No valid phone numbers found in the file.\n"
            "Please ensure each line contains a phone number starting with '+'."
        )
        return
    
    await update.message.reply_text(
        f"📋 Found {len(phone_numbers)} phone numbers.\n"
        f"🚀 Starting to check statuses...\n\n"
        f"This may take a few moments. Please wait..."
    )
    
    # Process the phone numbers
    await process_phone_numbers(update, phone_numbers)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages (single phone number check)."""
    user_id = update.message.from_user.id
    message_text = update.message.text.strip()
    
    # Check if user is in single number check mode
    if user_id in user_data_store and user_data_store[user_id].get('state') == 'waiting_single_number':
        if message_text.startswith('+'):
            await update.message.reply_text(
                f"📱 Checking status for: {message_text}\n"
                f"⏳ Please wait..."
            )
            await process_phone_numbers(update, [message_text])
            # Clear user state
            del user_data_store[user_id]
        else:
            await update.message.reply_text(
                "❌ Invalid phone number format.\n"
                "Please send a phone number starting with '+'\n"
                "Example: +351303527488"
            )
    else:
        # Default response
        await update.message.reply_text(
            "Please use /start to see available options."
        )


async def process_phone_numbers(update: Update, phone_numbers: List[str]) -> None:
    """Process a list of phone numbers and check their status."""
    results = {
        'on': [],
        'off': [],
        'error': []
    }
    
    # Send SMS to all numbers
    await update.message.reply_text(
        f"📤 Sending test SMS to {len(phone_numbers)} number(s)..."
    )
    
    message_ids = {}
    
    # Send SMS one by one for better tracking
    for phone in phone_numbers:
        response = send_sms([phone], "Phone status check - Please ignore this message.")
        
        if response.get('status') == 'success' and response.get('queued_message_ids'):
            message_ids[phone] = response['queued_message_ids'][0]
        else:
            results['error'].append(phone)
    
    if not message_ids:
        await update.message.reply_text(
            "❌ Failed to send SMS. Please check your API configuration."
        )
        return
    
    await update.message.reply_text(
        f"⏳ SMS sent. Waiting for delivery status (30 seconds)..."
    )
    
    # Wait for SMS to be processed
    await asyncio.sleep(30)
    
    # Check status for each message
    await update.message.reply_text(
        f"🔍 Checking delivery status..."
    )
    
    for phone, msg_id in message_ids.items():
        status_response = check_sms_status(msg_id)
        
        if status_response.get('status') == 'success':
            sms_status = status_response.get('sms_status', '').lower()
            
            if sms_status == 'delivered':
                results['on'].append(phone)
            elif sms_status == 'sent':
                results['off'].append(phone)
            else:
                results['error'].append(phone)
        else:
            results['error'].append(phone)
    
    # Format and send results
    result_message = "📊 *Status Check Results:*\n\n"
    
    if results['on']:
        result_message += "✅ *Phone(s) SWITCHED ON (Delivered):*\n"
        for phone in results['on']:
            result_message += f"  • {phone}\n"
        result_message += "\n"
    
    if results['off']:
        result_message += "⏳ *Phone(s) SWITCHED OFF (Sent but not delivered):*\n"
        for phone in results['off']:
            result_message += f"  • {phone}\n"
        result_message += "\n"
    
    if results['error']:
        result_message += "❌ *Error/Invalid Number(s):*\n"
        for phone in results['error']:
            result_message += f"  • {phone}\n"
        result_message += "\n"
    
    result_message += f"\n📈 *Summary:*\n"
    result_message += f"Total checked: {len(phone_numbers)}\n"
    result_message += f"Online: {len(results['on'])}\n"
    result_message += f"Offline: {len(results['off'])}\n"
    result_message += f"Errors: {len(results['error'])}"
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        result_message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.message:
        await update.message.reply_text(
            "❌ An error occurred while processing your request. Please try again."
        )


def main() -> None:
    """Start the bot."""
    # Check if required environment variables are set
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is not set in environment variables!")
        print("❌ Error: TELEGRAM_BOT_TOKEN is not set!")
        print("Please copy .env.example to .env and configure your tokens.")
        return
    
    if not SMS_API_KEY:
        logger.error("SMS_API_KEY is not set in environment variables!")
        print("❌ Error: SMS_API_KEY is not set!")
        print("Please copy .env.example to .env and configure your API key.")
        return
    
    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Register error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Bot is starting...")
    print("🤖 Phone Status Checker Bot is running!")
    print("Press Ctrl+C to stop")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
