"""
Product Analysis Module
Analyzes top products, best sellers, and product performance
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)


class ProductAnalyzer:
    """Analyze product performance"""
    
    def __init__(self, data_path=None):
        """Initialize with path to cleaned data"""
        if data_path is None:
            self.data_path = Path(__file__).parent.parent / 'data' / 'processed' / 'superstore_clean.csv'
        else:
            self.data_path = Path(data_path)
        
        self.output_dir = Path(__file__).parent.parent / 'output' / 'product_analysis'
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
    
    def analyze_top_products_by_sales(self, top_n=10):
        """Analyze top products by sales revenue"""
        print("\n" + "="*70)
        print(f"TOP {top_n} PRODUCTS BY SALES")
        print("="*70)
        
        product_sales = self.df.groupby('Product Name').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum',
            'Order ID': 'count'
        }).round(2)
        
        product_sales.columns = ['Total_Sales', 'Total_Profit', 'Quantity_Sold', 'Orders']
        product_sales['Profit_Margin_%'] = (product_sales['Total_Profit'] / 
                                            product_sales['Total_Sales'] * 100).round(2)
        product_sales['Avg_Sale_Price'] = (product_sales['Total_Sales'] / 
                                           product_sales['Quantity_Sold']).round(2)
        
        # Get top products by sales
        top_products = product_sales.sort_values('Total_Sales', ascending=False).head(top_n)
        
        print(f"\nTop {top_n} Products by Sales Revenue:")
        print(top_products)
        
        # Save to CSV
        product_sales.sort_values('Total_Sales', ascending=False).to_csv(
            self.output_dir / 'products_by_sales.csv'
        )
        print(f"\n✓ Saved complete product sales data")
        
        return top_products
    
    def analyze_top_products_by_profit(self, top_n=10):
        """Analyze top products by profit"""
        print("\n" + "="*70)
        print(f"TOP {top_n} PRODUCTS BY PROFIT")
        print("="*70)
        
        product_profit = self.df.groupby('Product Name').agg({
            'Profit': 'sum',
            'Sales': 'sum',
            'Quantity': 'sum',
            'Order ID': 'count'
        }).round(2)
        
        product_profit.columns = ['Total_Profit', 'Total_Sales', 'Quantity_Sold', 'Orders']
        product_profit['Profit_Margin_%'] = (product_profit['Total_Profit'] / 
                                             product_profit['Total_Sales'] * 100).round(2)
        
        # Top profitable products
        top_profitable = product_profit.sort_values('Total_Profit', ascending=False).head(top_n)
        
        print(f"\nTop {top_n} Most Profitable Products:")
        print(top_profitable)
        
        # Least profitable (biggest losses)
        print(f"\n{top_n} Least Profitable Products (Biggest Losses):")
        worst_products = product_profit.sort_values('Total_Profit', ascending=True).head(top_n)
        print(worst_products)
        
        # Save to CSV
        product_profit.sort_values('Total_Profit', ascending=False).to_csv(
            self.output_dir / 'products_by_profit.csv'
        )
        
        return top_profitable, worst_products
    
    def analyze_top_products_by_quantity(self, top_n=10):
        """Analyze best-selling products by quantity"""
        print("\n" + "="*70)
        print(f"TOP {top_n} PRODUCTS BY QUANTITY SOLD")
        print("="*70)
        
        product_quantity = self.df.groupby('Product Name').agg({
            'Quantity': 'sum',
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'count'
        }).round(2)
        
        product_quantity.columns = ['Quantity_Sold', 'Total_Sales', 'Total_Profit', 'Orders']
        product_quantity['Avg_Price'] = (product_quantity['Total_Sales'] / 
                                         product_quantity['Quantity_Sold']).round(2)
        
        top_by_quantity = product_quantity.sort_values('Quantity_Sold', ascending=False).head(top_n)
        
        print(f"\nTop {top_n} Best-Selling Products by Quantity:")
        print(top_by_quantity)
        
        # Save to CSV
        product_quantity.sort_values('Quantity_Sold', ascending=False).to_csv(
            self.output_dir / 'products_by_quantity.csv'
        )
        
        return top_by_quantity
    
    def analyze_category_subcategory_performance(self):
        """Analyze performance by category and sub-category"""
        print("\n" + "="*70)
        print("CATEGORY & SUB-CATEGORY PERFORMANCE")
        print("="*70)
        
        # Category performance
        category_perf = self.df.groupby('Category').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum',
            'Product ID': 'nunique',
            'Order ID': 'count'
        }).round(2)
        
        category_perf.columns = ['Sales', 'Profit', 'Quantity', 'Unique_Products', 'Orders']
        category_perf['Profit_Margin_%'] = (category_perf['Profit'] / 
                                            category_perf['Sales'] * 100).round(2)
        category_perf['Avg_Sale_Per_Product'] = (category_perf['Sales'] / 
                                                  category_perf['Unique_Products']).round(2)
        
        print("\nCategory Performance:")
        print(category_perf.sort_values('Sales', ascending=False))
        
        # Sub-category performance
        subcat_perf = self.df.groupby('Sub-Category').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum',
            'Order ID': 'count'
        }).round(2)
        
        subcat_perf.columns = ['Sales', 'Profit', 'Quantity', 'Orders']
        subcat_perf['Profit_Margin_%'] = (subcat_perf['Profit'] / 
                                          subcat_perf['Sales'] * 100).round(2)
        
        print("\nTop 10 Sub-Categories by Sales:")
        print(subcat_perf.sort_values('Sales', ascending=False).head(10))
        
        # Save to CSV
        category_perf.to_csv(self.output_dir / 'category_performance.csv')
        subcat_perf.sort_values('Sales', ascending=False).to_csv(
            self.output_dir / 'subcategory_performance.csv'
        )
        
        return category_perf, subcat_perf
    
    def analyze_product_segments(self):
        """Analyze which customer segments buy which products"""
        print("\n" + "="*70)
        print("PRODUCT SALES BY CUSTOMER SEGMENT")
        print("="*70)
        
        segment_category = pd.crosstab(
            self.df['Segment'],
            self.df['Category'],
            values=self.df['Sales'],
            aggfunc='sum'
        ).round(2)
        
        print("\nSales by Customer Segment and Category:")
        print(segment_category)
        
        # Calculate percentages
        segment_category_pct = segment_category.div(segment_category.sum(axis=1), axis=0) * 100
        
        print("\nPercentage Distribution:")
        print(segment_category_pct.round(2))
        
        segment_category.to_csv(self.output_dir / 'segment_category_sales.csv')
        
        return segment_category
    
    def create_product_visualizations(self, top_products_sales, top_products_profit, 
                                      top_quantity, category_perf):
        """Create visualizations for product analysis"""
        print("\nCreating visualizations...")
        
        # 1. Top 10 Products by Sales
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Truncate long product names for display
        products = [name[:40] + '...' if len(name) > 40 else name 
                   for name in top_products_sales.index]
        sales = top_products_sales['Total_Sales'].values
        
        y_pos = np.arange(len(products))
        bars = ax.barh(y_pos, sales, color='#2E86AB', edgecolor='black', alpha=0.8)
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(products, fontsize=10)
        ax.invert_yaxis()
        ax.set_xlabel('Total Sales ($)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Product', fontsize=12, fontweight='bold')
        ax.set_title('Top 10 Products by Sales Revenue', fontsize=14, fontweight='bold', pad=20)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.1f}K'))
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, v in enumerate(sales):
            ax.text(v, i, f'  ${v/1000:.1f}K', va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'top_10_products_sales.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: top_10_products_sales.png")
        plt.close()
        
        # 2. Top 10 Products by Profit
        fig, ax = plt.subplots(figsize=(14, 8))
        
        products_profit = [name[:40] + '...' if len(name) > 40 else name 
                          for name in top_products_profit.index]
        profits = top_products_profit['Total_Profit'].values
        
        y_pos = np.arange(len(products_profit))
        colors = ['#06A77D' if p > 0 else '#C1121F' for p in profits]
        bars = ax.barh(y_pos, profits, color=colors, edgecolor='black', alpha=0.8)
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(products_profit, fontsize=10)
        ax.invert_yaxis()
        ax.set_xlabel('Total Profit ($)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Product', fontsize=12, fontweight='bold')
        ax.set_title('Top 10 Products by Profit', fontsize=14, fontweight='bold', pad=20)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.1f}K'))
        ax.grid(True, alpha=0.3, axis='x')
        ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
        
        # Add value labels
        for i, v in enumerate(profits):
            ax.text(v, i, f'  ${v/1000:.1f}K', va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'top_10_products_profit.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: top_10_products_profit.png")
        plt.close()
        
        # 3. Category Performance Dashboard
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        categories = category_perf.index.tolist()
        
        # Sales by category
        sales_cat = category_perf['Sales'].values
        ax1.bar(categories, sales_cat, color='#2E86AB', edgecolor='black', alpha=0.8)
        ax1.set_ylabel('Sales ($)', fontsize=11, fontweight='bold')
        ax1.set_title('Sales by Category', fontsize=12, fontweight='bold')
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        ax1.grid(True, alpha=0.3, axis='y')
        for i, v in enumerate(sales_cat):
            ax1.text(i, v, f'${v/1000:.0f}K', ha='center', va='bottom', fontweight='bold')
        
        # Profit by category
        profit_cat = category_perf['Profit'].values
        colors_profit = ['#06A77D' if p > 0 else '#C1121F' for p in profit_cat]
        ax2.bar(categories, profit_cat, color=colors_profit, edgecolor='black', alpha=0.8)
        ax2.set_ylabel('Profit ($)', fontsize=11, fontweight='bold')
        ax2.set_title('Profit by Category', fontsize=12, fontweight='bold')
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        for i, v in enumerate(profit_cat):
            ax2.text(i, v, f'${v/1000:.0f}K', ha='center', 
                    va='bottom' if v > 0 else 'top', fontweight='bold')
        
        # Quantity by category
        quantity_cat = category_perf['Quantity'].values
        ax3.bar(categories, quantity_cat, color='#F18F01', edgecolor='black', alpha=0.8)
        ax3.set_ylabel('Quantity Sold', fontsize=11, fontweight='bold')
        ax3.set_title('Quantity Sold by Category', fontsize=12, fontweight='bold')
        ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.1f}K'))
        ax3.grid(True, alpha=0.3, axis='y')
        for i, v in enumerate(quantity_cat):
            ax3.text(i, v, f'{v/1000:.1f}K', ha='center', va='bottom', fontweight='bold')
        
        # Profit margin by category
        margin_cat = category_perf['Profit_Margin_%'].values
        colors_margin = ['green' if m > 10 else 'orange' if m > 5 else 'red' for m in margin_cat]
        ax4.bar(categories, margin_cat, color=colors_margin, edgecolor='black', alpha=0.8)
        ax4.set_ylabel('Profit Margin (%)', fontsize=11, fontweight='bold')
        ax4.set_title('Profit Margin by Category', fontsize=12, fontweight='bold')
        ax4.grid(True, alpha=0.3, axis='y')
        ax4.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        for i, v in enumerate(margin_cat):
            ax4.text(i, v, f'{v:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'category_performance_dashboard.png', 
                   dpi=300, bbox_inches='tight')
        print(f"✓ Saved: category_performance_dashboard.png")
        plt.close()
        
        # 4. Top Products by Quantity
        fig, ax = plt.subplots(figsize=(14, 8))
        
        products_qty = [name[:40] + '...' if len(name) > 40 else name 
                       for name in top_quantity.index]
        quantities = top_quantity['Quantity_Sold'].values
        
        y_pos = np.arange(len(products_qty))
        ax.barh(y_pos, quantities, color='#A23B72', edgecolor='black', alpha=0.8)
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(products_qty, fontsize=10)
        ax.invert_yaxis()
        ax.set_xlabel('Quantity Sold', fontsize=12, fontweight='bold')
        ax.set_ylabel('Product', fontsize=12, fontweight='bold')
        ax.set_title('Top 10 Products by Quantity Sold', fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, v in enumerate(quantities):
            ax.text(v, i, f'  {int(v):,}', va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'top_10_products_quantity.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: top_10_products_quantity.png")
        plt.close()
    
    def run_full_analysis(self):
        """Run complete product analysis"""
        print("="*70)
        print("PRODUCT PERFORMANCE ANALYSIS")
        print("="*70)
        
        if not self.load_data():
            return
        
        # Run analyses
        top_products_sales = self.analyze_top_products_by_sales()
        top_products_profit, worst_products = self.analyze_top_products_by_profit()
        top_quantity = self.analyze_top_products_by_quantity()
        category_perf, subcat_perf = self.analyze_category_subcategory_performance()
        segment_category = self.analyze_product_segments()
        
        # Create visualizations
        self.create_product_visualizations(top_products_sales, top_products_profit,
                                          top_quantity, category_perf)
        
        print("\n" + "="*70)
        print("✓ PRODUCT ANALYSIS COMPLETE")
        print(f"✓ Results saved to: {self.output_dir}")
        print("="*70)


def main():
    """Main execution"""
    analyzer = ProductAnalyzer()
    analyzer.run_full_analysis()


if __name__ == "__main__":
    main()
