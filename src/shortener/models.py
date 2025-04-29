from sqlalchemy.orm import mapped_column, Mapped

from database import Base


class ShortUrlOrm(Base):
    __tablename__ = 'urls'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    original_url: Mapped[str]
    short_url: Mapped[str]

