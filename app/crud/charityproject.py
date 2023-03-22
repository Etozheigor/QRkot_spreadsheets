from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CharityProjectCRUD(CRUDBase):
    async def get_projects_by_completion_rate(self, session: AsyncSession):
        """Кастомный crud-метод для получения отсортированного списка всех закрытых проектов."""
        projects = await session.execute(
            select(
                CharityProject.name,
                CharityProject.create_date,
                CharityProject.close_date,
                CharityProject.description
            ).where(
                CharityProject.fully_invested == 1).order_by(
                func.julianday(CharityProject.close_date) - func.julianday(CharityProject.create_date)))
        return projects.all()


charity_project_crud = CharityProjectCRUD(CharityProject)