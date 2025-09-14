import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_processor import load_and_process_data
from ai_insights import ask_ai

st.set_page_config(page_title="Marketing Intelligence Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

@st.cache_data
def load_data():
    return load_and_process_data()

def create_chart(data, chart_type, x, y, title, **kwargs):
    if chart_type == "bar":
        fig = px.bar(data, x=x, y=y, title=title, **kwargs)
    elif chart_type == "scatter":
        fig = px.scatter(data, x=x, y=y, title=title, **kwargs)
    return fig

def main():
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; border-bottom: 2px solid #e0e0e0; margin-bottom: 2rem;">
        <h1 style="color: #1f2937; margin: 0; font-size: 2.5rem;">Marketing Intelligence Dashboard</h1>
        <p style="color: #6b7280; margin: 0.5rem 0 0 0; font-size: 1.1rem;">AI-Powered Marketing Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    marketing_data, business_data = load_data()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## Analysis Controls")
        st.markdown("---")
        min_date, max_date = marketing_data['date'].min(), marketing_data['date'].max()
        date_range = st.date_input("Select period", value=(min_date, max_date), min_value=min_date, max_value=max_date, label_visibility="collapsed")
        st.markdown("---")
        platforms = st.multiselect("Select platforms", marketing_data['platform'].unique(), default=marketing_data['platform'].unique(), label_visibility="collapsed")
    
    # Filter data
    if len(date_range) == 2:
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered_marketing = marketing_data[(marketing_data['date'] >= start_date) & (marketing_data['date'] <= end_date) & (marketing_data['platform'].isin(platforms))]
        filtered_business = business_data[(business_data['date'] >= start_date) & (business_data['date'] <= end_date)]
    else:
        filtered_marketing = marketing_data[marketing_data['platform'].isin(platforms)]
        filtered_business = business_data
    
    # Executive Summary
    st.markdown("## Executive Summary")
    st.markdown("---")
    total_spend = filtered_marketing['spend'].sum()
    total_revenue = filtered_marketing['attributed revenue'].sum()
    roas = total_revenue / total_spend if total_spend > 0 else 0
    total_orders = filtered_business['# of orders'].sum() if len(filtered_business) > 0 else 0
    new_customers = filtered_business['new customers'].sum() if len(filtered_business) > 0 else 0
    cac = total_spend / new_customers if new_customers > 0 else 0
    
    def format_compact(num):
        if abs(num) >= 1_000_000:
            return f"{num/1_000_000:.2f}M"
        elif abs(num) >= 1_000:
            return f"{num/1_000:.2f}K"
        else:
            return f"{num:.0f}"

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.metric("Marketing Spend", f"${format_compact(total_spend)}")
    with col2: st.metric("Attributed Revenue", f"${format_compact(total_revenue)}")
    with col3: st.metric("ROAS", f"{roas:.2f}x")
    with col4: st.metric("Total Orders", f"{format_compact(total_orders)}")
    with col5: st.metric("Customer Acquisition Cost", f"${format_compact(cac)}")
    
    # Channel Performance
    st.markdown("## Channel Performance")
    st.markdown("---")
    if len(filtered_marketing) > 0:
        channel_analysis = filtered_marketing.groupby('platform').agg({'spend': 'sum', 'attributed revenue': 'sum', 'roas': 'mean'}).round(2)
        col1, col2 = st.columns(2)
        with col1: st.plotly_chart(create_chart(channel_analysis.reset_index(), "bar", 'platform', 'roas', "ROAS by Platform", color='roas', color_continuous_scale='RdYlGn'), use_container_width=True)
        with col2: st.plotly_chart(create_chart(channel_analysis.reset_index(), "scatter", 'spend', 'attributed revenue', "Marketing Efficiency", size='roas', color='platform', color_discrete_map={'Facebook': '#1877F2', 'Google': '#4285F4', 'TikTok': '#000000'}), use_container_width=True)
    else:
        st.info("No marketing data available for the selected filters.")
    
    # Geographic Analysis
    st.markdown("## Geographic Analysis")
    st.markdown("---")
    if len(filtered_marketing) > 0:
        state_analysis = filtered_marketing.groupby('state').agg({'spend': 'sum', 'attributed revenue': 'sum', 'roas': 'mean'}).round(2)
        col1, col2 = st.columns(2)
        with col1: st.plotly_chart(create_chart(state_analysis.reset_index(), "bar", 'state', 'roas', "ROAS by State", color='roas', color_continuous_scale='RdYlGn'), use_container_width=True)
        with col2: st.plotly_chart(create_chart(state_analysis.reset_index(), "scatter", 'spend', 'attributed revenue', "Market Opportunity", size='roas', color='state', color_discrete_map={'CA': '#FF6B6B', 'NY': '#4ECDC4'}), use_container_width=True)
    else:
        st.info("No geographic data available for the selected filters.")
    
    # Performance Trends
    st.markdown("## Performance Trends")
    st.markdown("---")
    if len(filtered_marketing) > 0:
        daily_data = filtered_marketing.groupby('date').agg({'spend': 'sum', 'attributed revenue': 'sum', 'roas': 'mean'}).reset_index()
        daily_data['spend_growth'] = daily_data['spend'].pct_change() * 100
        fig = make_subplots(rows=2, cols=2, subplot_titles=('Marketing Spend', 'Revenue Generation', 'ROAS Performance', 'Growth Rate'))
        fig.add_trace(go.Scatter(x=daily_data['date'], y=daily_data['spend'], name='Spend', line=dict(color='#1f77b4')), row=1, col=1)
        fig.add_trace(go.Scatter(x=daily_data['date'], y=daily_data['attributed revenue'], name='Revenue', line=dict(color='#2ca02c')), row=1, col=2)
        fig.add_trace(go.Scatter(x=daily_data['date'], y=daily_data['roas'], name='ROAS', line=dict(color='#ff7f0e')), row=2, col=1)
        fig.add_trace(go.Scatter(x=daily_data['date'], y=daily_data['spend_growth'], name='Growth', line=dict(color='#d62728')), row=2, col=2)
        fig.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No trend data available for the selected filters.")
    
    # Business Impact
    if len(filtered_business) > 0:
        st.markdown("## Business Impact")
        st.markdown("---")
        daily_marketing = filtered_marketing.groupby('date').agg({'spend': 'sum', 'attributed revenue': 'sum'}).reset_index()
        daily_business = filtered_business.groupby('date').agg({'# of orders': 'sum', 'total revenue': 'sum'}).reset_index()
        combined = daily_marketing.merge(daily_business, on='date', how='inner')
        col1, col2 = st.columns(2)
        with col1: st.plotly_chart(create_chart(combined, "scatter", 'spend', '# of orders', "Spend Impact on Orders", color='attributed revenue', color_continuous_scale='RdYlGn'), use_container_width=True)
        with col2: st.plotly_chart(create_chart(combined, "scatter", 'attributed revenue', 'total revenue', "Attributed vs Total Revenue", color_continuous_scale='RdYlGn'), use_container_width=True)
    
    # Strategic Recommendations
    st.markdown("## Strategic Recommendations")
    st.markdown("---")
    if len(filtered_marketing) > 0:
        channel_performance = filtered_marketing.groupby('platform').agg({'spend': 'sum', 'attributed revenue': 'sum', 'roas': 'mean', 'ctr': 'mean', 'cpc': 'mean'}).round(2)
        state_performance = filtered_marketing.groupby('state').agg({'spend': 'sum', 'attributed revenue': 'sum', 'roas': 'mean'}).round(2)
        tactic_performance = filtered_marketing.groupby('tactic').agg({'spend': 'sum', 'attributed revenue': 'sum', 'roas': 'mean'}).round(2)
        
        avg_roas = channel_performance['roas'].mean()
        avg_ctr = channel_performance['ctr'].mean()
        avg_cpc = channel_performance['cpc'].mean()
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Growth Opportunities")
            if len(channel_performance) > 0:
                best_channel = channel_performance['roas'].idxmax()
                best_channel_roas = channel_performance['roas'].max()
                best_channel_spend = channel_performance.loc[best_channel, 'spend']
                spend_share = (best_channel_spend / channel_performance['spend'].sum()) * 100
                st.success(f"**Scale {best_channel} Campaigns**")
                st.write(f"• Current ROAS: {best_channel_roas:.2f}x (vs avg {avg_roas:.2f}x)")
                st.write(f"• Current spend share: {spend_share:.1f}%")
                st.write(f"• Recommendation: Increase budget by 20-30%")
            
            if len(state_performance) > 0:
                best_state = state_performance['roas'].idxmax()
                best_state_roas = state_performance['roas'].max()
                best_state_spend = state_performance.loc[best_state, 'spend']
                st.success(f"**Expand {best_state} Market**")
                st.write(f"• ROAS: {best_state_roas:.2f}x")
                st.write(f"• Current investment: ${best_state_spend:,.0f}")
                st.write(f"• Recommendation: Test new tactics and increase geo-targeting")
            
            if len(tactic_performance) > 0:
                best_tactic = tactic_performance['roas'].idxmax()
                best_tactic_roas = tactic_performance['roas'].max()
                st.success(f"**Optimize {best_tactic} Strategy**")
                st.write(f"• ROAS: {best_tactic_roas:.2f}x")
                st.write(f"• Recommendation: Apply this tactic across all platforms")
        
        with col2:
            st.markdown("### Optimization Areas")
            if len(channel_performance) > 0:
                underperforming = channel_performance[channel_performance['roas'] < avg_roas]
                if len(underperforming) > 0:
                    worst_channel = underperforming['roas'].idxmin()
                    worst_roas = underperforming.loc[worst_channel, 'roas']
                    worst_cpc = underperforming.loc[worst_channel, 'cpc']
                    st.warning(f"**Improve {worst_channel} Performance**")
                    st.write(f"• Current ROAS: {worst_roas:.2f}x (below avg {avg_roas:.2f}x)")
                    st.write(f"• CPC: ${worst_cpc:.2f} (vs avg ${avg_cpc:.2f})")
                    st.write(f"• Action: Review targeting, creative, or pause campaigns")
            
            if len(channel_performance) > 0:
                high_cpc = channel_performance[channel_performance['cpc'] > avg_cpc * 1.2]
                if len(high_cpc) > 0:
                    expensive_channel = high_cpc['cpc'].idxmax()
                    expensive_cpc = high_cpc.loc[expensive_channel, 'cpc']
                    st.warning(f"**Reduce {expensive_channel} Costs**")
                    st.write(f"• Current CPC: ${expensive_cpc:.2f}")
                    st.write(f"• Industry benchmark: ${avg_cpc:.2f}")
                    st.write(f"• Action: Optimize keywords, improve CTR, or adjust bids")
            
            if len(channel_performance) > 1:
                total_spend = channel_performance['spend'].sum()
                low_roi_channels = channel_performance[channel_performance['roas'] < avg_roas]
                if len(low_roi_channels) > 0:
                    realloc_amount = low_roi_channels['spend'].sum()
                    realloc_potential = realloc_amount * 0.5
                    st.info(f"**Budget Reallocation Opportunity**")
                    st.write(f"• Underperforming spend: ${realloc_amount:,.0f}")
                    st.write(f"• Reallocation potential: ${realloc_potential:,.0f}")
                    st.write(f"• Expected impact: 15-25% ROAS improvement")
        
        # Strategic Insights
        st.markdown("### Strategic Insights")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Overall ROAS", f"{roas:.2f}x", delta="Above Target" if roas > 3.0 else "Needs Improvement")
        with col2: st.metric("Marketing Efficiency", f"{(roas / 4.0) * 100:.0f}/100", delta="Excellent" if (roas / 4.0) * 100 > 80 else "Good" if (roas / 4.0) * 100 > 60 else "Needs Work")
        with col3: st.metric("Growth Potential", f"{((channel_performance['roas'].max() - channel_performance['roas'].min()) / channel_performance['roas'].min()) * 100:.0f}%" if len(channel_performance) > 0 else "0%", delta="High Opportunity" if len(channel_performance) > 0 and ((channel_performance['roas'].max() - channel_performance['roas'].min()) / channel_performance['roas'].min()) * 100 > 50 else "Moderate")
    
    else:
        st.info("No marketing data available for strategic recommendations. Please adjust your filters to see insights.")
    
    # AI Assistant
    st.markdown("---")
    st.markdown("## AI Marketing Assistant")
    st.markdown("---")
    
    
        
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("Ask about your marketing data below..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your data..."):
                response = ask_ai(prompt, filtered_marketing, filtered_business)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()