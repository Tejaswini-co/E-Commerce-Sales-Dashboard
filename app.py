"""
Production-Ready Dashboard for Deployment
Optimized for free hosting on Render, Railway, or similar platforms
"""

import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import os


# Load data
def load_data():
    """Load the cleaned data"""
    # Try multiple paths for deployment environments
    possible_paths = [
        'data/processed/superstore_clean.csv',
        './data/processed/superstore_clean.csv',
        '../data/processed/superstore_clean.csv',
        'superstore_clean.csv'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path, parse_dates=['Order Date', 'Ship Date'])
            print(f"✓ Loaded {len(df)} records from {path}")
            return df
    
    # If no file found, create sample data (fallback for demo)
    print("⚠ Data file not found, using sample data")
    return create_sample_data()


def create_sample_data():
    """Create sample data if CSV not available"""
    np.random.seed(42)
    n = 1000
    
    df = pd.DataFrame({
        'Order Date': pd.date_range('2014-01-01', periods=n, freq='D'),
        'Sales': np.random.uniform(100, 10000, n),
        'Profit': np.random.uniform(-500, 3000, n),
        'Region': np.random.choice(['East', 'West', 'Central', 'South'], n),
        'Category': np.random.choice(['Technology', 'Furniture', 'Office Supplies'], n),
        'Segment': np.random.choice(['Consumer', 'Corporate', 'Home Office'], n),
        'Order ID': [f'ORD-{i:05d}' for i in range(n)],
        'Customer ID': [f'CUST-{i%100:03d}' for i in range(n)],
        'Product Name': [f'Product {i%50}' for i in range(n)],
        'Year_Month': pd.date_range('2014-01-01', periods=n, freq='D').strftime('%Y-%m'),
        'Year': pd.date_range('2014-01-01', periods=n, freq='D').year
    })
    return df


# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server  # Required for deployment

# Load data
df = load_data()

# Custom styling
custom_style = {
    'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'padding': '30px',
    'borderRadius': '15px',
    'marginBottom': '30px',
    'boxShadow': '0 10px 30px rgba(0,0,0,0.3)'
}

card_style = {
    'borderRadius': '15px',
    'boxShadow': '0 4px 15px rgba(0,0,0,0.1)',
    'border': 'none',
    'transition': 'transform 0.3s'
}

