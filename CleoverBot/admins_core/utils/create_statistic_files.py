import io

from db.models.agency_stats import AgencyStatModel

import openpyxl

from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.engine import ScalarResult
from sqlalchemy import select


async def get_statistic_data(session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            stat_res: ScalarResult = await session.execute(
                select(AgencyStatModel).options(
                    joinedload(AgencyStatModel.user),
                    joinedload(AgencyStatModel.transaction),
                )
            )
            return stat_res.scalars().all()


async def get_transactions_document(session_maker: sessionmaker):
    statistic_data = await get_statistic_data(session_maker)
    if statistic_data:
        file_name = "media/stat_files/agency-stat.xlsx"
        counter = 1
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.append(
            [
                "№",
                "TG ID",
                "Имя пользователя",
                "ID транзакции",
                "Дата",
                "Стоимость",
                "Доля агентства",
            ]
        )
        for stat in statistic_data:
            sheet.append(
                [
                    counter,
                    stat.user.user_id,
                    stat.user.username,
                    stat.transaction.uuid,
                    stat.payment_datetime,
                    stat.transaction.amount,
                    stat.transaction.amount * 0.125,
                ]
            )
            counter += 1
        wb.save(file_name)
        return file_name
    return None


async def get_users_document(session_maker: sessionmaker):
    statistic_data = await get_statistic_data(session_maker)
    if statistic_data:
        users = {}
        for stat in statistic_data:
            if str(stat.user.user_id) in users:
                users[str(stat.user.user_id)]["sum"] += stat.transaction.amount
                users[str(stat.user.user_id)]["agency_share"] += (
                    stat.transaction.amount * 0.125
                )
            else:
                users[str(stat.user.user_id)] = {
                    "username": stat.user.username,
                    "sum": stat.transaction.amount,
                    "agency_share": stat.transaction.amount * 0.125,
                }
        file_name = "media/stat_files/agency-stat.xlsx"
        counter = 1
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.append(
            ["№", "TG ID", "Имя пользователя", "Cумма транзакций", "Доля агентства"]
        )
        for user in users.keys():
            sheet.append(
                [
                    counter,
                    user,
                    users[user]["username"],
                    users[user]["sum"],
                    users[user]["agency_share"],
                ]
            )
            counter += 1
        wb.save(file_name)
        return file_name
    return None
