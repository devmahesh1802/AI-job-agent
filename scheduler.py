from providers import all_jobs
from matcher import match
from database import upsert
from datetime import datetime,timezone,timedelta
def run_search(profile):
 raw=all_jobs(); cutoff=datetime.now(timezone.utc)-timedelta(days=int(profile.get("days_back",7))); rows=[]
 for x in raw:
  try:
   d=datetime.fromisoformat(x["posted_at"].replace("Z","+00:00"))
   if d.tzinfo is None:d=d.replace(tzinfo=timezone.utc)
   if d<cutoff:continue
  except Exception: pass
  score,found,missing=match(x,profile)
  if score<int(profile.get("minimum_score",35)):continue
  x.update(match_score=score,matched_skills=", ".join(found),missing_skills=", ".join(missing))
  rows.append(x)
 rows.sort(key=lambda x:x["match_score"],reverse=True)
 rows=rows[:50]
 return {"processed":len(rows),"new":upsert(rows)}
