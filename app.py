import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="UIDAI Automated Analytics", layout="wide")

st.title("UIDAI Biometric Update Automated Analytics System")
st.write("Upload UIDAI Excel or CSV dataset. The system will analyze automatically.")

file = st.file_uploader("Upload UIDAI Dataset", type=["csv", "xlsx"])

if file:

    # Read dataset
    if file.name.endswith(".xlsx"):
        df = pd.read_excel(file)
    else:
        df = pd.read_csv(file)

    st.success("Dataset uploaded successfully")

    # Preview
    st.subheader("Original Dataset Preview")
    st.dataframe(df.head(10))

    # Detect age columns automatically
    age5_col = None
    age17_col = None

    for col in df.columns:
        if "5" in col and "age" in col.lower():
            age5_col = col
        if "17" in col and "age" in col.lower():
            age17_col = col

    if age5_col is None or age17_col is None:
        st.error("Age group columns not detected automatically.")
        st.stop()

    # 🔹 Row-wise Total Update Calculation
    df["total_updates"] = df[age5_col] + df[age17_col]

    st.subheader("Dataset with Row-wise Total Updates")
    st.dataframe(df.head(10))

    # KPI Section
    st.subheader("Key Performance Indicators")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Records", len(df))
    c2.metric("Total Updates (All Rows)", int(df["total_updates"].sum()))
    c3.metric("Average Updates per Record", int(df["total_updates"].mean()))

    # State filter
    if "state" in df.columns:
        state = st.selectbox("Select State", df["state"].unique())
        filtered = df[df["state"] == state]
    else:
        filtered = df

    # District chart
    if "district" in df.columns:

        chart_data = filtered.groupby("district")["total_updates"].sum()
        chart_data = chart_data.sort_values(ascending=False).head(10)

        chart_type = st.radio("Select Chart Type", ["Bar Chart", "Pie Chart"])

        fig, ax = plt.subplots(figsize=(8,6))

        if chart_type == "Bar Chart":
            chart_data.plot(kind="bar", ax=ax)
            plt.xticks(rotation=45, ha="right")
            ax.set_ylabel("Total Updates")
        else:
            chart_data.plot(kind="pie", autopct="%1.1f%%", ax=ax)
            ax.set_ylabel("")

        ax.set_title("Top 10 District Biometric Updates")
        plt.tight_layout()
        st.pyplot(fig)

        # Insights
        st.subheader("Automated Insights")
        st.write(f"Total biometric updates in selected data: {chart_data.sum()}")
        st.write(f"Highest update district: {chart_data.idxmax()} with {chart_data.max()} updates")
        st.write(f"Lowest update district among top 10: {chart_data.idxmin()}")

    # Download analyzed data
    st.subheader("Download Analyzed Dataset")

    st.download_button(
        "Download CSV with Row-wise Total Updates",
        df.to_csv(index=False),
        file_name="uidai_analyzed_data.csv"
    )
