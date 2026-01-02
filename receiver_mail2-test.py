import time
import signal
import sys
from aiosmtpd.controller import Controller
import requests
from email.parser import BytesParser
from email.policy import default

# ====== KONFIG TELEGRAM ======
TELEGRAM_BOT_TOKEN = "8470745901:AAFCqAd-PiOmkBlaAESEBKELQeuvCEFTXFM"  # <-- ganti!
TELEGRAM_CHAT_ID = "1084308578"
# ==============================

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)

class MyHandler:
    async def handle_DATA(self, server, session, envelope):
        # RAW BODY EMAIL (TANPA HEADER)
        raw_text = envelope.content.decode(errors="ignore").strip()

        # Bersihkan kemungkinan newline berlebih
        raw_text = raw_text.replace("\r\n", "\n").strip()

        print("=== RAW ALERT RECEIVED ===")
        print(raw_text)

        # KIRIM KE TELEGRAM APA ADANYA
        send_telegram(raw_text)

        print("📨 Raw alert forwarded to Telegram")
        return '250 Message accepted for delivery'

        # Parse email agar subject & body bisa dipisah
        msg = BytesParser(policy=default).parsebytes(envelope.content)

        subject = msg["subject"]
        body = msg.get_body(preferencelist=('plain', 'html'))
        body_text = body.get_content() if body else "(no body)"



controller = Controller(MyHandler(), hostname='0.0.0.0', port=2525)
controller.start()
print("🚀 Listening on port 2525... (Press Ctrl+C to stop)")

def shutdown(sig, frame):
    print("\n🛑 Stopping SMTP server...")
    controller.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

while True:
    time.sleep(1)
