from datetime import datetime
from smartCity import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    cart = db.Column(db.String(90000), nullable = False)
    ItemsInCart = db.Column(db.Integer(), nullable = False)

    def levelUp(self):
        editUser = User.query.filter_by(username=self.username).first()
        editUser.experience -= 100
        editUser.level += 1
        dbsession.commit()

    def giveExp(self, expGot):
        editUser = User.query.filter_by(username=self.username).first()
        editUser.experience += expGot
        db.session.commit()
        if editUser.experience >= 100:
            levelUp()


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.experience}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable = False, default = "")
    stock = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
class Transport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    qrCode = db.Column(db.String(20), nullable=False)

    def _repr__(self):
        return f"Transport('{self.name}', '{self.price}', '{self.qrCode}')"
