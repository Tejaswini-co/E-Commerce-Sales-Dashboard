"""
Main Analysis Script
Runs all analyses in sequence
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from data_loader import SuperstoreDataLoader
from revenue_trends import RevenueTrendsAnalyzer
from regional_analysis import RegionalAnalyzer
from profit_analysis import ProfitAnalyzer
from product_analysis import ProductAnalyzer


def print_header(title):
    """Print a formatted header"""
    print("\n\n" + "="*80)
    print(f"  {title}")
    print("="*80)


def main():
    """Run all analyses"""
    print("="*80)
    print("  E-COMMERCE SALES ANALYSIS DASHBOARD")
    print("  Comprehensive Analysis of Superstore Dataset")
    print("="*80)
    
    # Step 1: Data Loading and Preprocessing
    print_header("STEP 1: DATA LOADING & PREPROCESSING")
    loader = SuperstoreDataLoader()
    df_clean = loader.run_full_pipeline()
    
    if df_clean is None:
        print("\n❌ Failed to load data. Please check that the dataset is available.")
        print("Download from: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final")
        return
    
    # Step 2: Revenue Trends Analysis
    print_header("STEP 2: REVENUE TRENDS ANALYSIS")
    revenue_analyzer = RevenueTrendsAnalyzer()
    revenue_analyzer.run_full_analysis()
    
    # Step 3: Regional Performance Analysis
    print_header("STEP 3: REGIONAL PERFORMANCE ANALYSIS")
    regional_analyzer = RegionalAnalyzer()
    regional_analyzer.run_full_analysis()
    
    # Step 4: Profit Margin Analysis
    print_header("STEP 4: PROFIT MARGIN ANALYSIS")
    profit_analyzer = ProfitAnalyzer()
    profit_analyzer.run_full_analysis()
    
    # Step 5: Product Performance Analysis
    print_header("STEP 5: PRODUCT PERFORMANCE ANALYSIS")
    product_analyzer = ProductAnalyzer()
    product_analyzer.run_full_analysis()
    
    # Final Summary
    print("\n\n" + "="*80)
    print("  ✓ ALL ANALYSES COMPLETE!")
    print("="*80)
    
    output_dir = Path(__file__).parent.parent / 'output'
    print(f"\nResults have been saved to: {output_dir}")
    
    print("\nGenerated Reports:")
    print("  • Revenue Trends Analysis")
    print("  • Regional Performance Analysis")
    print("  • Profit Margin Analysis")
    print("  • Product Performance Analysis")
    
    print("\nVisualizations:")
    print("  • Monthly/Yearly revenue trends")
    print("  • Regional sales comparisons")
    print("  • Profit margin analysis charts")
    print("  • Top 10 products charts")
    print("  • Category performance dashboards")
    
    print("\nNext Steps:")
    print("  1. Review the CSV reports in the output/ folders")
    print("  2. Examine the visualizations (PNG files)")
    print("  3. Run 'python visualizations/dashboard.py' for interactive dashboard")
    print("  4. Import data into Tableau/Power BI for further visualization")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
