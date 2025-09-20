# 2FA Password Manager - Perfect Version

## Project Overview

This is a password manager program with two-factor authentication (2FA). Users can pair their mobile 2FA applications by scanning a QR code, and then securely store and manage account passwords.

## Features

1. **2FA Device Pairing**:
   - Generate QR codes for mobile app scanning
   - Complete pairing by entering the verification code displayed on the phone
   - If there are passwords in the password library, re-pairing 2FA requires verifying the current 2FA code

2. **Password Management**:
   - Add, edit, and delete password records
   - All passwords are encrypted using AES encryption algorithm
   - Local SQLite database storage

3. **Security Verification**:
   - 2FA verification required for editing and viewing passwords
   - Double-click username to view complete password information (requires 2FA verification)
   - 10-second verification cache mechanism (no need to verify again within 10 seconds)
   - Adding passwords does not require 2FA verification

4. **Data Management**:
   - Clear all data function - click to clear all data and unbind 2FA
   - Password deletion does not require 2FA verification
   - Data clearing only requires user confirmation, no 2FA code verification required

5. **User Interface**:
   - Intuitive graphical interface based on PyQt5
   - Table format to display password list
   - Various operation buttons for convenience
   - **Multi-language support (English/Chinese)** - default language is English, language can be switched in the top-right corner of the main page (EN/CN)
   - First-time use prompt defaults to English

6. **Enhanced Features**:
   - When the password box is empty, prompt to bind 2FA device first in the password list, otherwise passwords are not accessible
   - When double-clicking to view passwords, initially display as ······, with a copy button on the right to copy the real password, and a show password button that replaces ······ with the real password when clicked

7. **Import Function**:
   - Support importing CSV files (such as password libraries exported from Google Chrome)
   - One-click batch password addition
   - Prompt users to confirm 2FA device binding before importing

## Program Structure

- `main.py` - Program entry point
- `init.py` - Initialization script, can automatically install dependencies
- `core/` - Core functionality modules
  - `auth.py` - 2FA authentication functionality
  - `encryption.py` - Data encryption and decryption
  - `database.py` - Database storage management
  - `language.py` - Multi-language support
- `ui/` - User interface modules
  - `main_window.py` - Main window interface
  - `auth_dialog.py` - Authentication dialog
  - `password_dialog.py` - Password management dialog
  - `qr_dialog.py` - QR code display dialog
  - `totp_dialog.py` - TOTP verification dialog
  - `password_detail_dialog.py` - Password details dialog
- `config/` - Configuration files
  - `settings.py` - Program configuration

## Security Features

1. All passwords are encrypted using AES encryption algorithm
2. 2FA keys are securely stored
3. Encryption keys are automatically generated and securely saved
4. Sensitive operations require 2FA verification
5. Data is stored locally, not uploaded to any server
6. 10-second verification cache mechanism to avoid frequent verification

## Usage Instructions

1. Run `python main.py` to start the program
2. Click "Show QR Code" to pair 2FA device
3. Enter the verification code displayed on your phone to complete pairing
4. Start adding and managing passwords
5. 2FA verification is required when double-clicking usernames or using edit functions
6. Use the "Reset Data" button to reset all data
7. Use the "Import CSV" button to batch import passwords
8. Switch language in the top-right corner of the main page (EN/CN)

## Installation Dependencies

```bash
pip install pyotp qrcode[pil] cryptography PyQt5 pyperclip
```

Or run the initialization script:

```bash
python init.py
```

## User Feedback Implementation

Based on user feedback, we have implemented the following improvements:

1. **2FA Binding Security Mechanism**:
   - If there are passwords in the password library, re-pairing 2FA requires verifying the current 2FA code
   - This prevents unauthorized devices from re-pairing

2. **Operation Verification Optimization**:
   - Adding passwords does not require 2FA verification
   - Deleting passwords does not require 2FA verification
   - Data clearing only requires user confirmation, no 2FA code verification required

3. **Delete Bug Fix**:
   - Password deletion function works properly
   - Data clearing function works properly, including correct database table recreation

4. **Enhanced User Experience**:
   - When the password box is empty, prompt to bind 2FA device first in the password list, otherwise passwords are not accessible
   - When double-clicking to view passwords, initially display as ······, with a copy button on the right to copy the real password, and a show password button that replaces ······ with the real password when clicked

5. **New Import Function**:
   - Support importing CSV files (such as password libraries exported from Google Chrome)
   - One-click batch password addition
   - Prompt users to confirm 2FA device binding before importing

6. **New Multi-language Support**:
   - Program default language is English, language can be switched in the top-right corner of the main page (EN/CN)
   - Support for English and Chinese languages
   - First-time use prompt defaults to English

## Testing and Verification

All functions have been tested and verified:
- 2FA pairing and verification functions work properly
- Password add, edit, and delete functions work properly
- Data encryption storage function works properly
- Data clearing function works properly, including correct database table recreation
- User interface interaction works properly
- QR code display logic is correct (must verify current 2FA code to re-pair when password library has passwords)
- Enhanced functions work properly
- CSV import function works properly
- Multi-language switching function works properly
- First-time use prompt defaults to English

## Final Implementation Notes

In the final implementation, we have implemented the following logic according to your specific requirements:
1. If there are passwords in the password library, re-pairing 2FA requires verifying the current 2FA code
2. This effectively prevents unauthorized devices from re-pairing, enhancing security
3. After clearing data, re-pairing can be done without verification (because the password library is empty)
4. Added password details dialog for better user experience
5. Added CSV import function to support one-click batch password addition
6. Added multi-language support, default language is English, language can be switched in the top-right corner of the main page (EN/CN)
7. First-time use prompt defaults to English

The program now works exactly as requested, and all functions have been thoroughly tested.
