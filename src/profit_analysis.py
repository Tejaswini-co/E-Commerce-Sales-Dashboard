"""
Profit Analysis Module
Analyzes profit margins, profitability by category, and discount impact
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)


class ProfitAnalyzer:
    """Analyze profit margins and profitability"""
    
    def __init__(self, data_path=None):
        """Initialize with path to cleaned data"""
        if data_path is None:
            self.data_path = Path(__file__).parent.parent / 'data' / 'processed' / 'superstore_clean.csv'
        else:
            self.data_path = Path(data_path)
        
        self.output_dir = Path(__file__).parent.parent / 'output' / 'profit_analysis'
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
            return False
    
    def analyze_overall_profitability(self):
        """Analyze overall profitability metrics"""
        print("\n" + "="*70)
        print("OVERALL PROFITABILITY ANALYSIS")
        print("="*70)
        
        total_sales = self.df['Sales'].sum()
        total_profit = self.df['Profit'].sum()
        total_discount = self.df['Discount_Amount'].sum()
        
        overall_margin = (total_profit / total_sales * 100)
        
        print(f"\nTotal Sales: ${total_sales:,.2f}")
        print(f"Total Profit: ${total_profit:,.2f}")
        print(f"Total Discounts Given: ${total_discount:,.2f}")
        print(f"Overall Profit Margin: {overall_margin:.2f}%")
        
        # Profit distribution
        profitable_orders = len(self.df[self.df['Profit'] > 0])
        loss_orders = len(self.df[self.df['Profit'] < 0])
        breakeven_orders = len(self.df[self.df['Profit'] == 0])
        
        print(f"\nProfit Distribution:")
        print(f"  Profitable Orders: {profitable_orders:,} ({profitable_orders/len(self.df)*100:.1f}%)")
        print(f"  Loss-making Orders: {loss_orders:,} ({loss_orders/len(self.df)*100:.1f}%)")
        print(f"  Break-even Orders: {breakeven_orders:,} ({breakeven_orders/len(self.df)*100:.1f}%)")
        
        # Save summary
        summary = {
            'Metric': ['Total Sales', 'Total Profit', 'Total Discounts', 'Profit Margin %',
                      'Profitable Orders', 'Loss Orders', 'Break-even Orders'],
            'Value': [f'${total_sales:,.2f}', f'${total_profit:,.2f}', f'${total_discount:,.2f}',
                     f'{overall_margin:.2f}%', profitable_orders, loss_orders, breakeven_orders]
        }
        pd.DataFrame(summary).to_csv(self.output_dir / 'overall_profitability.csv', index=False)
    
    def analyze_profit_by_category(self):
        """Analyze profitability by category and sub-category"""
        print("\n" + "="*70)
        print("PROFITABILITY BY CATEGORY")
        print("="*70)
        
        # Category level
        category_profit = self.df.groupby('Category').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Discount_Amount': 'sum',
            'Order ID': 'count'
        }).round(2)
        
        category_profit.columns = ['Sales', 'Profit', 'Discounts', 'Orders']
        category_profit['Profit_Margin_%'] = (category_profit['Profit'] / 
                                               category_profit['Sales'] * 100).round(2)
        category_profit['Avg_Profit_Per_Order'] = (category_profit['Profit'] / 
                                                    category_profit['Orders']).round(2)
        
        category_profit = category_profit.sort_values('Profit', ascending=False)
        
        print("\nCategory Profitability:")
        print(category_profit)
        
        category_profit.to_csv(self.output_dir / 'category_profitability.csv')
        
        # Sub-category level
        print("\n" + "-"*70)
        print("PROFITABILITY BY SUB-CATEGORY")
        print("-"*70)
        
        subcat_profit = self.df.groupby(['Category', 'Sub-Category']).agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'count'
        }).round(2)
        
        subcat_profit.columns = ['Sales', 'Profit', 'Orders']
        subcat_profit['Profit_Margin_%'] = (subcat_profit['Profit'] / 
                                            subcat_profit['Sales'] * 100).round(2)
        
        # Top 10 most profitable sub-categories
        top_subcat = subcat_profit.sort_values('Profit', ascending=False).head(10)
        print("\nTop 10 Most Profitable Sub-Categories:")
        print(top_subcat)
        
        # Bottom 10 (least profitable)
        bottom_subcat = subcat_profit.sort_values('Profit', ascending=True).head(10)
        print("\nBottom 10 Sub-Categories (Lowest Profit):")
        print(bottom_subcat)
        
        subcat_profit.to_csv(self.output_dir / 'subcategory_profitability.csv')
        
        return category_profit, subcat_profit
    
    def analyze_discount_impact(self):
        """Analyze the impact of discounts on profitability"""
        print("\n" + "="*70)
        print("DISCOUNT IMPACT ANALYSIS")
        print("="*70)
        
        # Create discount bins
        self.df['Discount_Bin'] = pd.cut(self.df['Discount'], 
                                         bins=[-0.01, 0, 0.1, 0.2, 0.3, 1.0],
                                         labels=['No Discount', '1-10%', '11-20%', '21-30%', '>30%'])
        
        discount_impact = self.df.groupby('Discount_Bin').agg({
            'Sales': ['sum', 'mean'],
            'Profit': ['sum', 'mean'],
            'Profit_Margin': 'mean',
            'Order ID': 'count'
        }).round(2)
        
        discount_impact.columns = ['Total_Sales', 'Avg_Sales', 'Total_Profit', 
                                   'Avg_Profit', 'Avg_Profit_Margin_%', 'Orders']
        
        print("\nImpact of Discounts on Profitability:")
        print(discount_impact)
        
        discount_impact.to_csv(self.output_dir / 'discount_impact.csv')
        
        # Correlation between discount and profit margin
        correlation = self.df[['Discount', 'Profit_Margin']].corr().iloc[0, 1]
        print(f"\nCorrelation between Discount and Profit Margin: {correlation:.3f}")
        
        return discount_impact
    
    def analyze_profit_trends(self):
        """Analyze profit trends over time"""
        print("\n" + "="*70)
        print("PROFIT TRENDS OVER TIME")
        print("="*70)
        
        # Monthly profit trends
        monthly_profit = self.df.groupby('Year_Month').agg({
            'Profit': 'sum',
            'Sales': 'sum',
            'Profit_Margin': 'mean'
        }).round(2)
        
        monthly_profit.columns = ['Profit', 'Sales', 'Avg_Profit_Margin_%']
        monthly_profit['Calculated_Margin_%'] = (monthly_profit['Profit'] / 
                                                 monthly_profit['Sales'] * 100).round(2)
        
        print("\nMonthly Profit Trends (Last 12 months):")
        print(monthly_profit.tail(12))
        
        monthly_profit.to_csv(self.output_dir / 'monthly_profit_trends.csv')
        
        # Yearly profit trends
        yearly_profit = self.df.groupby('Year').agg({
            'Profit': 'sum',
            'Sales': 'sum'
        }).round(2)
        
        yearly_profit['Profit_Margin_%'] = (yearly_profit['Profit'] / 
                                            yearly_profit['Sales'] * 100).round(2)
        yearly_profit['Profit_Growth_%'] = yearly_profit['Profit'].pct_change() * 100
        
        print("\nYearly Profit Trends:")
        print(yearly_profit)
        
        yearly_profit.to_csv(self.output_dir / 'yearly_profit_trends.csv')
        
        return monthly_profit, yearly_profit
    
    def create_profit_visualizations(self, category_profit, discount_impact, monthly_profit):
        """Create visualizations for profit analysis"""
        print("\nCreating visualizations...")
        
        # 1. Category Profit Comparison
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        categories = category_profit.index.tolist()
        profits = category_profit['Profit'].values
        margins = category_profit['Profit_Margin_%'].values
        
        # Profit by category
        colors = ['#06A77D' if p > 0 else '#C1121F' for p in profits]
        ax1.bar(categories, profits, color=colors, edgecolor='black', alpha=0.8)
        ax1.set_xlabel('Category', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Total Profit ($)', fontsize=12, fontweight='bold')
        ax1.set_title('Total Profit by Category', fontsize=14, fontweight='bold')
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        ax1.grid(True, alpha=0.3, axis='y')
        ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        
        # Add value labels
        for i, v in enumerate(profits):
            ax1.text(i, v, f'${v/1000:.0f}K', ha='center', 
                    va='bottom' if v > 0 else 'top', fontweight='bold')
        
        # Profit margin by category
        ax2.bar(categories, margins, color='#F18F01', edgecolor='black', alpha=0.8)
        ax2.set_xlabel('Category', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Profit Margin (%)', fontsize=12, fontweight='bold')
        ax2.set_title('Profit Margin by Category', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for i, v in enumerate(margins):
            ax2.text(i, v, f'{v:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'category_profit_analysis.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: category_profit_analysis.png")
        plt.close()
        
        # 2. Discount Impact
        fig, ax = plt.subplots(figsize=(12, 6))
        
        discount_bins = discount_impact.index.tolist()
        avg_margins = discount_impact['Avg_Profit_Margin_%'].values
        
        colors_disc = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(discount_bins)))
        bars = ax.bar(discount_bins, avg_margins, color=colors_disc, edgecolor='black', alpha=0.8)
        
        ax.set_xlabel('Discount Range', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Profit Margin (%)', fontsize=12, fontweight='bold')
        ax.set_title('Impact of Discounts on Profit Margin', fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='y')
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        
        # Add value labels
        for i, v in enumerate(avg_margins):
            ax.text(i, v, f'{v:.1f}%', ha='center', 
                   va='bottom' if v > 0 else 'top', fontweight='bold')
        
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.savefig(self.output_dir / 'discount_impact.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: discount_impact.png")
        plt.close()
        
        # 3. Profit Trend
        fig, ax = plt.subplots(figsize=(16, 6))
        
        x_range = range(len(monthly_profit))
        
        ax.plot(x_range, monthly_profit['Profit'], marker='o', linewidth=2.5, 
               markersize=7, label='Monthly Profit', color='#06A77D')
        ax.fill_between(x_range, monthly_profit['Profit'], alpha=0.3, color='#06A77D')
        ax.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.7)
        
        ax.set_xlabel('Month', fontsize=12, fontweight='bold')
        ax.set_ylabel('Profit ($)', fontsize=12, fontweight='bold')
        ax.set_title('Monthly Profit Trend', fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)
        
        # Set x-axis labels
        step = max(1, len(monthly_profit) // 12)
        ax.set_xticks(x_range[::step])
        ax.set_xticklabels(monthly_profit.index[::step], rotation=45, ha='right')
        
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'monthly_profit_trend.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: monthly_profit_trend.png")
        plt.close()
    
    def run_full_analysis(self):
        """Run complete profit analysis"""
        print("="*70)
        print("PROFIT MARGIN ANALYSIS")
        print("="*70)
        
        if not self.load_data():
            return
        
        # Run analyses
        self.analyze_overall_profitability()
        category_profit, subcat_profit = self.analyze_profit_by_category()
        discount_impact = self.analyze_discount_impact()
        monthly_profit, yearly_profit = self.analyze_profit_trends()
        
        # Create visualizations
        self.create_profit_visualizations(category_profit, discount_impact, monthly_profit)
        
        print("\n" + "="*70)
        print("✓ PROFIT ANALYSIS COMPLETE")
        print(f"✓ Results saved to: {self.output_dir}")
        print("="*70)


def main():
    """Main execution"""
    analyzer = ProfitAnalyzer()
    analyzer.run_full_analysis()


if __name__ == "__main__":
    main()
