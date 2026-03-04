"""
Create Static Charts and Visualizations
Generates comprehensive static charts for the analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
sns.set_palette("husl")


class ChartCreator:
    """Create comprehensive static visualizations"""
    
    def __init__(self):
        self.data_path = Path(__file__).parent.parent / 'data' / 'processed' / 'superstore_clean.csv'
        self.output_dir = Path(__file__).parent.parent / 'output' / 'charts'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.df = None
    
    def load_data(self):
        """Load the cleaned data"""
        try:
            self.df = pd.read_csv(self.data_path, parse_dates=['Order Date', 'Ship Date'])
            print(f"✓ Loaded {len(self.df)} records")
            return True
        except FileNotFoundError:
            print(f"❌ Error: Data file not found")
            print("Please run: python src/data_loader.py first")
            return False
    
    def create_executive_summary_dashboard(self):
        """Create an executive summary dashboard"""
        print("\nCreating Executive Summary Dashboard...")
        
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Total Sales by Year
        ax1 = fig.add_subplot(gs[0, 0])
        yearly_sales = self.df.groupby('Year')['Sales'].sum() / 1000
        ax1.bar(yearly_sales.index, yearly_sales.values, color='#2E86AB', edgecolor='black', alpha=0.8)
        ax1.set_title('Annual Revenue ($K)', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Revenue ($K)')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # 2. Sales by Region (Pie)
        ax2 = fig.add_subplot(gs[0, 1])
        region_sales = self.df.groupby('Region')['Sales'].sum()
        colors = ['#06A77D', '#2E86AB', '#F18F01', '#C1121F']
        ax2.pie(region_sales, labels=region_sales.index, autopct='%1.1f%%', 
               colors=colors, startangle=90)
        ax2.set_title('Sales by Region', fontsize=12, fontweight='bold')
        
        # 3. Sales by Category
        ax3 = fig.add_subplot(gs[0, 2])
        category_sales = self.df.groupby('Category')['Sales'].sum() / 1000
        ax3.bar(category_sales.index, category_sales.values, color='#F18F01', 
               edgecolor='black', alpha=0.8)
        ax3.set_title('Sales by Category ($K)', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Category')
        ax3.set_ylabel('Sales ($K)')
        ax3.grid(True, alpha=0.3, axis='y')
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # 4. Monthly Sales Trend
        ax4 = fig.add_subplot(gs[1, :])
        monthly_sales = self.df.groupby('Year_Month')['Sales'].sum() / 1000
        x_range = range(len(monthly_sales))
        ax4.plot(x_range, monthly_sales.values, marker='o', linewidth=2, markersize=5, color='#06A77D')
        ax4.fill_between(x_range, monthly_sales.values, alpha=0.3, color='#06A77D')
        ax4.set_title('Monthly Sales Trend', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Month')
        ax4.set_ylabel('Sales ($K)')
        ax4.grid(True, alpha=0.3)
        step = max(1, len(monthly_sales) // 15)
        ax4.set_xticks(x_range[::step])
        ax4.set_xticklabels(monthly_sales.index[::step], rotation=45, ha='right')
        
        # 5. Profit Margin by Category
        ax5 = fig.add_subplot(gs[2, 0])
        cat_profit = self.df.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum'})
        cat_profit['Margin'] = (cat_profit['Profit'] / cat_profit['Sales'] * 100)
        ax5.bar(cat_profit.index, cat_profit['Margin'], color='#A23B72', edgecolor='black', alpha=0.8)
        ax5.set_title('Profit Margin by Category', fontsize=12, fontweight='bold')
        ax5.set_xlabel('Category')
        ax5.set_ylabel('Profit Margin (%)')
        ax5.grid(True, alpha=0.3, axis='y')
        plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # 6. Customer Segment Analysis
        ax6 = fig.add_subplot(gs[2, 1])
        segment_sales = self.df.groupby('Segment')['Sales'].sum()
        ax6.pie(segment_sales, labels=segment_sales.index, autopct='%1.1f%%', startangle=90)
        ax6.set_title('Sales by Customer Segment', fontsize=12, fontweight='bold')
        
        # 7. Shipping Mode Distribution
        ax7 = fig.add_subplot(gs[2, 2])
        ship_mode = self.df['Ship Mode'].value_counts()
        ax7.barh(ship_mode.index, ship_mode.values, color='#C1121F', edgecolor='black', alpha=0.8)
        ax7.set_title('Orders by Shipping Mode', fontsize=12, fontweight='bold')
        ax7.set_xlabel('Number of Orders')
        ax7.grid(True, alpha=0.3, axis='x')
        
        plt.suptitle('E-Commerce Sales Analysis - Executive Summary', 
                    fontsize=18, fontweight='bold', y=0.995)
        
        plt.savefig(self.output_dir / 'executive_summary_dashboard.png', 
                   dpi=300, bbox_inches='tight')
        print(f"✓ Saved: executive_summary_dashboard.png")
        plt.close()
    
    def create_comprehensive_analysis_chart(self):
        """Create a comprehensive multi-panel analysis"""
        print("\nCreating Comprehensive Analysis Chart...")
        
        fig, axes = plt.subplots(3, 3, figsize=(20, 15))
        fig.suptitle('Comprehensive E-Commerce Sales Analysis', 
                    fontsize=18, fontweight='bold')
        
        # Chart 1: Top 10 States
        top_states = self.df.groupby('State')['Sales'].sum().sort_values(ascending=False).head(10) / 1000
        axes[0, 0].barh(range(len(top_states)), top_states.values, color='#2E86AB', alpha=0.8)
        axes[0, 0].set_yticks(range(len(top_states)))
        axes[0, 0].set_yticklabels(top_states.index)
        axes[0, 0].invert_yaxis()
        axes[0, 0].set_xlabel('Sales ($K)')
        axes[0, 0].set_title('Top 10 States by Sales', fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3, axis='x')
        
        # Chart 2: Sub-Category Performance
        subcat = self.df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(10) / 1000
        axes[0, 1].barh(range(len(subcat)), subcat.values, color='#06A77D', alpha=0.8)
        axes[0, 1].set_yticks(range(len(subcat)))
        axes[0, 1].set_yticklabels(subcat.index, fontsize=9)
        axes[0, 1].invert_yaxis()
        axes[0, 1].set_xlabel('Sales ($K)')
        axes[0, 1].set_title('Top 10 Sub-Categories', fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3, axis='x')
        
        # Chart 3: Quarterly Trends
        quarterly = self.df.groupby('Quarter')['Sales'].sum() / 1000
        axes[0, 2].bar(['Q1', 'Q2', 'Q3', 'Q4'], quarterly.values, color='#F18F01', alpha=0.8)
        axes[0, 2].set_ylabel('Sales ($K)')
        axes[0, 2].set_title('Sales by Quarter', fontweight='bold')
        axes[0, 2].grid(True, alpha=0.3, axis='y')
        
        # Chart 4: Discount Distribution
        axes[1, 0].hist(self.df['Discount'], bins=20, color='#A23B72', alpha=0.7, edgecolor='black')
        axes[1, 0].set_xlabel('Discount Rate')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].set_title('Discount Distribution', fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # Chart 5: Profit vs Sales Scatter
        sample = self.df.sample(min(1000, len(self.df)))
        axes[1, 1].scatter(sample['Sales'], sample['Profit'], alpha=0.5, c='#2E86AB', s=10)
        axes[1, 1].set_xlabel('Sales ($)')
        axes[1, 1].set_ylabel('Profit ($)')
        axes[1, 1].set_title('Profit vs Sales Relationship', fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].axhline(y=0, color='red', linestyle='--', linewidth=1)
        
        # Chart 6: Orders by Day of Week
        dow_orders = self.df.groupby('Day_of_Week').size()
        dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_counts = [dow_orders.get(day, 0) for day in dow_order]
        axes[1, 2].bar(range(7), dow_counts, color='#C1121F', alpha=0.8)
        axes[1, 2].set_xticks(range(7))
        axes[1, 2].set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], rotation=45)
        axes[1, 2].set_ylabel('Number of Orders')
        axes[1, 2].set_title('Orders by Day of Week', fontweight='bold')
        axes[1, 2].grid(True, alpha=0.3, axis='y')
        
        # Chart 7: Sales Heatmap by Region and Category
        heatmap_data = self.df.pivot_table(values='Sales', index='Region', 
                                           columns='Category', aggfunc='sum')
        sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd', 
                   ax=axes[2, 0], cbar_kws={'label': 'Sales ($)'})
        axes[2, 0].set_title('Sales Heatmap: Region x Category', fontweight='bold')
        
        # Chart 8: Profit Distribution
        axes[2, 1].hist(self.df['Profit'], bins=50, color='#06A77D', alpha=0.7, edgecolor='black')
        axes[2, 1].axvline(x=0, color='red', linestyle='--', linewidth=2, label='Break-even')
        axes[2, 1].set_xlabel('Profit ($)')
        axes[2, 1].set_ylabel('Frequency')
        axes[2, 1].set_title('Profit Distribution', fontweight='bold')
        axes[2, 1].legend()
        axes[2, 1].grid(True, alpha=0.3, axis='y')
        
        # Chart 9: Quantity Distribution
        axes[2, 2].hist(self.df['Quantity'], bins=range(1, 15), color='#F18F01', 
                       alpha=0.7, edgecolor='black')
        axes[2, 2].set_xlabel('Quantity per Order')
        axes[2, 2].set_ylabel('Frequency')
        axes[2, 2].set_title('Order Quantity Distribution', fontweight='bold')
        axes[2, 2].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'comprehensive_analysis.png', 
                   dpi=300, bbox_inches='tight')
        print(f"✓ Saved: comprehensive_analysis.png")
        plt.close()
    
    def run_all(self):
        """Generate all charts"""
        print("="*70)
        print("CREATING STATIC VISUALIZATIONS")
        print("="*70)
        
        if not self.load_data():
            return
        
        self.create_executive_summary_dashboard()
        self.create_comprehensive_analysis_chart()
        
        print("\n" + "="*70)
        print("✓ ALL CHARTS CREATED SUCCESSFULLY")
        print(f"✓ Charts saved to: {self.output_dir}")
        print("="*70)


def main():
    """Main execution"""
    creator = ChartCreator()
    creator.run_all()


if __name__ == "__main__":
    main()
