from sqlalchemy import BigInteger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncAttrs
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from select import select
from sqlalchemy import delete as sqlalchemy_delete, DateTime, Column
from sqlalchemy import update as sqlalchemy_update

from config import conf


# DATABASE_URL = 'postgresql+psycopg2://postgres:1@localhost:5439/fastapi_db'

class Base(AsyncAttrs, DeclarativeBase):

    @declared_attr
    def __tablename__(self) -> str:
        __name = self.__name__.lower()
        if __name.endswith('y'):
            __name = __name[:-1] + 'ie'
        return __name + 's'


class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    def init(self):
        self._engine = create_async_engine(conf.db.db_url)
        self._session = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


db = AsyncDatabaseSession()
db.init()

# --------------------- CRUD ----------------------

class AbstractClass:
    @staticmethod
    def commit():
        try:
            db.commit()
        except Exception as e:
            print(f'commit failed {e}')
            db.rollback()

    @classmethod
    def create(cls, **kwargs):
        item = cls(**kwargs)
        db.add(item)
        cls.commit()
        return item

    @classmethod
    def get(cls, item_id):
        get_item = select(cls).where(cls.id == item_id)
        item = db.execute(get_item).scalar()
        if item is None:
            print(f'item {item_id} not found')
        return item

    @classmethod
    def update(cls, item_id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == item_id)
            .values(**kwargs)
            .execution_options(synchronized_session='fetch')
        )
        db.execute(query)
        cls.commit()

    @classmethod
    def delete(cls, item_id):
        query = sqlalchemy_delete(cls).where(cls.id == item_id)
        db.execute(query)
        cls.commit()

    @classmethod
    def get_all(cls):
        return db.execute(select(cls)).scalars()


class CreateModel(Base, AbstractClass):
    __abstract__ = True
    created_at = Column(DateTime(), default=datetime.utcnow())


class BaseModel(Base, AbstractClass):
    __abstract__ = True
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    def __str__(self):
        return f'{self.id}'


class CreatedBaseModel(BaseModel):
    __abstract__ = True
