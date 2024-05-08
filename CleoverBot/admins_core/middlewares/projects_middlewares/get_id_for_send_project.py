from db.models.users import UserModel
from db.models.projects import ProjectModel

from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class SendProjectMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        state: FSMContext = data["state"]
        context_data = await state.get_data()
        title = context_data.get("title")
        category = context_data.get("category_id")
        description = context_data.get("description")
        links = context_data.get("links")
        photos = context_data.get("photos")
        videos = context_data.get("videos")
        owner_id = event.from_user.id
        users_id = []
        async with session_maker() as session:
            async with session.begin():
                try:
                    new_project: ProjectModel = ProjectModel(
                        title=title,
                        project_category_id=category,
                        description=description,
                        photos=photos,
                        videos=videos,
                        links=links,
                    )
                    session.add(new_project)

                    res: ScalarResult = await session.execute(
                        select(UserModel).where(UserModel.is_subscriber == True)
                    )
                    users: list[UserModel] = res.scalars().all()
                    for user in users:
                        if user.user_id != owner_id:
                            users_id.append(user.user_id)
                    data["users_id"] = users_id
                    data["result"] = "success"
                    await session.commit()
                except Exception:
                    data["users_id"] = []
                    data["result"] = "error"
        return await handler(event, data)
