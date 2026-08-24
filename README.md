# senior-wellbeing-analytics

a person-centered decision matrix built with data analytics for choosing which programs actually earn the resources they're given in for profit social enterprises.

Social enterprises account for a large umber of a lack of productivity and profitability based on the organization's goals in alignment with profitability, they face a real constraint: limited staff, limited time, in addition to already limited profit and resources — spending those resources on the wrong programming, not because they cannot choose between options, but rather because the programs get built around precedent and assumption instead of the people they're meant to serve. This isn't a data problem. It's a broken decision system: organizations choose confidently, and choose wrong, because the input feeding that decision was never built around the person on the receiving end.

The deeper issue is how "impact" itself gets defined. A program can be genuinely beneficial to someone's wellbeing in the long run and still fail completely — because if it isn't something a senior actually wants to engage with, the benefit never happens. Wellbeing and engagement have to be measured together, or "impact" is just a story an organization tells itself. That's what makes this human-centered, not just data-driven: it isn't about feeding more data into the same broken system — it's about building a system-centered, person-centered method for choosing which programs actually earn the resources they're given, balancing profitability with purpose and real reach.

This project, anchored by Amari Eden Living and Programs, exists to build that method — home by home, program by program — so that resource-allocation decisions are made on evidence of what actually works, not on convenience or tradition.

This mission statement was drafted with assistance from AI (Claude, Anthropic), synthesized directly from the author's own reasoning and language developed across extended discussion during this project's planning — see the AI Disclosure Form for the full account of how AI was used throughout this project.

## Repository Structure

```
senior-wellbeing-analytics/
├── data/
│   └── raw/               # untouched CQC source files, with provenance README
├── notebooks/             # exploratory analysis
├── src/
│   └── etl/               # pipeline DAG, anonymization check, privacy audit logging
├── docs/                  # governance framework, GX validation suite, bias detection report, audit log, illustrative simulation
├── README.md
└── requirements.txt
```

**Note on repository evolution:** the structure above reflects Module 3's implemented pipeline. Module 1-2 planning explored CDC BRFSS and Yelp Open Dataset as potential sources (see prior commit history and the Vision Document); the project's Module 3 dataset ultimately pivoted to UK Care Quality Commission (CQC) data as a proof-of-concept, given data-access constraints on Canadian/Alberta-specific senior programming data within the project timeline. See `docs/` for the full rationale.

## Data Sources

- **CQC (Care Quality Commission)** — Care directory with ratings, cqc.gov.uk. Real, non-synthetic, publicly downloadable. Used as the Module 3 proof-of-concept dataset; the pipeline architecture is designed to transfer to Amari Eden's own program data once collected.
- Supporting literature (not modeling data): Towers et al. (2021) MiCareHQ study on CQC ratings and quality of life; Bath and North East Somerset Council's CQC domain interpretation.
- Prior candidate sources evaluated but not used in the final pipeline: CDC BRFSS, Yelp Open Dataset, CIHI, CMS Nursing Home Compare, NCI-AD, UCI wearable sensor data — see AI Disclosure Form for the evaluation process.

## Setup

```bash
git clone <your-repo-url>
cd senior-wellbeing-analytics
pip install -r requirements.txt
```

Large raw files exceeding GitHub's 25MB limit are stored as filtered extracts in `data/raw/`, with full provenance and re-download instructions in `data/raw/README.md`.

## Usage & Reuse

This repository is shared publicly for academic transparency and portfolio purposes. Viewing and running the code locally is permitted. Reuse, modification, or redistribution is not authorized without the author's permission — no open-source license is attached, and all rights are reserved by default.

## Project Status

Built as part of BAN6800's module sequence: Vision Document (Module 1) → Project Overview & Planning (Module 2) → Data Pipeline (Module 3, current state) → Predictive Modeling (Module 4) → Stakeholder Dashboard (Module 5) → Deployment (Module 6) → Final Integrated Project.
