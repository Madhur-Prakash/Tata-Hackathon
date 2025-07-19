import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import Base, engine
from models import RouteHistory  # Import your SQLAlchemy models here

# Create all tables
Base.metadata.create_all(bind=engine)
print("✅ Database tables created successfully.")
