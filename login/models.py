from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Sequence

db = SQLAlchemy()

class DDuser(db.Model):
    __tablename__ = 'users'  # Oracle의 경우 테이블 이름을 명시적으로 지정
    id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)  # 시퀀스 사용
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    phon = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(80), nullable=True)

    def __repr__(self):
        return f'<DDuser {self.username}>'
