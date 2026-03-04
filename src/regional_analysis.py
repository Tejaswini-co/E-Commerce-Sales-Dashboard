"""
Regional Performance Analysis
Analyzes sales and profit performance across different regions, states, and cities
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)


class RegionalAnalyzer:
    """Analyze regional performance"""
    
    def __init__(self, data_path=None):
        """Initialize with path to cleaned data"""
        if data_path is None:
            self.data_path = Path(__file__).parent.parent / 'data' / 'processed' / 'superstore_clean.csv'
        else:
            self.data_path = Path(data_path)
        
        self.output_dir = Path(__file__).parent.parent / 'output' / 'regional_analysis'
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
    
    def analyze_by_region(self):
        """Analyze performance by region"""
        print("\n" + "="*70)
        print("REGIONAL PERFORMANCE ANALYSIS")
        print("="*70)
        
        regional_stats = self.df.groupby('Region').agg({
            'Sales': ['sum', 'mean', 'count'],
            'Profit': ['sum', 'mean'],
            'Quantity': 'sum',
            'Order ID': 'nunique',
            'Customer ID': 'nunique'
        }).round(2)
        
        regional_stats.columns = ['Total_Sales', 'Avg_Sales', 'Transactions', 
                                   'Total_Profit', 'Avg_Profit', 'Quantity',
                                   'Unique_Orders', 'Unique_Customers']
        
        # Calculate additional metrics
        regional_stats['Profit_Margin_%'] = (regional_stats['Total_Profit'] / 
                                              regional_stats['Total_Sales'] * 100).round(2)
        regional_stats['Avg_Order_Value'] = (regional_stats['Total_Sales'] / 
                                              regional_stats['Unique_Orders']).round(2)
        regional_stats['Sales_Per_Customer'] = (regional_stats['Total_Sales'] / 
                                                 regional_stats['Unique_Customers']).round(2)
        
        # Sort by total sales
        regional_stats = regional_stats.sort_values('Total_Sales', ascending=False)
        
        print("\nRegional Performance Summary:")
        print(regional_stats)
        
        # Calculate market share
        total_sales = regional_stats['Total_Sales'].sum()
        regional_stats['Market_Share_%'] = (regional_stats['Total_Sales'] / total_sales * 100).round(2)
        
        # Save to CSV
        regional_stats.to_csv(self.output_dir / 'regional_performance.csv')
        print(f"\n✓ Saved to: {self.output_dir / 'regional_performance.csv'}")
        
        return regional_stats
    
    def analyze_by_state(self, top_n=15):
        """Analyze performance by state"""
        print("\n" + "="*70)
        print(f"TOP {top_n} STATES BY SALES")
        print("="*70)
        
        state_stats = self.df.groupby('State').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'nunique',
            'Customer ID': 'nunique'
        }).round(2)
        
        state_stats.columns = ['Total_Sales', 'Total_Profit', 'Orders', 'Customers']
        state_stats['Profit_Margin_%'] = (state_stats['Total_Profit'] / 
                                          state_stats['Total_Sales'] * 100).round(2)
        
        # Get top states
        top_states = state_stats.sort_values('Total_Sales', ascending=False).head(top_n)
        
        print(f"\nTop {top_n} States:")
        print(top_states)
        
        # Save to CSV
        state_stats.sort_values('Total_Sales', ascending=False).to_csv(
            self.output_dir / 'state_performance.csv'
        )
        print(f"\n✓ Saved complete state analysis to: {self.output_dir / 'state_performance.csv'}")
        
        return top_states, state_stats
    
    def analyze_by_city(self, top_n=20):
        """Analyze performance by city"""
        print("\n" + "="*70)
        print(f"TOP {top_n} CITIES BY SALES")
        print("="*70)
        
        city_stats = self.df.groupby('City').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'nunique',
            'Customer ID': 'nunique'
        }).round(2)
        
        city_stats.columns = ['Total_Sales', 'Total_Profit', 'Orders', 'Customers']
        city_stats['Profit_Margin_%'] = (city_stats['Total_Profit'] / 
                                         city_stats['Total_Sales'] * 100).round(2)
        
        # Get top cities
        top_cities = city_stats.sort_values('Total_Sales', ascending=False).head(top_n)
        
        print(f"\nTop {top_n} Cities:")
        print(top_cities)
        
        # Save to CSV
        city_stats.sort_values('Total_Sales', ascending=False).to_csv(
            self.output_dir / 'city_performance.csv'
        )
        
        return top_cities
    
    def analyze_regional_trends(self):
        """Analyze how regions perform over time"""
        print("\n" + "="*70)
        print("REGIONAL TRENDS OVER TIME")
        print("="*70)
        
        regional_trends = self.df.groupby(['Year', 'Region']).agg({
            'Sales': 'sum',
            'Profit': 'sum'
        }).round(2)
        
        regional_trends.columns = ['Sales', 'Profit']
        
        # Pivot for better view
        sales_pivot = regional_trends['Sales'].unstack()
        profit_pivot = regional_trends['Profit'].unstack()
        
        print("\nSales by Region and Year:")
        print(sales_pivot)
        
        print("\nProfit by Region and Year:")
        print(profit_pivot)
        
        # Calculate year-over-year growth
        sales_growth = sales_pivot.pct_change() * 100
        
        print("\nYear-over-Year Sales Growth by Region (%):")
        print(sales_growth.round(2))
        
        # Save to CSV
        sales_pivot.to_csv(self.output_dir / 'regional_sales_trends.csv')
        profit_pivot.to_csv(self.output_dir / 'regional_profit_trends.csv')
        sales_growth.to_csv(self.output_dir / 'regional_growth_rates.csv')
        
        return sales_pivot, profit_pivot
    
    def create_regional_visualizations(self, regional_stats, top_states, sales_pivot):
        """Create visualizations for regional analysis"""
        print("\nCreating visualizations...")
        
        # 1. Regional Sales Comparison
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Sales by region
        regions = regional_stats.index.tolist()
        sales = regional_stats['Total_Sales'].values
        colors = sns.color_palette("viridis", len(regions))
        
        ax1.bar(regions, sales, color=colors, edgecolor='black', alpha=0.8)
        ax1.set_xlabel('Region', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Total Sales ($)', fontsize=12, fontweight='bold')
        ax1.set_title('Total Sales by Region', fontsize=14, fontweight='bold')
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for i, v in enumerate(sales):
            ax1.text(i, v, f'${v/1000:.0f}K', ha='center', va='bottom', fontweight='bold')
        
        # Market share pie chart
        market_share = regional_stats['Market_Share_%'].values
        ax2.pie(market_share, labels=regions, autopct='%1.1f%%', startangle=90,
                colors=colors, textprops={'fontweight': 'bold'})
        ax2.set_title('Market Share by Region', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'regional_sales_comparison.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: regional_sales_comparison.png")
        plt.close()
        
        # 2. Top States
        fig, ax = plt.subplots(figsize=(14, 8))
        
        states = top_states.index.tolist()
        state_sales = top_states['Total_Sales'].values
        
        y_pos = np.arange(len(states))
        bars = ax.barh(y_pos, state_sales, color='#06A77D', edgecolor='black', alpha=0.8)
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(states)
        ax.invert_yaxis()
        ax.set_xlabel('Total Sales ($)', fontsize=12, fontweight='bold')
        ax.set_ylabel('State', fontsize=12, fontweight='bold')
        ax.set_title('Top States by Sales', fontsize=14, fontweight='bold', pad=20)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, v in enumerate(state_sales):
            ax.text(v, i, f'  ${v/1000:.0f}K', va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'top_states.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: top_states.png")
        plt.close()
        
        # 3. Regional Trends
        fig, ax = plt.subplots(figsize=(14, 7))
        
        for region in sales_pivot.columns:
            ax.plot(sales_pivot.index, sales_pivot[region], marker='o', 
                   linewidth=2.5, markersize=8, label=region)
        
        ax.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax.set_ylabel('Sales ($)', fontsize=12, fontweight='bold')
        ax.set_title('Regional Sales Trends Over Time', fontsize=14, fontweight='bold', pad=20)
        ax.legend(title='Region', fontsize=10, title_fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'regional_trends.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: regional_trends.png")
        plt.close()
        
        # 4. Profit Margin by Region
        fig, ax = plt.subplots(figsize=(12, 6))
        
        regions = regional_stats.index.tolist()
        margins = regional_stats['Profit_Margin_%'].values
        colors_pm = ['green' if x > 10 else 'orange' if x > 5 else 'red' for x in margins]
        
        ax.bar(regions, margins, color=colors_pm, edgecolor='black', alpha=0.8)
        ax.set_xlabel('Region', fontsize=12, fontweight='bold')
        ax.set_ylabel('Profit Margin (%)', fontsize=12, fontweight='bold')
        ax.set_title('Profit Margin by Region', fontsize=14, fontweight='bold', pad=20)
        ax.axhline(y=10, color='green', linestyle='--', linewidth=1, alpha=0.5, label='Target: 10%')
        ax.grid(True, alpha=0.3, axis='y')
        ax.legend()
        
        # Add value labels
        for i, v in enumerate(margins):
            ax.text(i, v, f'{v:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'regional_profit_margins.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: regional_profit_margins.png")
        plt.close()
    
    def run_full_analysis(self):
        """Run complete regional analysis"""
        print("="*70)
        print("REGIONAL PERFORMANCE ANALYSIS")
        print("="*70)
        
        if not self.load_data():
            return
        
        # Run analyses
        regional_stats = self.analyze_by_region()
        top_states, all_states = self.analyze_by_state()
        top_cities = self.analyze_by_city()
        sales_pivot, profit_pivot = self.analyze_regional_trends()
        
        # Create visualizations
        self.create_regional_visualizations(regional_stats, top_states, sales_pivot)
        
        print("\n" + "="*70)
        print("✓ REGIONAL ANALYSIS COMPLETE")
        print(f"✓ Results saved to: {self.output_dir}")
        print("="*70)


def main():
    """Main execution"""
    analyzer = RegionalAnalyzer()
    analyzer.run_full_analysis()


if __name__ == "__main__":
    main()
