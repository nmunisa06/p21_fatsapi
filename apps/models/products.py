from sqlalchemy import BigInteger, String, VARCHAR, ForeignKey, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.models.db import CreatedBaseModel

class Category(CreatedBaseModel):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    products: Mapped[list['Product']] = relationship('Product', back_populates='category')


class Product(CreatedBaseModel):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    price: Mapped[float] = mapped_column(BigInteger)
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Category.id, ondelete="CASCADE"))
    category: Mapped[list['Category']] = relationship('Category', back_populates='products')


    @classmethod
    async def get_all(cls, session: AsyncSession):
        result = await session.execute(select(cls))
        return result.scalars().all()
