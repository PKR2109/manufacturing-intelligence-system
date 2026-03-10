import streamlit as st
import pandas as pd
import plotly.express as px
# PAGE CONFIG
st.set_page_config(
    page_title="Manufacturing Intelligence System",
    page_icon="🏭",
    layout="wide",
     initial_sidebar_state="expanded"
)

st.title("🏭 Manufacturing Intelligence System")

st.caption(
"Interactive analytics platform for identifying defect patterns in manufacturing production data."
)
with st.sidebar:

    st.header("About")

    st.write(
    """
    Manufacturing Intelligence System analyzes production datasets
    to identify defect patterns across machines, shifts, and tools.
    """
    )

    st.header("Capabilities")

    st.write(
    """
    • Machine defect analysis  
    • Shift correlation heatmap  
    • Tool performance insights  
    • Production timeline monitoring
    """
    )
# ------------------------------------------------
# GOOGLE STYLE THEME
# ------------------------------------------------

st.markdown("""
<style>

.stApp{
background:#f8fafc;
}

/* titles */

h1{
font-weight:600;
color:#202124;
}

h2,h3{
font-weight:500;
color:#202124;
}

/* cards */

.card{
background:white;
padding:20px;
border-radius:12px;
box-shadow:0 2px 6px rgba(0,0,0,0.08);
margin-bottom:18px;
}

/* insight panel */

.insight{
padding:10px;
border-left:4px solid #4285F4;
margin-bottom:10px;
background:#f1f5ff;
border-radius:6px;
}

</style>
""", unsafe_allow_html=True)

PASS="#34A853"
FAIL="#EA4335"

# ------------------------------------------------
# LOAD
# ------------------------------------------------

def load(file):

    if file.name.endswith(".csv"):
        return pd.read_csv(file)

    return pd.read_excel(file)

# ------------------------------------------------
# INSIGHTS
# ------------------------------------------------

def generate_summary(df):

    total=len(df)
    fails=(df["result"]=="FAIL").sum()

    machine=(
        df[df["result"]=="FAIL"]
        .groupby("machine_id")
        .size()
        .sort_values(ascending=False)
    )

    shift=(
        df[df["result"]=="FAIL"]
        .groupby("shift")
        .size()
        .sort_values(ascending=False)
    )

    tool=(
        df[df["result"]=="FAIL"]
        .groupby("tool_id")
        .size()
        .sort_values(ascending=False)
    )

    insights=[]

    insights.append(f"{fails} failures detected out of {total} parts.")

    if len(machine)>0:
        insights.append(f"Machine {machine.index[0]} produces most defects.")

    if len(shift)>0:
        insights.append(f"Shift {shift.index[0]} shows highest failure rate.")

    if len(tool)>0:
        insights.append(f"Tool {tool.index[0]} strongly correlates with failures.")

    return insights

# ------------------------------------------------
# HEADER
# ------------------------------------------------

st.title("Manufacturing Intelligence")

st.caption("Production monitoring and defect analytics")

# ------------------------------------------------
# UPLOAD
# ------------------------------------------------

file=st.file_uploader("Upload production dataset")

if file:

    df=load(file)

    df["timestamp"]=pd.to_datetime(df["timestamp"])

    main,side=st.columns([3,1])

# ------------------------------------------------
# MAIN DASHBOARD
# ------------------------------------------------

    with main:

        st.markdown("### Production Health")

        total=len(df)
        fails=(df["result"]=="FAIL").sum()
        rate=(fails/total)*100

        m1,m2,m3=st.columns(3)

        m1.metric("Parts Produced",total)
        m2.metric("Failures",fails)
        m3.metric("Defect Rate",f"{rate:.2f}%")

        fail_df=df[df["result"]=="FAIL"]

# ------------------------------------------------
# CHART GRID
# ------------------------------------------------

        c1,c2=st.columns(2)

        machine=(
            fail_df.groupby("machine_id")
            .size()
            .reset_index(name="failures")
        )

        fig1=px.pie(
            machine,
            names="machine_id",
            values="failures",
            hole=0.6,
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        with c1:
            st.plotly_chart(fig1,use_container_width=True)

        heat=(
            fail_df
            .pivot_table(
                index="machine_id",
                columns="shift",
                aggfunc="size",
                fill_value=0
            )
        )

        fig2=px.imshow(
            heat,
            color_continuous_scale="Blues"
        )

        with c2:
            st.plotly_chart(fig2,use_container_width=True)

        c3,c4=st.columns(2)

        timeline=px.scatter(
            df,
            x="timestamp",
            y="machine_id",
            color="result",
            color_discrete_map={"PASS":PASS,"FAIL":FAIL}
        )

        timeline.update_traces(marker=dict(size=6))

        with c3:
            st.plotly_chart(timeline,use_container_width=True)

        tool=(
            fail_df.groupby("tool_id")
            .size()
            .reset_index(name="failures")
        )

        fig4=px.bar(
            tool,
            x="tool_id",
            y="failures",
            color="failures",
            color_continuous_scale="teal"
        )

        with c4:
            st.plotly_chart(fig4,use_container_width=True)

# ------------------------------------------------
# INSIGHTS PANEL
# ------------------------------------------------

    with side:

        st.markdown("### Insights")

        insights=generate_summary(df)

        for i in insights:

            st.markdown(
            f"""
            <div class="insight">
            {i}
            </div>
            """,
            unsafe_allow_html=True
            )
            
# Footer  
         
st.markdown("---")

st.caption(
"Manufacturing Intelligence System | Built with Python, Streamlit, and Plotly"
)          