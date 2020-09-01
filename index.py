from app import app, db
from app.models import User


@app.cli.command('first_init')
def first_init():
    db.create_all()
    user = User(username='Admin')
    user.set_password('Admin')
    db.session.add(user)
    db.session.commit()





