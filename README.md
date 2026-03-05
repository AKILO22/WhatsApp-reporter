# WhatsApp Reporter - Termux Edition

Automated WhatsApp account reporting tool designed for Termux on Android devices.

## Features

- 🚀 **CLI-based** - Easy command-line interface
- 📱 **Termux Compatible** - Works perfectly on Android
- 🔄 **Batch Processing** - Report multiple accounts at once
- ⚙️ **Configurable** - Customize settings as needed
- 📝 **Logging** - Track all reporting activities
- 🛡️ **Safe** - Input validation and error handling

## Requirements

- Python 3.7+
- Termux app (for Android)
- No external API keys needed

## Installation

### 1. Install on Termux

```bash
# Update packages
pkg update && pkg upgrade

# Install Python
pkg install python

# Clone the repository
git clone https://github.com/AKILO22/whatsapp-reporter
cd whatsapp-reporter

# Install dependencies
pip install -r requirements.txt

# Make main script executable
chmod +x main.py
```

### 2. First Run Setup

```bash
python3 main.py config --list
```

## Usage

### Single Report

Report a single WhatsApp account:

```bash
python3 main.py report --phone 1234567890 --reason spam
python3 main.py report --phone 1234567890 --reason abuse --description "Harassment messages"
```

**Valid Reasons:**
- `spam` - Unwanted spam messages
- `abuse` - Abusive behavior
- `harassment` - Harassment
- `scam` - Scam/fraud
- `other` - Other reasons

### Batch Reporting

Report multiple accounts from a file:

```bash
# Create a file with phone numbers (one per line)
echo "1234567890
0987654321
5551234567" > numbers.txt

# Process batch report
python3 main.py batch --file numbers.txt --reason spam --delay 2
```

**Options:**
- `--file` - Path to file with phone numbers
- `--reason` - Reason for reporting
- `--delay` - Delay between reports in seconds (default: 2)

### Configuration

Manage your settings:

```bash
# View all settings
python3 main.py config --list

# Set a value
python3 main.py config --set phone 1234567890
python3 main.py config --set report_delay 3

# Get a specific value
python3 main.py config --get phone

# Reset to defaults
python3 main.py config --reset
```

### Check Status

```bash
python3 main.py status
```

## Configuration File

Configuration is stored at: `~/.whatsapp_reporter/config.json`

Default configuration:
```json
{
  "phone": "",
  "language": "en",
  "log_level": "INFO",
  "report_delay": 2,
  "batch_enabled": true,
  "auto_backup": true
}
```

## Logs

- **Application logs:** `whatsapp_reporter.log`
- **Report logs:** `~/.whatsapp_reporter/reports/reports.log`

## File Structure

```
whatsapp-reporter/
├── main.py           # CLI entry point
├── reporter.py       # Core reporting logic
├── config.py         # Configuration management
├── utils.py          # Utility functions
├── requirements.txt  # Python dependencies
├── README.md         # This file
└── .gitignore        # Git ignore file
```

## Examples

### Example 1: Single Report

```bash
python3 main.py report --phone +1234567890 --reason spam
```

Output:
```
✓ Successfully reported +1234567890 for spam
```

### Example 2: Batch Reporting

```bash
python3 main.py batch --file spammers.txt --reason abuse --delay 3
```

Output:
```
Processing 10 accounts with 3s delay between reports...

[1/10] Reporting 1234567890... ✓
[2/10] Reporting 0987654321... ✓
[3/10] Reporting 5551234567... ✓
...

--- Batch Report Summary ---
Total: 10
Successful: 10
Failed: 0
```

### Example 3: Configuration

```bash
python3 main.py config --set language es
python3 main.py config --get language
```

## Troubleshooting

### Python not found
Make sure Python is installed in Termux:
```bash
pkg install python
```

### Permission denied
Make the script executable:
```bash
chmod +x main.py
```

### File not found errors
Check that files are in the correct directory and use full/relative paths correctly.

## Notes

- Phone numbers can be in various formats (with or without country code)
- Reports are logged locally for your records
- Batch operations can take time depending on delay settings
- Always validate phone numbers before reporting

## Safety & Legal

Use this tool responsibly and only for legitimate reporting purposes. False reports may violate terms of service.

## License

MIT License - Feel free to use and modify

## Support

For issues or questions, check the application logs:
```bash
cat whatsapp_reporter.log
```

---

**Made for Termux** | **Developed by AKILO22**