"""Email sender module using SendGrid API."""
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class EmailSender:
    """Handles sending formatted emails via SendGrid."""
    
    def __init__(self, sendgrid_api_key, sender_email):
        """Initialize email sender with SendGrid configuration."""
        self.api_key = sendgrid_api_key
        self.sender_email = sender_email
        self.client = SendGridAPIClient(self.api_key)
    
    def format_data_as_html(self, data):
        """Format job data as HTML table."""
        if not data:
            return "<p>No job data available for today.</p>"
        
        all_keys = set()
        for row in data:
            all_keys.update(row.keys())
        headers = sorted(all_keys)
        
        today = datetime.now().strftime('%B %d, %Y')
        
        html = f"""
<html>
<body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
<div style="background-color: white; border-radius: 8px; padding: 30px; max-width: 900px; margin: 0 auto;">
<h2 style="color: #1a73e8;">📋 Daily Job Updates</h2>
<div style="background-color: #e8f0fe; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
<strong>Date:</strong> {today}<br>
<strong>Total Jobs:</strong> {len(data)}
</div>
<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr>
"""
        
        for header in headers:
            html += f'<th style="background-color: #1a73e8; color: white; padding: 12px; text-align: left;">{header}</th>'
        
        html += "</tr></thead><tbody>"
        
        for i, row in enumerate(data):
            bg = "#f8f9fa" if i % 2 == 0 else "white"
            html += f'<tr style="background-color: {bg};">'
            for header in headers:
                value = row.get(header, '')
                if header.lower() == 'links' and value.startswith('http'):
                    html += f'<td style="border: 1px solid #ddd; padding: 12px;"><a href="{value}" style="color: #1a73e8;">View Job</a></td>'
                else:
                    html += f'<td style="border: 1px solid #ddd; padding: 12px;">{value}</td>'
            html += "</tr>"
        
        html += """
</tbody>
</table>
<div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px; text-align: center;">
Automated daily job updates via Sheet Notifier
</div>
</div>
</body>
</html>
"""
        return html
    
    def send_email(self, recipient_email, subject, data):
        """Send email with job data using SendGrid."""
        html_content = self.format_data_as_html(data)
        
        text_content = f"Daily Job Updates - {datetime.now().strftime('%B %d, %Y')}\n\n"
        text_content += f"Total Jobs: {len(data)}\n\n"
        
        if data:
            for i, row in enumerate(data, 1):
                text_content += f"Job {i}:\n"
                for key, value in row.items():
                    text_content += f"  {key}: {value}\n"
                text_content += "\n"
        
        message = Mail(
            from_email=self.sender_email,
            to_emails=recipient_email,
            subject=subject,
            html_content=html_content
        )
        message.add_content(text_content, "text/plain")
        
        try:
            response = self.client.send(message)
            if response.status_code >= 200 and response.status_code < 300:
                return True
            else:
                raise Exception(f"SendGrid returned status code: {response.status_code}")
        except Exception as e:
            raise Exception(f"Failed to send email via SendGrid: {str(e)}")
