from db.models.projects import ProjectModel
from db.models.users import UserModel
from typing import Callable, Dict, Any, Awaitable

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
                await state.update_data(projects_page=1)
                await state.update_data(category_id=int(event.data.split("_")[-1]))
                context_data = await state.get_data()
            elif "_notifications_category_" in event.data:
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
                                        current_user.projects.append(project)
                                else:
                                    current_user.projects = []
                                await session.commit()
                            except Exception:
                                pass
            elif "_project_notification_for_user_" in event.data:
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
                            except Exception:
                                pass
            else:
                page = context_data.get("projects_page")
                if "next_projects_page_for_user_choise_project" == event.data:
                    new_page = page + 1
                elif "back_projects_page_for_user_choise_project" == event.data:
                    new_page = page - 1
                await state.update_data(projects_page=new_page)
                context_data = await state.get_data()

            async with session_maker() as session:
                async with session.begin():
                    projects_page = context_data.get("projects_page")
                    category_id = context_data.get("category_id")
                    user_res: ScalarResult = await session.execute(
                        select(UserModel)
                        .options(selectinload(UserModel.projects))
                        .where(UserModel.user_id == event.from_user.id)
                    )
                    current_user: UserModel = user_res.scalars().one_or_none()

                    res: ScalarResult = await session.execute(
                        select(ProjectModel).where(
                            ProjectModel.project_category_id == category_id
                        )
                    )
                    projects: list[ProjectModel] = res.unique().scalars().all()
                    projects_dict = {}
                    if len(projects) <= 5:
                        for project in projects:
                            projects_dict[project.title] = [
                                str(project.id),
                                project in current_user.projects,
                            ]
                        page = "one"
                    elif projects_page == 1:
                        for project in projects[:5]:
                            projects_dict[project.title] = [
                                str(project.id),
                                project in current_user.projects,
                            ]
                        page = "first"
                    else:
                        if 5 * projects_page == len(projects):
                            for project in projects[-5:]:
                                projects_dict[project.title] = [
                                    str(project.id),
                                    project in current_user.projects,
                                ]
                            page = "last"
                        elif 5 * projects_page < len(projects):
                            for project in projects[
                                (5 * projects_page) - 5 : (5 * projects_page)
                            ]:
                                projects_dict[project.title] = [
                                    str(project.id),
                                    project in current_user.projects,
                                ]
                            page = "middle"
                        elif (
                            5 * projects_page > len(projects)
                            and 5 * projects_page - len(projects) < 5
                        ):
                            for project in projects[(5 * (projects_page - 1)) :]:
                                projects_dict[project.title] = [
                                    str(project.id),
                                    project in current_user.projects,
                                ]
                            page = "last"
                    data["projects"] = projects_dict
                    data["page"] = page
                    data["category_id"] = category_id
                    return await handler(event, data)
        except TypeError:
            pass
