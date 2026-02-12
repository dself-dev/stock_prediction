from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from api.database import User  # Import from the 'api' subfolder

# Connect to  DB (relative path from root)
engine = create_engine("sqlite:///users.db")
session = Session(engine)

# Query all users
stmt = select(User)
users = session.execute(stmt).scalars().all()

# Print all the user with hashed passwords... i forgot all passwords lol wtf
if not users:
    print("No users found in the database.")
else:
    for user in users:
        print(f"ID: {user.id}")
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Country: {user.country}")
        print(f"State: {user.state}")
        print(f"Hashed Password: {user.hashed_password}")
        print("---")

session.close()