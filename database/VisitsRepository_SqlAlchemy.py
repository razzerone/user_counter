from typing import Tuple, Any

from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from Domain.Visit import Visit
from database.VisitsRepository import VisitsRepository
from database.tables import engine, DatabaseVisit


class VisitsRepositoryImpl(VisitsRepository):
    def __init__(self):
        self.engine = engine
        self.session_factory = sessionmaker(bind=engine)

    def add_new_visit(self, ip: str, page: str, user_agent: str, country: str, user_id: int | None) -> int:
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

    def get_last(self) -> tuple[Any, Any, Any, Any, Any, Any, Any]:
        session = self.session_factory()

        visit = session.query(DatabaseVisit).order_by(DatabaseVisit.id.desc()).first()
        session.commit()

        return (visit.id, visit.ip,
                visit.page,
                visit.time,
                visit.user_agent,
                visit.country,
                visit.user_id,
                )

    def get_first(self) -> tuple[Any, Any, Any, Any, Any, Any, Any]:
        session = self.session_factory()

        visit = session.query(DatabaseVisit).order_by(DatabaseVisit.id).first()
        session.commit()

        return (visit.id, visit.ip,
                visit.page,
                visit.time,
                visit.user_agent,
                visit.country,
                visit.user_id,
                )

    def get_users_count(self) -> int:
        session = self.session_factory()
        count = session.query(DatabaseVisit).count()
        session.commit()

        return count

    def get_records_by_id(self, id) -> tuple[tuple[Any, Any, Any, Any, Any, Any, Any]]:
        session = self.session_factory()
        visits = session.query(DatabaseVisit).filter(DatabaseVisit.user_id == id).all()
        session.commit()
        for visit in visits:
            yield (visit.id, visit.ip,
                   visit.page,
                   visit.time,
                   visit.user_agent,
                   visit.country,
                   visit.user_id,
                   )

    def get_all_records(self) -> tuple[tuple[Any, Any, Any, Any, Any, Any, Any]]:
        session = self.session_factory()
        visits = session.query(DatabaseVisit).all()
        session.commit()
        for visit in visits:
            yield (visit.id, visit.ip,
                   visit.page,
                   visit.time,
                   visit.user_agent,
                   visit.country,
                   visit.user_id,
                   )
