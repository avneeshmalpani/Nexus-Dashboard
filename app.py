
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import random

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="NEXUS | Smart Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0b1020;
    color: #f1f5f9;
}

[data-testid="stSidebar"] {
    background: #11182b;
    border-right: 1px solid #26334d;
}

[data-testid="stSidebar"] * {
    color: #e2e8f0;
}

.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -1px;
}

.subtitle {
    color: #94a3b8;
    font-size: 14px;
    margin-bottom: 25px;
}

.metric-card {
    background: linear-gradient(145deg, #17233c, #111a2e);
    padding: 22px;
    border: 1px solid #283956;
    border-radius: 16px;
    min-height: 125px;
}

.metric-label {
    color: #94a3b8;
    font-size: 13px;
    font-weight: 500;
}

.metric-value {
    color: #f8fafc;
    font-size: 27px;
    font-weight: 800;
    margin-top: 10px;
}

.metric-change {
    color: #34d399;
    font-size: 12px;
    margin-top: 5px;
}

.section-title {
    color: #f8fafc;
    font-size: 19px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 12px;
}

div[data-testid="stMetric"] {
    background: #17233c;
    border: 1px solid #283956;
    padding: 17px;
    border-radius: 14px;
}

.stButton > button {
    border-radius: 9px;
    border: 1px solid #3b82f6;
    background: #2563eb;
    color: white;
    font-weight: 600;
}

.stButton > button:hover {
    background: #1d4ed8;
    border-color: #60a5fa;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #283956;
    border-radius: 12px;
}

hr {
    border-color: #26334d;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SAMPLE DATA
# --------------------------------------------------

@st.cache_data
def create_sample_data():

    random.seed(42)

    dates = pd.date_range(
        end=date.today(),
        periods=90,
        freq="D"
    )

    categories = [
        "Electronics",
        "Fashion",
        "Food",
        "Books",
        "Accessories"
    ]

    data = []

    for d in dates:
        for category in categories:
            data.append({
                "Date": d,
                "Category": category,
                "Sales": random.randint(1000, 12000),
                "Orders": random.randint(5, 60),
                "Profit": random.randint(200, 4000)
            })

    return pd.DataFrame(data)


if "data" not in st.session_state:
    st.session_state.data = create_sample_data()

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "notes" not in st.session_state:
    st.session_state.notes = ""


df = st.session_state.data.copy()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("# ⚡ NEXUS")
    st.caption("SMART ANALYTICS PLATFORM")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Analytics",
            "Tasks",
            "Notes",
            "Data Manager",
            "About"
        ],
        label_visibility="visible"
    )

    st.divider()

    st.markdown("### ⚙️ Preferences")

    show_data = st.toggle("Show raw data", False)

    st.caption("NEXUS Dashboard v1.0")
    st.caption("Built with Python & Streamlit")


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">NEXUS Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your data. Your insights. Your control. '
    + datetime.now().strftime("%A, %d %B %Y")
    + '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------

