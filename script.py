from app.models.user import User
from app.extensions import db
from datetime import datetime, time

def seed():
    clear_data()
    
    user = User(firstname="Barış", lastname="Yıldırım", email="baris.yildirim@ug.bilkent.edu.tr", birthdate=datetime.now(), phone_number="1231231231", password="test123")
    db.session.add(user)
    db.session.commit()

def clear_data():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        db.session.execute(table.delete())
    db.session.commit()