import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Config
st.set_page_config(
    page_title="Boehringer Ingelheim Annual Highlights",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Dark Theme Styling ---
st.markdown("""
<style>
body {background-color: #0d1117; color: white;}
.main {background: transparent;}
[data-testid="stHeader"] {background: transparent;}
[data-testid="stSidebar"] {background: linear-gradient(135deg, #0d1117, #161b22);}
[data-testid="stToolbar"] {right: 2rem;}
div.stButton>button {
    background-color: #6a0dad;
    color: white;
    border-radius: 10px;
    padding: 10px 24px;
    font-weight: bold;
}
.header-banner {
    background: linear-gradient(90deg, #6a0dad, #00c6ff);
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
}
.header-banner h1 {
    color: white;
    font-size: 3rem;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# --- Landing Banner ---
st.markdown("""
<div class="header-banner">
    <h1>Boehringer Ingelheim</h1>
    <marquee behavior="scroll" direction="left" style="color:white;font-size:18px;">
        🚀 Innovation | 🌍 Global Reach | 💊 Human Pharma | 🧬 Animal Health | 🌱 Sustainability 
    </marquee>
</div>
""", unsafe_allow_html=True)

# --- Data Definitions ---
data = {
    '2020': {
        'metrics': {'Total Revenue': "€19.566B", 'R&D Investment': "€3.696B", 'Operating Income': "€4.624B"},
        'trend': {'Year': [2017, 2018, 2019, 2020], 'Revenue': [18.1, 17.5, 19.0, 19.566], 'R&D Expenses': [3.2, 3.5, 3.6, 3.696]}
    },
    '2021': {
        'metrics': {'Total Revenue': "€20.6B", 'R&D Investment': "€4.093B", 'Operating Income': "€4.728B"},
        'trend': {'Year': [2018, 2019, 2020, 2021], 'Revenue': [17.5, 19.0, 19.566, 20.6], 'R&D Expenses': [3.5, 3.6, 3.696, 4.093]}
    },
    '2022': {
        'metrics': {'Total Revenue': "€24.1B", 'R&D Investment': "€5.002B", 'Operating Income': "€5.083B"},
        'trend': {'Year': [2019, 2020, 2021, 2022], 'Revenue': [19.0, 19.566, 20.6, 24.1], 'R&D Expenses': [3.6, 3.696, 4.093, 5.002]}
    },
    '2023': {
        'metrics': {'Total Revenue': "€25.6B", 'R&D Investment': "€5.8B", 'Operating Income': "€4.9B"},
        'trend': {'Year': [2020, 2021, 2022, 2023], 'Revenue': [19.566, 20.6, 24.1, 25.6], 'R&D Expenses': [3.696, 4.093, 5.002, 5.8]}
    },
    '2024': {
        'metrics': {'Total Revenue': "€26.8B", 'R&D Investment': "€6.2B", 'Operating Income': "TBD"},
        'trend': {'Year': [2021, 2022, 2023, 2024], 'Revenue': [20.6, 24.1, 25.6, 26.8], 'R&D Expenses': [4.093, 5.002, 5.8, 6.2]}
    }
}

# --- Sidebar Year Selector ---
st.sidebar.title("Select Year")
year = st.sidebar.selectbox("", sorted(data.keys()), index=3)
selected = data[year]

# --- App Title ---
st.markdown("# 💊 Boehringer Ingelheim Annual Highlights (2020–2024)")

# --- KPI Cards ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", selected['metrics']['Total Revenue'])
col2.metric("R&D Investment", selected['metrics']['R&D Investment'])
col3.metric("Operating Income", selected['metrics']['Operating Income'])

st.markdown("---")

# --- Trend Line: Revenue and R&D Investment ---
fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(x=selected['trend']['Year'], y=selected['trend']['Revenue'], mode='lines+markers', name='Revenue (Billion €)', line=dict(color='cyan')))
fig_trend.add_trace(go.Scatter(x=selected['trend']['Year'], y=selected['trend']['R&D Expenses'], mode='lines+markers', name='R&D Investment (Billion €)', line=dict(color='magenta')))
fig_trend.update_layout(title="📈 Revenue and R&D Investment Trends", xaxis_title="Year", yaxis_title="Billion €", template="plotly_dark")
st.plotly_chart(fig_trend, use_container_width=True)

# --- Bubble Chart: Product Growth ---
products_df = pd.DataFrame({
    'Product': ['JARDIANCE®', 'OFEV®', 'TRADJENTA®', 'SPIRIVA®', 'ACTILYSE®'],
    'Revenue': [8.3, 3.7, 1.6, 1.0, 0.6],
    'Growth': [13.2, 7.3, -5.0, -17.7, 10.7]
})
products_df['BubbleSize'] = products_df['Growth'].abs()
fig_bubble = px.scatter(
    products_df,
    x="Product",
    y="Revenue",
    size="BubbleSize",
    color="Growth",
    size_max=60,
    template="plotly_dark",
    title="🚀 Top Products by Revenue and Growth Impact"
)
st.plotly_chart(fig_bubble, use_container_width=True)

# --- Plan of Action ---
st.markdown("### 📋 Strategic Plan of Action")
actions = [
    "Expand R&D investment into Cardiovascular, Oncology, CNS, Fibrosis",
    "Drive Digital Health and AI-driven drug discovery",
    "Expand Access to Healthcare across Emerging Markets",
    "Achieve Carbon Neutrality by 2030",
    "Strengthen Human and Animal Health synergies"
]
for action in actions:
    st.success(f"✅ {action}")

# --- Footer ---
st.markdown("---")
st.caption("Boehringer Ingelheim • Powered by Streamlit 🚀 | 2020–2024 Annual Insights")
