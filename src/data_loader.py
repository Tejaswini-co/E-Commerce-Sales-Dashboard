"""
Data Loader and Preprocessing Module
Loads and cleans the Superstore dataset for analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class SuperstoreDataLoader:
    """Class to handle loading and preprocessing of Superstore data"""
    
    def __init__(self, data_path=None):
        """
        Initialize the data loader
        
        Args:
            data_path: Path to the raw CSV file
        """
        if data_path is None:
            self.data_path = Path(__file__).parent.parent / 'data' / 'raw' / 'Sample - Superstore.csv'
        else:
            self.data_path = Path(data_path)
        
        self.df = None
        self.processed_path = Path(__file__).parent.parent / 'data' / 'processed'
        self.processed_path.mkdir(parents=True, exist_ok=True)
    
    def load_data(self):
        """Load the raw CSV data"""
        try:
            print(f"Loading data from {self.data_path}...")
            self.df = pd.read_csv(self.data_path, encoding='latin-1')
            print(f"✓ Data loaded successfully: {len(self.df)} rows, {len(self.df.columns)} columns")
            return self.df
        except FileNotFoundError:
            print(f"❌ Error: File not found at {self.data_path}")
            print("\nPlease download the dataset from:")
            print("https://www.kaggle.com/datasets/vivek468/superstore-dataset-final")
            print(f"And place it in: {self.data_path.parent}")
            return None
    
    def explore_data(self):
        """Display basic information about the dataset"""
        if self.df is None:
            print("No data loaded. Call load_data() first.")
            return
        
        print("\n" + "="*70)
        print("DATASET OVERVIEW")
        print("="*70)
        
        print(f"\nShape: {self.df.shape[0]} rows × {self.df.shape[1]} columns")
        
        print("\nColumn Names and Types:")
        print(self.df.dtypes)
        
        print("\nFirst Few Rows:")
        print(self.df.head())
        
        print("\nMissing Values:")
        missing = self.df.isnull().sum()
        if missing.sum() > 0:
            print(missing[missing > 0])
        else:
            print("No missing values found ✓")
        
        print("\nBasic Statistics:")
        print(self.df.describe())
        
        print("\n" + "="*70)
    
    def clean_data(self):
        """Clean and preprocess the data"""
        if self.df is None:
            print("No data to clean. Load data first.")
            return None
        
        print("\nCleaning data...")
        df_clean = self.df.copy()
        
        # Convert date columns to datetime
        date_columns = ['Order Date', 'Ship Date']
        for col in date_columns:
            if col in df_clean.columns:
                df_clean[col] = pd.to_datetime(df_clean[col])
                print(f"✓ Converted '{col}' to datetime")
        
        # Create additional time-based features
        if 'Order Date' in df_clean.columns:
            df_clean['Year'] = df_clean['Order Date'].dt.year
            df_clean['Month'] = df_clean['Order Date'].dt.month
            df_clean['Quarter'] = df_clean['Order Date'].dt.quarter
            df_clean['Month_Name'] = df_clean['Order Date'].dt.strftime('%B')
            df_clean['Year_Month'] = df_clean['Order Date'].dt.to_period('M').astype(str)
            df_clean['Day_of_Week'] = df_clean['Order Date'].dt.day_name()
            print("✓ Created time-based features")
        
        # Calculate profit margin
        if 'Profit' in df_clean.columns and 'Sales' in df_clean.columns:
            df_clean['Profit_Margin'] = (df_clean['Profit'] / df_clean['Sales'] * 100).round(2)
            df_clean['Profit_Margin'] = df_clean['Profit_Margin'].replace([np.inf, -np.inf], 0)
            print("✓ Calculated profit margin")
        
        # Calculate discount amount
        if 'Discount' in df_clean.columns and 'Sales' in df_clean.columns:
            df_clean['Discount_Amount'] = (df_clean['Sales'] * df_clean['Discount']).round(2)
            print("✓ Calculated discount amount")
        
        # Handle missing values
        df_clean = df_clean.dropna()
        
        # Remove duplicates
        initial_rows = len(df_clean)
        df_clean = df_clean.drop_duplicates()
        removed = initial_rows - len(df_clean)
        if removed > 0:
            print(f"✓ Removed {removed} duplicate rows")
        
        # Sort by order date
        if 'Order Date' in df_clean.columns:
            df_clean = df_clean.sort_values('Order Date')
        
        print(f"✓ Cleaning complete: {len(df_clean)} rows remaining")
        
        self.df_clean = df_clean
        return df_clean
    
    def save_processed_data(self):
        """Save the cleaned data to CSV"""
        if not hasattr(self, 'df_clean'):
            print("No cleaned data to save. Run clean_data() first.")
            return
        
        output_path = self.processed_path / 'superstore_clean.csv'
        self.df_clean.to_csv(output_path, index=False)
        print(f"\n✓ Processed data saved to: {output_path}")
        
        # Also save to Excel for easy viewing
        excel_path = self.processed_path / 'superstore_clean.xlsx'
        self.df_clean.to_excel(excel_path, index=False, engine='openpyxl')
        print(f"✓ Excel version saved to: {excel_path}")
    
    def get_summary_stats(self):
        """Generate and save summary statistics"""
        if not hasattr(self, 'df_clean'):
            print("No cleaned data available.")
            return
        
        df = self.df_clean
        
        print("\n" + "="*70)
        print("SUMMARY STATISTICS")
        print("="*70)
        
        # Date range
        if 'Order Date' in df.columns:
            print(f"\nDate Range: {df['Order Date'].min().date()} to {df['Order Date'].max().date()}")
        
        # Total metrics
        print(f"\nTotal Orders: {df['Order ID'].nunique():,}")
        print(f"Total Customers: {df['Customer ID'].nunique():,}")
        print(f"Total Products: {df['Product ID'].nunique():,}")
        
        # Financial metrics
        if 'Sales' in df.columns:
            print(f"\nTotal Sales: ${df['Sales'].sum():,.2f}")
            print(f"Average Order Value: ${df['Sales'].mean():,.2f}")
        
        if 'Profit' in df.columns:
            print(f"Total Profit: ${df['Profit'].sum():,.2f}")
            print(f"Average Profit per Order: ${df['Profit'].mean():,.2f}")
        
        if 'Profit_Margin' in df.columns:
            print(f"Average Profit Margin: {df['Profit_Margin'].mean():.2f}%")
        
        # Category breakdown
        if 'Category' in df.columns:
            print(f"\nCategories: {df['Category'].nunique()}")
            print(df['Category'].value_counts())
        
        # Regional breakdown
        if 'Region' in df.columns:
            print(f"\nRegions: {df['Region'].nunique()}")
            print(df['Region'].value_counts())
        
        # Segment breakdown
        if 'Segment' in df.columns:
            print(f"\nCustomer Segments: {df['Segment'].nunique()}")
            print(df['Segment'].value_counts())
        
        print("\n" + "="*70)
    
    def run_full_pipeline(self):
        """Run the complete data loading and preprocessing pipeline"""
        print("="*70)
        print("SUPERSTORE DATA PREPROCESSING PIPELINE")
        print("="*70)
        
        # Load data
        self.load_data()
        if self.df is None:
            return None
        
        # Explore data
        self.explore_data()
        
        # Clean data
        self.clean_data()
        
        # Generate summary stats
        self.get_summary_stats()
        
        # Save processed data
        self.save_processed_data()
        
        print("\n" + "="*70)
        print("✓ PIPELINE COMPLETE")
        print("="*70)
        
        return self.df_clean


def main():
    """Main execution function"""
    # Initialize and run the data loader
    loader = SuperstoreDataLoader()
    df_clean = loader.run_full_pipeline()
    
    if df_clean is not None:
        print("\n✓ Data is ready for analysis!")
        print(f"  Access cleaned data at: {loader.processed_path}")


if __name__ == "__main__":
    main()
