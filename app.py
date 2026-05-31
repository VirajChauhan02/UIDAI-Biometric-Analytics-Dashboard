import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page Config
st.set_page_config(page_title="UIDAI Societal Trend Analytics", layout="wide")

st.title("UIDAI Aadhaar Update Trend Analytics System")
st.write(
    "Upload Aadhaar enrolment / biometric update dataset. "
    "System will automatically analyze societal trends and insights."
)

# File Upload
file = st.file_uploader("Upload Aadhaar Dataset (CSV / Excel)", type=["csv", "xlsx"])


# Utility function to find column
def find_column(keywords, columns):
    for col in columns:
        for key in keywords:
            if key in col.lower():
                return col
    return None


if file:

    # Read file
    if file.name.endswith(".xlsx"):
        df = pd.read_excel(file)
    else:
        df = pd.read_csv(file)

    st.success("Dataset uploaded successfully")

    # Preview
    st.subheader("Dataset Preview")
    st.dataframe(df.head(10))

    # Lowercase column names for matching
    cols_lower = [c.lower() for c in df.columns]

    # Auto detect columns
    state_col = find_column(["state"], cols_lower)
    district_col = find_column(["district"], cols_lower)
    age5_col = find_column(["5"], cols_lower)
    age17_col = find_column(["17"], cols_lower)

    # Map back to original column names
    if state_col:
        state_col = df.columns[cols_lower.index(state_col)]
    if district_col:
        district_col = df.columns[cols_lower.index(district_col)]
    if age5_col:
        age5_col = df.columns[cols_lower.index(age5_col)]
    if age17_col:
        age17_col = df.columns[cols_lower.index(age17_col)]

    # Validation
    if not age5_col or not age17_col:
        st.error(
            "Dataset structure not recognized automatically. "
            "Please upload UIDAI formatted dataset."
        )
        st.stop()

    # Row-wise total calculation
    df["total_updates"] = df[age5_col] + df[age17_col]

    # KPI Section
    st.subheader("Key Societal Indicators")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Records", len(df))
    c2.metric("Total Biometric Updates", int(df["total_updates"].sum()))
    c3.metric("Average Updates per Region", int(df["total_updates"].mean()))

    # State Filter
    if state_col:
        state = st.selectbox("Select State", df[state_col].unique())
        filtered = df[df[state_col] == state]
    else:
        filtered = df
        state = "All Regions"

    # District Trend Chart
    if district_col:

        chart_data = filtered.groupby(district_col)["total_updates"].sum()
        chart_data = chart_data.sort_values(ascending=False)

        top10 = chart_data.head(10)
        bottom5 = chart_data.tail(5)

        chart_type = st.radio("Select Visualization", ["Bar Chart", "Pie Chart"])

        fig, ax = plt.subplots(figsize=(8, 6))

        if chart_type == "Bar Chart":
            top10.plot(kind="bar", ax=ax)
            plt.xticks(rotation=45, ha="right")
            ax.set_ylabel("Total Updates")
        else:
            top10.plot(kind="pie", autopct="%1.1f%%", ax=ax)
            ax.set_ylabel("")

        ax.set_title("Top Districts Biometric Update Distribution")
        plt.tight_layout()
        st.pyplot(fig)

        # Insights
        st.subheader("Automated Societal Insights")

        st.write(f"Total biometric updates in {state}: {int(top10.sum())}")
        st.write(
            f"Highest update district: {top10.idxmax()} with {int(top10.max())} updates"
        )
        st.write(f"Lowest update district among top 10: {top10.idxmin()}")

        st.write("### Anomaly Detection (Low Activity Districts)")
        st.dataframe(bottom5)

    # Download Section
    st.subheader("Download Decision-Ready Dataset")

    st.download_button(
        "Download Analyzed Dataset",
        df.to_csv(index=False),
        file_name="uidai_trend_analyzed_data.csv"
    )
