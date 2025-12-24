import requests
import os 
from datetime import datetime

WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

#message = "hello world from PYTHON"
#date = "every day 17:00" 日付は cron で指定して送りましょう

message = {"text": f"\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} \nhello world from PYTHON !"}
status = requests.post(WEBHOOK_URL, json=message) 
print(status.status_code, status.text)

log_file_name = "post_check.log"
with open(log_file_name, "a") as f:
    f.write(f"\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: {status.status_code} {status.text}")