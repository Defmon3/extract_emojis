"""
A Discord bot that extracts emojis from a server, saves them to a JSON file, and downloads the images locally.

Dependencies:
    pip install discord.py httpx loguru python-dotenv

Author: https://github.com/Defmon3
"""

import json
import os
from pathlib import Path

import discord
import httpx
from dotenv import load_dotenv
from loguru import logger as log

load_dotenv()


class EmojiExtractor(discord.Client):
    @staticmethod
    async def download_emoji(url: str, path: Path, client: httpx.AsyncClient) -> None:
        """
        Downloads an emoji from a URL and saves it to the specified path.

        :param url: The URL of the emoji to download.
        :param path: The file path where the emoji will be saved.
        :param client: An instance of httpx.AsyncClient for making the request.
        """
        try:
            response = await client.get(url)
            if response.status_code == 200:
                with open(path, "wb") as file:
                    file.write(response.content)
                    log.info(f"Downloaded {path}")
        except Exception as e:
            log.error(f"httpx error: {e}")

    @staticmethod
    async def get_emojis_from_server(guild: discord.Guild) -> list[dict[str, str]]:
        """
        Retrieves all emojis from a Discord server (guild).

        :param guild: The Discord guild object to fetch emojis from.
        :return: A list of dictionaries containing emoji names and URLs.
        """
        emojis = guild.emojis
        log.info(f"Found {len(emojis)} emojis.")
        return [{"name": emoji.name, "url": str(emoji.url)} for emoji in emojis]

    @staticmethod
    async def write_emoji_file_list(emojis: list[dict[str, str]], file_path: str) -> None:
        """
        Writes the list of emojis to a JSON file.

        :param emojis: A list of dictionaries containing emoji data (name and URL).
        :param file_path: The path where the JSON file will be saved.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(emojis, f, ensure_ascii=False, indent=2)

    async def on_ready(self) -> None:
        """
        Called when the Discord client is ready. Extracts emojis from the specified server,
        saves them to a JSON file, and downloads the images locally.
        """
        server_id = os.environ.get("SERVER_ID", "")

        guild = self.get_guild(int(server_id))

        data_path: Path = Path("data")
        data_path.mkdir(exist_ok=True)

        download_path: Path = data_path / "emojis"
        download_path.mkdir(exist_ok=True)

        emojis: list[dict] = await self.get_emojis_from_server(guild)

        await self.write_emoji_file_list(emojis, str(data_path / "emojis.json"))

        async with httpx.AsyncClient() as client:
            for emoji in emojis:
                await self.download_emoji(emoji["url"], (download_path / f"{emoji['name']}.png"), client)
                log.info("Downloaded", emoji["name"])

        await self.close()


def dot_env_exists() -> bool:
    """
    Checks if the .env file exists in the current directory.

    :return: True if the .env file exists, False otherwise.
    """
    env_path = Path(".env")
    if not env_path.exists():
        env_path.write_text('''DISCORD_TOKEN = ""  \nSERVER_ID = ''')
        return False
    return True


def main() -> None:
    """
    Initializes the EmojiExtractor bot and starts the client.
    """
    if not dot_env_exists():
        raise SystemExit("Please fill in the .env file with your Discord token and server ID.")

    intents = discord.Intents.default()
    intents.guilds = True

    client = EmojiExtractor(intents=intents)
    client.run(os.environ.get("DISCORD_TOKEN", ""))


if __name__ == "__main__":
    main()
