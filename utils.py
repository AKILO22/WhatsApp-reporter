"""
Utility functions for WhatsApp Reporter
"""

import re
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format.
    
    Args:
        phone: Phone number string
    
    Returns:
        bool: True if valid, False otherwise
    """
    # Remove common formatting characters
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    
    # Check if it's all digits and reasonable length (7-15 digits)
    if re.match(r'^\d{7,15}$', cleaned):
        return True
    
    logger.warning(f'Invalid phone number format: {phone}')
    return False


def log_report(report_data: dict) -> bool:
    """
    Log a report to the reports file.
    
    Args:
        report_data: Dictionary containing report information
    
    Returns:
        bool: True if successful
    """
    try:
        log_dir = Path.home() / '.whatsapp_reporter' / 'reports'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = log_dir / 'reports.log'
        
        with open(report_file, 'a') as f:
            f.write(f"[{report_data['timestamp']}] Phone: {report_data['phone']}, "
                   f"Reason: {report_data['reason']}, "
                   f"Description: {report_data['description']}\n")
        
        logger.debug(f'Report logged: {report_data}')
        return True
    
    except Exception as e:
        logger.error(f'Error logging report: {str(e)}')
        return False


def read_numbers_from_file(file_path: str) -> list:
    """
    Read phone numbers from a file.
    
    Args:
        file_path: Path to file containing phone numbers
    
    Returns:
        list: List of phone numbers
    """
    try:
        path = Path(file_path)
        if not path.exists():
            logger.error(f'File not found: {file_path}')
            return []
        
        numbers = []
        with open(path, 'r') as f:
            for line in f:
                number = line.strip()
                if number and validate_phone_number(number):
                    numbers.append(number)
        
        logger.info(f'Read {len(numbers)} valid phone numbers from {file_path}')
        return numbers
    
    except Exception as e:
        logger.error(f'Error reading file: {str(e)}')
        return []


def format_phone_number(phone: str) -> str:
    """
    Format phone number to standard format.
    
    Args:
        phone: Phone number string
    
    Returns:
        str: Formatted phone number
    """
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    return cleaned


def get_timestamp() -> str:
    """
    Get current timestamp.
    
    Returns:
        str: Formatted timestamp
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')