import asyncio
import datetime
import typing

from backend.entities.game import GameState
from backend.services.bot.game.accessor import GameAccessor
from backend.services.bot.tg_models import Chat, Update
from backend.services.database import (
    Game as GameModel,
    Player as PlayerModel,
    User as UserModel,
    Question as QuestionModel
)

if typing.TYPE_CHECKING:
    from backend.services.bot.bot import Bot


class GameHandler:
    def __init__(self, bot: "Bot"):
        self._bot = bot
        self._accessor = GameAccessor(bot)

    async def run_command(self, command: str, update: Update):
        if command == "/game":
            task = asyncio.create_task(self.run_game(update))
        if command.startswith("/join"):
            task = asyncio.create_task(self.add_player_to_game(update))
        elif command == "/stat":
            task = asyncio.create_task(self.show_stats(update))
        elif command == "/stop":
            task = asyncio.create_task(self.stop_game(update))

    async def create_new_game(self, chat: Chat):
        question: QuestionModel = await self._accessor.get_random_question(
            await self._accessor.find_question_ids()
        )
        game = GameModel(
            chat_id=chat.id,
            game_state=GameState.creating.value,
            created_at=datetime.datetime.now(),
            question_id=question.id
        )
        game = await self._accessor.save_game(game=game)
        await self._bot.send_message(
            chat_id=chat.id,
            text=f"Начинается новая игра 100 к 1."
                 f"\nОжидаем игроков в течение 20 секунд"
                 f"\nЖми /join чтобы присоединиться"
        )
        await asyncio.sleep(10)
        return game

    async def run_game(self, update: Update):
        if await self._accessor.find_active_chat_game(update.message.chat.id):
            return
        new_game = await self.create_new_game(update.message.chat)
        await self._accessor.update_game_state(new_game.id, GameState.running)
        try:
            new_game = await self._accessor.find_running_game_by_chat_id(new_game.chat_id)
            await self._bot.send_message(
                chat_id=new_game.chat_id,
                text=new_game.question.title,
            )
        finally:
            await self.stop_game(update)

    async def add_player_to_game(self, update: Update):
        user: UserModel = await self._accessor.find_user_by_id(update.message.from_.id)
        if user is None:
            user = await self._accessor.add_user(
                UserModel(
                    id=update.message.from_.id,
                    is_bot=update.message.from_.is_bot,
                    first_name=update.message.from_.first_name,
                    username=update.message.from_.username
                )
            )
        game: GameModel = await self._accessor.find_creating_game_by_chat_id(update.message.chat.id)
        if game is not None:
            player = PlayerModel(
                user_id=user.id,
                game_id=game.id
            )
            player = await self._accessor.add_player(player)

    async def show_stats(self, update: Update):
        game = await self._accessor.find_running_game_by_chat_id(update.message.chat.id)
        # print(game)

    async def stop_game(self, update: Update):
        game: GameModel = await self._accessor.find_running_game_by_chat_id(update.message.chat.id)
        if game is not None:
            await self._accessor.update_game_state(game_id=game.id, new_state=GameState.finished)
