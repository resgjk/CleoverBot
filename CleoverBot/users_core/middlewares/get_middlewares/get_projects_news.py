from db.models.projects_news import ProjectNewsModel
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from datetime import datetime, timezone

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
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
                await state.update_data(
                    news_page=1, project_id=int(event.data.split("_")[-1])
                )
                context_data = await state.get_data()
            else:
                page = context_data.get("news_page")
                if "next_project_news_page" == event.data:
                    new_page = page + 1
                elif "back_project_news_page" == event.data:
                    new_page = page - 1
                await state.update_data(news_page=new_page)
                context_data = await state.get_data()

            async with session_maker() as session:
                async with session.begin():
                    news_page = context_data.get("news_page")
                    project_id = context_data.get("project_id")

                    res: ScalarResult = await session.execute(
                        select(ProjectNewsModel).where(
                            ProjectNewsModel.project_id == project_id,
                            (
                                datetime.now(tz=timezone.utc).date()
                                - ProjectNewsModel.create_date
                            )
                            <= 30,
                        )
                    )
                    news = res.scalars().all()
                    news_dict = {}
                    if len(news) <= 5:
                        for one_news in news:
                            news_dict[one_news.title] = [
                                str(one_news.id),
                                one_news.description,
                            ]
                        page = "one"
                    elif news_page == 1:
                        for one_news in news[:5]:
                            news_dict[one_news.title] = [
                                str(one_news.id),
                                one_news.description,
                            ]
                        page = "first"
                    else:
                        if 5 * news_page == len(news):
                            for one_news in news[-5:]:
                                news_dict[one_news.title] = [
                                    str(one_news.id),
                                    one_news.description,
                                ]
                            page = "last"
                        elif 5 * news_page < len(news):
                            for one_news in news[(5 * news_page) - 5 : (5 * news_page)]:
                                news_dict[one_news.title] = [
                                    str(one_news.id),
                                    one_news.description,
                                ]
                            page = "middle"
                        elif (
                            5 * news_page > len(news) and 5 * news_page - len(news) < 5
                        ):
                            for one_news in news[(5 * (news_page - 1)) :]:
                                news_dict[one_news.title] = [
                                    str(one_news.id),
                                    one_news.description,
                                ]
                            page = "last"
                    data["news"] = news_dict
                    data["page"] = page
                    return await handler(event, data)
        except TypeError:
            pass
