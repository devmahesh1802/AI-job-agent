import sqlite3
from pathlib import Path
from datetime import datetime,timezone
DB=Path("data/jobs.db"); DB.parent.mkdir(exist_ok=True)
def con():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def init_db():
 with con() as c:
  c.execute("""CREATE TABLE IF NOT EXISTS jobs(id INTEGER PRIMARY KEY, external_id TEXT UNIQUE,title TEXT,company TEXT,location TEXT,source TEXT,posted_at TEXT,description TEXT,url TEXT,match_score REAL,matched_skills TEXT,missing_skills TEXT,status TEXT DEFAULT 'Not Applied',notes TEXT,first_seen TEXT)""")
def upsert(rows):
 n=0; now=datetime.now(timezone.utc).isoformat()
 with con() as c:
  for x in rows:
   cur=c.execute("""INSERT OR IGNORE INTO jobs(external_id,title,company,location,source,posted_at,description,url,match_score,matched_skills,missing_skills,status,first_seen) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
    (x["external_id"],x["title"],x["company"],x["location"],x["source"],x["posted_at"],x["description"],x["url"],x["match_score"],x["matched_skills"],x["missing_skills"],"Not Applied",now))
   n+=cur.rowcount
 return n
def get_jobs():
 with con() as c: return [dict(r) for r in c.execute("SELECT * FROM jobs ORDER BY first_seen DESC")]
def update_status(i,s,n):
 with con() as c: c.execute("UPDATE jobs SET status=?,notes=? WHERE id=?",(s,n,i))
def get_stats():
 with con() as c:
  return {"total":c.execute("SELECT COUNT(*) FROM jobs").fetchone()[0],"today":c.execute("SELECT COUNT(*) FROM jobs WHERE date(first_seen)=date('now')").fetchone()[0],"excellent":c.execute("SELECT COUNT(*) FROM jobs WHERE match_score>=90").fetchone()[0],"not_applied":c.execute("SELECT COUNT(*) FROM jobs WHERE status='Not Applied'").fetchone()[0]}
