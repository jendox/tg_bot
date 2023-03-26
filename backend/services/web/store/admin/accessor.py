import typing
from hashlib import sha256

from sqlalchemy import select

from backend.entities.admin import Admin as AdminEntity
from backend.services.database.models.admin import Admin
from backend.services.web.store.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from backend.services.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application"):
        if not await self.get_by_email(email=app.config.admin.email):
            await self.create_admin(
                email=app.config.admin.email,
                password=app.config.admin.password
            )

    async def get_by_email(self, email: str) -> AdminEntity | None:
        admin = None
        async with self.app.database.session() as session:
            stmt = select(Admin).filter_by(email=email)
            result = await session.execute(stmt)
            if result.raw.rowcount == 1:
                admin = result.scalars().one()
        return admin

    async def create_admin(self, email: str, password: str) -> AdminEntity:
        admin = Admin(
            email=email,
            password=sha256(password.encode()).hexdigest()
        )
        async with self.app.database.session() as session:
            async with session.begin():
                session.add(admin)
