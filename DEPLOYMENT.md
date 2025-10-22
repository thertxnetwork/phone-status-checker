# Deployment Guide

## Quick Deployment Checklist

### Prerequisites
- [ ] Python 3.8 or higher installed
- [ ] Telegram account
- [ ] IllyVoIP account with API access
- [ ] Server or local machine to run the bot

### Step 1: Get Telegram Bot Token
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the prompts to create your bot
4. Copy the token (format: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)
5. Save it for later

### Step 2: Get IllyVoIP API Credentials
1. Log in to your IllyVoIP account
2. Navigate to API settings
3. Copy your API Key (X-API-KEY header value)
4. Copy your Session ID (PHPSESSID cookie value)
5. Note your preferred sender name

### Step 3: Install and Configure

```bash
# Clone the repository
git clone https://github.com/thertxnetwork/phone-status-checker.git
cd phone-status-checker

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # or use your preferred editor
```

Edit `.env`:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
SMS_API_KEY=your_api_key_here
SMS_API_SESSION=your_session_id_here
SMS_FROM_NAME=RABBI RTX
```

### Step 4: Test the Bot

```bash
# Run component tests
python test_bot.py

# Expected output: All tests passed ✅
```

### Step 5: Start the Bot

```bash
python bot.py
```

Expected output:
```
🤖 Phone Status Checker Bot is running!
Press Ctrl+C to stop
```

### Step 6: Test in Telegram
1. Open Telegram
2. Search for your bot by username
3. Send `/start`
4. Test with a single number or upload a file

## Production Deployment

### Option 1: Running on Linux Server

**Using systemd service:**

1. Create service file:
```bash
sudo nano /etc/systemd/system/phone-checker-bot.service
```

2. Add configuration:
```ini
[Unit]
Description=Phone Status Checker Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/phone-status-checker
Environment="PATH=/path/to/phone-status-checker/venv/bin"
ExecStart=/path/to/phone-status-checker/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. Enable and start:
```bash
sudo systemctl enable phone-checker-bot
sudo systemctl start phone-checker-bot
sudo systemctl status phone-checker-bot
```

4. View logs:
```bash
sudo journalctl -u phone-checker-bot -f
```

### Option 2: Running with Docker

**Create Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

**Create docker-compose.yml:**
```yaml
version: '3.8'

services:
  bot:
    build: .
    env_file:
      - .env
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
```

**Run:**
```bash
docker-compose up -d
docker-compose logs -f
```

### Option 3: Running with Screen (Simple)

```bash
screen -S phone-bot
cd /path/to/phone-status-checker
source venv/bin/activate
python bot.py

# Detach: Ctrl+A then D
# Reattach: screen -r phone-bot
```

## Monitoring and Maintenance

### Checking Bot Status
```bash
# If using systemd
sudo systemctl status phone-checker-bot

# If using screen
screen -ls

# If using docker
docker-compose ps
```

### Viewing Logs
Bot logs are output to console by default. You can redirect them:

```bash
python bot.py >> bot.log 2>&1 &
```

Or configure logging in the code to write to file.

### Updating the Bot
```bash
# Stop the bot
sudo systemctl stop phone-checker-bot  # or docker-compose down

# Pull updates
git pull

# Update dependencies if needed
pip install -r requirements.txt

# Restart
sudo systemctl start phone-checker-bot  # or docker-compose up -d
```

## Security Best Practices

1. **Environment Variables**
   - Never commit `.env` file
   - Use strong, unique tokens
   - Rotate API keys periodically

2. **File Permissions**
   ```bash
   chmod 600 .env
   chmod 755 bot.py
   ```

3. **Server Security**
   - Use firewall (ufw, iptables)
   - Keep system updated
   - Use SSH keys instead of passwords
   - Run bot as non-root user

4. **Monitoring**
   - Set up alerts for bot downtime
   - Monitor API usage and costs
   - Check logs regularly for errors

## Troubleshooting

### Bot Doesn't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Check dependencies
pip install -r requirements.txt

# Test configuration
python test_bot.py
```

### SMS Not Sending
- Verify API credentials are correct
- Check IllyVoIP account balance
- Test API endpoints manually with curl
- Check network connectivity

### Bot Not Responding
- Check bot token is valid
- Verify bot is running: `ps aux | grep bot.py`
- Check logs for errors
- Test with `/start` command

### Memory Issues
```bash
# Monitor memory usage
htop

# If needed, restart bot regularly via cron
0 3 * * * systemctl restart phone-checker-bot
```

## Cost Estimation

**API Costs (IllyVoIP):**
- SMS cost per message: ~€0.40
- 100 checks = ~€40
- 1000 checks = ~€400

**Server Costs:**
- VPS (minimal): €5-10/month
- AWS/GCP/Azure: $5-20/month
- Local hosting: Free (electricity only)

**Recommendations:**
- Start with VPS for reliability
- Budget based on expected SMS volume
- Monitor API usage to control costs

## Support and Maintenance

**Regular Tasks:**
- [ ] Monitor bot logs weekly
- [ ] Check API balance monthly
- [ ] Update dependencies quarterly
- [ ] Review and optimize code annually

**Emergency Contacts:**
- IllyVoIP Support: [Your support contact]
- Telegram Support: https://telegram.org/support
- Project Issues: GitHub Issues

## Scaling Considerations

For high volume usage:

1. **Rate Limiting**: Add delays between bulk operations
2. **Queue System**: Use Redis/Celery for SMS queue
3. **Database**: Store results in PostgreSQL/MySQL
4. **Load Balancing**: Run multiple bot instances
5. **Caching**: Cache API responses for duplicate checks

## Backup Strategy

**What to Backup:**
- `.env` file (secure location only)
- Bot configuration
- User data (if implementing database)
- Logs (for audit trail)

**Backup Commands:**
```bash
# Backup configuration
tar -czf backup-$(date +%Y%m%d).tar.gz .env bot.py

# Automated daily backup
0 2 * * * cd /path/to/bot && tar -czf /backups/bot-$(date +\%Y\%m\%d).tar.gz .env bot.py
```

## License and Legal

- Ensure compliance with SMS regulations in your country
- Respect user privacy (GDPR, CCPA, etc.)
- Include terms of service for bot users
- Document data retention policies

---

**Need Help?** 
Open an issue on GitHub or consult the README.md for more details.
