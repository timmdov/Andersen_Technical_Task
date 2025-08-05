import logging
import app.users.models  # noqa: F401
import app.tasks.models  # noqa: F401

from app.db.base import Base
from app.db.session import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Database tables creation")
    Base.metadata.create_all(bind=engine)
    logger.info("Tables created")

if __name__ == "__main__":
    main()
