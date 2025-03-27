from app.extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class WorkbooksList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(512), nullable=False)
    img = db.Column(db.String(512), nullable=False)
    
    def __repr__(self):
        return f"WorkbooksList('{self.title}', '{self.link}')"


class Workbook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    data = db.Column(db.JSON, nullable=False)
    
    def __repr__(self):
        return f"Workbook('{self.title}')"


from app.extensions import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
