# Workana Evalbids Order Case Study

## Overview
This repository contains the analysis for Workana's Growth team experiment to improve the relevance of freelancer ordering in the Evalbids system through an A/B test.

## Problem Statement
The current relevance ordering logic in Evalbids (the page showing suggested freelancers who submitted proposals) is outdated and doesn't represent the true relevance of freelancers. This impacts client conversion rates when selecting freelancers for their projects.

## Experiment Design
**A/B Test Implementation:**
- **Control Group:** Current ordering logic
- **Test Group:** New relevance ordering with weighted scoring system

**Target Categories:**
- Design & Multimedia - Web design
- IT & Programming - Wordpress
- Sales & Marketing - SEO
- IT & Programming - E-commerce
- IT & Programming - Web design
- Design & Multimedia - 3D Models
- Engineering & Manufacturing - CAD drawing
- Design & Multimedia - Corporate image
- Engineering & Manufacturing - 3D modelling
- IT & Programming - Apps programming (Android, iOS and others)

## New Relevance Scoring System
- **Gamification Level:** 30%
- **Projects worked in category:** 20%
- **Projects won in subcategory:** 20%
- **The Accelerator (expert freelancer badge):** 2.5%
- **Skills matching percentage:** 10%
- **Total Workana ranking:** 10%
- **Successful projects percentage:** 5%
- **Membership:** 2.5%

## Filtering Criteria
Only freelancers meeting these criteria will be shown as recommended:
- Gamification Gold or higher
- Top 1000 in project category ranking
- Top 5000 in total Workana ranking
- 1+ project with 5 stars

## Analysis Objectives
1. **Primary Success Metric:** Define and evaluate the main metric to measure experiment impact
2. **Complementary Metrics:** Identify additional metrics to monitor user behavior
3. **Results Analysis:** Compare control vs. test groups for significant differences
4. **Conclusions & Decisions:** Determine next steps based on results
5. **Future Iterations:** Propose improvements and next hypotheses to explore

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Upload Your Data
Place your Excel data file in the `data/` directory. The file should contain columns like:
- `group` (control/test)
- `category` (project category)
- `gamification_level` (Hero, Platinum, Gold, etc.)
- `el1_conversion` (0/1 for client response)
- `bids_received`, `accepted_bids`
- `skills_matching_pct`
- `total_ranking`
- And other relevant metrics

### 3. Run Analysis
```bash
python3 analysis/workana_analysis.py
```

### 4. Test with Sample Data
If you don't have data yet, the script will generate sample data for demonstration:
```bash
python3 analysis/workana_analysis.py
```

## Repository Structure
```
workana-case/
├── data/           # Raw data files (Excel, CSV, etc.)
├── analysis/       # Analysis scripts and notebooks
│   └── workana_analysis.py  # Main analysis script
├── docs/          # Documentation and reports
│   └── ANALYSIS_GUIDE.md    # Detailed analysis guide
├── output/        # Generated charts, tables, and results
├── requirements.txt # Python dependencies
└── README.md      # This file
```

## Business Definitions
- **EL1:** Client responds to a proposal or inquiry through messaging
- **Bid:** Proposals sent by freelancers
- **Thread:** Conversations between clients and freelancers
- **Messages:** Messages exchanged within conversations
- **Accepted Bids:** Proposals accepted by clients
- **Gamification Levels:** Hero > Platinum > Gold > Silver > Bronze > Iron
- **Client Types:** New (never paid) vs. Rebuy (has made payments)

## Analysis Features
- **A/B Test Comparison:** Control vs. test group analysis
- **Statistical Significance:** Chi-square tests for conversion rates
- **Key Metrics Analysis:** EL1 conversion, accepted bids, engagement
- **Quality Assessment:** Gamification levels, skills matching
- **Business Recommendations:** Actionable insights and next steps

## Next Steps
1. **Upload your Excel data file** to the `data/` directory
2. **Run the analysis** with real data
3. **Review results** and generate insights
4. **Prepare stakeholder presentation** with key findings
5. **Make data-driven decisions** about the experiment

---
*This analysis will be presented as a data story to business stakeholders, prioritizing clarity, impact, and decision-making focus.*
