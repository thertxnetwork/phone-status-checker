# Quick Start Guide

## Setup in 5 Minutes

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Your Bot
Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
SMS_API_KEY=f0dce5c6fcfc021b602643c31a7ebcb8c00a4d3a6e5e8f35f010f9e64cae0953
SMS_API_SESSION=734503de6a003cadcc011e49035c0729
SMS_FROM_NAME=RABBI RTX
```

### 3. Run the Bot
```bash
python bot.py
```

### 4. Use the Bot

1. Open Telegram and find your bot
2. Send `/start`
3. Choose "📤 Upload Phone Numbers File" or "📱 Check Single Number"

## Example Phone Numbers File

Create `test_numbers.txt`:
```
+351303527488
+351934014201
+351934014202
```

Upload this file to the bot and wait for results!

## Understanding Results

- ✅ **Delivered** = Phone is switched ON and received the SMS
- ⏳ **Sent** = Phone is switched OFF (SMS sent but not delivered)
- ❌ **Error** = Invalid number or API error

## Troubleshooting

**Bot won't start?**
- Check your `TELEGRAM_BOT_TOKEN` is correct
- Run: `python bot.py` to see error messages

**SMS not sending?**
- Verify your `SMS_API_KEY` and `SMS_API_SESSION`
- Check your IllyVoIP account has credit
- Ensure phone numbers start with `+` and country code

**All numbers show as OFF?**
- Wait at least 30 seconds for delivery status
- Some carriers may take longer to report delivery

## Need Help?

Check the full [README.md](README.md) for detailed documentation.
