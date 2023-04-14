from typing import List

from backend.services.bot.tg_models import Update


class BotCommand:
    def __init__(self, supported_commands: List[str]):
        self._commands = supported_commands

    def parse_command(self, update: Update) -> str | None:
        if message := update.message:
            if entities := message.entities:
                entity = entities[-1]
                if entity.type == "bot_command":
                    offset = entity.offset
                    command = message.text[offset:offset + entity.length]
                    if command in self._commands:
                        return command
        return None
