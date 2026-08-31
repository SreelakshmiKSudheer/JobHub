from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.models.Mixins import PKMixin
from app.db.types import ShortTextType

class Skill(Base, PKMixin):
    __tablename__ = "skills"

    name: Mapped[str] = mapped_column(
        ShortTextType,
        nullable=False,
        unique=True
    )
    
    # --- relationships ---