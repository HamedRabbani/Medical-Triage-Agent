from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..base import Base


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic repository for common persistence operations."""

    def __init__(self, session: Session, model: type[ModelType]):
        self.session = session
        self.model = model

    def get_by_id(self, entity_id: int) -> ModelType | None:
        """Return an entity by primary key."""
        return self.session.get(self.model, entity_id)

    def get_all(self) -> list[ModelType]:
        """Return all entities."""
        statement = select(self.model)
        return list(self.session.scalars(statement).all())

    def add(self, entity: ModelType) -> ModelType:
        """Add an entity to the current session."""
        self.session.add(entity)
        self.session.flush()
        return entity

    def delete(self, entity: ModelType) -> None:
        """Delete an entity from the current session."""
        self.session.delete(entity)