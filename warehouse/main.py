import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from database_setup import create_warehouse_structure
from load_to_warehouse import load

load_dotenv()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

engine = create_engine(
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST', 'localhost')}:5434"
    f"/{os.getenv('DB_NAME')}"
)

create_warehouse_structure()
load(engine, log)