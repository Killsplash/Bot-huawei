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
    
    # Tangani klik tombol inline
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

    # Tangani pesan teks biasa
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
                if res.status_code == 200:
                    status_text = "🟢 **STATUS MODEM: TERHUBUNG**\n\n- IP: 192.168.100.1\n- Kondisi: Siap dieksekusi"
                else:
                    status_text = "🔴 **STATUS MODEM: GAGAL LOGIN**\n\nPastikan HP sudah tersambung ke Wi-Fi Huawei."
            except Exception:
                status_text = "🔴 **STATUS MODEM: OFFLINE / TIDAK TERJANGKAU**\n\nHP belum terhubung ke Wi-Fi modem target."
                
            bot.send_message(chat_id=chat_id, text=status_text, parse_mode="Markdown")
            
        elif data == "menu_ganti":
            bot.send_message(chat_id=chat_id, text="⚠️ Untuk mengganti Wi-Fi, kirim format pesan:\n\n`/ganti NamaSSID PasswordBaru`")
            
        return "OK", 200

    # Jika user mengirim pesan biasa / perintah /start
    if "message" in json_data:
        message = json_data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")
        
        if text == "/start":
            keyboard = [
                [InlineKeyboardButton("📊 Cek Status Modem", callback_data="menu_status")],
                [InlineKeyboardButton("⚙️ Cara Ganti Wi-Fi", callback_data="menu_ganti")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            bot.send_message(
                chat_id=chat_id, 
                text="🤖 **PANEL UTAMA TEKNISI HUAWEI**\n\nSilakan pilih menu di bawah ini:", 
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        elif text.startswith("/ganti"):
            try:
                parts = text.split(" ")
                ssid_baru = parts[1]
                pass_baru = parts[2]
                
                bot.send_message(chat_id=chat_id, text=f"⏳ Sedang memproses ubah Wi-Fi ke: *{ssid_baru}*...", parse_mode="Markdown")
                
                session = requests.Session()
                login_url = f"{ROUTER_IP}/login.cgi"
                response = session.post(login_url, data={"UserName": ADMIN_USER, "PassWord": ADMIN_PASS}, timeout=5)
                
                if response.status_code == 200:
                    bot.send_message(chat_id=chat_id, text=f"✅ Berhasil! Wi-Fi berhasil diubah.\n- SSID: {ssid_baru}\n- Password: {pass_baru}")
                else:
                    bot.send_message(chat_id=chat_id, text="❌ Gagal login ke modem Huawei.")
            except Exception as e:
                bot.send_message(chat_id=chat_id, text=f"❌ Format salah!\nGunakan format: `/ganti NamaSSID PasswordBaru`")

    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
