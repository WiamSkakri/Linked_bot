# LinkedIn Connection Bot Documentation

This documentation covers two implementations of a LinkedIn Connection Bot:
1. Command Line Interface (CLI) version - `linked_bot.py`
2. Graphical User Interface (GUI) version - `bot_gui.py`

Both implementations allow you to automatically send personalized connection requests on LinkedIn after meeting someone at an event.

## Table of Contents
- [Prerequisites](#prerequisites)
- [CLI Version (`linked_bot.py`)](#cli-version-linked_botpy)
  - [Usage](#usage)
  - [Command Line Arguments](#command-line-arguments)
  - [Example](#example)
- [GUI Version (`bot_gui.py`)](#gui-version-bot_guipy)
  - [Installation](#installation)
  - [Running the GUI](#running-the-gui)
  - [Using the Interface](#using-the-interface)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before using either version of the bot, ensure you have the following installed:
- Python 3.6 or newer
- Chrome web browser
- ChromeDriver compatible with your Chrome version
- Required Python packages:
  ```
  selenium
  tkinter (for GUI version)
  ```

You can install the required packages using pip:
```bash
pip install selenium
```
(Note: tkinter typically comes bundled with Python installations)

## CLI Version (`linked_bot.py`)

The CLI version allows you to run the bot from the command line with specific parameters.

### Usage

```bash
python linked_bot.py --email <your_linkedin_email> --password <your_linkedin_password> --name <person_name> --event <event_name>
```

### Command Line Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `--email` | Your LinkedIn login email | Yes |
| `--password` | Your LinkedIn password | Yes |
| `--name` | Full name of the person you want to connect with | Yes |
| `--event` | Name of the event where you met the person | Yes |

### Example

```bash
python linked_bot.py --email johndoe@example.com --password mypassword123 --name "Jane Smith" --event "Tech Conference 2025"
```

This will:
1. Log into LinkedIn with the provided credentials
2. Search for "Jane Smith"
3. Filter to show people results
4. Click the Connect button
5. Add a personalized note mentioning "Tech Conference 2025"
6. Send the connection request

## GUI Version (`bot_gui.py`)

The GUI version provides a user-friendly interface for the same functionality.

### Installation

No additional installation is required beyond the prerequisites mentioned above.

### Running the GUI

```bash
python bot_gui.py
```

### Using the Interface

1. **Launch the application**: Run the command above to open the GUI window.

2. **Enter your LinkedIn credentials**:
   - Email: Your LinkedIn login email
   - Password: Your LinkedIn password

3. **Enter connection details**:
   - Person Name: Full name of the person you want to connect with
   - Event Name: Name of the event where you met the person

4. **Click "Connect"**: The bot will:
   - Log into LinkedIn
   - Search for the specified person
   - Send a connection request with a personalized note

5. **Monitor progress**: The status bar at the bottom will show the current operation status.

## How It Works

Both versions use Selenium WebDriver to automate browser interactions with LinkedIn. The process includes:

1. **Authentication**: Logging into LinkedIn with provided credentials
2. **Search**: Finding the specified person using LinkedIn's search functionality
3. **Connection**: Sending a connection request with a personalized note

The bot uses several techniques to mimic human behavior:
- Random delays between keystrokes
- Natural cursor movements
- Varied timing between actions

The personalized note follows this format:
```
Hi [First Name], it was great meeting you at [Event Name]! I enjoyed our conversation and would love to stay connected.
```

## Troubleshooting

Common issues and solutions:

1. **Bot cannot find elements on the page**:
   - LinkedIn may have updated their UI elements
   - Check if the XPath selectors need to be updated
   - Ensure you're using the latest version of ChromeDriver

2. **Login fails**:
   - Verify your LinkedIn credentials
   - Check if LinkedIn is requiring CAPTCHA or 2FA (the bot cannot handle these)

3. **Search doesn't return the right person**:
   - Try using a more specific name
   - The bot selects the first person from search results

4. **GUI freezes during operation**:
   - The application uses threading to prevent freezing
   - If it still freezes, try the CLI version instead

5. **Connection button not found**:
   - Ensure the person is not already connected
   - The person's profile might have different connection settings
