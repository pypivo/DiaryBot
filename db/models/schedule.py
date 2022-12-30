from typing import List

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db import Base

class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("user.user_telegram_id"))
    day_of_week = Column(String)
    name = Column(String)
    description = Column(String, nullable=True)
    time_start = Column(String)
    time_end = Column(String)

    def __init__(self, params: dict):
        self.day_of_week = params['day_of_week']
        self.name = params['name']
        self.description = params['description']
        self.time_start = params['time_start']
        self.time_end = params['time_end']
        self.user_id = params['user_id']

    @staticmethod
    async def del_schedule_by_id(schedule_id: int, session: AsyncSession):
        schedule_result = await session.execute((select(Schedule).where(Schedule.id == schedule_id)))
        await session.delete(schedule_result.scalars().first())
        await session.commit()

    @staticmethod
    async def get_schedule(user_id: str, day_of_week: str, session: AsyncSession):
        schedule_result = await session.execute(select(Schedule).
                                          where(Schedule.user_id == user_id, Schedule.day_of_week == day_of_week).
                                          order_by(Schedule.time_start))
        schedules = schedule_result.scalars().all()
        return schedules

    @staticmethod
    async def create_schedule(params: dict, session: AsyncSession):
        # try:
        schedule = Schedule(params)
        session.add(schedule)
        await session.commit()
        print("\n\nВсе отработало!\n\n")
        # except:
        #     await session.rollback()
        # finally:
        #     await session.close()
