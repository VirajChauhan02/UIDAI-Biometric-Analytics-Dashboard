import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="UIDAI Automated Analytics", layout="wide")

st.title("UIDAI Biometric Update Automated Analytics System")
st.write("Upload UIDAI Excel/CSV file. System will analyze automatically.")

file = st.file_uploader("Upload UIDAI Dataset", type=["csv","xlsx"])

if file:

    # ---- Read File ----
    if file.name.endswith(".xlsx"):
        df = pd.read_excel(file)
    else:
        df = pd.read_csv(file)

    st.success("Dataset uploaded successfully!")

    # ---- Preview ----
    st.subheader("Dataset Preview")
    st.dataframe(df.head(10))

    # ---- Detect Age Columns ----
    age5_col = None
    age17_col = None

    for col in df.columns:
        if "5" in col and "age" in col.lower():
            age5_col = col
        if "17" in col and "age" in col.lower():
            age17_col = col

    if age5_col is None or age17_col is None:
        st.error("Age columns not detected. Please rename properly.")
        st.stop()

    df["total_updates"] = df[age5_col] + df[age17_col]

    # ---- KPI SECTION ----
    st.subheader("Key Performance Indicators")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Records", len(df))
    col2.metric("Total Updates", int(df["total_updates"].sum()))
    col3.metric("Average Updates", int(df["total_updates"].mean()))

    # ---- State Selection ----
    if "state" in df.columns:
        state = st.selectbox("Select State", df["state"].unique())
        filtered = df[df["state"] == state]
    else:
        filtered = df

    # ---- District Chart ----
    if "district" in df.columns:

        chart_data = filtered.groupby("district")["total_updates"].sum()
        chart_data = chart_data.sort_values(ascending=False).head(10)

        chart_type = st.radio("Chart Type", ["Bar Chart", "Pie Chart"])

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

        # ---- INSIGHTS ----
        st.subheader("Automated Insights")

        st.write(f"Total biometric updates in {state if 'state' in df.columns else 'dataset'}: {chart_data.sum()}")
        st.write(f"Highest update district: {chart_data.idxmax()} with {chart_data.max()} updates")
        st.write(f"Lowest update district in top 10: {chart_data.idxmin()}")

    # ---- Download Analyzed Data ----
    st.subheader("Download Analyzed Dataset")

    st.download_button(
        "Download CSV with Total Updates",
        df.to_csv(index=False),
        file_name="uidai_analyzed_data.csv"
    )