def metric_card(label, value, change):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-change">{change}</div>
    </div>
    """, unsafe_allow_html=True)


def style_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#cbd5e1"),
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        )
    )
    return fig


# --------------------------------------------------
# OVERVIEW PAGE
# --------------------------------------------------

if page == "Overview":

    total_sales = df["Sales"].sum()
    total_orders = df["Orders"].sum()
    total_profit = df["Profit"].sum()
    avg_sales = df["Sales"].mean()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "TOTAL REVENUE",
            f"₹{total_sales:,.0f}",
            "↗ Sample dataset"
        )

    with c2:
        metric_card(
            "TOTAL ORDERS",
            f"{total_orders:,}",
            "↗ Sample dataset"
        )

    with c3:
        metric_card(
            "TOTAL PROFIT",
            f"₹{total_profit:,.0f}",
            "↗ Sample dataset"
        )

    with c4:
        metric_card(
            "AVERAGE SALES",
            f"₹{avg_sales:,.0f}",
            "Per category-day"
        )

    st.markdown('<div class="section-title">Revenue Overview</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns([1.7, 1])

    with col1:

        daily = df.groupby("Date", as_index=False)["Sales"].sum()

        fig = px.area(
            daily,
            x="Date",
            y="Sales",
            title="Daily Revenue Trend"
        )

        fig.update_traces(
            line_color="#818cf8",
            fillcolor="rgba(129,140,248,0.18)"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    with col2:

        category = df.groupby(
            "Category",
            as_index=False
        )["Sales"].sum()

        fig = px.pie(
            category,
            names="Category",
            values="Sales",
            hole=0.65,
            title="Revenue by Category"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    st.markdown(
        '<div class="section-title">Performance Analysis</div>',
        unsafe_allow_html=True
    )

    performance = df.groupby(
        "Category",
        as_index=False
    )[["Sales", "Profit", "Orders"]].sum()

    fig = px.bar(
        performance,
        x="Category",
        y=["Sales", "Profit"],
        barmode="group",
        title="Sales vs Profit"
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True
    )

    st.markdown("### Recent Records")
    st.dataframe(
        df.tail(10),
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# ANALYTICS PAGE
# --------------------------------------------------

elif page == "Analytics":

    st.markdown("## 📊 Advanced Analytics")
    st.caption("Explore your data with interactive filters.")

    selected_categories = st.multiselect(
        "Select categories",
        df["Category"].unique(),
        default=list(df["Category"].unique())
    )

    filtered = df[
        df["Category"].isin(selected_categories)
    ]

    if filtered.empty:
        st.warning("Select at least one category.")
    else:

        st.metric(
            "Filtered Revenue",
            f"₹{filtered['Sales'].sum():,.0f}"
        )

        fig = px.line(
            filtered.groupby(
                ["Date", "Category"],
                as_index=False
            )["Sales"].sum(),
            x="Date",
            y="Sales",
            color="Category",
            markers=True,
            title="Category-wise Revenue"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

        fig = px.scatter(
            filtered,
            x="Sales",
            y="Profit",
            size="Orders",
            color="Category",
            hover_data=["Date"],
            title="Sales vs Profit Relationship"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

        st.markdown("### Statistical Summary")
        st.dataframe(
            filtered[["Sales", "Orders", "Profit"]].describe(),
            use_container_width=True
        )


# --------------------------------------------------
# TASK MANAGER
# --------------------------------------------------

elif page == "Tasks":

    st.markdown("## ✅ Productivity Centre")
    st.caption("Organise your work and track your progress.")

    with st.form("task_form", clear_on_submit=True):

        task_name = st.text_input(
            "Task description",
            placeholder="Enter a task..."
        )

        priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High"]
        )

        deadline = st.date_input(
            "Deadline",
            value=date.today()
        )

        submitted = st.form_submit_button("Add Task")

        if submitted and task_name.strip():

            st.session_state.tasks.append({
                "Task": task_name.strip(),
                "Priority": priority,
                "Deadline": deadline,
                "Completed": False
            })

            st.success("Task added successfully!")

    st.divider()

    tasks = st.session_state.tasks

    if tasks:

        completed = sum(
            1 for t in tasks if t["Completed"]
        )

        total = len(tasks)

        st.progress(
            completed / total,
            text=f"{completed} of {total} tasks completed"
        )

        for i, task in enumerate(tasks):

            col1, col2, col3 = st.columns([5, 2, 1])

            with col1:

                checked = st.checkbox(
                    f"{task['Task']} — {task['Priority']} priority",
                    value=task["Completed"],
                    key=f"task_{i}"
                )

                st.session_state.tasks[i]["Completed"] = checked

            with col2:
                st.caption(f"Due: {task['Deadline']}")

            with col3:
                if st.button("🗑️", key=f"delete_{i}"):
                    st.session_state.tasks.pop(i)
                    st.rerun()

    else:
        st.info("No tasks yet. Add your first task above!")


# --------------------------------------------------
# NOTES PAGE
# --------------------------------------------------

elif page == "Notes":

    st.markdown("## 📝 Personal Notes")
    st.caption("Your personal space for ideas and reminders.")

    st.session_state.notes = st.text_area(
        "Write your notes here",
        value=st.session_state.notes,
        height=300,
        placeholder="Start writing..."
    )

    st.success("Notes are maintained during this session.")

    st.download_button(
        "⬇️ Download Notes",
        data=st.session_state.notes,
        file_name="my_notes.txt",
        mime="text/plain"
    )


# --------------------------------------------------
# DATA MANAGER
# --------------------------------------------------

elif page == "Data Manager":

    st.markdown("## 🗂️ Data Management")

    st.write(
        "Upload your own CSV dataset to replace the sample data."
    )

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if uploaded_file:

        try:
            new_df = pd.read_csv(uploaded_file)

            required_columns = {
                "Date", "Category", "Sales", "Orders", "Profit"
            }

            if required_columns.issubset(new_df.columns):

                new_df["Date"] = pd.to_datetime(
                    new_df["Date"],
                    errors="coerce"
                )

                new_df = new_df.dropna(
                    subset=["Date", "Category", "Sales",
                            "Orders", "Profit"]
                )

                if new_df.empty:
                    st.error("The uploaded file has no valid records.")
                else:
                    st.session_state.data = new_df
                    st.success("Dataset uploaded successfully!")
                    st.rerun()

            else:
                st.error(
                    "CSV must contain: Date, Category, Sales, "
                    "Orders and Profit."
                )

        except Exception as e:
            st.error(f"Could not read the file: {e}")

    st.markdown("### Current Dataset")

    st.write(f"Total records: {len(df)}")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "⬇️ Export Dataset as CSV",
        data=df.to_csv(index=False),
        file_name="nexus_data.csv",
        mime="text/csv"
    )

    if st.button("Reset to Sample Dataset"):

        st.session_state.data = create_sample_data()
        st.success("Sample data restored!")
        st.rerun()


# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------

elif page == "About":

    st.markdown("## ⚡ About NEXUS")

    st.markdown("""
    Welcome to **NEXUS**, a modern analytics and productivity
    dashboard.

    ### Features

    - Interactive analytics and charts
    - Revenue and performance tracking
    - Category-wise comparisons
    - Personal task management
    - Notes and reminders
    - CSV import and export
    - Customisable data exploration

    ### Technology Stack

    | Technology | Purpose |
    |---|---|
    | Python | Core programming |
    | Streamlit | Web application |
    | Pandas | Data management |
    | Plotly | Interactive charts |

    **Version:** 1.0

    **Note:** The initial dataset is randomly generated
    sample data. It does not represent actual business revenue.
    """)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    "<center style='color:#64748b;font-size:12px;'>"
    "NEXUS © 2026 | Built with Python & Streamlit"
    "</center>",
    unsafe_allow_html=True
)
