"""Configuration management for Sheet Notifier."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration."""
    
    # Google Sheets
    GOOGLE_SHEET_URL = os.getenv('GOOGLE_SHEET_URL')
    
    # SendGrid Configuration
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    SENDER_EMAIL = os.getenv('SENDER_EMAIL')
    # Support multiple recipients (comma-separated in env, plus hardcoded defaults)
    _env_recipients = os.getenv('RECIPIENT_EMAIL', '').split(',')
    RECIPIENT_EMAIL = [email.strip() for email in _env_recipients if email.strip()]
    RECIPIENT_EMAIL.append('yashwanthkp753@gmail.com')
    RECIPIENT_EMAIL.append('sreekarsmailbox@gmail.com')
    # Remove duplicates while preserving order
    RECIPIENT_EMAIL = list(dict.fromkeys(RECIPIENT_EMAIL))
    
    # Optional Configuration
    EMAIL_SUBJECT = os.getenv('EMAIL_SUBJECT', 'Daily Job Updates')
    
    @classmethod
    def validate(cls, email_required=True):
        """Validate configuration.
        
        Args:
            email_required (bool): Whether to enforce email-related config presence.
        """
        required = {
            'GOOGLE_SHEET_URL': cls.GOOGLE_SHEET_URL,
        }
        
        if email_required:
            required.update({
                'SENDGRID_API_KEY': cls.SENDGRID_API_KEY,
                'SENDER_EMAIL': cls.SENDER_EMAIL,
                'RECIPIENT_EMAIL': cls.RECIPIENT_EMAIL, # List is truthy if not empty
            })
        
        missing = [key for key, value in required.items() if not value]
        
        if missing:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing)}\n"
                "Please check your .env file or environment variables."
            )
        
        return True
