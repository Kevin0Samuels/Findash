import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from core.calculators import SIPCalculator

def create_price_chart(data, title):
    """Create interactive price chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['history'].index,
        y=data['history']['Close'],
        mode='lines',
        name='Price',
        line=dict(color='#1f77b4', width=2),
        hovertemplate='<b>Date:</b> %{x}<br><b>Price:</b> $%{y:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"{title} - 30 Day Price History",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        hovermode='x unified',
        showlegend=False,
        height=400
    )
    
    return fig

def create_sip_chart(timeline_data):
    """Create SIP growth chart"""
    df = pd.DataFrame(timeline_data)
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('SIP Growth Over Time', 'Investment vs Returns', 
                       'Year-wise Progress', 'Monthly Contribution Impact'),
        specs=[[{"secondary_y": False}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )

    fig.add_trace(
        go.Scatter(x=df['year'], y=df['invested'], name='Invested', line=dict(color='blue')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df['year'], y=df['value'], name='Portfolio Value', 
                  fill='tonexty', line=dict(color='green')),
        row=1, col=1
    )
    
    final_data = timeline_data[-1]
    fig.add_trace(
        go.Bar(x=['Invested', 'Returns', 'Profit'], 
               y=[final_data['invested'], final_data['value'], final_data['profit']],
               marker_color=['lightblue', 'lightgreen', 'gold'],
               showlegend=False),
        row=1, col=2
    )
    
    yearly_data = [d for d in timeline_data if d['month'] % 12 == 0]
    if yearly_data:
        years = [d['year'] for d in yearly_data]
        invested = [d['invested'] for d in yearly_data]
        values = [d['value'] for d in yearly_data]
        
        fig.add_trace(
            go.Bar(x=years, y=invested, name='Invested', marker_color='lightblue', showlegend=False),
            row=2, col=1
        )
        fig.add_trace(
            go.Bar(x=years, y=values, name='Value', marker_color='lightgreen', showlegend=False),
            row=2, col=1
        )
    
    amounts = [5000, 10000, 15000, 20000, 25000]
    calc = SIPCalculator()
    final_values = []
    
    for amount in amounts:
        years = len(timeline_data) / 12
        result = calc.calculate_sip_future_value(amount, 12, years)
        final_values.append(result['future_value'])
    
    fig.add_trace(
        go.Bar(x=amounts, y=final_values, marker_color='coral', showlegend=False),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=True, title_text="📊 SIP Analysis Dashboard")
    return fig