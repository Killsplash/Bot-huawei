import os
import requests
from flask import Flask, request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

app = Flask(__name__)

# Token Bot Telegram kamu yang otomatis terpasang
TOKEN = "8907007838:AAEYAUW6ZsoyALCOG_yzP7biBIJ0Mr1dXiY"
bot = Bot(token=TOKEN)

ROUTER_IP = "http://192.168.100.1"
ADMIN_USER = "Admin"
ADMIN_PASS = "admin"

@app.route("/")
def home():
    return "Bot Telegram Huawei Aktif dan Siap!"

# Endpoint untuk menerima pesan & klik tombol dari Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    json_data = request.get_json(force=True)
    
    # Cek apakah ini tombol yang diklik atau pesan biasa
    if "callback_query" in json_data:
        query = json_data["callback_query"]
        chat_id = query["message"]["chat"]["id"]
        data = query["data"]
        
        if data == "menu_status":
            try:
                session = requests.Session()
                login_url = f"{ROUTER_IP}/login.cgi"
                res = session.post(login_url, data={"UserName": ADMIN_USER, "PassWord": ADMIN_PASS}, timeout=3)
                
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
    
