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

    # Remove first row
    df = df.iloc[1:].reset_index(drop=True)

    # Promote first row as headers
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)

    # Convert numeric columns
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    return df

df = load_data()

numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

# TITLE
st.title("🛢️ Russian Oil Well Production Intelligence Platform Streamlit App")
st.markdown("Actionable insights derived from oil well production data")

# TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Data Overview",
    "📈 Production Trends",
    "🏭 Well Performance",
    "🧠 Clustering Insights",
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
    st.subheader("Production Trend Analysis")

    metric = st.selectbox("Select Production Metric", numeric_cols)
    window = st.slider("Smoothing Window", 10, 100, 50)

    rolling_avg = df[metric].rolling(window).mean()

    fig, ax = plt.subplots(figsize=(18, 6))
    ax.scatter(df.index, df[metric], alpha=0.3, s=10, label="Raw Production")
    ax.plot(df.index, rolling_avg, linewidth=2, label="Rolling Average")

    ax.set_xlabel("Well Index")
    ax.set_ylabel(metric)
    ax.set_title(f"{metric} Production Trend")
    ax.legend()

    st.pyplot(fig)

    st.info("🔍 Rolling averages reveal long-term production decline or growth patterns. It helps identify aging or high-risk wells")

# TAB 3: WELL PERFORMANCE
with tab3:
    st.subheader("High vs Low Performing Wells")

    perf_metric = st.selectbox("Choose Performance Metric", numeric_cols)

    threshold = st.slider(
        "Performance Threshold",
        float(df[perf_metric].min()),
        float(df[perf_metric].max()),
        float(df[perf_metric].median())
    )

    col1, col2 = st.columns(2)

    with col1:
        st.success("High Performing Wells")
        st.dataframe(df[df[perf_metric] >= threshold])

    with col2:
        st.warning("Low Performing Wells")
        st.dataframe(df[df[perf_metric] < threshold])

    st.info("📌 Target declining wells for intervention and optimization.")

# TAB 4: CLUSTERING INSIGHTS (IMPROVED & LABELED)
with tab4:
    st.subheader("Oil Well Segmentation Using K-Means")

    cluster_features = st.multiselect(
        "Select Features for Clustering",
        numeric_cols,
        default=numeric_cols[:2]
    )

    if len(cluster_features) >= 2:
        k = st.slider("Number of Clusters (k)", 2, 6, 3)

        data = df[cluster_features].dropna().copy()

        model = KMeans(n_clusters=k, random_state=42)
        data["Cluster"] = model.fit_predict(data)

        centroids = model.cluster_centers_

        # Meaningful cluster labels
        cluster_labels = {
            0: "Moderate Producers",
            1: "Low Producers",
            2: "High Producers"
        }

        fig, ax = plt.subplots(figsize=(12, 6))

        for cluster_id, label in cluster_labels.items():
            subset = data[data["Cluster"] == cluster_id]
            ax.scatter(
                subset[cluster_features[0]],
                subset[cluster_features[1]],
                alpha=0.6,
                s=25,
                label=label
            )

        # Plot centroids
        ax.scatter(
            centroids[:, 0],
            centroids[:, 1],
            c="black",
            s=250,
            marker="X",
            label="Cluster Centroids"
        )

        # Annotate centroids
        for i, centroid in enumerate(centroids):
            ax.annotate(
                cluster_labels.get(i, f"Cluster {i}"),
                (centroid[0], centroid[1]),
                textcoords="offset points",
                xytext=(10, 10),
                fontsize=10,
                fontweight="bold"
            )

        ax.set_xlabel(cluster_features[0])
        ax.set_ylabel(cluster_features[1])
        ax.set_title("Oil Well Clusters by Production Performance")
        ax.legend(title="Well Categories")
        ax.grid(alpha=0.3)

        st.pyplot(fig)

        # Show labeled cluster data
        data["Cluster Name"] = data["Cluster"].map(cluster_labels)
        st.dataframe(data)

        st.info("""
        🧠 **Cluster Meaning**
        • **Low Producers:** Declining or marginal wells  
        • **Moderate Producers:** Stable, mid-life wells  
        • **High Producers:** Strategic high-value assets  

        🎯 Apply different operational strategies per cluster.
        """)

    else:
        st.warning("Select at least two features for clustering.")

# TAB 5: STRATEGIC INSIGHTS
with tab5:
    st.subheader("Strategic Decision Support")

    st.markdown("""
    **Key Actions Derived from Data**
    - Prioritize high-producing wells
    - Optimize moderate producers
    - Intervene early in declining wells
    - Allocate budgets using cluster behavior
    """)

    st.success("✔ Enables evidence-based oil production decisions.")

# FOOTER
st.markdown("---")
st.caption("Developed using Streamlit | Russian Oil Well Production Analytics")
