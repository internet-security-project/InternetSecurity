# app.py
from flask import Flask, request, jsonify
from models import db, DayQuest

app = Flask(__name__)

# Oracle 데이터베이스 연결 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://system:1234@localhost:1521/xe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 데이터베이스 초기화
db.init_app(app)

# 퀘스트 추가 엔드포인트
@app.route('/add_quest', methods=['POST'])
def add_quest():
    data = request.json  # 요청 데이터 가져오기
    try:
        new_quest = DayQuest(
            dquest=data['dquest'],
            title=data['title'],
            description=data['description']
        )
        db.session.add(new_quest)
        db.session.commit()
        return jsonify({'message': 'Quest added successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# 모든 퀘스트 조회 엔드포인트
@app.route('/quests', methods=['GET'])
def get_quests():
    quests = DayQuest.query.all()
    return jsonify([{
        'id': quest.id,
        'dquest': quest.dquest,
        'title': quest.title,
        'description': quest.description
    } for quest in quests]), 200

# 특정 퀘스트 조회 엔드포인트
@app.route('/quests/<int:id>', methods=['GET'])
def get_quest(id):
    quest = DayQuest.query.get_or_404(id)
    return jsonify({
        'id': quest.id,
        'dquest': quest.dquest,
        'title': quest.title,
        'description': quest.description
    }), 200

# 퀘스트 삭제 엔드포인트
@app.route('/quests/<int:id>', methods=['DELETE'])
def delete_quest(id):
    quest = DayQuest.query.get_or_404(id)
    db.session.delete(quest)
    db.session.commit()
    return jsonify({'message': 'Quest deleted successfully!'}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
