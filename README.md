# senior-wellbeing-analytics

a person-centered decision matrix built with data analytics for choosing which programs actually earn the resources they're given in for profit social enterprises.

Social enterprises account for a large umber of a lack of productivity and profitability based on the organization's goals in alignment with profitability, they face a real constraint: limited staff, limited time, in addition to already limited profit and resources — spending those resources on the wrong programming, not because they cannot choose between options, but rather because the programs get built around precedent and assumption instead of the people they're meant to serve. This isn't a data problem. It's a broken decision system: organizations choose confidently, and choose wrong, because the input feeding that decision was never built around the person on the receiving end.

The deeper issue is how "impact" itself gets defined. A program can be genuinely beneficial to someone's wellbeing in the long run and still fail completely — because if it isn't something a senior actually wants to engage with, the benefit never happens. Wellbeing and engagement have to be measured together, or "impact" is just a story an organization tells itself. That's what makes this human-centered, not just data-driven: it isn't about feeding more data into the same broken system — it's about building a system-centered, person-centered method for choosing which programs actually earn the resources they're given, balancing profitability with purpose and real reach.

This project, anchored by Amari Eden Living and Programs, exists to build that method — home by home, program by program — so that resource-allocation decisions are made on evidence of what actually works, not on convenience or tradition.

This mission statement was drafted with assistance from AI (Claude, Anthropic), synthesized directly from the author's own reasoning and language developed across extended discussion during this project's planning — see the AI Disclosure Form for the full account of how AI was used throughout this project.

## Live Deployments

- **Stakeholder Dashboard:** https://senior-wellbeing-analytics-kwppqd6woxnezaznmga2z8.streamlit.app/
- **Prediction API (interactive docs):** https://analytics-for-social-enterprises.onrender.com/docs#/default/predict_predict_post

The API's free-tier hosting spins down after periods of inactivity; the first request after idle time may take a few seconds to respond while it wakes up.

## Repository Structure

```
senior-wellbeing-analytics/
├── data/
│   └── raw/               # untouched CQC source files, with provenance README
├── notebooks/             # exploratory analysis
├── dashboards/             # stakeholder dashboard app, model, and data
├── src/
│   ├── etl/                # pipeline DAG, anonymization check, privacy audit logging
│   ├── tests/               # automated test suite (CI/CD)
│   ├── app_v2.py            # FastAPI prediction service
│   └── api_demo.py          # scripted demonstration of the API
├── monitoring/              # monitoring dashboard (performance & fairness over time)
├── docs/                   # governance framework, GX validation suite, bias detection
│                           # report, audit log, Model Card, Ethical AI Framework
├── .github/workflows/       # CI/CD pipeline (GitHub Actions)
├── docker-compose.yml       # multi-container orchestration (API, dashboard, monitoring)
├── README.md
└── requirements.txt
```

**Note on repository evolution:** Module 1-2 planning explored CDC BRFSS and Yelp Open Dataset as potential sources (see prior commit history and the Vision Document); Module 3 pivoted to UK Care Quality Commission (CQC) data as a proof-of-concept, given data-access constraints on Canadian/Alberta-specific senior programming data within the project timeline. Module 4 further reframed the predictive model from administrative facility attributes to CQC quality-of-care domain scores, improving both accuracy and fairness. See `docs/` and the Integrated Report for the full rationale.

## Data Sources

- **CQC (Care Quality Commission)** — Care directory with ratings, cqc.gov.uk. Real, non-synthetic, publicly downloadable. Used as the proof-of-concept dataset throughout; the pipeline and modeling architecture are designed to transfer to Amari Eden's own program data once collected.
- Supporting literature (not modeling data): Towers et al. (2021) MiCareHQ study on CQC ratings and quality of life; Bath and North East Somerset Council's CQC domain interpretation; Tanuwidjaja (2023) on ML model deployment for data analysts; Odegua (2020) on applied machine learning, consulted while reviewing alternative algorithms (KNN).
- Prior candidate sources evaluated but not used in the final pipeline: CDC BRFSS, Yelp Open Dataset, CIHI, CMS Nursing Home Compare, NCI-AD, UCI wearable sensor data — see AI Disclosure Form for the evaluation process.

## Setup

```bash
git clone <your-repo-url>
cd senior-wellbeing-analytics
pip install -r requirements.txt
```

Large raw files exceeding GitHub's 25MB limit are stored as filtered extracts in `data/raw/`, with full provenance and re-download instructions in `data/raw/README.md`.

### Running locally with Docker Compose

```bash
docker compose up --build
```

This starts three services: the prediction API (port 8000), the stakeholder dashboard (port 8501), and the monitoring dashboard (port 8502).

### Running the test suite

```bash
cd src
pip install -r requirements.txt pytest httpx
pytest tests/ -v
```

## Usage & Reuse

This repository is shared publicly for academic transparency and portfolio purposes. Viewing and running the code locally is permitted. Reuse, modification, or redistribution is not authorized without the author's permission — no open-source license is attached, and all rights are reserved by default.

## Project Status

Built as part of BAN6800's module sequence: Vision Document (Module 1) → Project Overview & Planning (Module 2) → Data Pipeline (Module 3) → Predictive Modeling & XAI (Module 4) → Stakeholder Dashboard (Module 5) → Final Integrated Project with CI/CD, containerized deployment, and monitoring (Module 6, current state).
