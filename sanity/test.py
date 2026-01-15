from db.session import engine
from db.base import Base
from models.user import User  # IMPORTANT: import model

Base.metadata.create_all(bind=engine)
