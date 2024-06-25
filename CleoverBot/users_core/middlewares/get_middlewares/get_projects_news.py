from datetime import datetime, timezone, timedelta
import logging
from typing import Callable, Dict, Any, Awaitable

from db.models.projects_news import ProjectNewsModel

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, desc
from sqlalchemy.engine import ScalarResult


class ProjectsNewsPagesMiddleware(BaseMiddleware):
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
            if "choise_project_for_user_view_" in event.data:
                if context_data.get("news_page"):
                    new_page = context_data.get("news_page")
                else:
                    new_page = 0
                await state.update_data(project_id=int(event.data.split("_")[-1]))
                context_data = await state.get_data()
            else:
                page = context_data.get("news_page")
                if "next_project_news_page" == event.data:
                    new_page = page + 1
                elif "back_project_news_page" == event.data:
                    if page > 0:
                        new_page = page - 1
                elif "return_to_project" in event.data:
                    new_page = page
                context_data = await state.get_data()

            async with session_maker() as session:
                async with session.begin():
                    project_id = context_data.get("project_id")

                    res: ScalarResult = await session.execute(
                        select(ProjectNewsModel)
                        .where(
                            ProjectNewsModel.project_id == project_id,
                            (
                                datetime.now(tz=timezone.utc)
                                - ProjectNewsModel.create_date
                            )
                            <= timedelta(days=30),
                        )
                        .order_by(desc(ProjectNewsModel.create_date))
                        .offset(new_page * 5)
                        .limit(5)
                    )
                    news = res.scalars().all()
                    if news:
                        news_dict = {}
                        for one_news in news:
                            news_dict[one_news.title] = [
                                str(one_news.id),
                                one_news.description,
                            ]
                        if not new_page:
                            if len(news) < 5:
                                page = "one"
                            else:
                                page = "first"
                        else:
                            if len(news) < 5:
                                page = "last"
                            else:
                                page = "middle"
                        data["news"] = news_dict
                        data["page"] = page
                        data["is_full"] = True
                        await state.update_data(news_page=new_page)
                    else:
                        data["news"] = {}
                        data["page"] = ""
                        data["is_full"] = False
            return await handler(event, data)
        except TypeError as e:
            logging.error(e)
