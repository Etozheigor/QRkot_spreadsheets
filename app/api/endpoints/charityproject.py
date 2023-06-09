from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_is_possible_to_change_amount,
                                check_project_exists,
                                check_project_name_duplicate,
                                check_project_was_closed,
                                check_project_was_invested)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.models import Donation
from app.schemas.charityproject import (CharityProjectCreate, CharityProjectDB,
                                        CharityProjectUpdate)
from app.services.investing_process import investing_process

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
    description='Получает список всех проектов'
)
async def get_all_charity_projects(session: AsyncSession = Depends(get_async_session)):
    all_charity_projects = await charity_project_crud.get_multi(session)
    return all_charity_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    description='Создает благотворительный проект.',
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    await check_project_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(charity_project, session)
    await investing_process(new_charity_project, Donation, session)
    return new_charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    description=('Закрытый проект нельзя редактировать, также нельзя '
                 'установить требуемую сумму меньше уже вложенной.'))
async def update_chariry_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_project_exists(project_id, session)
    await check_project_was_closed(charity_project)
    await check_is_possible_to_change_amount(charity_project, obj_in)
    if obj_in.name:
        await check_project_name_duplicate(obj_in.name, session)
    charity_project = await charity_project_crud.update(charity_project, obj_in, session)
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    description=('Удаляет проект. Нельзя удалить проект, в который уже '
                 'были инвестированы средства, его можно только закрыть.')
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    charity_project = await check_project_exists(project_id, session)
    await check_project_was_invested(charity_project)
    charity_project = await charity_project_crud.remove(charity_project, session)
    return charity_project
