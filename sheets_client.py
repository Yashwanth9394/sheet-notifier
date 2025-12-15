"""Google Sheets client for fetching public sheet data."""
import re
import csv
from datetime import datetime, timedelta
from io import StringIO
import requests
from urllib.parse import quote

class SheetsClient:
    """Client for fetching data from public Google Sheets."""
    
    def __init__(self, sheet_url):
        """Initialize with Google Sheets URL."""
        self.sheet_url = sheet_url
        self.sheet_id = self._extract_sheet_id(sheet_url)
    
    def _extract_sheet_id(self, url):
        """Extract sheet ID from Google Sheets URL."""
        match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
        if not match:
            raise ValueError(f"Invalid Google Sheets URL: {url}")
        return match.group(1)
    
    def _get_today_sheet_name(self):
        """Get today's date formatted as sheet name (e.g., 'December 5').
        If today is a weekend, returns the last Friday's date."""
        today = datetime.now()
        weekday = today.weekday()  # Monday=0, Sunday=6
        
        # On weekends (Saturday=5, Sunday=6), fetch Friday's data
        if weekday >= 5:
            # Saturday: 1 day back, Sunday: 2 days back
            days_back = weekday - 4  # Friday is weekday 4
            last_friday = today - timedelta(days=days_back)
            return last_friday.strftime('%B %-d')
        
        # Monday-Friday: use current day
        return today.strftime('%B %-d')
    
    def fetch_today_data(self):
        """Fetch data from today's sheet."""
        sheet_name = self._get_today_sheet_name()
        return self.fetch_sheet_by_name(sheet_name)
    
    def fetch_sheet_by_name(self, sheet_name):
        """Fetch data from a specific sheet by name."""
        # Use Google Sheets gviz API which supports sheet name parameter
        url = f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/gviz/tq?tqx=out:csv&sheet={quote(sheet_name)}"
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse CSV data
            csv_data = StringIO(response.text)
            reader = csv.reader(csv_data)
            rows = list(reader)
            
            if not rows or len(rows) < 2:
                return []
            
            # Skip first row (merged header "Software Engineering/Developer")
            # Second row contains actual headers: Date, Company, Links
            headers = rows[1]
            data = []
            
            # Start from row 3 (index 2) for actual data
            for row in rows[2:]:
                if row and any(cell.strip() for cell in row):  # Skip empty rows
                    row_dict = {}
                    for i, header in enumerate(headers):
                        if header.strip():  # Only include non-empty headers
                            row_dict[header] = row[i] if i < len(row) else ''
                    if row_dict:  # Only add if we have data
                        data.append(row_dict)
            
            return data
            
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch sheet '{sheet_name}': {str(e)}")
