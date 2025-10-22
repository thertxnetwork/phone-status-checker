# Bot Interface Documentation

## User Flow and Interface

### 1. Starting the Bot

When a user sends `/start` to the bot, they see:

```
👋 Welcome to Phone Status Checker Bot!

This bot helps you check if phone numbers are switched on or off by sending SMS.

Choose an option below to get started:

[📤 Upload Phone Numbers File]
[📱 Check Single Number]
[ℹ️ Help]
```

### 2. Upload Phone Numbers File Option

When user clicks "📤 Upload Phone Numbers File":

```
📤 Please upload a text file containing phone numbers.

Format: One phone number per line
Example:
+351303527488
+351934014201
+351934014202
```

User then uploads a .txt file, and the bot processes it:

```
📥 Processing your file...
📋 Found 3 phone numbers.
🚀 Starting to check statuses...

This may take a few moments. Please wait...

📤 Sending test SMS to 3 number(s)...
⏳ SMS sent. Waiting for delivery status (30 seconds)...
🔍 Checking delivery status...

📊 Status Check Results:

✅ Phone(s) SWITCHED ON (Delivered):
  • +351303527488

⏳ Phone(s) SWITCHED OFF (Sent but not delivered):
  • +351934014201
  • +351934014202

📈 Summary:
Total checked: 3
Online: 1
Offline: 2
Errors: 0

[🔙 Back to Menu]
```

### 3. Check Single Number Option

When user clicks "📱 Check Single Number":

```
📱 Please send a phone number to check.

Format: +[country_code][phone_number]
Example: +351303527488
```

User sends a phone number (e.g., `+351303527488`), then:

```
📱 Checking status for: +351303527488
⏳ Please wait...

📤 Sending test SMS to 1 number(s)...
⏳ SMS sent. Waiting for delivery status (30 seconds)...
🔍 Checking delivery status...

📊 Status Check Results:

✅ Phone(s) SWITCHED ON (Delivered):
  • +351303527488

📈 Summary:
Total checked: 1
Online: 1
Offline: 0
Errors: 0

[🔙 Back to Menu]
```

### 4. Help Option

When user clicks "ℹ️ Help":

```
ℹ️ How to use this bot:

1️⃣ Upload Phone Numbers File
   Upload a .txt file with phone numbers (one per line)

2️⃣ Check Single Number
   Send a single phone number to check its status

📊 Status Meanings:
• ✅ Delivered - Phone is switched ON
• ⏳ Sent - Phone is switched OFF
• ❌ Failed - Invalid number or error

Use /start to return to the main menu.

[🔙 Back to Menu]
```

### 5. Error Handling

If user uploads a non-.txt file:
```
❌ Please upload a .txt file containing phone numbers.
```

If file has no valid numbers:
```
❌ No valid phone numbers found in the file.
Please ensure each line contains a phone number starting with '+'.
```

If user sends invalid phone number format:
```
❌ Invalid phone number format.
Please send a phone number starting with '+'
Example: +351303527488
```

If API error occurs:
```
❌ Failed to send SMS. Please check your API configuration.
```

## API Integration Details

### SMS Sending Process
1. Bot sends HTTP POST to IllyVoIP API
2. Receives message IDs for tracking
3. Waits 30 seconds for delivery
4. Checks status of each message

### Status Interpretation
- **delivered**: Message delivered → Phone is ON
- **sent**: Message sent but not delivered → Phone is OFF
- **failed/error**: Invalid number or API error

## User Experience Features

✅ **Inline Keyboard Navigation**: All actions through buttons, no typing commands
✅ **Real-time Progress**: User sees each step of the process
✅ **Clear Status Indicators**: Emojis and formatting for easy understanding
✅ **Error Messages**: Clear feedback when something goes wrong
✅ **Batch Processing**: Can check multiple numbers at once
✅ **Single Check**: Quick check for individual numbers
✅ **Back Navigation**: Easy to return to main menu
