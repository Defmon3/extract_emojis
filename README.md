# Emoji Extractor

This project extracts all emojis from a Discord server and downloads them to a local folder. The extracted emoji information is also saved in a JSON file.

## Features
- Extract all emojis from a specified Discord server.
- Save emoji metadata (name and URL) in a `emojis.json` file.
- Download emoji images locally to an `emojis` folder.
- Logs actions using `loguru` for better debugging.

## Requirements
- Python 3.12 or higher
- A Discord bot token with appropriate permissions
- `loguru`, `httpx`, `discord.py`, and `python-dotenv` installed

## Installation
1. Clone this repository or copy the script.
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Setup
1. Create a `.env` file in the project directory with the following content:
   ```env
   DISCORD_TOKEN=your_discord_bot_token
   SERVER_ID=your_server_id
   ```
   Replace `your_discord_bot_token` with your bot token and `your_server_id` with the server's ID.

2. Ensure your bot has the `Manage Emojis` permission in the server.

## Usage
1. Run the script:
   ```bash
   python extract.py
   ```
2. The script will:
   - Fetch all emojis from the server.
   - Save emoji metadata in `emojis.json`.
   - Download emoji images to an `emojis` folder.

## Output
- A JSON file `emojis.json` containing emoji metadata:
  ```json
  [
    {
      "name": "example_emoji",
      "url": "https://cdn.discordapp.com/emojis/example.png"
    }
  ]
  ```
- Downloaded emoji images in the `emojis` folder.

## Notes
- The bot token and server ID must be set in the `.env` file.
- Animated emojis will be downloaded with the `.png` extension. If needed, you can modify the script to handle `.gif` extensions for animated emojis.

## Troubleshooting
- If the script cannot find the server, ensure the server ID and bot permissions are correct.
- Check the logs for detailed debugging information.

## Dependencies
- `discord.py`
- `httpx`
- `loguru`
- `python-dotenv`

Install them using:
```bash
pip install discord.py httpx loguru python-dotenv
```

