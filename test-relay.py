import smtplib 
from email.mime.text import MIMEText 

msg = MIMEText("Ini test alert manual ke Telegram.") 
msg["Subject"] = "Test Relay Telegram" 
msg["From"] = "edge.d@local" 
msg["To"] = "omar.d@edge.id" 

with smtplib.SMTP("127.0.0.1", 2525) as s: s.send_message(msg) 
print("Email test dikirim ke relay.")
