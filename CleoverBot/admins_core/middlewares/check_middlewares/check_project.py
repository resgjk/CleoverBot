from typing import Callable, Dict, Any, Awaitable

from db.models.projects import ProjectModel

from aiogram import BaseMiddleware
from aiogram.types import Message, ContentType, CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class CheckProjectMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        state: FSMContext = data["state"]
        context_data = await state.get_data()
        category_id = context_data.get("category_id")

        if event.content_type != ContentType.TEXT:
            data["result"] = "invalid"
            return await handler(event, data)
        async with session_maker() as session:
            async with session.begin():
                res: ScalarResult = await session.execute(
                    select(ProjectModel).where(
                        ProjectModel.title == event.text,
                        ProjectModel.project_category_id == category_id,
                    )
                )
                current_project: ProjectModel = res.scalars().one_or_none()
                if current_project:
                    data["result"] = "in_db"
                else:
                    data["result"] = "not_in_db"
        return await handler(event, data)


class CheckProjectForAddNewsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        async with session_maker() as session:
            async with session.begin():
                res: ScalarResult = await session.execute(
                    select(ProjectModel).where(
                        ProjectModel.id == int(event.data.split("_")[-1])
                    )
                )
                current_project: ProjectModel = res.scalars().one_or_none()
                if current_project:
                    data["result"] = "success"
                else:
                    data["result"] = "error"
        return await handler(event, data)
