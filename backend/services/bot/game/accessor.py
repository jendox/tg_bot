import random
import typing
from typing import List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import immediateload, joinedload

from backend.entities import ChatId, GameId, GameState, UserId, QuestionId
from backend.services.database import Game, User, Player, Question
from backend.services.database.models.answer import Answer

if typing.TYPE_CHECKING:
    from backend.services.bot.bot import Bot

from logging import getLogger

logger = getLogger()


class GameAccessor:
    def __init__(self, bot: "Bot"):
        self._bot = bot

    async def find_user_by_id(self, user_id: UserId) -> User | None:
        user = None
        async with self._bot.database.session() as session:
            try:
                stmt = select(User).where(User.id == user_id)
                result = await session.execute(stmt)
                if result.raw.rowcount:
                    user = result.scalars().one()
            except Exception as e:
                logger.error(f"An error occurred when finding user: {e}")
            finally:
                return user

    async def add_user(self, user: User) -> User | None:
        async with self._bot.database.session() as session:
            try:
                session.add(user)
                await session.commit()
            except Exception as e:
                logger.error(f"An error occurred when adding user: {e}")
                return None
            return user

    async def add_player(self, player: Player):
        async with self._bot.database.session() as session:
            try:
                session.add(player)
                await session.commit()
            except Exception as e:
                logger.error(f"An error occurred when adding player: {e}")
                return None
            return player

    async def save_game(self, game: Game):
        async with self._bot.database.session() as session:
            try:
                session.add(game)
                await session.commit()
            except Exception as e:
                logger.error(f"An error occurred when saving game: {e}")
                return None
            return game

    async def find_active_chat_game(self, chat_id: ChatId) -> bool:
        async with self._bot.database.session() as session:
            stmt = select(Game.game_state).where(Game.chat_id == chat_id).order_by().limit(1)
            result = await session.execute(stmt)
            if result.raw.rowcount:
                result = result.scalars().one()
                if result in [GameState.creating.value, GameState.running.value]:
                    return True
            return False

    async def find_creating_game_by_chat_id(self, chat_id: ChatId) -> Game | None:
        async with self._bot.database.session() as session:
            stmt = select(Game).where(Game.chat_id == chat_id).where(Game.game_state == GameState.creating.value)
            result = await session.execute(stmt)
            if result.raw.rowcount:
                return result.scalars().one()
            return None

    async def find_running_game_by_chat_id(self, chat_id: ChatId) -> Game | None:
        async with self._bot.database.session() as session:
            stmt = select(Game)\
                .where(Game.chat_id == chat_id)\
                .where(Game.game_state == GameState.running.value)\
                .options(immediateload(Game.question))
            result = await session.execute(stmt)
            if result.raw.rowcount:
                return result.scalars().one()
            return None

    async def find_last_game_by_chat_id(self, chat_id: ChatId):
        async with self._bot.database.session() as session:
            stmt = select(Game).where(Game.chat_id == chat_id). \
                order_by().limit(1).options(immediateload(Game.players))
            result = await session.execute(stmt)
            if result.raw.rowcount:
                return result.scalars().one()
            return None

    async def update_game_state(self, game_id: GameId, new_state: GameState):
        async with self._bot.database.session() as session:
            try:
                stmt = update(Game).where(Game.id == game_id).values(game_state=new_state.value)
                await session.execute(stmt)
                await session.commit()
            except Exception as e:
                logger.error(f"An error occurred when updating game state: {e}")
                return False
            return True

    async def find_question_ids(self) -> List[int]:
        async with self._bot.database.session() as session:
            result = await session.execute(select(Question.id))
            if result.raw.rowcount > 0:
                return result.scalars().all()
            return []

    async def get_random_question(self, ids: List[QuestionId]) -> Question:
        async with self._bot.database.session() as session:
            question_id = ids[random.randint(0, len(ids) - 1)]
            stmt = select(Question).where(Question.id == question_id).options(immediateload(Question.answers))
            result = await session.execute(stmt)
            return result.scalars().one()
