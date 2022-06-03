from database.tables import engine, Base

Base.metadata.create_all(engine)
