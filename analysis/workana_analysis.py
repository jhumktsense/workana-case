#!/usr/bin/env python3
"""
Workana Evalbids Order Case Study Analysis
==========================================

This script analyzes the A/B test results for improving freelancer relevance ordering
in the Evalbids system.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class WorkanaAnalysis:
    """Main analysis class for the Workana Evalbids case study"""
    
    def __init__(self):
        self.data = None
        self.gamification_levels = ['Hero', 'Platinum', 'Gold', 'Silver', 'Bronze', 'Iron']
        self.target_categories = [
            'Design & Multimedia - Web design',
            'IT & Programming - Wordpress',
            'Sales & Marketing - SEO',
            'IT & Programming - E-commerce',
            'IT & Programming - Web design',
            'Design & Multimedia - 3D Models',
            'Engineering & Manufacturing - CAD drawing',
            'Design & Multimedia - Corporate image',
            'Engineering & Manufacturing - 3D modelling',
            'IT & Programming - Apps programming'
        ]
        
        # Relevance scoring weights
        self.scoring_weights = {
            'gamification_level': 0.30,
            'projects_in_category': 0.20,
            'projects_won_subcategory': 0.20,
            'accelerator_badge': 0.025,
            'skills_matching': 0.10,
            'total_ranking': 0.10,
            'successful_projects_pct': 0.05,
            'membership': 0.025
        }
    
    def generate_sample_data(self, n_samples=1000):
        """Generate sample data for testing purposes"""
        np.random.seed(42)
        
        data = {
            'project_id': range(1, n_samples + 1),
            'group': np.random.choice(['control', 'test'], n_samples),
            'category': np.random.choice(self.target_categories, n_samples),
            'client_type': np.random.choice(['New', 'Rebuy'], n_samples),
            'gamification_level': np.random.choice(self.gamification_levels, n_samples, p=[0.05, 0.10, 0.20, 0.25, 0.25, 0.15]),
            'projects_in_category': np.random.poisson(15, n_samples),
            'projects_won_subcategory': np.random.poisson(8, n_samples),
            'accelerator_badge': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
            'skills_matching_pct': np.random.uniform(0.3, 1.0, n_samples),
            'total_ranking': np.random.randint(1, 50000, n_samples),
            'successful_projects_pct': np.random.uniform(0.5, 1.0, n_samples),
            'membership': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
            'el1_conversion': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
            'bids_received': np.random.poisson(12, n_samples),
            'accepted_bids': np.random.poisson(3, n_samples)
        }
        
        self.data = pd.DataFrame(data)
        print("Sample data generated successfully")
        print(f"Data shape: {self.data.shape}")
        return True
    
    def analyze_experiment_results(self):
        """Analyze the A/B test results"""
        if self.data is None:
            print("No data loaded. Please load data first.")
            return
        
        # Split data into control and test groups
        control_group = self.data[self.data['group'] == 'control'].copy()
        test_group = self.data[self.data['group'] == 'test'].copy()
        
        print(f"Control group size: {len(control_group)}")
        print(f"Test group size: {len(test_group)}")
        
        # Analyze key metrics
        self.analyze_conversion_metrics(control_group, test_group)
        self.analyze_engagement_metrics(control_group, test_group)
        self.analyze_quality_metrics(control_group, test_group)
        
    def analyze_conversion_metrics(self, control_group, test_group):
        """Analyze conversion-related metrics"""
        print("\n" + "="*50)
        print("CONVERSION METRICS ANALYSIS")
        print("="*50)
        
        # EL1 Conversion Rate
        control_el1_rate = control_group['el1_conversion'].mean()
        test_el1_rate = test_group['el1_conversion'].mean()
        
        print(f"EL1 Conversion Rate:")
        print(f"  Control: {control_el1_rate:.3f} ({control_el1_rate*100:.1f}%)")
        print(f"  Test: {test_el1_rate:.3f} ({test_el1_rate*100:.1f}%)")
        print(f"  Difference: {test_el1_rate - control_el1_rate:.3f} ({(test_el1_rate/control_el1_rate - 1)*100:.1f}%)")
        
        # Statistical significance test
        chi2, p_value = stats.chi2_contingency(
            pd.crosstab(self.data['group'], self.data['el1_conversion'])
        )[0:2]
        
        print(f"  Statistical significance: p-value = {p_value:.4f}")
        print(f"  {'Significant' if p_value < 0.05 else 'Not significant'} difference")
        
        # Accepted Bids Rate
        control_accept_rate = (control_group['accepted_bids'] / control_group['bids_received']).mean()
        test_accept_rate = (test_group['accepted_bids'] / test_group['bids_received']).mean()
        
        print(f"\nAccepted Bids Rate:")
        print(f"  Control: {control_accept_rate:.3f} ({control_accept_rate*100:.1f}%)")
        print(f"  Test: {test_accept_rate:.3f} ({test_accept_rate*100:.1f}%)")
        print(f"  Difference: {test_accept_rate - control_accept_rate:.3f} ({(test_accept_rate/control_accept_rate - 1)*100:.1f}%)")
        
    def analyze_engagement_metrics(self, control_group, test_group):
        """Analyze engagement-related metrics"""
        print("\n" + "="*50)
        print("ENGAGEMENT METRICS ANALYSIS")
        print("="*50)
        
        # Bids received per project
        control_bids = control_group['bids_received'].mean()
        test_bids = test_group['bids_received'].mean()
        
        print(f"Average Bids Received per Project:")
        print(f"  Control: {control_bids:.1f}")
        print(f"  Test: {test_bids:.1f}")
        print(f"  Difference: {test_bids - control_bids:.1f}")
        
    def analyze_quality_metrics(self, control_group, test_group):
        """Analyze quality-related metrics"""
        print("\n" + "="*50)
        print("QUALITY METRICS ANALYSIS")
        print("="*50)
        
        # Gamification level distribution
        print("Gamification Level Distribution:")
        control_gamification = control_group['gamification_level'].value_counts().sort_index()
        test_gamification = test_group['gamification_level'].value_counts().sort_index()
        
        for level in self.gamification_levels:
            control_pct = control_gamification.get(level, 0) / len(control_group) * 100
            test_pct = test_gamification.get(level, 0) / len(test_group) * 100
            print(f"  {level}: Control {control_pct:.1f}% | Test {test_pct:.1f}%")
        
        # Skills matching quality
        control_skills = control_group['skills_matching_pct'].mean()
        test_skills = test_group['skills_matching_pct'].mean()
        
        print(f"\nAverage Skills Matching:")
        print(f"  Control: {control_skills:.3f} ({control_skills*100:.1f}%)")
        print(f"  Test: {test_skills:.3f} ({test_skills*100:.1f}%)")
        
    def generate_recommendations(self):
        """Generate business recommendations based on the analysis"""
        print("\n" + "="*50)
        print("BUSINESS RECOMMENDATIONS")
        print("="*50)
        
        print("Based on the analysis, here are the key recommendations:")
        print("\n1. PRIMARY SUCCESS METRIC:")
        print("   - EL1 Conversion Rate (Client Response Rate)")
        print("   - This directly measures the impact on client engagement")
        
        print("\n2. COMPLEMENTARY METRICS:")
        print("   - Accepted Bids Rate")
        print("   - Average Bids Received per Project")
        print("   - Skills Matching Quality")
        print("   - Gamification Level Distribution")
        
        print("\n3. NEXT STEPS:")
        print("   - Upload your Excel data file to the data/ directory")
        print("   - Run the analysis with real data")
        print("   - Generate insights and stakeholder presentation")
        
    def run_complete_analysis(self):
        """Run the complete analysis pipeline"""
        print("🚀 Starting Workana Evalbids Case Study Analysis...")
        print("="*60)
        
        # Generate sample data if no real data is available
        if self.data is None:
            print("No data loaded. Generating sample data for demonstration...")
            self.generate_sample_data()
        
        # Run analysis
        self.analyze_experiment_results()
        
        # Generate recommendations
        self.generate_recommendations()
        
        print("\n✅ Analysis complete!")
        print("📁 Next step: Upload your Excel data file to the data/ directory")


def main():
    """Main execution function"""
    analyzer = WorkanaAnalysis()
    analyzer.run_complete_analysis()


if __name__ == "__main__":
    main()
