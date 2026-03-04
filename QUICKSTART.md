# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Download the Dataset
1. Visit: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
2. Download `Sample - Superstore.csv`
3. Place it in: `data/raw/Sample - Superstore.csv`

### Step 3: Run Data Preprocessing
```bash
python src/data_loader.py
```

### Step 4: Run Analysis
```bash
# Run all analyses at once
python src/analysis.py

# Or run individual analyses
python src/revenue_trends.py
python src/regional_analysis.py
python src/profit_analysis.py
python src/product_analysis.py
```

### Step 5: Create Visualizations
```bash
# Create static charts
python visualizations/create_charts.py

# Launch interactive dashboard
python visualizations/dashboard.py
```

## 📊 What You'll Get

After running the analyses, you'll have:

### CSV Reports in `output/` folder:
- Monthly revenue trends
- Regional performance metrics
- Profit margin analysis
- Top products list
- And more...

### Visualizations:
- Revenue trend charts
- Regional comparison graphs
- Profit margin analysis
- Top 10 products charts
- Category performance dashboards
- Executive summary dashboard

### Interactive Dashboard:
- Web-based interactive dashboard
- Filter by region, category, segment, year
- Real-time chart updates
- Access at `http://localhost:8050/`

## 🔧 Troubleshooting

### Issue: "File not found"
**Solution:** Make sure you've downloaded the dataset and placed it in `data/raw/`

### Issue: "Module not found"
**Solution:** Install requirements: `pip install -r requirements.txt`

### Issue: Dashboard won't start
**Solution:** Check if port 8050 is available. Change port in `visualizations/dashboard.py` if needed.

## 📁 Output Structure

```
output/
├── revenue_trends/
│   ├── monthly_revenue.csv
│   ├── yearly_revenue.csv
│   └── *.png charts
├── regional_analysis/
│   ├── regional_performance.csv
│   ├── state_performance.csv
│   └── *.png charts
├── profit_analysis/
│   ├── category_profitability.csv
│   ├── discount_impact.csv
│   └── *.png charts
└── product_analysis/
    ├── products_by_sales.csv
    ├── products_by_profit.csv
    └── *.png charts
```

## 💡 Tips

1. **Start with analysis.py** - It runs everything in the right order
2. **Check CSV files first** - They contain all the numbers
3. **View PNG charts** - Visual summaries of the data
4. **Use the dashboard** - Most interactive and user-friendly

## 🎯 Next Steps

1. Review the analysis results
2. Use insights to create your presentation
3. Import data into Tableau/Power BI for advanced dashboards
4. Customize the scripts for your specific needs

---

Need help? Check the full README.md for detailed documentation.
