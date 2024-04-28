from db.models.projects import ProjectModel
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class ProjectsPagesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        state: FSMContext = data["state"]
        context_data = await state.get_data()
        try:
            if "set_project_category_for_choise_project" in event.data:
                await state.update_data(projects_page=1)
                await state.update_data(category_id=int(event.data.split("_")[-1]))
                context_data = await state.get_data()
            else:
                page = context_data.get("projects_page")
                if "next_projects_page" in event.data:
                    new_page = page + 1
                elif "back_projects_page" in event.data:
                    new_page = page - 1
                await state.update_data(projects_page=new_page)
                context_data = await state.get_data()

            async with session_maker() as session:
                async with session.begin():
                    projects_page = context_data.get("projects_page")
                    category_id = context_data.get("category_id")
                    res: ScalarResult = await session.execute(
                        select(ProjectModel).where(
                            ProjectModel.project_category_id == category_id
                        )
                    )
                    projects = res.unique().scalars().all()
                    projects_dict = {}
                    if len(projects) <= 5:
                        for project in projects:
                            projects_dict[project.title] = str(project.id)
                        page = "one"
                    elif projects_page == 1:
                        for project in projects[:5]:
                            projects_dict[project.title] = str(project.id)
                        page = "first"
                    else:
                        if 5 * projects_page == len(projects):
                            for project in projects[-5:]:
                                projects_dict[project.title] = str(project.id)
                            page = "last"
                        elif 5 * projects_page < len(projects):
                            for project in projects[
                                (5 * projects_page) - 5 : (5 * projects_page)
                            ]:
                                projects_dict[project.title] = str(project.id)
                            page = "middle"
                        elif (
                            5 * projects_page > len(projects)
                            and 5 * projects_page - len(projects) < 5
                        ):
                            for project in projects[(5 * (projects_page - 1)) :]:
                                projects_dict[project.title] = str(project.id)
                            page = "last"
                    data["projects"] = projects_dict
                    data["page"] = page
                    return await handler(event, data)
        except TypeError:
            pass
