from sqlalchemy import Column, BOOLEAN, DATE, INTEGER, BIGINT, VARCHAR
from db.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    user_id = Column(BIGINT, unique=True, nullable=False)
    is_subscriber = Column(BOOLEAN, nullable=False, default=False, unique=False)
    subscriber_until = Column(DATE, nullable=True, unique=False)
    bank = Column(VARCHAR(15), nullable=False, default="Zero bank")
    notification = Column(VARCHAR(10), nullable=False, default="1 Hour")
    defi_activity = Column(BOOLEAN, default=False)
    airdrops_activity = Column(BOOLEAN, default=False)
    news_activity = Column(BOOLEAN, default=False)
    ido_ico_activity = Column(BOOLEAN, default=False)
    ambassador_programs_activity = Column(BOOLEAN, default=False)
    nft_activity = Column(BOOLEAN, default=False)

    def __repr__(self) -> str:
        return f"{self.id} {self.user_id} {self.is_subscriber} {self.subscriber_until}"
