# AI Job Search Engine v3

## Run locally (Windows)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
streamlit run app.py
```

## Cloud deployment
1. Push this folder to a private GitHub repository.
2. In Render, create a Blueprint and connect that repository.
3. Review `render.yaml`; choose a paid service with persistent disk.
4. Add Adzuna and Jooble API credentials as Render environment variables.
5. Deploy. The dashboard starts a daily 08:00 Asia/Kolkata search scheduler.

## Job source coverage
Included: Remotive and Arbeitnow public feeds; optional Adzuna and Jooble APIs.
This version does not directly scrape LinkedIn, Naukri, Indeed or Glassdoor. Use authorized partner APIs or licensed providers and comply with each platform's terms. Do not bypass login, CAPTCHA or anti-bot controls.
Firecrawl is connected to the user's ChatGPT session for research, but connector credentials cannot be transferred to this standalone app. Firecrawl app-side integration needs a separate API key and implementation.

## Matching
Keyword-overlap screening score based on the resume skills entered in Settings. It is not an employer ATS score. Review extracted skills. No automatic applications are submitted.
## Persistent data
SQLite is stored in `data/jobs.db`. Use one Render instance only while on SQLite. For horizontal scaling, migrate to PostgreSQL and a separate worker.