# Layout
app.layout = dbc.Container([
    # Header with gradient background
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("📊 E-Commerce Sales Analytics Dashboard", 
                       className="text-center mb-2",
                       style={'color': 'white', 'fontWeight': 'bold', 'fontSize': '2.5rem'}),
                html.P("Real-time Business Intelligence & Performance Monitoring",
                       className="text-center",
                       style={'color': 'rgba(255,255,255,0.9)', 'fontSize': '1.1rem'})
            ], style=custom_style)
        ])
    ]),
    
    # KPI Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Span("💰", style={'fontSize': '2rem'}),
                        html.H6("Total Revenue", className="text-muted mb-2"),
                        html.H2(f"${df['Sales'].sum():,.0f}", 
                               style={'color': '#06A77D', 'fontWeight': 'bold'}),
                        html.P(f"+{len(df):,} transactions", 
                              className="text-muted small mb-0")
                    ])
                ])
            ], style=card_style, className="mb-4")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Span("💵", style={'fontSize': '2rem'}),
                        html.H6("Total Profit", className="text-muted mb-2"),
                        html.H2(f"${df['Profit'].sum():,.0f}", 
                               style={'color': '#F18F01', 'fontWeight': 'bold'}),
                        html.P(f"Margin: {(df['Profit'].sum()/df['Sales'].sum()*100):.1f}%", 
                              className="text-muted small mb-0")
                    ])
                ])
            ], style=card_style, className="mb-4")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Span("🛒", style={'fontSize': '2rem'}),
                        html.H6("Total Orders", className="text-muted mb-2"),
                        html.H2(f"{df['Order ID'].nunique():,}", 
                               style={'color': '#2E86AB', 'fontWeight': 'bold'}),
                        html.P(f"{df['Customer ID'].nunique():,} customers", 
                              className="text-muted small mb-0")
                    ])
                ])
            ], style=card_style, className="mb-4")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Span("📈", style={'fontSize': '2rem'}),
                        html.H6("Avg Order Value", className="text-muted mb-2"),
                        html.H2(f"${df.groupby('Order ID')['Sales'].sum().mean():,.0f}", 
                               style={'color': '#A23B72', 'fontWeight': 'bold'}),
                        html.P(f"{df['Order ID'].nunique()/df['Customer ID'].nunique():.1f} orders/customer", 
                              className="text-muted small mb-0")
                    ])
                ])
            ], style=card_style, className="mb-4")
        ], width=3),
    ]),
    
    # Filters Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🎯 Filter Analytics", className="mb-3", 
                           style={'color': '#667eea', 'fontWeight': 'bold'}),
                    dbc.Row([
                        dbc.Col([
                            html.Label("🗺️ Region:", style={'fontWeight': 'bold', 'color': '#555'}),
                            dcc.Dropdown(
                                id='region-filter',
                                options=[{'label': '🌍 All Regions', 'value': 'All'}] + 
                                        [{'label': f'📍 {r}', 'value': r} for r in sorted(df['Region'].unique())],
                                value='All',
                                clearable=False,
                                style={'marginBottom': '15px'}
                            )
                        ], width=3),
                        
                        dbc.Col([
                            html.Label("📦 Category:", style={'fontWeight': 'bold', 'color': '#555'}),
                            dcc.Dropdown(
                                id='category-filter',
                                options=[{'label': '📊 All Categories', 'value': 'All'}] + 
                                        [{'label': f'🏷️ {c}', 'value': c} for c in sorted(df['Category'].unique())],
                                value='All',
                                clearable=False,
                                style={'marginBottom': '15px'}
                            )
                        ], width=3),
                        
                        dbc.Col([
                            html.Label("👥 Segment:", style={'fontWeight': 'bold', 'color': '#555'}),
                            dcc.Dropdown(
                                id='segment-filter',
                                options=[{'label': '👨‍💼 All Segments', 'value': 'All'}] + 
                                        [{'label': f'🎯 {s}', 'value': s} for s in sorted(df['Segment'].unique())],
                                value='All',
                                clearable=False,
                                style={'marginBottom': '15px'}
                            )
                        ], width=3),
                        
                        dbc.Col([
                            html.Label("📅 Year:", style={'fontWeight': 'bold', 'color': '#555'}),
                            dcc.Dropdown(
                                id='year-filter',
                                options=[{'label': '🗓️ All Years', 'value': 'All'}] + 
                                        [{'label': f'📆 {y}', 'value': y} for y in sorted(df['Year'].unique())],
                                value='All',
                                clearable=False,
                                style={'marginBottom': '15px'}
                            )
                        ], width=3),
                    ])
                ])
            ], style={'borderRadius': '15px', 'boxShadow': '0 4px 15px rgba(0,0,0,0.1)'})
        ])
    ], className="mb-4"),
    
    # Charts Row 1
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='monthly-revenue-chart')
        ], width=8),
        
        dbc.Col([
            dcc.Graph(id='regional-pie-chart')
        ], width=4),
    ]),
    
    # Charts Row 2
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='category-bar-chart')
        ], width=6),
        
        dbc.Col([
            dcc.Graph(id='profit-margin-chart')
        ], width=6),
    ]),
    
    # Charts Row 3
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='top-products-chart')
        ], width=12),
    ]),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(style={'margin': '40px 0'}),
            html.Div([
                html.P([
                    "📊 E-Commerce Sales Analytics Dashboard  |  ",
                    html.Span("Superstore Dataset 2014-2017", style={'fontWeight': 'bold'}),
                    "  |  Built with Python, Plotly & Dash"
                ], className="text-center", 
                   style={'color': '#666', 'fontSize': '0.9rem', 'marginBottom': '10px'}),
                html.P([
                    "💡 Real-time interactive analytics for data-driven business decisions"
                ], className="text-center", 
                   style={'color': '#999', 'fontSize': '0.85rem'})
            ], style={
                'background': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
                'padding': '20px',
                'borderRadius': '10px'
            })
        ])
    ], className="mb-4")
    
], fluid=True)


