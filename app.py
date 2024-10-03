from flask import Flask, jsonify # type: ignore
import threading
import time
from plyer import notification  # type: ignore

app = Flask(__name__)

# 알림 제어 플래그
send_notifications = False

def notify_user():
    global send_notifications
    while True:
        if send_notifications:
            for _ in range(3):  # 3번의 알림을 표시
                notification.notify(
                    title="Alert",
                    message="자세를 교정하세요",
                    timeout=5
                )
                time.sleep(5)  # 각 알림 사이에 5초 대기

            # 1시간 대기 후 다음 알림 주기 시작
            time.sleep(30)  # 30초 대기
            send_notifications = True  # 다음 알림을 위해 비활성화
        else:
            time.sleep(1)  # 상태 확인 주기

@app.route('/notify', methods=['GET'])
def notify():
    global send_notifications
    send_notifications = True  # 알림 전송 시작
    return jsonify({"message": "알림이 시작되었습니다!"})

if __name__ == "__main__":
    # 알림 처리 스레드를 시작
    thread = threading.Thread(target=notify_user, daemon=True)
    thread.start()
    
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        print("서버가 종료됩니다.")
