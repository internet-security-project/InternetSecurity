from flask import Flask, jsonify, request
from flask_cors import CORS
from models import DDuser, db
from werkzeug.security import generate_password_hash, check_password_hash  # 비밀번호 암호화

app = Flask(__name__)
CORS(app)

# Oracle DB 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://system:1234@localhost:1521/xe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 데이터베이스 초기화
db.init_app(app)

# 테이블 생성 (존재하지 않는 경우)
with app.app_context():
    db.create_all() 

# 회원가입 부분
@app.route('/register', methods=['POST'])
def register():
    data = request.json  
    if not data:
        return jsonify({'message': '잘못된 요청'})

    print("Received data:", data)
    
    username = data.get('username')
    password = data.get('password')
    phon = data.get('phon')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({'message': '필수 입력 값이 없습니다.'}), 400

    existing_user = DDuser.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': '중복된 사용자 이름입니다.'}), 409

    hashed_password = generate_password_hash(password)  # 비밀번호 암호화
    new_user = DDuser(username=username, password=hashed_password, phon=phon, email=email)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': '회원가입 성공!!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '회원가입 실패', 'error': str(e)}), 500

# 로그인 부분
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return jsonify({'message': '잘못된 요청'})

    print("Received data:", data)
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': '필수 입력 값이 없습니다.'}), 400

    user = DDuser.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return jsonify({'message': '로그인 성공!!'}), 200  
    else:
        return jsonify({'message': '로그인 실패'}), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
