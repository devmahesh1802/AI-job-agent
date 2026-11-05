import os,requests,hashlib
S=requests.Session(); S.headers["User-Agent"]="MaheshJobSearch/1.0"
def row(src,title,company,loc,date,desc,url):
 if not url:return None
 return {"external_id":hashlib.sha256(url.encode()).hexdigest(),"title":title or "Untitled","company":company or "Not listed","location":loc or "Not specified","source":src,"posted_at":date or "Date unavailable","description":(desc or "")[:15000],"url":url}
def remotive():
 out=[]
 # Search broad all-role terms, not only software titles.
 for q in ["graduate","junior","entry level","associate","trainee","software","analyst","support"]:
  try:
   js=S.get("https://remotive.com/api/remote-jobs",params={"search":q},timeout=25).json().get("jobs",[])
   out += [z for x in js if (z:=row("Remotive",x.get("title"),x.get("company_name"),x.get("candidate_required_location"),x.get("publication_date"),x.get("description"),x.get("url")))]
  except Exception as e: print("Remotive",e)
 return out
def arbeitnow():
 out=[]
 try:
  for x in S.get("https://www.arbeitnow.com/api/job-board-api",timeout=25).json().get("data",[]):
   out.append(row("Arbeitnow",x.get("title"),x.get("company_name"),x.get("location"),x.get("created_at"),x.get("description"),x.get("url")))
 except Exception as e: print("Arbeitnow",e)
 return [x for x in out if x]
def adzuna():
 out=[]; aid=os.getenv("ADZUNA_APP_ID"); key=os.getenv("ADZUNA_APP_KEY")
 if not aid or not key:return out
 countries=os.getenv("ADZUNA_COUNTRIES","in,gb,fr,de,nl,ie,be").split(",")
 terms=["graduate","junior","entry level","associate","trainee","developer","analyst","support"]
 for country in countries:
  for q in terms:
   try:
    data=S.get(f"https://api.adzuna.com/v1/api/jobs/{country.strip()}/search/1",params={"app_id":aid,"app_key":key,"results_per_page":50,"what":q,"sort_by":"date"},timeout=25).json()
    for x in data.get("results",[]):
     z=row("Adzuna",x.get("title"),(x.get("company") or {}).get("display_name"),(x.get("location") or {}).get("display_name"),x.get("created"),x.get("description"),x.get("redirect_url"))
     if z:out.append(z)
   except Exception as e:print("Adzuna",country,e)
 return out
def jooble():
 out=[]; key=os.getenv("JOOBLE_API_KEY")
 if not key:return out
 for loc in os.getenv("JOOBLE_LOCATIONS","India,France,Germany,Netherlands,Ireland,Remote").split(","):
  for q in ["graduate","junior","entry level","associate","trainee","jobs"]:
   try:
    data=S.post(f"https://jooble.org/api/{key}",json={"keywords":q,"location":loc.strip()},timeout=25).json()
    for x in data.get("jobs",[]):
     z=row("Jooble",x.get("title"),x.get("company"),x.get("location"),x.get("updated"),x.get("snippet"),x.get("link"))
     if z:out.append(z)
   except Exception as e:print("Jooble",loc,e)
 return out
def all_jobs():
 allrows=remotive()+arbeitnow()+adzuna()+jooble()
 seen={}
 for x in allrows: seen[x["external_id"]]=x
 return list(seen.values())
