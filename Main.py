#!/usr/bin/env python3
"""
WhatsApp Reporter - Automated Reporting Tool for Termux
Main CLI entry point with argument parsing
"""

import argparse
import sys
import logging
from pathlib import Path
from reporter import Reporter
from config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('whatsapp_reporter.log')
    ]
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(
        description='WhatsApp Reporter - Automated Reporting Tool for Termux',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s report --phone 1234567890 --reason spam
  %(prog)s batch --file accounts.txt --reason abuse
  %(prog)s config --set phone 1234567890
  %(prog)s config --get phone
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Report a WhatsApp account')
    report_parser.add_argument('--phone', required=True, help='Phone number to report')
    report_parser.add_argument('--reason', required=True, 
                             choices=['spam', 'abuse', 'harassment', 'scam', 'other'],
                             help='Reason for reporting')
    report_parser.add_argument('--description', help='Additional description')
    
    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Report multiple accounts from file')
    batch_parser.add_argument('--file', required=True, help='File with phone numbers (one per line)')
    batch_parser.add_argument('--reason', required=True,
                            choices=['spam', 'abuse', 'harassment', 'scam', 'other'],
                            help='Reason for reporting')
    batch_parser.add_argument('--delay', type=int, default=2, help='Delay between reports in seconds')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Manage configuration')
    config_parser.add_argument('--set', nargs=2, metavar=('KEY', 'VALUE'), help='Set configuration value')
    config_parser.add_argument('--get', metavar='KEY', help='Get configuration value')
    config_parser.add_argument('--list', action='store_true', help='List all configurations')
    config_parser.add_argument('--reset', action='store_true', help='Reset to default configuration')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show reporting status')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'report':
            handle_report(args)
        elif args.command == 'batch':
            handle_batch(args)
        elif args.command == 'config':
            handle_config(args)
        elif args.command == 'status':
            handle_status()
        else:
            parser.print_help()
            sys.exit(0)
            
    except KeyboardInterrupt:
        logger.info('Operation cancelled by user')
        sys.exit(0)
    except Exception as e:
        logger.error(f'An error occurred: {str(e)}')
        sys.exit(1)


def handle_report(args):
    """Handle single report command."""
    logger.info(f'Processing report for phone: {args.phone}')
    
    reporter = Reporter()
    success = reporter.report_account(
        phone=args.phone,
        reason=args.reason,
        description=getattr(args, 'description', None)
    )
    
    if success:
        logger.info(f'Successfully reported account: {args.phone}')
        print(f'✓ Successfully reported {args.phone} for {args.reason}')
    else:
        logger.error(f'Failed to report account: {args.phone}')
        print(f'✗ Failed to report {args.phone}')
        sys.exit(1)


def handle_batch(args):
    """Handle batch reporting command."""
    file_path = Path(args.file)
    
    if not file_path.exists():
        logger.error(f'File not found: {args.file}')
        print(f'Error: File not found - {args.file}')
        sys.exit(1)
    
    # Read phone numbers from file
    try:
        with open(file_path, 'r') as f:
            phone_numbers = [line.strip() for line in f if line.strip()]
    except IOError as e:
        logger.error(f'Error reading file: {str(e)}')
        print(f'Error reading file: {str(e)}')
        sys.exit(1)
    
    if not phone_numbers:
        logger.warning('No phone numbers found in file')
        print('No phone numbers found in file')
        sys.exit(1)
    
    logger.info(f'Starting batch reporting for {len(phone_numbers)} accounts')
    print(f'\nProcessing {len(phone_numbers)} accounts with {args.delay}s delay between reports...\n')
    
    reporter = Reporter()
    successful = 0
    failed = 0
    
    for i, phone in enumerate(phone_numbers, 1):
        print(f'[{i}/{len(phone_numbers)}] Reporting {phone}...', end=' ')
        
        success = reporter.report_account(
            phone=phone,
            reason=args.reason,
            delay=args.delay
        )
        
        if success:
            print('✓')
            successful += 1
        else:
            print('✗')
            failed += 1
    
    # Summary
    print(f'\n--- Batch Report Summary ---')
    print(f'Total: {len(phone_numbers)}')
    print(f'Successful: {successful}')
    print(f'Failed: {failed}')
    logger.info(f'Batch reporting completed: {successful} successful, {failed} failed')


def handle_config(args):
    """Handle configuration command."""
    config = Config()
    
    if args.set:
        key, value = args.set
        config.set_value(key, value)
        logger.info(f'Configuration updated: {key}={value}')
        print(f'✓ Configuration updated: {key}={value}')
    
    elif args.get:
        value = config.get_value(args.get)
        if value is not None:
            print(f'{args.get}={value}')
        else:
            print(f'Configuration not found: {args.get}')
    
    elif args.list:
        print('\n--- Current Configuration ---')
        for key, value in config.get_all().items():
            print(f'{key}: {value}')
    
    elif args.reset:
        config.reset_to_defaults()
        logger.info('Configuration reset to defaults')
        print('✓ Configuration reset to defaults')
    
    else:
        print('Use --set, --get, --list, or --reset with config command')


def handle_status():
    """Handle status command."""
    logger.info('Checking application status')
    print('\n--- WhatsApp Reporter Status ---')
    print('✓ Application is running')
    print('✓ Configuration loaded')
    print('✓ Ready for reporting')
    print()


if __name__ == '__main__':
    main()
