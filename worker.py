import json
from pathlib import Path
from apscheduler.schedulers.blocking import BlockingScheduler
from scheduler import run_search
def run():
 p=json.loads(Path("data/profile.json").read_text()); print(run_search(p))
if __name__=="__main__":
 s=BlockingScheduler(timezone="Asia/Kolkata"); s.add_job(run,"cron",hour=8,minute=0); print("Daily job search: 08:00 IST"); s.start()