# Callbacks
@app.callback(
    [Output('monthly-revenue-chart', 'figure'),
     Output('regional-pie-chart', 'figure'),
     Output('category-bar-chart', 'figure'),
     Output('profit-margin-chart', 'figure'),
     Output('top-products-chart', 'figure')],
    [Input('region-filter', 'value'),
     Input('category-filter', 'value'),
     Input('segment-filter', 'value'),
     Input('year-filter', 'value')]
)
def update_charts(region, category, segment, year):
    # Filter data
    filtered_df = df.copy()
    
    if region != 'All':
        filtered_df = filtered_df[filtered_df['Region'] == region]
    if category != 'All':
        filtered_df = filtered_df[filtered_df['Category'] == category]
    if segment != 'All':
        filtered_df = filtered_df[filtered_df['Segment'] == segment]
    if year != 'All':
        filtered_df = filtered_df[filtered_df['Year'] == year]
    
    # Chart 1: Monthly Revenue Trend
    monthly_sales = filtered_df.groupby('Year_Month')['Sales'].sum().reset_index()
    fig1 = px.line(monthly_sales, x='Year_Month', y='Sales',
                  title='📈 Monthly Revenue Trend',
                  labels={'Sales': 'Revenue ($)', 'Year_Month': 'Month'})
    fig1.update_traces(line_color='#667eea', line_width=4, 
                      fill='tozeroy', fillcolor='rgba(102, 126, 234, 0.1)')
    fig1.update_layout(
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=12),
        title_font=dict(size=18, color='#333', family="Arial Black"),
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    # Chart 2: Regional Distribution (Pie)
    regional_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()
    fig2 = px.pie(regional_sales, values='Sales', names='Region',
                 title='🗺️ Sales Distribution by Region',
                 color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#4facfe'])
    fig2.update_traces(textposition='inside', textinfo='percent+label',
                      marker=dict(line=dict(color='white', width=2)))
    fig2.update_layout(
        showlegend=True,
        font=dict(family="Arial, sans-serif", size=12),
        title_font=dict(size=18, color='#333', family="Arial Black"),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    # Chart 3: Category Performance (Bar)
    category_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index()
    category_sales = category_sales.sort_values('Sales', ascending=True)
    fig3 = px.bar(category_sales, x='Sales', y='Category',
                 title='📦 Sales Performance by Category',
                 orientation='h',
                 color='Sales',
                 color_continuous_scale=[[0, '#4facfe'], [0.5, '#667eea'], [1, '#764ba2']])
    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=12),
        title_font=dict(size=18, color='#333', family="Arial Black"),
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
        yaxis=dict(showgrid=False),
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=False
    )
    fig3.update_traces(marker_line_color='white', marker_line_width=1.5)
    
    # Chart 4: Profit Margin by Category
    profit_data = filtered_df.groupby('Category').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    profit_data['Profit_Margin'] = (profit_data['Profit'] / profit_data['Sales'] * 100)
    fig4 = px.bar(profit_data, x='Category', y='Profit_Margin',
                 title='💰 Profit Margin Performance by Category',
                 color='Profit_Margin',
                 color_continuous_scale=[[0, '#ff6b6b'], [0.5, '#ffd93d'], [1, '#6bcf7f']])
    fig4.update_layout(
        yaxis_title='Profit Margin (%)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=12),
        title_font=dict(size=18, color='#333', family="Arial Black"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=False
    )
    fig4.update_traces(marker_line_color='white', marker_line_width=1.5)
    
    # Chart 5: Top 10 Products
    top_products = filtered_df.groupby('Product Name')['Sales'].sum().nlargest(10).reset_index()
    top_products = top_products.sort_values('Sales', ascending=True)
    fig5 = px.bar(top_products, x='Sales', y='Product Name',
                 title='🏆 Top 10 Bestselling Products',
                 orientation='h',
                 color='Sales',
                 color_continuous_scale=[[0, '#f093fb'], [0.5, '#667eea'], [1, '#764ba2']])
    fig5.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=12),
        title_font=dict(size=18, color='#333', family="Arial Black"),
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
        yaxis=dict(showgrid=False),
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=False
    )
    fig5.update_traces(marker_line_color='white', marker_line_width=1.5)
    
    return fig1, fig2, fig3, fig4, fig5


if __name__ == '__main__':
    # Get port from environment variable (for deployment) or use 8050 (for local)
    port = int(os.environ.get('PORT', 8050))
    
    print("="*70)
    print("🚀 DASHBOARD LAUNCHING")
    print("="*70)
    print(f"✓ Running on port: {port}")
    print(f"✓ Debug mode: {os.environ.get('DEBUG', 'True')}")
    print("="*70)
    
    app.run(debug=os.environ.get('DEBUG', 'True') == 'True', 
            host='0.0.0.0', 
            port=port)
