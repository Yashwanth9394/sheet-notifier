"""Monitor script to check if today's sheet exists."""
import csv
import logging
import os
from datetime import datetime
from config import Config
from sheets_client import SheetsClient

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

LOG_FILE = 'monitoring_log.csv'

def init_log_file():
    """Initialize header if file doesn't exist."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Check_Time_UTC', 'Target_Sheet', 'Status', 'Notes'])

def main():
    try:
        # Load config to get URL
        Config.validate(email_required=False)
        client = SheetsClient(Config.GOOGLE_SHEET_URL)
        
        # Get target sheet name
        target_sheet = client._get_today_sheet_name()
        
        # Current time
        now_utc = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        status = "MISSING"
        notes = ""
        
        try:
            # Try to fetch
            data = client.fetch_sheet_by_name(target_sheet)
            status = "FOUND"
            notes = f"Row count: {len(data)}"
        except Exception as e:
            if "server_error" in str(e).lower() or "not found" in str(e).lower():
                status = "MISSING"
                notes = "Sheet not present yet"
            else:
                # Some other error, maybe connection
                status = "ERROR"
                notes = str(e)[:100]  # Truncate error
        
        # Write to log
        init_log_file()
        with open(LOG_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([now_utc, target_sheet, status, notes])
            
        logger.info(f"Check complete. {target_sheet}: {status}")
        
    except Exception as e:
        logger.error(f"Critical script failure: {e}")
        exit(1)

if __name__ == '__main__':
    main()
