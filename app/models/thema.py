"""
SQLAlchemy models voor de Thema Database
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from app.db.session import Base

class Thema(Base):
    """Hoofd thema tabel (verjaardag, liefde, huwelijk, etc.)"""
    __tablename__ = "themas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    display_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    professional_prompt = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    elements = relationship("ThemaElement", back_populates="thema", cascade="all, delete-orphan")
    rhyme_sets = relationship("ThemaRhymeSet", back_populates="thema", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Thema(name='{self.name}', display_name='{self.display_name}')>"

class ThemaElement(Base):
    """Thema elementen: keywords, power_phrases, genres, etc."""
    __tablename__ = "thema_elements"

    id = Column(Integer, primary_key=True, index=True)
    thema_id = Column(Integer, ForeignKey("themas.id", ondelete="CASCADE"), nullable=False)
    element_type = Column(String(30), nullable=False, index=True)  # 'keyword', 'power_phrase', 'genre', 'bpm', etc.
    content = Column(Text, nullable=False)
    usage_context = Column(String(50), nullable=True)  # 'intro', 'chorus', 'bridge', 'any'
    weight = Column(Integer, default=1, nullable=False)  # Voor random selection
    suno_format = Column(Text, nullable=True)  # Suno.ai specifieke formatting
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    # Relationships
    thema = relationship("Thema", back_populates="elements")

    def __repr__(self):
        return f"<ThemaElement(type='{self.element_type}', content='{self.content[:30]}...')>"

class ThemaRhymeSet(Base):
    """Rijmwoorden sets per thema"""
    __tablename__ = "thema_rhyme_sets"

    id = Column(Integer, primary_key=True, index=True)
    thema_id = Column(Integer, ForeignKey("themas.id", ondelete="CASCADE"), nullable=False)
    rhyme_pattern = Column(String(10), nullable=False)  # 'AABB', 'ABAB', etc.
    words = Column(ARRAY(String), nullable=False)  # ['hart', 'start', 'apart']
    difficulty_level = Column(String(20), default='medium', nullable=False)  # 'easy', 'medium', 'hard'
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    # Relationships
    thema = relationship("Thema", back_populates="rhyme_sets")

    def __repr__(self):
        return f"<ThemaRhymeSet(pattern='{self.rhyme_pattern}', words={self.words})>" 