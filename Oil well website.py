import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.cluster import KMeans
import numpy as np

# PAGE CONFIG
st.set_page_config(
    page_title="Oil Well Production Insights - Russia",
    page_icon="🛢️",
    layout="wide"
)

# LOAD & CLEAN DATA
@st.cache_data
def load_data():
    df = pd.read_csv("Oil well.csv")

    df = df.iloc[1:].reset_index(drop=True)
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    return df

df = load_data()
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

# TITLE
st.title("🛢️ Russian Oil Well Production Intelligence Platform")

# TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Data Overview",
    "📈 Production Trends",
    "⚙️ Performance Periods",
    "🧠 Production Regimes",
    "📌 Strategic Insights"
])

# TAB 1: DATA OVERVIEW
with tab1:
    st.subheader("Dataset Overview")
    st.dataframe(df, use_container_width=True)

    st.subheader("Summary Statistics")
    st.dataframe(df.describe(), use_container_width=True)

# TAB 2: PRODUCTION TRENDS
with tab2:
    st.subheader("Production Trend Analysis Over Time")

    metric = st.selectbox("Select Production Metric", numeric_cols)
    window = st.slider("Smoothing Window", 10, 100, 50)

    rolling_avg = df[metric].rolling(window).mean()

    fig, ax = plt.subplots(figsize=(18, 6))
    ax.scatter(df.index, df[metric], alpha=0.3, s=10, label="Daily Measurements")
    ax.plot(df.index, rolling_avg, linewidth=2, label="Rolling Average")

    ax.set_xlabel("Time Index")
    ax.set_ylabel(metric)
    ax.set_title(f"{metric} Trend")
    ax.legend()

    st.pyplot(fig)

    st.info("🔍 Highlights long-term decline, instability, or recovery phases in the well lifecycle.")

# TAB 3: PERFORMANCE PERIODS
with tab3:
    st.subheader("High vs Low Production Periods")

    perf_metric = st.selectbox("Choose Metric", numeric_cols)

    threshold = st.slider(
        "Performance Threshold",
        float(df[perf_metric].min()),
        float(df[perf_metric].max()),
        float(df[perf_metric].median())
    )

    col1, col2 = st.columns(2)

    with col1:
        st.success("High Production Periods")
        st.dataframe(df[df[perf_metric] >= threshold])

    with col2:
        st.warning("Low Production Periods")
        st.dataframe(df[df[perf_metric] < threshold])

    st.info("📌 Identifies periods requiring optimization or intervention.")

# TAB 4: PRODUCTION REGIME CLUSTERING
with tab4:
    st.subheader("Production Regime Segmentation")

    cluster_features = st.multiselect(
        "Select Features for Clustering",
        numeric_cols,
        default=numeric_cols[:2]
    )

    if len(cluster_features) >= 2:
        k = st.slider("Number of Production Regimes", 2, 5, 3)

        data = df[cluster_features].dropna().copy()

        model = KMeans(n_clusters=k, random_state=42)
        data["Regime"] = model.fit_predict(data)

        centroids = model.cluster_centers_

        regime_labels = {
            0: "Stable Production",
            1: "Declining / Water-Dominated",
            2: "High Output / Optimal Operation"
        }

        fig, ax = plt.subplots(figsize=(12, 6))

        for regime_id in np.unique(data["Regime"]):
            subset = data[data["Regime"] == regime_id]
            ax.scatter(
                subset[cluster_features[0]],
                subset[cluster_features[1]],
                alpha=0.6,
                s=25,
                label=regime_labels.get(regime_id, f"Regime {regime_id}")
            )

        ax.scatter(
            centroids[:, 0],
            centroids[:, 1],
            c="black",
            s=250,
            marker="X",
            label="Cluster Centroids"
        )

        ax.set_xlabel(cluster_features[0])
        ax.set_ylabel(cluster_features[1])
        ax.set_title("Oil Well Production Regimes")
        ax.legend(title="Operational States")
        ax.grid(alpha=0.3)

        st.pyplot(fig)

        data["Regime Description"] = data["Regime"].map(regime_labels)
        st.dataframe(data)

        st.info("""
        🧠 **Interpretation**
        - Clusters represent **operating regimes over time**
        - Useful for identifying instability, water breakthrough, and late-life decline
        """)

    else:
        st.warning("Select at least two features.")

# TAB 5: STRATEGIC INSIGHTS
with tab5:
    st.subheader("Operational Decision Support")

    st.markdown("""
    - Detect transition into water-dominated flow
    - Identify optimal operating windows
    - Support shut-in or workover decisions
    - Enable future real-time monitoring via database integration
    """)

    st.success("✔ Time-based intelligence for production optimization.")

# FOOTER
st.markdown("---")
st.caption("Oil Well Production Analytics")
