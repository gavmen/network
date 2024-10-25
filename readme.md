
---

# Wi-Fi Password Attempt CLI Tool

## Overview

The Wi-Fi Password Attempt CLI Tool is a Python command-line application designed to list available Wi-Fi networks and attempt to connect to them using a specified list of passwords. The application utilizes the `psutil` library for network management and `subprocess` for executing system commands.

## Features

- **List Network Connections**: Displays the current network connections on the device.
- **List Available Wi-Fi Networks**: Shows all Wi-Fi networks within range.
- **Connect to a Wi-Fi Network**: Connects to a specified Wi-Fi network using a given password.
- **Try Multiple Passwords**: Attempts to connect to a Wi-Fi network using a list of passwords concurrently, improving speed and efficiency.

## Requirements

- Python 3.x
- `psutil` library

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/wifi-password-attempt-cli.git
   cd wifi-password-attempt-cli
   ```

2. Install the required Python packages:

   ```bash
   pip install psutil
   ```

3. Ensure you have the necessary permissions to access network configurations on your operating system.

## Usage

1. **Run the application**:

   ```bash
   python network.py
   ```

2. **Authenticate**: You'll be prompted to enter a password for accessing network details.

3. **Available Commands**:

   - List current network connections:
     ```bash
     python network.py --list
     ```

   - List available Wi-Fi networks:
     ```bash
     python network.py --wifi
     ```

   - Attempt to connect to a specified Wi-Fi network using a password:
     ```bash
     python network.py --connect "Your_SSID" "Your_Password"
     ```

   - Attempt to connect to a specified Wi-Fi network using a list of passwords:
     ```bash
     python network.py --try-passwords "Your_SSID" "passwords.txt"
     ```
     Where `passwords.txt` is a text file containing a list of passwords (one password per line).

## Important Notes

- **Ethical Use**: This tool is intended for educational purposes only. Ensure that you have permission to connect to the networks you are testing.
- **Platform Compatibility**: The application is primarily developed for Windows. Other operating systems may require additional adjustments.

## Contributing

If you would like to contribute to this project, feel free to fork the repository and submit a pull request. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [psutil](https://github.com/giampaolo/psutil) for providing an easy interface to access system and network details.
- Inspiration from various open-source network management tools.

---
