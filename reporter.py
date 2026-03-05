"""
Core reporting functionality for WhatsApp accounts
"""

import time
import logging
from typing import Optional
from utils import validate_phone_number, log_report

logger = logging.getLogger(__name__)


class Reporter:
    """Handles automated WhatsApp account reporting."""
    
    VALID_REASONS = ['spam', 'abuse', 'harassment', 'scam', 'other']
    
    def __init__(self):
        """Initialize the Reporter."""
        self.reports_count = 0
        self.failed_count = 0
    
    def report_account(self, phone: str, reason: str, description: Optional[str] = None, 
                      delay: int = 0) -> bool:
        """
        Report a WhatsApp account.
        
        Args:
            phone: Phone number to report
            reason: Reason for reporting
            description: Optional additional description
            delay: Delay in seconds before processing
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate inputs
            if not validate_phone_number(phone):
                logger.warning(f'Invalid phone number: {phone}')
                return False
            
            if reason not in self.VALID_REASONS:
                logger.warning(f'Invalid reason: {reason}')
                return False
            
            # Apply delay if specified
            if delay > 0:
                time.sleep(delay)
            
            # Process report
            logger.info(f'Processing report: phone={phone}, reason={reason}')
            
            # Simulate report processing (would integrate with actual API/service)
            report_data = {
                'phone': phone,
                'reason': reason,
                'description': description or 'No description provided',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Log the report
            log_report(report_data)
            
            self.reports_count += 1
            logger.info(f'Report processed successfully: {phone}')
            return True
            
        except Exception as e:
            logger.error(f'Error reporting account {phone}: {str(e)}')
            self.failed_count += 1
            return False
    
    def get_stats(self) -> dict:
        """
        Get reporting statistics.
        
        Returns:
            dict: Statistics about reports processed
        """
        return {
            'total_reports': self.reports_count,
            'failed_reports': self.failed_count,
            'successful_reports': self.reports_count - self.failed_count
        }