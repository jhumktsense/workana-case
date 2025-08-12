# Data Template for Workana Evalbids Case Study

## Expected Data Structure

Your Excel file should contain the following columns for the A/B test analysis:

### Required Columns

| Column Name | Description | Data Type | Example Values |
|-------------|-------------|-----------|----------------|
| `project_id` | Unique identifier for each project | Integer | 1, 2, 3, ... |
| `group` | A/B test group assignment | String | "control", "test" |
| `category` | Project category and subcategory | String | "Design & Multimedia - Web design" |
| `client_type` | Type of client | String | "New", "Rebuy" |

### Freelancer Quality Metrics

| Column Name | Description | Data Type | Example Values |
|-------------|-------------|-----------|----------------|
| `gamification_level` | Freelancer level in platform | String | "Hero", "Platinum", "Gold", "Silver", "Bronze", "Iron" |
| `projects_in_category` | Number of projects in this category | Integer | 15, 25, 8, ... |
| `projects_won_subcategory` | Number of projects won in subcategory | Integer | 8, 12, 5, ... |
| `accelerator_badge` | Has expert freelancer badge | Binary | 0, 1 |
| `skills_matching_pct` | Percentage of skills that match project | Float | 0.75, 0.90, 0.60, ... |
| `total_ranking` | Overall ranking in Workana | Integer | 1250, 5000, 15000, ... |
| `successful_projects_pct` | Percentage of successful projects | Float | 0.85, 0.95, 0.70, ... |
| `membership` | Has premium membership | Binary | 0, 1 |

### Outcome Metrics

| Column Name | Description | Data Type | Example Values |
|-------------|-------------|-----------|----------------|
| `el1_conversion` | Client responded to proposal/inquiry | Binary | 0, 1 |
| `bids_received` | Total number of bids received | Integer | 12, 8, 15, ... |
| `accepted_bids` | Number of bids accepted | Integer | 3, 1, 5, ... |
| `conversion_rate` | Overall project conversion rate | Float | 0.25, 0.40, 0.15, ... |

## Sample Data Row

```
project_id: 1
group: "test"
category: "IT & Programming - Web design"
client_type: "Rebuy"
gamification_level: "Gold"
projects_in_category: 18
projects_won_subcategory: 12
accelerator_badge: 1
skills_matching_pct: 0.85
total_ranking: 2500
successful_projects_pct: 0.90
membership: 1
el1_conversion: 1
bids_received: 14
accepted_bids: 4
conversion_rate: 0.29
```

## Data Requirements

1. **Balanced Groups**: Ensure roughly equal numbers of control and test projects
2. **Category Distribution**: Include projects from all target categories
3. **Time Period**: Ideally 3-6 months of data for statistical significance
4. **Data Quality**: No missing values in key metrics
5. **Randomization**: Projects should be randomly assigned to groups

## File Format

- **Preferred**: Excel (.xlsx) or CSV (.csv)
- **Encoding**: UTF-8
- **Delimiter**: Comma for CSV
- **Sheet Name**: Use descriptive names if multiple sheets

## Upload Instructions

1. Place your data file in the `data/` directory
2. Update the file path in the analysis script if needed
3. Run the analysis: `python3 analysis/workana_analysis.py`

## Questions?

If you need help with data preparation or have questions about the expected format, refer to the `ANALYSIS_GUIDE.md` in the `docs/` directory.
