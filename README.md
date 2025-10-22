# Phone Status Checker - Telegram Bot

A Telegram bot that checks if phone numbers are switched on or off by sending SMS through the IllyVoIP API.

## Features

- 📤 **Bulk Check**: Upload a text file with multiple phone numbers
- 📱 **Single Check**: Check individual phone numbers
- 🎯 **Status Detection**: 
  - ✅ Delivered = Phone is ON
  - ⏳ Sent = Phone is OFF
  - ❌ Failed = Invalid number or error
- 🎮 **Inline Menu**: All functionality through easy-to-use inline buttons

## Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- IllyVoIP API Key and Session ID

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/thertxnetwork/phone-status-checker.git
   cd phone-status-checker
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   SMS_API_KEY=your_api_key_here
   SMS_API_SESSION=your_session_id_here
   SMS_FROM_NAME=RABBI RTX
   ```

## Getting Your API Credentials

### Telegram Bot Token
1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow the instructions
3. Copy the token provided

### IllyVoIP API Credentials
- **API Key**: Your IllyVoIP API key (X-API-KEY header)
- **Session ID**: Your PHP session ID (PHPSESSID cookie)
- **From Name**: The sender name for SMS (default: "RABBI RTX")

## Usage

### Starting the Bot

Run the bot:
```bash
python bot.py
```

### Using the Bot on Telegram

1. **Start the bot**: Send `/start` to your bot on Telegram
2. **Choose an option**:
   - **Upload Phone Numbers File**: Upload a `.txt` file with phone numbers (one per line)
   - **Check Single Number**: Send a single phone number to check
   - **Help**: View detailed instructions

### Phone Number Format

Phone numbers must be in international format:
```
+351303527488
+351934014201
+351934014202
```

### Example Text File

Create a file `numbers.txt`:
```
+351303527488
+351934014201
+351934014202
```

Then upload it to the bot.

## How It Works

1. **SMS Sending**: The bot sends a test SMS to the phone number(s)
2. **Status Check**: After 30 seconds, it checks the delivery status
3. **Result Analysis**:
   - **Delivered**: The SMS was delivered → Phone is ON
   - **Sent**: The SMS was sent but not delivered → Phone is OFF
   - **Error**: Failed to send or invalid number

## API Integration

The bot uses the IllyVoIP SMS API with two endpoints:

### Send SMS
```bash
POST https://illyvoip.com/my/api.php?action=sms_api&subaction=send
```

### Check Status
```bash
GET https://illyvoip.com/my/api.php?action=sms_api&subaction=status&message_id={id}
```

## Project Structure

```
phone-status-checker/
├── bot.py              # Main bot application
├── requirements.txt    # Python dependencies
├── .env.example       # Example environment configuration
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Dependencies

- `python-telegram-bot==20.7` - Telegram Bot API wrapper
- `requests==2.31.0` - HTTP library for API calls
- `python-dotenv==1.0.0` - Environment variable management

## Troubleshooting

### Bot doesn't start
- Check if `TELEGRAM_BOT_TOKEN` is correctly set in `.env`
- Verify the token with [@BotFather](https://t.me/botfather)

### SMS not sending
- Verify `SMS_API_KEY` and `SMS_API_SESSION` are correct
- Check your IllyVoIP account balance
- Ensure phone numbers are in international format

### Status always shows "OFF"
- Wait at least 30 seconds for delivery status
- Some networks may take longer to deliver
- Check if the phone number is valid and active

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys and tokens secure
- The `.env` file is included in `.gitignore` by default

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.