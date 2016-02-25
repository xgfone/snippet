# encoding: utf8
from __future__ import print_function

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name,
                self.fullname, self.password)


engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
session.add(ed_user)
session.add_all([
    User(name='wendy', fullname='Wendy Williams', password='foobar'),
    User(name='mary', fullname='Mary Contrary', password='xxg527'),
    User(name='fred', fullname='Fred Flinstone', password='blah')])
session.commit()

print(session.query(User).offset(1).limit(2).all())
# SELECT users.id AS users_id, users.name AS users_name, users.fullname AS users_fullname, \
# users.password AS users_password FROM users LIMIT 2 OFFSET 1

for row in session.query(User, User.name).all():
    print(row.User, row.name)

#ed_user.name = "ed2"
#session.commit()
with session.begin(subtransactions=True):
    ed_user.name = "ed2"

session.delete(ed_user)
