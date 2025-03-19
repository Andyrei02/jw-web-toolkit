from app.extensions import db

def create_db():
    """Initialize the database."""
    db.create_all()
