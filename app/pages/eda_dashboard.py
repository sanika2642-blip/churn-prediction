import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(layout="wide")

# (Keep the same CSS from Home for consistency)

st.markdown("<h2 style='letter-spacing: -1px;'>Intelligence Overview</h2>", unsafe_allow_html=True)

# --- CUSTOM METRICS (The "Numbers" in your inspo) ---
m1, m2, m3, m4 = st.columns(4)

def styled_metric(label, value, delta):
    st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); padding: 25px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);">
            <p style="color: #888; font-size: 0.9rem; margin-bottom: 5px;">{label}</p>
            <h2 style="margin: 0; font-size: 2rem;">{value}</h2>
            <p style="color: #00CC96; font-size: 0.8rem; margin: 0;">↑ {delta}</p>
        </div>
    """, unsafe_allow_html=True)

with m1: styled_metric("Active Users", "5,493", "12%")
with m2: styled_metric("Retention", "94.2%", "2.1%")
with m3: styled_metric("MRR", "$134,985", "4.5%")
with m4: styled_metric("Churn Risk", "Low", "Stable")

st.write("##")

# --- HIGH-END CHART (Custom Plotly) ---
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("### Revenue vs Retention Trend")
    # Custom Gradient Area Chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1,2,3,4,5], y=[10,15,13,17,22], fill='tozeroy', 
                             line=dict(color='#636EFA', width=4),
                             fillcolor='rgba(99, 110, 250, 0.2)'))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, color='#555'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#555'),
        margin=dict(l=0, r=0, t=0, b=0), height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("### Segment Distribution")
    # Modern Donut
    fig_pie = go.Figure(data=[go.Pie(labels=['Fiber', 'DSL', 'None'], values=[4500, 2500, 1000], hole=.8)])
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0), height=400,
        annotations=[dict(text='Services', x=0.5, y=0.5, font_size=20, showarrow=False, font_color="white")]
    )
    fig_pie.update_traces(marker=dict(colors=['#636EFA', '#AB63FA', '#00CC96']))
    st.plotly_chart(fig_pie, use_container_width=True)