# senior-wellbeing-analytics

a person-centered decision matrix built with data analytics for choosing which programs actually earn the resources they're given in for profit social enterprises.

Social enterprises account for a large umber of a lack of productivity and profitability based on the organization's goals in alignment with profitability, they face a real constraint: limited staff, limited time, in addition to already limited profit and resources — spending those resources on the wrong programming, not because they cannot choose between options, but rather because the programs get built around precedent and assumption instead of the people they're meant to serve. This isn't a data problem. It's a broken decision system: organizations choose confidently, and choose wrong, because the input  feeding that decision was never built around the person on the receiving end.

The deeper issue is how "impact" itself gets defined. A program can be genuinely beneficial to someone's wellbeing in the long run and still fail completely — because if it isn't something a senior actually wants to engage with, the benefit never happens. Wellbeing and engagement have to be measured together, or "impact" is just a story an organization tells itself. That's what makes this human-centered, not just data-driven: it isn't about feeding more data into the same broken system — it's about building a system-centered, person-centered method for choosing which programs actually earn the resources they're given, balancing profitability with purpose and real reach.

This project, anchored by Amari Eden Living and Programs, exists to build that method — home by home, program by program — so that resource-allocation decisions are made on evidence of what actually works, not on convenience or tradition.

This mission statement was drafted with assistance from AI (Claude, Anthropic), synthesized directly from the author's own reasoning and language developed across extended discussion during this project's planning — see the AI Disclosure Form for the full account of how AI was used throughout this project.

## Repository Structure

senior-wellbeing-analytics/
├── data/
│   ├── brfss/
│   │   ├── raw/          # untouched BRFSS extracts as downloaded
│   │   └── processed/    # cleaned, module-filtered BRFSS data
│   └── yelp/
│       ├── raw/          # untouched Yelp Open Dataset extracts
│       └── processed/    # cleaned, category-filtered, sentiment-scored reviews
├── notebooks/             # exploratory analysis
├── src/
│   ├── etl/               # extraction and transformation scripts
│   ├── models/
│   │   ├── diagnostic_brfss/      # regression / Random Forest feature-importance analysis
│   │   └── diagnostic_sentiment/  # sentiment analysis on Yelp review text
│   └── prescriptive/      # combines both diagnostic outputs into program-type recommendations
├── dashboards/             # Power BI files
├── docs/                   # vision document, AI disclosure, references, diagrams
├── README.md
└── requirements.txt
```

**Why two parallel diagnostic folders:** BRFSS (structured survey data) and Yelp reviews (unstructured text) are analyzed with different techniques and are never merged into a single dataset — there is no shared identifier linking a BRFSS respondent to a Yelp reviewer. Both diagnostic outputs feed into `src/prescriptive/`, which is the layer that actually produces the program-type ranking used to guide resource allocation.

## Data Sources

- **CDC BRFSS** — Behavioral Risk Factor Surveillance System, cdc.gov/brfss. Real, non-synthetic, publicly downloadable.
- **Yelp Open Dataset** — filtered to health, wellness, and senior-service categories. Real, non-synthetic, publicly downloadable at business.yelp.com/data/resources/open-dataset.
- Supporting literature (not modeling data): National Institute on Ageing's Ageing in Canada Survey, and SHARE (Survey of Health, Ageing and Retirement in Europe), cited for context — SHARE's raw data is not used directly in this project due to its scientific-use-only, non-commercial licensing terms.

## Setup

```bash
git clone <your-repo-url>
cd senior-wellbeing-analytics
pip install -r requirements.txt
```

Raw data files are not included in this repository (see `.gitignore`) and must be downloaded separately from the sources listed above into their respective `data/*/raw/` folders.

## Usage & Reuse

This repository is shared publicly for academic transparency and portfolio purposes. Viewing and running the code locally is permitted. Reuse, modification, or redistribution is not authorized without the author's permission — no open-source license is attached, and all rights are reserved by default.

## Project Status

Built as part of BAN6800's module sequence: Vision Document (Module 1) → Project Overview & Planning (Module 2, current state) → Data Pipeline (Module 3) → Predictive Modeling (Module 4) → Stakeholder Dashboard (Module 5) → Deployment (Module 6) → Final Integrated Project.
