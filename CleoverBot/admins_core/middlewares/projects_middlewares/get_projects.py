import logging

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
                new_page = 0
                await state.update_data(category_id=int(event.data.split("_")[-1]))
                context_data = await state.get_data()
            else:
                page = context_data.get("projects_page")
                if "next_projects_page" in event.data:
                    new_page = page + 1
                elif "back_projects_page" in event.data:
                    if page > 0:
                        new_page = page - 1
                context_data = await state.get_data()

            async with session_maker() as session:
                async with session.begin():
                    category_id = context_data.get("category_id")
                    res: ScalarResult = await session.execute(
                        select(ProjectModel)
                        .where(ProjectModel.project_category_id == category_id)
                        .offset(new_page * 5)
                        .limit(5)
                    )
                    projects = res.unique().scalars().all()
                    if projects:
                        projects_dict = {}
                        for project in projects:
                            projects_dict[project.title] = str(project.id)
                        if not new_page:
                            if len(projects) < 5:
                                page = "one"
                            else:
                                page = "first"
                        else:
                            if len(projects) < 5:
                                page = "last"
                            else:
                                page = "middle"
                        data["projects"] = projects_dict
                        data["page"] = page
                        data["is_full"] = True
                        await state.update_data(projects_page=new_page)
                    else:
                        data["projects"] = {}
                        data["page"] = ""
                        data["is_full"] = False
                    return await handler(event, data)
        except TypeError as e:
            logging.error(e)
