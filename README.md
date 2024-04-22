```markdown
# Telegram Bot with Google Sheets API Integration

## Project Description
This project is a Telegram bot that creates questions and alternatives in Telegram. When you respond and send data, it automatically feeds a Google Sheets API spreadsheet.

## Features
The bot has several features:
- It interacts with users through Telegram, asking questions and providing alternatives for responses.
- It integrates with Google Sheets API to store the responses from users.
- It provides different functionalities based on the commands given.

## Installation and Setup
To install and setup the bot, follow these steps:
1. Clone the repository.
2. Install the required Python packages using pip:
    ```
    pip3 install -r requirements.txt
    ```
3. You need to have a token from the Google Sheets API. To get this, follow the instructions provided by Google Sheets API documentation.
4. Generate a Telegram bot token. You can do this by creating a new bot on Telegram. Once you've created the bot, Telegram will give you a token. Replace this token in the `main()` function in `app_telegram.py`.
5. Run the bot using Python.

## Usage
After setting up the bot, you can interact with it through Telegram. The bot will ask you questions and provide alternatives for responses. Your responses will be stored in a Google Sheets spreadsheet. To start the bot, you can use the `/start` command in Telegram.

## Code
The code for this bot is divided into two main parts:
- `google_sheets_api.py`: This file contains the code for interacting with Google Sheets API. It includes functions for inserting incomes, outcomes, and transfers, as well as displaying reports.
- `app_telegram.py`: This file contains the code for the Telegram bot. It handles different commands and interacts with the Google Sheets API.

## License
This project is not currently under any license.

## Author
👤 Joao Melo
- Github: @johnmelodev
- LinkedIn: @joao-melo-dev

## Show your support
Give a ⭐️ if this project helped you!
```