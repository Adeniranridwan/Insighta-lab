from sqlalchemy import Column, String, Float, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from app.database import Base


from sqlalchemy import Index


class Profile(Base):
    __tablename__ = "profiles"

    id               = Column(UUID(as_uuid=True), primary_key=True)
    name             = Column(String, unique=True, nullable=False)
    gender           = Column(String, nullable=False)
    gender_probability = Column(Float, nullable=False)
    age              = Column(Integer, nullable=False)
    age_group        = Column(String, nullable=False)
    country_id       = Column(String(2), nullable=False)
    country_name     = Column(String, nullable=False)
    country_probability = Column(Float, nullable=False)
    created_at       = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


    # After the class definition, add:
Index("ix_profiles_gender", Profile.gender)
Index("ix_profiles_age_group", Profile.age_group)
Index("ix_profiles_country_id", Profile.country_id)
Index("ix_profiles_age", Profile.age)