"""
Interactive Dashboard using Plotly Dash
Launch an interactive web-based dashboard for sales analysis
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


class SalesDashboard:
    """Interactive sales dashboard"""
    
    def __init__(self):
        self.data_path = Path(__file__).parent.parent / 'data' / 'processed' / 'superstore_clean.csv'
        self.df = None
        self.app = None
    
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
    
    def create_app(self):
        """Create the Dash application"""
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
        self.app.title = "E-Commerce Sales Dashboard"
        
        # Custom CSS styling
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
        self.app.layout = dbc.Container([
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
            
            # KPI Cards with enhanced styling
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.Span("💰", style={'fontSize': '2rem'}),
                                html.H6("Total Revenue", className="text-muted mb-2"),
                                html.H2(f"${self.df['Sales'].sum():,.0f}", 
                                       style={'color': '#06A77D', 'fontWeight': 'bold'}),
                                html.P(f"+{len(self.df):,} transactions", 
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
                                html.H2(f"${self.df['Profit'].sum():,.0f}", 
                                       style={'color': '#F18F01', 'fontWeight': 'bold'}),
                                html.P(f"Margin: {(self.df['Profit'].sum()/self.df['Sales'].sum()*100):.1f}%", 
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
                                html.H2(f"{self.df['Order ID'].nunique():,}", 
                                       style={'color': '#2E86AB', 'fontWeight': 'bold'}),
                                html.P(f"{self.df['Customer ID'].nunique():,} customers", 
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
                                html.H2(f"${self.df.groupby('Order ID')['Sales'].sum().mean():,.0f}", 
                                       style={'color': '#A23B72', 'fontWeight': 'bold'}),
                                html.P(f"{self.df['Order ID'].nunique()/self.df['Customer ID'].nunique():.1f} orders/customer", 
                                      className="text-muted small mb-0")
                            ])
                        ])
                    ], style=card_style, className="mb-4")
                ], width=3),
            ]),
            
            # Filters Section with enhanced styling
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
                                                [{'label': f'📍 {r}', 'value': r} for r in sorted(self.df['Region'].unique())],
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
                                                [{'label': f'🏷️ {c}', 'value': c} for c in sorted(self.df['Category'].unique())],
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
                                                [{'label': f'🎯 {s}', 'value': s} for s in sorted(self.df['Segment'].unique())],
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
                                                [{'label': f'📆 {y}', 'value': y} for y in sorted(self.df['Year'].unique())],
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
        self.setup_callbacks()
    
    def setup_callbacks(self):
        """Setup interactive callbacks"""
        
        @self.app.callback(
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
            filtered_df = self.df.copy()
            
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
    
    def run(self, debug=True, port=8050):
        """Run the dashboard"""
        print("="*70)
        print("LAUNCHING INTERACTIVE DASHBOARD")
        print("="*70)
        print(f"\n✓ Dashboard is running at: http://localhost:{port}/")
        print("\nPress Ctrl+C to stop the server\n")
        print("="*70)
        
        self.app.run(debug=debug, port=port)


def main():
    """Main execution"""
    dashboard = SalesDashboard()
    
    if not dashboard.load_data():
        print("\n❌ Cannot load data. Please run data preprocessing first:")
        print("   python src/data_loader.py")
        return
    
    dashboard.create_app()
    dashboard.run()


if __name__ == "__main__":
    main()
