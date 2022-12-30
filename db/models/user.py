import datetime

from sqlalchemy import Column, String, Date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from sqlalchemy.future import select

from db import Base

class User(Base):
    __tablename__ = "user"

    user_telegram_id = Column(String, primary_key=True)
    username = Column(String)

    reg_date = Column(Date, default=datetime.date.today())
    upd_date = Column(Date, default=datetime.date.today())

    schedule = relationship("Schedule", backref="user")

    @staticmethod
    async def get_user(user_telegram_id: int, session: AsyncSession):
        user_telegram_id = str(user_telegram_id)
        user_result = await session.execute(select(User).where(User.user_telegram_id == user_telegram_id))
        return user_result.scalars().first()

    @staticmethod
    async def create_user(user_telegram_id: str, username: str, session: AsyncSession):
        user_telegram_id = str(user_telegram_id)
        user_result = await session.execute(select(User).where(User.user_telegram_id == user_telegram_id))
        if user_result.scalars().first() is None:
            user_result = User(user_telegram_id=user_telegram_id, username=username)
            try:
                session.add(user_result)
                await session.commit()
                print("\n\nВсе отработало!\n\n")
            except:
                await session.rollback()
            finally:
                await session.close()
        return user_result
