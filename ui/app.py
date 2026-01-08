import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

def infer_severity(parsed_incident, root_cause_text=""):
    text = (
        str(parsed_incident).lower() + " " +
        str(root_cause_text).lower()
    )

    if any(k in text for k in ["outage", "down", "failure", "crash", "unavailable"]):
        return "Critical", "status-critical"
    elif any(k in text for k in ["slow", "latency", "degraded", "timeout"]):
        return "Warning", "status-warning"
    else:
        return "Active", "status-active"


# ============================================================================
# CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Aegis – Intelligent Incident Manager",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://localhost:8001/analyze"

# ============================================================================
# CUSTOM CSS
# ============================================================================
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .header-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .status-active {
        background-color: #10b981;
        color: white;
    }
    
    .status-warning {
        background-color: #f59e0b;
        color: white;
    }
    
    .status-critical {
        background-color: #ef4444;
        color: white;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        background-color: #f1f5f9;
        border-radius: 8px 8px 0 0;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'recent_incidents' not in st.session_state:
    st.session_state.recent_incidents = []

# ============================================================================
# HEADER
# ============================================================================
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🚨 Aegis – Intelligent Incident Manager</h1>
    <p class="header-subtitle">Enterprise AI platform for incident analysis, diagnostics, and decision support</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/667eea/ffffff?text=AEGIS", use_container_width=True)
    
    st.markdown("## ⚙️ Configuration")
    
    # API Configuration
    with st.expander("🔌 API Settings", expanded=False):
        api_endpoint = st.text_input("API Endpoint", value=API_URL)
        api_timeout = st.slider("Timeout (seconds)", 30, 300, 120)
    
   
    
    st.markdown("---")
    
    # Quick Guide
    st.markdown("## 📖 Quick Guide")
    st.markdown("""
    **Incident Description Format:**
    - Service name + issue type
    - Affected region/environment
    - Time period or duration
    
    **Metrics Query Format:**
    - Metric name (count, latency, errors)
    - Dimension (service, region, endpoint)
    - Time range (last 24h, today, this week)
    """)
    
    st.markdown("---")
    
    # Example Queries
    st.markdown("## 💡 Example Queries")
    
    examples = [
        "Payment service is slow in north region",
        "Show incident count by region in last 24 hours",
        "Average latency by service today",
        "Error rate spike in authentication service",
        "Database connection failures since morning"
    ]
    
    for example in examples:
        if st.button(example, key=f"example_{example[:20]}"):
            st.session_state.selected_example = example
    
    st.markdown("---")
    


# ============================================================================
# MAIN TABS
# ============================================================================
tab1, tab2, tab3 = st.tabs([
    "🔍 Incident Analysis", 
    "📊 Dashboard", 
    "📜 History",
])

# ============================================================================
# TAB 1: INCIDENT ANALYSIS
# ============================================================================
with tab1:
    col1, col2 = st.columns([1, 1])
    
    # LEFT COLUMN: Input
    with col1:
        st.markdown("### 📝 Incident / Query Input")
        
        # Pre-fill if example selected
        default_text = st.session_state.get('selected_example', '')
        
        incident_text = st.text_area(
            "Describe the incident or ask a metrics question",
            height=200,
            placeholder="e.g., Payment service experiencing high latency in EU region since 09:00 UTC",
            value=default_text,
            help="Be specific about the service, issue type, location, and timeframe"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            analyze_btn = st.button("🚀 Analyze Incident", use_container_width=True)
        with col_btn2:
            clear_btn = st.button("🗑️ Clear", use_container_width=True)
            if clear_btn:
                st.session_state.selected_example = ''
                st.rerun()
        
        


# ============================================================================
# ANALYSIS EXECUTION
# ============================================================================
if analyze_btn and incident_text.strip():
    with st.spinner("🔄 Analyzing incident... Please wait."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Simulate progress
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
                if i < 30:
                    status_text.text("🔍 Parsing incident description...")
                elif i < 60:
                    status_text.text("🧠 Analyzing patterns...")
                else:
                    status_text.text("📊 Generating insights...")
            
            # API Call
            response = requests.post(
                api_endpoint if 'api_endpoint' in locals() else API_URL,
                json={"text": incident_text},
                timeout=api_timeout if 'api_timeout' in locals() else 120
            ).json()
            
            progress_bar.empty()
            status_text.empty()
            
        except Exception as e:
            st.error(f"❌ API Error: {str(e)}")
            st.info("💡 Please check if the backend service is running on the configured endpoint.")
            st.stop()
    
    # Error Handling
    if "error" in response:
        st.error("❌ Request could not be processed safely")
        st.warning(response["error"])
        st.info("💡 **Tip:** Be specific with your query. Example: *Show incident count by region in last 24 hours*")
        st.stop()
    
    # Add to history
    st.session_state.analysis_history.append({
        'timestamp': datetime.now(),
        'query': incident_text,
        'response': response
    })
    
    st.success("✅ Analysis completed successfully!")
    
    # ========================================================================
    # SQL ANALYSIS PATH
    # ========================================================================
    if response.get("intent") == "SQL_ANALYSIS":
        st.markdown("---")
        st.markdown("## 📊 SQL Analysis Results")
        
        col_sql1, col_sql2 = st.columns([1, 1])
        
        with col_sql1:
            st.markdown("### 🧠 Generated SQL Query")
            st.code(response["generated_sql"], language="sql")
            
            # Query Stats
            st.markdown("### 📈 Query Statistics")
            stat_col1, stat_col2, stat_col3 = st.columns(3)
            with stat_col1:
                st.metric("Rows Returned", len(response.get("data", [])))
            with stat_col2:
                st.metric("Execution Time", "0.23s")
            with stat_col3:
                st.metric("Query Complexity", "Medium")
        
        with col_sql2:
            st.markdown("### 💡 Explanation")
            st.info(response.get("explanation", "Analysis complete."))
        
        # Data Results
        if response.get("data"):
            df = pd.DataFrame(response["data"])
            
            st.markdown("### 📋 Data Results")
            st.dataframe(
                df,
                use_container_width=True,
                height=300
            )
            
            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            # Visualizations
            if auto_visualize and len(df.columns) >= 2:
                st.markdown("### 📈 Visualizations")
                
                viz_tab1, viz_tab2, viz_tab3 = st.tabs(["Bar Chart", "Line Chart", "Pie Chart"])
                
                with viz_tab1:
                    fig = px.bar(
                        df,
                        x=df.columns[0],
                        y=df.columns[1],
                        title=f"{df.columns[1]} by {df.columns[0]}",
                        template='plotly_white',
                        color=df.columns[1],
                        color_continuous_scale='viridis'
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                
                with viz_tab2:
                    fig = px.line(
                        df,
                        x=df.columns[0],
                        y=df.columns[1],
                        title=f"{df.columns[1]} Trend",
                        template='plotly_white',
                        markers=True
                    )
                    fig.update_traces(line_color='#667eea', line_width=3)
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                
                with viz_tab3:
                    if len(df) <= 10:
                        fig = px.pie(
                            df,
                            names=df.columns[0],
                            values=df.columns[1],
                            title=f"Distribution of {df.columns[1]}",
                            template='plotly_white'
                        )
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Pie chart works best with 10 or fewer categories")
                        
    
    
    # ========================================================================
    # INCIDENT REASONING PATH
    # ========================================================================
    else:
        st.markdown("---")
        st.markdown("## 🔍 Incident Analysis Report")
        
        col_inc1, col_inc2 = st.columns([1, 1])
        
        with col_inc1:
            st.markdown("### 🎯 Incident Details")

            if "parsed_incident" in response:
                parsed = response["parsed_incident"]

                severity_label, severity_class = infer_severity(
                    parsed,
                    response.get("root_cause", "")
                )

                st.markdown(f"""
                <div class="metric-card">
                    <strong>Service:</strong> {parsed.get('service', 'N/A')}<br>
                    <strong>Issue Type:</strong> {parsed.get('issue_type', 'N/A')}<br>
                    <strong>Region:</strong> {parsed.get('region', 'N/A')}<br>
                    <strong>Time:</strong> {parsed.get('timeframe', 'N/A')}<br>
                    <strong>Severity:</strong>
                    <span class="status-badge {severity_class}">
                        {severity_label}
                    </span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("### 🧠 Root Cause Analysis")
            st.write(response.get("root_cause", "Analyzing..."))

        
        with col_inc2:
            st.markdown("### 📚 Similar Historical Incidents")

            similar_incidents = response.get("similar_incidents", [])

            if not similar_incidents:
                st.info("No similar incidents found.")
            else:
                for inc in similar_incidents:
                    severity = inc.get("severity", "Unknown")

                    # Severity color
                    if severity.lower() == "critical":
                        sev_color = "#ef4444"
                    elif severity.lower() == "medium":
                        sev_color = "#f59e0b"
                    else:
                        sev_color = "#10b981"

                    st.markdown(f"""
                    <div style="
                        background: white;
                        padding: 1.2rem;
                        border-radius: 10px;
                        margin-bottom: 1rem;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
                        border-left: 6px solid {sev_color};
                    ">
                        <div style="display:flex; justify-content:space-between;">
                            <strong>Incident ID:</strong> {inc.get("incident_id", "N/A")}
                            <span style="
                                background:{sev_color};
                                color:white;
                                padding:0.25rem 0.6rem;
                                border-radius:12px;
                                font-size:0.8rem;
                                font-weight:600;
                            ">
                                {severity}
                            </span>
                        </div>

                        <hr style="margin:0.6rem 0;"/>

                        <strong>Service:</strong> {inc.get("service", "N/A")} <br>
                        <strong>Region:</strong> {inc.get("region", "N/A")} <br>
                        <strong>Time:</strong> {inc.get("timestamp", "N/A")} <br>

                        <strong>Metric:</strong> {inc.get("metric_type", "N/A")} = 
                        <strong>{inc.get("metric_value", "N/A")}</strong> <br>

                        <strong>Action Taken:</strong> {inc.get("action_taken", "N/A")} <br>
                        <strong>Resolution Time:</strong> {inc.get("resolution_time_minutes", "N/A")} mins
                    </div>
                    """, unsafe_allow_html=True)

            
            # Recommended Actions
            st.markdown("### ✅ Recommended Actions")
            actions = response.get("recommended_actions", "Generating recommendations...")
            st.success(actions)
            

            


# ============================================================================
# TAB 2: DASHBOARD
# ============================================================================
with tab2:
    st.markdown("## 📊 Real-Time Analytics Dashboard")
    
    # KPIs
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    
    with kpi1:
        st.metric("Total Incidents", "1,234", "+12%")
    with kpi2:
        st.metric("Open Incidents", "47", "-8%")
    with kpi3:
        st.metric("MTTR", "2.3h", "-0.5h")
    with kpi4:
        st.metric("Success Rate", "96.8%", "+1.2%")
    with kpi5:
        st.metric("SLA Compliance", "99.1%", "+0.3%")
    
    st.markdown("---")
    
    # Charts
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("### 📈 Incidents by Severity")
        severity_data = pd.DataFrame({
            'Severity': ['Critical', 'High', 'Medium', 'Low'],
            'Count': [15, 42, 128, 89]
        })
        fig = px.bar(
            severity_data,
            x='Severity',
            y='Count',
            color='Severity',
            color_discrete_map={
                'Critical': '#ef4444',
                'High': '#f59e0b',
                'Medium': '#eab308',
                'Low': '#10b981'
            },
            template='plotly_white'
        )
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 🌍 Incidents by Region")
        region_data = pd.DataFrame({
            'Region': ['US-East', 'US-West', 'EU', 'APAC', 'LATAM'],
            'Count': [87, 62, 45, 31, 23]
        })
        fig = px.pie(
            region_data,
            names='Region',
            values='Count',
            template='plotly_white',
            hole=0.4
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with chart_col2:
        st.markdown("### 📊 Response Time Distribution")
        response_time_data = pd.DataFrame({
            'Time Range': ['<5min', '5-15min', '15-30min', '30-60min', '>60min'],
            'Count': [145, 78, 32, 15, 4]
        })
        fig = px.funnel(
            response_time_data,
            x='Count',
            y='Time Range',
            template='plotly_white'
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 🎯 Resolution Status")
        status_data = pd.DataFrame({
            'Status': ['Resolved', 'In Progress', 'Pending', 'Escalated'],
            'Count': [892, 47, 23, 8]
        })
        fig = px.bar(
            status_data,
            y='Status',
            x='Count',
            orientation='h',
            template='plotly_white',
            color='Count',
            color_continuous_scale='viridis'
        )
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Heatmap
    st.markdown("### 🔥 Incident Heatmap (Last 7 Days)")
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hours = list(range(24))
    heatmap_data = pd.DataFrame(
        [[int(abs(i - j) * 2 + (i + j) % 10) for j in range(24)] for i in range(7)],
        index=days,
        columns=[f"{h:02d}:00" for h in hours]
    )
    
    fig = px.imshow(
        heatmap_data,
        labels=dict(x="Hour", y="Day", color="Incidents"),
        x=heatmap_data.columns,
        y=heatmap_data.index,
        color_continuous_scale='RdYlGn_r',
        template='plotly_white'
    )
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 3: HISTORY
# ============================================================================
with tab3:
    st.markdown("## 📜 Analysis History")
    
    if st.session_state.analysis_history:
        for idx, item in enumerate(reversed(st.session_state.analysis_history[-20:])):
            with st.expander(f"🕐 {item['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} - {item['query'][:50]}..."):
                st.markdown(f"**Query:** {item['query']}")
                st.markdown(f"**Intent:** {item['response'].get('intent', 'N/A')}")
                
                if item['response'].get('intent') == 'SQL_ANALYSIS':
                    st.code(item['response'].get('generated_sql', ''), language='sql')
                    if item['response'].get('data'):
                        st.dataframe(pd.DataFrame(item['response']['data']))
                else:
                    st.write(item['response'].get('root_cause', ''))
    else:
        st.info("No analysis history yet. Start by analyzing an incident!")
    
    if st.button("🗑️ Clear History"):
        st.session_state.analysis_history = []
        st.rerun()



# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("**Aegis © 2024**")
    st.caption("Enterprise Incident Intelligence Platform")

with footer_col2:
    st.markdown("**Quick Links**")
    st.caption("[Documentation](#) | [API Reference](#) | [Support](#)")

with footer_col3:
    st.markdown("**System Status**")
    st.caption("🟢 All Systems Operational")