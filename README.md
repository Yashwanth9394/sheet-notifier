# Sheet Notifier

Automatically fetch daily job data from a public Google Sheet and send formatted email updates.

## Features

- 📊 Fetches data from public Google Sheets (no API credentials needed)
- 📧 Sends formatted HTML emails via Gmail
- ☁️ Runs automatically in the cloud via GitHub Actions
- 🎯 Finds today's sheet by date (e.g., "December 5")

## Quick Start

### 1. Clone and Install

```bash
cd /Users/yashwanth/workspace/current_projects/sheet-notifier
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your details:

```bash
cp .env.example .env
```

Edit `.env`:
```
GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_gmail_app_password
RECIPIENT_EMAIL=friend_email@example.com
```

### 3. Get Gmail App Password

1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Enable **2-Step Verification** (Security → 2-Step Verification)
3. Go to **Security** → **App passwords**
4. Generate password for "Mail"
5. Copy the 16-character password to `.env` as `SENDER_PASSWORD`

### 4. Test Locally

```bash
python main.py
```

## GitHub Actions Setup (Cloud Scheduling)

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_REPO_URL
git push -u origin main
```

### 2. Add GitHub Secrets

Go to: **Repository Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these secrets:
- `GOOGLE_SHEET_URL` - Your Google Sheets URL
- `SENDER_EMAIL` - Your Gmail address
- `SENDER_PASSWORD` - Your Gmail app password
- `RECIPIENT_EMAIL` - Friend's email address

### 3. Schedule

The workflow runs daily at 9 AM UTC (configured in `.github/workflows/daily-notify.yml`).

You can also trigger it manually from the **Actions** tab.

## How It Works

1. **Finds Today's Sheet**: Looks for today's date in sheet names
2. **Fetches Data**: Retrieves all job data from the public sheet
3. **Formats Email**: Creates an HTML table with all information
4. **Sends Email**: Delivers via Gmail SMTP

## Customization

### Change Schedule Time

Edit `.github/workflows/daily-notify.yml`:

```yaml
schedule:
  - cron: '0 14 * * *'  # 2 PM UTC = 9 AM EST
```

### Customize Email Format

Edit `email_sender.py` to modify the HTML template.

## Troubleshooting

**Sheet not found**: Ensure sheet name matches date format exactly (e.g., "December 5")

**Email not sending**: 
- Verify Gmail app password is correct
- Check 2-Step Verification is enabled
- Ensure sender email is correct

**GitHub Actions failing**:
- Verify all secrets are added correctly
- Check Actions tab for error logs

## Project Structure

```
sheet-notifier/
├── main.py                    # Main orchestration
├── sheets_client.py           # Google Sheets fetching
├── email_sender.py            # Email sending
├── config.py                  # Configuration
├── requirements.txt           # Dependencies
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
└── .github/workflows/
    └── daily-notify.yml      # GitHub Actions
```

## License

MIT
