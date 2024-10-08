import logging
from typing import Callable, Dict, Any, Awaitable

from db.models.projects import ProjectModel
from db.models.users import UserModel

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import sessionmaker, selectinload
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
            if "set_project_category_for_user_choise_project" in event.data:
                new_page = 0
                await state.update_data(category_id=int(event.data.split("_")[-1]))
                context_data = await state.get_data()
            elif "_notifications_category_" in event.data:
                new_page = context_data.get("projects_page")
                async with session_maker() as session:
                    async with session.begin():
                        category_id = context_data.get("category_id")
                        res: ScalarResult = await session.execute(
                            select(ProjectModel).where(
                                ProjectModel.project_category_id == category_id
                            )
                        )
                        projects: list[ProjectModel] = res.unique().scalars().all()

                        user_res: ScalarResult = await session.execute(
                            select(UserModel)
                            .options(selectinload(UserModel.projects))
                            .where(UserModel.user_id == event.from_user.id)
                        )
                        current_user: UserModel = user_res.scalars().one_or_none()

                        if current_user:
                            try:
                                if "enable" in event.data:
                                    for project in projects:
                                        if project not in current_user.projects:
                                            current_user.projects.append(project)
                                else:
                                    current_user.projects = []
                                await session.commit()
                            except Exception as e:
                                logging.error(e)
            elif "_project_notification_for_user_" in event.data:
                new_page = context_data.get("projects_page")
                async with session_maker() as session:
                    async with session.begin():
                        project_id = int(event.data.split("_")[-1])
                        project_res: ScalarResult = await session.execute(
                            select(ProjectModel).where(ProjectModel.id == project_id)
                        )
                        current_project: ProjectModel = (
                            project_res.scalars().one_or_none()
                        )

                        user_res: ScalarResult = await session.execute(
                            select(UserModel)
                            .options(selectinload(UserModel.projects))
                            .where(UserModel.user_id == event.from_user.id)
                        )
                        current_user: UserModel = user_res.scalars().one_or_none()

                        if current_user and current_project:
                            try:
                                if event.data.split("_")[0] == "disable":
                                    current_user.projects.append(current_project)
                                else:
                                    del current_user.projects[
                                        current_user.projects.index(current_project)
                                    ]
                                await session.commit()
                            except Exception as e:
                                logging.error(e)
            else:
                page = context_data.get("projects_page")
                if "next_projects_page_for_user_choise_project" == event.data:
                    new_page = page + 1
                elif "back_projects_page_for_user_choise_project" == event.data:
                    if page > 0:
                        new_page = page - 1
                elif "return_to_category" in event.data:
                    new_page = page
                context_data = await state.get_data()

            async with session_maker() as session:
                async with session.begin():
                    category_id = context_data.get("category_id")
                    user_res: ScalarResult = await session.execute(
                        select(UserModel)
                        .options(selectinload(UserModel.projects))
                        .where(UserModel.user_id == event.from_user.id)
                    )
                    current_user: UserModel = user_res.scalars().one_or_none()

                    res: ScalarResult = await session.execute(
                        select(ProjectModel)
                        .where(ProjectModel.project_category_id == category_id)
                        .offset(new_page * 5)
                        .limit(5)
                    )
                    projects: list[ProjectModel] = res.unique().scalars().all()
                    if projects:
                        projects_dict = {}
                        for project in projects:
                            projects_dict[project.title] = [
                                str(project.id),
                                project in current_user.projects,
                            ]
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
                        data["category_id"] = category_id
                        data["is_full"] = True
                        await state.update_data(projects_page=new_page)
                    else:
                        data["projects"] = {}
                        data["page"] = ""
                        data["category_id"] = 0
                        data["is_full"] = False
                    return await handler(event, data)
        except TypeError as e:
            logging.error(e)
