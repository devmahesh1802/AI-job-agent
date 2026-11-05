import streamlit as st, pandas as pd, json
from pathlib import Path
from dotenv import load_dotenv
from database import init_db, get_jobs, get_stats, update_status
from scheduler import run_search
from apscheduler.schedulers.background import BackgroundScheduler
load_dotenv()
st.set_page_config(page_title="AI Job Search Engine", page_icon="🎯", layout="wide")
init_db()
PROFILE=Path("data/profile.json")
if not PROFILE.exists():
    PROFILE.write_text(json.dumps({"name":"Ponugoti Mahesh","skills":["Java","Spring Boot","SQL","REST APIs","Angular","JavaScript","C#",".NET","AWS","Docker","Kubernetes","Terraform","Jenkins","Python","Linux","Git","MySQL","SQL Server"],"experience":"Software development experience at Genpact; verify exact dates and responsibilities against the uploaded resume.","education":"B.Tech Computer Science and Engineering","locations":["India","France","Germany","Netherlands","Ireland","Belgium","Remote"],"minimum_score":35,"days_back":7},indent=2))
def profile(): return json.loads(PROFILE.read_text())
@st.cache_resource
def scheduler():
    s=BackgroundScheduler(timezone="Asia/Kolkata")
    s.add_job(lambda: run_search(profile()),"cron",hour=8,minute=0,id="daily",replace_existing=True,max_instances=1)
    s.start()
    return s
scheduler()
st.title("🎯 AI Job Search Engine")
st.caption("All-role job discovery • Resume match • Apply links • Application tracker")
st.info("This version searches configured public feeds and APIs. Firecrawl is connected to ChatGPT for live research, but its ChatGPT connector authentication is separate from this hosted app; add a Firecrawl API credential separately if you want direct app-side Firecrawl calls.")
with st.sidebar:
    page=st.radio("Navigation",["Dashboard","All Jobs","Application Tracker","Settings"])
    if st.button("Search jobs now",type="primary"):
        with st.spinner("Searching job sources..."):
            result=run_search(profile())
        st.success(f"Processed {result['processed']} relevant listings; {result['new']} are new.")
        st.rerun()
jobs=get_jobs(); df=pd.DataFrame(jobs)
if not df.empty:
    df["match_score"]=pd.to_numeric(df["match_score"],errors="coerce").fillna(0)
if page=="Dashboard":
    stats=get_stats(); a,b,c,d=st.columns(4)
    a.metric("Jobs saved",stats["total"]); b.metric("New today",stats["today"]); c.metric("90%+ matches",stats["excellent"]); d.metric("Not applied",stats["not_applied"])
    st.subheader("Best matches")
    if df.empty: st.warning("No jobs saved yet. Run a search or configure API keys.")
    else:
        view=df.sort_values(["match_score","posted_at"],ascending=[False,False]).head(50)
        st.dataframe(view[["title","company","location","source","posted_at","match_score","url","status"]],hide_index=True,use_container_width=True,
          column_config={"url":st.column_config.LinkColumn("Apply link",display_text="Open job")})
elif page in ["All Jobs","Application Tracker"]:
    st.subheader(page)
    if df.empty: st.info("No jobs saved yet.")
    else:
        if page=="Application Tracker": df=df[df.status!="Not Applied"]
        q=st.text_input("Filter by title/company/location")
        if q: df=df[df.apply(lambda r:q.lower() in " ".join(str(r.get(k,"")) for k in ["title","company","location"]).lower(),axis=1)]
        st.dataframe(df.sort_values("match_score",ascending=False)[["title","company","location","source","posted_at","match_score","url","status","notes"]],hide_index=True,use_container_width=True,
            column_config={"url":st.column_config.LinkColumn("Apply link",display_text="Open job")})
        st.markdown("**Update application status**")
        ids=df.id.tolist()
        if ids:
            jid=st.selectbox("Job",ids,format_func=lambda i:f"{df[df.id==i].iloc[0].company} — {df[df.id==i].iloc[0].title}")
            status=st.selectbox("Status",["Not Applied","Interested","Applied","Assessment","Interview","Rejected","Offer Received","Expired"])
            note=st.text_input("Notes")
            if st.button("Save status"): update_status(jid,status,note); st.success("Saved"); st.rerun()
else:
    st.subheader("Resume & search settings")
    p=profile()
    st.write("Profile seeded with Java/software/cloud skills from your recent resume context. Upload the exact latest PDF to extract and verify its contents.")
    up=st.file_uploader("Upload resume PDF/DOCX/TXT",type=["pdf","docx","txt"])
    if up and st.button("Extract resume skills"):
        from resume import extract_text, extract_skills
        p["skills"]=extract_skills(extract_text(up.getvalue(),up.name))
        PROFILE.write_text(json.dumps(p,indent=2))
        st.success("Extracted skill list saved. Please review below.")
        st.rerun()
    with st.form("settings"):
        skills=st.text_area("Resume skills (comma-separated)",", ".join(p.get("skills",[])))
        locations=st.text_area("Target locations (comma-separated)",", ".join(p.get("locations",[])))
        days=st.selectbox("Look back", [1,3,7,14,30],index=[1,3,7,14,30].index(p.get("days_back",7)))
        score=st.slider("Minimum resume match",0,100,p.get("minimum_score",35))
        if st.form_submit_button("Save"):
            p.update(skills=[x.strip() for x in skills.split(",") if x.strip()],locations=[x.strip() for x in locations.split(",") if x.strip()],days_back=days,minimum_score=score)
            PROFILE.write_text(json.dumps(p,indent=2)); st.success("Saved")
    st.markdown("**Optional API credentials**")
    st.code("ADZUNA_APP_ID=...\\nADZUNA_APP_KEY=...\\nJOOBLE_API_KEY=...\\nFIRECRAWL_API_KEY=...",language="bash")
    st.caption("Set secrets in your cloud host's environment settings, not in source code. Firecrawl API support is not yet wired into this hosted app; the connected ChatGPT Firecrawl plugin is available for searches in this conversation.")
