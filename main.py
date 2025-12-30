from flask import Flask, request, jsonify
import requests
import os
import threading
import time

app = Flask(__name__)

# 환경변수 설정
TOKEN = os.environ.get('TELEGRAM_TOKEN')
# Render 배포 후 생성되는 본인의 URL (예: https://my-bot.onrender.com)
SELF_URL = os.environ.get('SELF_URL') 

@app.route('/')
def home():
    return "Render Bot is Awake!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        # 답장 보내기
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": f"Render 봇 응답: {text}"})
    
    return "ok", 200

# --- Keep-alive 로직 시작 ---
def keep_alive():
    """10분마다 자신의 홈 페이지에 접속하여 서버가 잠들지 않게 합니다."""
    while True:
        try:
            if SELF_URL:
                requests.get(SELF_URL)
                print("Self-ping successful. Staying awake!")
            else:
                print("SELF_URL not set. Skipping self-ping.")
        except Exception as e:
            print(f"Self-ping failed: {e}")
        
        # 10분(600초) 대기
        time.sleep(600)

# 백그라운드 스레드로 실행
if SELF_URL:
    threading.Thread(target=keep_alive, daemon=True).start()
# --- Keep-alive 로직 끝 ---

if __name__ == "__main__":
    # Render는 PORT 환경변수를 자동으로 부여합니다.
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)