"""Main script to fetch sheet data and send email updates."""
import sys
import logging
from config import Config
from sheets_client import SheetsClient
from email_sender import EmailSender

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main execution function."""
    try:
        # Validate configuration
        logger.info("Validating configuration...")
        Config.validate()
        
        # Initialize clients
        logger.info("Initializing Google Sheets client...")
        sheets_client = SheetsClient(Config.GOOGLE_SHEET_URL)
        
        logger.info("Initializing SendGrid email sender...")
        email_sender = EmailSender(
            Config.SENDGRID_API_KEY,
            Config.SENDER_EMAIL
        )
        
        # Fetch today's data
        logger.info("Fetching today's sheet data...")
        data = sheets_client.fetch_today_data()
        logger.info(f"Found {len(data)} jobs in today's sheet")
        
        # Send email
        logger.info(f"Sending email to {Config.RECIPIENT_EMAIL}...")
        email_sender.send_email(
            Config.RECIPIENT_EMAIL,
            Config.EMAIL_SUBJECT,
            data
        )
        
        logger.info("✅ Email sent successfully via SendGrid!")
        return 0
        
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
