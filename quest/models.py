# models.py
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy 인스턴스 생성
db = SQLAlchemy()

class DayQuest(db.Model):
    __tablename__ = 'QUESTS'  # 테이블 이름 정의 (대소문자 구분하지 않음)

    id = db.Column(db.Integer, primary_key=True)  # 자동 증가 ID, 시퀀스와 트리거에 의해 관리됨
    dquest = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<DayQuest {self.title}>'
