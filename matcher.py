import re
def clean(s): return re.sub(r"[^a-z0-9+#. ]"," ",(s or "").lower())
def match(job,profile):
 text=clean(job["title"]+" "+job["description"])
 skills=profile.get("skills",[])
 found=[s for s in skills if clean(s).strip() and clean(s) in text]
 missing=[s for s in skills if s not in found]
 # Score is resume keyword evidence, not an employer ATS score.
 score=round(100*len(found)/max(1,min(12,len(skills))))
 title=clean(job["title"])
 if any(w in title for w in ["senior","lead","principal","director","manager"]): score=max(0,score-20)
 return score,found,missing
