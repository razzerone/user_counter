from typing import Iterable

from sqlalchemy.orm import Query, Session, sessionmaker

import domain.visit
from database.visit_repository import VisitsRepository
from database.tables import DatabaseVisit
from domain import identifier


class VisitsRepositoryImpl(VisitsRepository):
    """Данный класс является реализацией VisitsRepository,которая работает,опираясь на SqlAlchemy."""

    def __init__(self, engine=None):
        self.engine = engine
        self.session_factory = sessionmaker(bind=engine)

    def add_new_visit(self, ip: str, page: str, user_agent: str, browser: str,
                      os: str, country: str, user_id: int | None) -> int:
        """Реализация добавления записи в базу данных."""
        session = self.session_factory()
        visit = DatabaseVisit(
            ip=ip,
            page=page,
            time=VisitsRepository.get_current_timestamp(),
            user_agent=user_agent,
            browser=browser,
            os=os,
            country=country,
            user_id=user_id)
        session.add(visit)
        session.commit()

        return visit.id

    def get_last(self) -> domain.visit.Visit:
        """Реализация получения последней записи из базы данных."""
        session = self.session_factory()

        visit = (session
                 .query(DatabaseVisit)
                 .order_by(DatabaseVisit.id.desc())
                 .first()
                 )
        session.commit()

        return domain.visit.Visit(
            id=visit.id,
            ip=visit.ip,
            page=visit.page,
            time=domain.visit.convert_date(str(visit.time)),
            user_agent=visit.user_agent,
            browser=visit.browser,
            os=visit.os,
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
            time=domain.visit.convert_date(str(visit.time)),
            user_agent=visit.user_agent,
            browser=visit.browser,
            os=visit.os,
            country=visit.country,
            user_id=visit.user_id,
        )

    def get_users_count(self) -> int:
        """Реализация получения количество записей из базы данных."""
        session = self.session_factory()
        count = session.query(DatabaseVisit).count()
        session.commit()

        return count

    def get_records_by_id(self, id_: int) -> Iterable[domain.visit.Visit]:
        """Реализация получения записей, соответствующих определенному пользователю, из базы данных."""
        session = self.session_factory()
        visits = session.query(DatabaseVisit) \
            .filter(DatabaseVisit.user_id == id_) \
            .all()
        session.commit()
        for visit in visits:
            yield domain.visit.Visit(
                id=visit.id,
                ip=visit.ip,
                page=visit.page,
                time=domain.visit.convert_date(str(visit.time)),
                user_agent=visit.user_agent,
                browser=visit.browser,
                os=visit.os,
                country=visit.country,
                user_id=visit.user_id,
            )

    def get_records_by_date(self, date_begin: str, date_end: str) -> \
            Iterable[domain.visit.Visit]:
        begin = int(f'{date_begin.replace("-", "")}000000')
        end = int(f'{date_end.replace("-", "")}235959')
        with self.session_factory() as s:
            visits = (s.query(DatabaseVisit)
                      .filter(DatabaseVisit.time > begin)
                      .filter(DatabaseVisit.time < end)
                      .all())
            s.commit()
            for visit in visits:
                yield domain.visit.Visit(
                    id=visit.id,
                    ip=visit.ip,
                    page=visit.page,
                    time=domain.visit.convert_date(str(visit.time)),
                    user_agent=visit.user_agent,
                    browser=visit.browser,
                    os=visit.os,
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
                time=domain.visit.convert_date(str(visit.time)),
                user_agent=visit.user_agent,
                browser=visit.browser,
                os=visit.os,
                country=visit.country,
                user_id=visit.user_id,
            )

    def get_records_by_condition(
            self,
            id_: int | None,
            date_begin: str,
            date_end: str,
            browser: str,
            os: str) -> Iterable[domain.visit.Visit]:
        with self.session_factory() as s:
            visits = self._get_visits(s, id_, date_begin,
                                      date_end, browser, os)
            s.commit()

        for visit in visits:
            yield domain.visit.Visit(
                id=visit.id,
                ip=visit.ip,
                page=visit.page,
                time=domain.visit.convert_date(str(visit.time)),
                user_agent=visit.user_agent,
                browser=visit.browser,
                os=visit.os,
                country=visit.country,
                user_id=visit.user_id,
            )

    def get_visit_count_by_condition(
            self,
            date_begin: str,
            date_end: str,
            browser: str,
            os: str) -> int:

        with self.session_factory() as s:
            count = self._get_visits(s, None, date_begin,
                                     date_end, browser, os).count()
            s.commit()

            return count

    @staticmethod
    def _get_visits(
            session: Session,
            id_: int | None,
            date_begin: str | None,
            date_end: str | None,
            browser: str | None,
            os: str | None) -> Query:
        visits = None

        if date_end is not None and date_begin is not None:
            begin = int(f'{date_begin.replace("-", "")}000000')
            end = int(f'{date_end.replace("-", "")}235959')

            visits = (session.query(DatabaseVisit)
                      .filter(DatabaseVisit.time > begin)
                      .filter(DatabaseVisit.time < end)
                      )

        if browser is not None and browser != '':
            if browser not in identifier.BROWSERS:
                visits = visits.filter(
                    DatabaseVisit.user_agent.contains(browser)
                )
            else:
                visits = visits.filter(DatabaseVisit.browser == browser)
        if browser is not None and os != '':
            if os not in identifier.OS:
                visits = visits.filter(
                    DatabaseVisit.user_agent.contains(os)
                )
            else:
                visits = visits.filter(DatabaseVisit.os == os)
        if id_ is not None:
            visits = visits.filter(DatabaseVisit.id == id_)

        return visits
