from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def investing_process(new_object: Union[CharityProject, Donation], model_to_invest, session: AsyncSession):
    objects_in_queue = await session.execute(
        select(model_to_invest).where(model_to_invest.fully_invested == 0))
    objects_in_queue = objects_in_queue.scalars().all()
    if objects_in_queue:
        new_object_balance = new_object.full_amount - new_object.invested_amount
        current_date = datetime.now()
        for object in objects_in_queue:
            object_balance = object.full_amount - object.invested_amount
            if new_object_balance >= object_balance:
                object.invested_amount = object.full_amount
                object.fully_invested = True
                object.close_date = current_date
                new_object_balance -= object_balance
            else:
                object.invested_amount += new_object_balance
                new_object_balance = 0
            session.add(object)
            if new_object_balance == 0:
                break
        new_object.invested_amount = new_object.full_amount - new_object_balance
        if new_object_balance == 0:
            new_object.fully_invested = True
            new_object.close_date = current_date
        session.add(new_object)
        await session.commit()
        await session.refresh(new_object)
