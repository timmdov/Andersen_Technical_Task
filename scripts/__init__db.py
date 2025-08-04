import logging
import app.users.models  # noqa: F401
import app.tasks.models  # noqa: F401

from app.db.base import Base
from app.db.session import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Creating database tables (if they don't exist)...")
    Base.metadata.create_all(bind=engine)
    logger.info("Done. Tables should now exist.")

if __name__ == "__main__":
    main()
