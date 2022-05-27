from typing import Any, Iterable

from sqlalchemy.orm import sessionmaker

import domain.visit
from database.visit_repository import VisitsRepository
from database.tables import DatabaseVisit


class VisitsRepositoryImpl(VisitsRepository):
    """Данный класс является реализацией VisitsRepository,которая работает,опираясь на SqlAlchemy."""

    def __init__(self, engine=None):
        self.engine = engine
        self.session_factory = sessionmaker(bind=engine)

    def add_new_visit(self, ip: str, page: str, user_agent: str, country: str,
                      user_id: int | None) -> int:
        """Реализация добавления записи в базу данных."""
        session = self.session_factory()
        visit = DatabaseVisit(
            ip=ip,
            page=page,
            time=VisitsRepository.get_current_timestamp(),
            user_agent=user_agent,
            country=country,
            user_id=user_id)
        session.add(visit)
        session.commit()

        return visit.id

    def get_last(self) -> domain.visit.Visit:
        """Реализация получения последней записи из базы данных."""
        session = self.session_factory()

        visit = session.query(DatabaseVisit).order_by(
            DatabaseVisit.id.desc()).first()
        session.commit()

        return domain.visit.Visit(
            id=visit.id,
            ip=visit.ip,
            page=visit.page,
            time=visit.time,
            user_agent=visit.user_agent,
            country=visit.country,
            user_id=visit.user_id,
        )

    def get_first(self) -> domain.visit.Visit:
        """Реализация получения первой записи из базы данных."""
        session = self.session_factory()

        visit = session.query(DatabaseVisit).order_by(DatabaseVisit.id).first()
        session.commit()

        return domain.visit.Visit(
            id=visit.id,
            ip=visit.ip,
            page=visit.page,
            time=visit.time,
            user_agent=visit.user_agent,
            country=visit.country,
            user_id=visit.user_id,
        )

    def get_users_count(self) -> int:
        """Реализация получения количество записей из базы данных."""
        session = self.session_factory()
        count = session.query(DatabaseVisit).count()
        session.commit()

        return count

    def get_records_by_id(self, id) -> Iterable[domain.visit.Visit]:
        """Реализация получения записей, соответствующих определенному пользователю, из базы данных."""
        session = self.session_factory()
        visits = session.query(DatabaseVisit) \
            .filter(DatabaseVisit.user_id == id) \
            .all()
        session.commit()
        for visit in visits:
            yield domain.visit.Visit(
                id=visit.id,
                ip=visit.ip,
                page=visit.page,
                time=visit.time,
                user_agent=visit.user_agent,
                country=visit.country,
                user_id=visit.user_id,
            )

    def get_all_records(self) -> Iterable[domain.visit.Visit]:
        """Реализация получения всех записей из базы данных."""
        session = self.session_factory()
        visits = session.query(DatabaseVisit).all()
        session.commit()
        for visit in visits:
            yield domain.visit.Visit(
                id=visit.id,
                ip=visit.ip,
                page=visit.page,
                time=visit.time,
                user_agent=visit.user_agent,
                country=visit.country,
                user_id=visit.user_id,
            )
