from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base  # think this is the Correct import for SQLAlchemy 2.0
from sqlalchemy.orm import sessionmaker  # For session management

# Database URL - creates a local file 'users.db' in the current directory
SQLITE_DATABASE_URL = "sqlite:///./users.db"

# Create engine and session
engine = create_engine(SQLITE_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# Define the User model/table (updated with new fields)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)  # New: unique email field
    country = Column(String)  # New: country field
    state = Column(String)  # New: state field
    hashed_password = Column(String)

# Create/update the table (I need this to run  to apply changes)
Base.metadata.create_all(bind=engine)