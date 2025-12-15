# Daily Automation Deployment Guide

## ✅ What's Ready
- Sheet Notifier is fully working
- Fetches all jobs from today's sheet
- Sends emails via SendGrid
- GitHub Actions workflow configured

## 🚀 Deploy to GitHub for Daily Automation

### Step 1: Initialize Git Repository
```bash
cd /Users/yashwanth/workspace/current_projects/sheet-notifier
git add .
git commit -m "Complete sheet notifier with SendGrid integration"
```

### Step 2: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `sheet-notifier`
3. Make it **Private** (recommended - contains sensitive data)
4. Click "Create repository"

### Step 3: Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/sheet-notifier.git
git branch -M main
git push -u origin main
```

### Step 4: Add GitHub Secrets
Go to your repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these 5 secrets:

| Secret Name | Value |
|------------|-------|
| `GOOGLE_SHEET_URL` | Your Google Sheets URL |
| `SENDGRID_API_KEY` | Your SendGrid API key (from .env file) |
| `SENDER_EMAIL` | Your sender email address |
| `RECIPIENT_EMAIL` | Your recipient email address |
| `EMAIL_SUBJECT` | `Daily Job Updates - Software Engineering` |

### Step 5: Enable GitHub Actions
1. Go to your repository → **Actions** tab
2. If prompted, click "I understand my workflows, go ahead and enable them"
3. You should see the "Daily Job Notifier" workflow

### Step 6: Test the Workflow
1. Click on "Daily Job Notifier" workflow
2. Click "Run workflow" dropdown
3. Click "Run workflow" button
4. Wait 30-60 seconds
5. Check yashwanth721@gmail.com for the email

## 📅 Automatic Daily Schedule

Once deployed, the workflow will run automatically:
- **Every day at 9 AM UTC** (4 AM EST / 1 AM PST)
- Fetches jobs from that day's sheet (December 7, December 8, etc.)
- Sends email to yashwanth721@gmail.com
- Continues through end of year

## ⚙️ Customization

### Change Schedule Time
Edit `.github/workflows/daily-notify.yml`:

```yaml
schedule:
  - cron: '0 14 * * *'  # 2 PM UTC = 9 AM EST
```

Cron format: `minute hour day month weekday`
- `0 9 * * *` = 9 AM UTC every day
- `0 14 * * *` = 2 PM UTC every day
- `30 12 * * 1-5` = 12:30 PM UTC Monday-Friday

### Change Recipient Email
Update the `RECIPIENT_EMAIL` secret in GitHub

### Change Email Subject
Update the `EMAIL_SUBJECT` secret in GitHub

## 🔍 Monitoring

### View Workflow Runs
- Go to repository → **Actions** tab
- See all past runs and their status
- Click on a run to see detailed logs

### Check SendGrid Activity
- Go to https://app.sendgrid.com/email_activity
- See all sent emails and delivery status

## ✅ Success Checklist
- [ ] Git repository initialized
- [ ] Pushed to GitHub
- [ ] All 5 secrets added
- [ ] GitHub Actions enabled
- [ ] Manual test run successful
- [ ] Email received

## 🎉 You're Done!
Your sheet notifier will now run automatically every day!
