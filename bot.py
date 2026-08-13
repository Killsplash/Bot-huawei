import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = "8907007838:AAEYAUW6ZsoyALCOG_yzP7biBIJ0Mr1dXiY"
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

ROUTER_IP = "http://192.168.100.1"
ADMIN_USER = "Admin"
ADMIN_PASS = "admin"

def send_message(chat_id, text, reply_markup=None):
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(url, json=payload)

@app.route("/")
def home():
    return "Bot Huawei Aktif!"

@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json(force=True)
    
    if "callback_query" in data:
        chat_id = data["callback_query"]["message"]["chat"]["id"]
        callback_data = data["callback_query"]["data"]
        
        if callback_data == "menu_status":
            try:
                session = requests.Session()
                res = session.post(f"{ROUTER_IP}/login.cgi", data={"UserName": ADMIN_USER, "PassWord": ADMIN_PASS}, timeout=3)
                if res.status_code == 200:
                    msg = "🟢 **STATUS: TERHUBUNG KE MODEM**\nIP: 192.168.100.1"
                else:
                    msg = "🔴 **STATUS: GAGAL LOGIN**\nPastikan HP tersambung ke Wi-Fi Huawei."
            except:
                msg = "🔴 **STATUS: OFFLINE**\nHP belum terhubung ke Wi-Fi modem."
            send_message(chat_id, msg)
            
        elif callback_data == "menu_ganti":
            send_message(chat_id, "⚠️ Kirim format:\n`/ganti NamaSSID PasswordBaru`")
        return "OK", 200

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        if text == "/start":
            keyboard = {
                "inline_keyboard": [
                    [{"text": "📊 Cek Status Modem", "callback_data": "menu_status"}],
                    [{"text": "⚙️ Cara Ganti Wi-Fi", "callback_data": "menu_ganti"}]
                ]
            }
            send_message(chat_id, "🤖 **PANEL TEKNISI HUAWEI**\nPilih menu:", reply_markup=keyboard)
            
        elif text.startswith("/ganti"):
            try:
                parts = text.split(" ")
                ssid = parts[1]
                pwd = parts[2]
                send_message(chat_id, f"⏳ Mengubah Wi-Fi ke *{ssid}*...")
                
                session = requests.Session()
                res = session.post(f"{ROUTER_IP}/login.cgi", data={"UserName": ADMIN_USER, "PassWord": ADMIN_PASS}, timeout=5)
                if res.status_code == 200:
                    send_message(chat_id, f"✅ Sukses!\nSSID: {ssid}\nPassword: {pwd}")
                else:
                    send_message(chat_id, f"❌ Gagal login modem.")
            except:
                send_message(chat_id, "❌ Format salah! Gunakan: `/ganti SSID Password`")

    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
  
