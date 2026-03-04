"""
Monthly Revenue Trends Analysis
Analyzes sales trends over time with monthly, quarterly, and yearly breakdowns
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)


class RevenueTrendsAnalyzer:
    """Analyze revenue trends over time"""
    
    def __init__(self, data_path=None):
        """Initialize with path to cleaned data"""
        if data_path is None:
            self.data_path = Path(__file__).parent.parent / 'data' / 'processed' / 'superstore_clean.csv'
        else:
            self.data_path = Path(data_path)
        
        self.output_dir = Path(__file__).parent.parent / 'output' / 'revenue_trends'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.df = None
    
    def load_data(self):
        """Load the cleaned data"""
        try:
            self.df = pd.read_csv(self.data_path, parse_dates=['Order Date', 'Ship Date'])
            print(f"✓ Loaded data: {len(self.df)} records")
            return True
        except FileNotFoundError:
            print(f"❌ Error: File not found at {self.data_path}")
            print("Run data_loader.py first to process the data.")
            return False
    
    def analyze_monthly_revenue(self):
        """Analyze monthly revenue trends"""
        print("\n" + "="*70)
        print("MONTHLY REVENUE ANALYSIS")
        print("="*70)
        
        # Group by year-month
        monthly_sales = self.df.groupby('Year_Month').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'count',
            'Quantity': 'sum'
        }).round(2)
        
        monthly_sales.columns = ['Revenue', 'Profit', 'Orders', 'Quantity']
        
        # Calculate month-over-month growth
        monthly_sales['Revenue_Growth_%'] = monthly_sales['Revenue'].pct_change() * 100
        monthly_sales['Profit_Growth_%'] = monthly_sales['Profit'].pct_change() * 100
        
        # Calculate profit margin
        monthly_sales['Profit_Margin_%'] = (monthly_sales['Profit'] / monthly_sales['Revenue'] * 100).round(2)
        
        print("\nMonthly Revenue Summary:")
        print(monthly_sales.tail(12))  # Last 12 months
        
        # Save to CSV
        monthly_sales.to_csv(self.output_dir / 'monthly_revenue.csv')
        print(f"\n✓ Saved to: {self.output_dir / 'monthly_revenue.csv'}")
        
        return monthly_sales
    
    def analyze_yearly_revenue(self):
        """Analyze yearly revenue trends"""
        print("\n" + "="*70)
        print("YEARLY REVENUE ANALYSIS")
        print("="*70)
        
        yearly_sales = self.df.groupby('Year').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'count',
            'Quantity': 'sum',
            'Customer ID': 'nunique'
        }).round(2)
        
        yearly_sales.columns = ['Revenue', 'Profit', 'Orders', 'Quantity', 'Customers']
        
        # Calculate year-over-year growth
        yearly_sales['Revenue_Growth_%'] = yearly_sales['Revenue'].pct_change() * 100
        yearly_sales['Profit_Growth_%'] = yearly_sales['Profit'].pct_change() * 100
        
        # Calculate metrics
        yearly_sales['Profit_Margin_%'] = (yearly_sales['Profit'] / yearly_sales['Revenue'] * 100).round(2)
        yearly_sales['Avg_Order_Value'] = (yearly_sales['Revenue'] / yearly_sales['Orders']).round(2)
        
        print("\nYearly Performance:")
        print(yearly_sales)
        
        # Save to CSV
        yearly_sales.to_csv(self.output_dir / 'yearly_revenue.csv')
        print(f"\n✓ Saved to: {self.output_dir / 'yearly_revenue.csv'}")
        
        return yearly_sales
    
    def analyze_quarterly_revenue(self):
        """Analyze quarterly revenue trends"""
        print("\n" + "="*70)
        print("QUARTERLY REVENUE ANALYSIS")
        print("="*70)
        
        # Create year-quarter column
        self.df['Year_Quarter'] = self.df['Year'].astype(str) + '-Q' + self.df['Quarter'].astype(str)
        
        quarterly_sales = self.df.groupby('Year_Quarter').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'count',
            'Quantity': 'sum'
        }).round(2)
        
        quarterly_sales.columns = ['Revenue', 'Profit', 'Orders', 'Quantity']
        
        # Calculate quarter-over-quarter growth
        quarterly_sales['Revenue_Growth_%'] = quarterly_sales['Revenue'].pct_change() * 100
        quarterly_sales['Profit_Margin_%'] = (quarterly_sales['Profit'] / quarterly_sales['Revenue'] * 100).round(2)
        
        print("\nQuarterly Performance:")
        print(quarterly_sales.tail(8))  # Last 8 quarters
        
        # Save to CSV
        quarterly_sales.to_csv(self.output_dir / 'quarterly_revenue.csv')
        print(f"\n✓ Saved to: {self.output_dir / 'quarterly_revenue.csv'}")
        
        return quarterly_sales
    
    def analyze_seasonal_patterns(self):
        """Analyze seasonal patterns in sales"""
        print("\n" + "="*70)
        print("SEASONAL PATTERN ANALYSIS")
        print("="*70)
        
        # By month of year
        monthly_pattern = self.df.groupby('Month').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'count'
        }).round(2)
        
        monthly_pattern.columns = ['Revenue', 'Profit', 'Orders']
        monthly_pattern.index = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        print("\nAverage Revenue by Month (Across All Years):")
        print(monthly_pattern)
        
        # By day of week
        dow_pattern = self.df.groupby('Day_of_Week').agg({
            'Sales': ['sum', 'mean'],
            'Order ID': 'count'
        }).round(2)
        
        print("\nRevenue by Day of Week:")
        print(dow_pattern)
        
        # Save results
        monthly_pattern.to_csv(self.output_dir / 'seasonal_monthly_pattern.csv')
        dow_pattern.to_csv(self.output_dir / 'seasonal_weekly_pattern.csv')
        
        return monthly_pattern, dow_pattern
    
    def create_revenue_visualizations(self, monthly_sales, yearly_sales):
        """Create visualizations for revenue trends"""
        print("\nCreating visualizations...")
        
        # 1. Monthly Revenue Trend
        fig, ax = plt.subplots(figsize=(16, 6))
        x_range = range(len(monthly_sales))
        
        ax.plot(x_range, monthly_sales['Revenue'], marker='o', linewidth=2, 
                markersize=6, label='Revenue', color='#2E86AB')
        ax.fill_between(x_range, monthly_sales['Revenue'], alpha=0.3, color='#2E86AB')
        
        ax.set_xlabel('Month', fontsize=12, fontweight='bold')
        ax.set_ylabel('Revenue ($)', fontsize=12, fontweight='bold')
        ax.set_title('Monthly Revenue Trend', fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)
        
        # Set x-axis labels (show every 6th month for readability)
        step = max(1, len(monthly_sales) // 12)
        ax.set_xticks(x_range[::step])
        ax.set_xticklabels(monthly_sales.index[::step], rotation=45, ha='right')
        
        # Format y-axis
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'monthly_revenue_trend.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: monthly_revenue_trend.png")
        plt.close()
        
        # 2. Revenue and Profit Comparison
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10))
        
        # Revenue
        ax1.bar(range(len(yearly_sales)), yearly_sales['Revenue'], 
                color='#06A77D', alpha=0.8, edgecolor='black')
        ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Revenue ($)', fontsize=12, fontweight='bold')
        ax1.set_title('Yearly Revenue', fontsize=14, fontweight='bold')
        ax1.set_xticks(range(len(yearly_sales)))
        ax1.set_xticklabels(yearly_sales.index, rotation=0)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for i, v in enumerate(yearly_sales['Revenue']):
            ax1.text(i, v, f'${v/1000:.0f}K', ha='center', va='bottom', fontweight='bold')
        
        # Profit
        ax2.bar(range(len(yearly_sales)), yearly_sales['Profit'], 
                color='#F18F01', alpha=0.8, edgecolor='black')
        ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Profit ($)', fontsize=12, fontweight='bold')
        ax2.set_title('Yearly Profit', fontsize=14, fontweight='bold')
        ax2.set_xticks(range(len(yearly_sales)))
        ax2.set_xticklabels(yearly_sales.index, rotation=0)
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for i, v in enumerate(yearly_sales['Profit']):
            ax2.text(i, v, f'${v/1000:.0f}K', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'yearly_revenue_profit.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: yearly_revenue_profit.png")
        plt.close()
        
        # 3. Growth Rate Chart
        fig, ax = plt.subplots(figsize=(14, 6))
        monthly_growth = monthly_sales['Revenue_Growth_%'].dropna()
        
        colors = ['green' if x >= 0 else 'red' for x in monthly_growth]
        ax.bar(range(len(monthly_growth)), monthly_growth, color=colors, alpha=0.7)
        
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        ax.set_xlabel('Month', fontsize=12, fontweight='bold')
        ax.set_ylabel('Growth Rate (%)', fontsize=12, fontweight='bold')
        ax.set_title('Month-over-Month Revenue Growth Rate', fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Set x-axis labels
        step = max(1, len(monthly_growth) // 12)
        ax.set_xticks(range(0, len(monthly_growth), step))
        ax.set_xticklabels(monthly_growth.index[::step], rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'revenue_growth_rate.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: revenue_growth_rate.png")
        plt.close()
    
    def run_full_analysis(self):
        """Run complete revenue trends analysis"""
        print("="*70)
        print("REVENUE TRENDS ANALYSIS")
        print("="*70)
        
        if not self.load_data():
            return
        
        # Run analyses
        monthly_sales = self.analyze_monthly_revenue()
        yearly_sales = self.analyze_yearly_revenue()
        quarterly_sales = self.analyze_quarterly_revenue()
        monthly_pattern, dow_pattern = self.analyze_seasonal_patterns()
        
        # Create visualizations
        self.create_revenue_visualizations(monthly_sales, yearly_sales)
        
        print("\n" + "="*70)
        print("✓ REVENUE TRENDS ANALYSIS COMPLETE")
        print(f"✓ Results saved to: {self.output_dir}")
        print("="*70)


def main():
    """Main execution"""
    analyzer = RevenueTrendsAnalyzer()
    analyzer.run_full_analysis()


if __name__ == "__main__":
    main()
