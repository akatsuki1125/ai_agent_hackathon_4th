import requests
import os 
from datetime import datetime

WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

#message = "hello world from PYTHON"
#date = "every day 17:00" 日付は cron で指定して送りましょう
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("8.8.8.8", 80))
local_ip = sock.getsockname()
sock.close()
print(local_ip[0])

message = {"text": f"\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} \nhello world from PYTHON !\nmy_ip_address: {str(local_ip[0])}:{str(local_ip[1])}"}
status = requests.post(WEBHOOK_URL, json=message) 
print(status.status_code, status.text)

log_file_name = "post_check.log"
with open(log_file_name, "a") as f:
    f.write(f"\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: {status.status_code} {status.text}\nip_address: {local_ip[0]}")