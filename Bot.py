import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Konfigurasi Target Modem Huawei
ROUTER_IP = "http://192.168.100.1"
ADMIN_USER = "Admin"
ADMIN_PASS = "admin"

@app.route("/")
def home():
    return "Bot Telegram Huawei Aktif!"

@app.route("/ganti-wifi", methods=["POST"])
def ganti_wifi():
    data = request.json
    ssid_baru = data.get("ssid")
    pass_baru = data.get("password")

    # 1. Proses Login ke Modem Huawei
    session = requests.Session()
    
    # Catatan: Endpoint login Huawei bisa bervariasi tergantung firmware, 
    # umumnya menggunakan /html/index.html atau langsung ke login.cgi
    login_url = f"{ROUTER_IP}/login.cgi"
    payload_login = {
        "UserName": ADMIN_USER,
        "PassWord": ADMIN_PASS
    }
    
    try:
        # Kirim permintaan login
        response = session.post(login_url, data=payload_login, timeout=5)
        
        if response.status_count == 200 or "index" in response.text.lower():
            # 2. Kirim perintah ubah SSID & Password Wi-Fi
            # (Sesuaikan URL path settingan wireless modem Huawei kamu di lapangan)
            config_url = f"{ROUTER_IP}/boaform/admin/formWlan" 
            payload_config = {
                "ssid": ssid_baru,
                "wpaKey": pass_baru
            }
            
            res_config = session.post(config_url, data=payload_config)
            if res_config.status_code == 200:
                return {"status": "success", "message": f"Wi-Fi berhasil diganti ke: {ssid_baru}"}
            else:
                return {"status": "failed", "message": "Gagal menyimpan konfigurasi Wi-Fi."}
        else:
            return {"status": "failed", "message": "Gagal login ke modem (Username/Password salah)."}
            
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
  
