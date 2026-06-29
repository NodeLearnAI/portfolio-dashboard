import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import plotly.graph_objects as go
from components import render_sidebar

render_sidebar()
st.title("Portfolio Analysis")

# Guard — check if holdings have been analysed yet
if "portfolio_returns" not in st.session_state:
    st.info("Go to My Holdings, enter your positions and click Analyse Portfolio first.")
    st.stop()

portfolio_returns = st.session_state["portfolio_returns"]
summary_df = st.session_state["summary_df"]  # you'll need to store this in 4_Holdings.py

col1, col2 = st.columns(2)

with col1:
    #Plot the pie chart
    pie_fig = go.Figure()
    pie_fig.add_trace(go.Pie(
        labels=summary_df['Ticker'],
        values = summary_df['Weight'],
        hole=0.4
    ))
    st.plotly_chart(pie_fig)

cumulative = (1+portfolio_returns).cumprod()

with col2:
    scatter_fig = go.Figure()
    scatter_fig.add_trace(go.Scatter(
        x=cumulative.index, y= cumulative.values, mode='lines'
    ))

    scatter_fig.update_xaxes(title_text='Date')
    scatter_fig.update_yaxes(title_text= 'Growth of $1')
    scatter_fig.update_layout(title= 'Portfolio Cumulative Returns')
    scatter_fig.add_hline(y=1.0, line_dash="dash", line_color="gray")
    
    st.plotly_chart(scatter_fig)


