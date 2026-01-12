import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="UIDAI Analytics", layout="wide")

st.title("UIDAI Biometric Update Analytics Dashboard")
st.write("Upload UIDAI biometric dataset to analyze trends.")

file = st.file_uploader("Upload CSV File", type=["csv"])

if file:
    df = pd.read_csv(file)

    st.subheader("Dataset Preview (First 10 Rows)")
    st.dataframe(df.head(10))

    st.subheader("Detected Columns")
    st.write(list(df.columns))

    # -------- AUTO COLUMN DETECTION ----------
    age5_col = None
    age17_col = None

    for col in df.columns:
        if "5" in col and "age" in col.lower():
            age5_col = col
        if "17" in col and "age" in col.lower():
            age17_col = col

    if age5_col is None or age17_col is None:
        st.error("Age group columns not detected automatically. Please rename columns properly.")
    else:
        df["total_updates"] = df[age5_col] + df[age17_col]

        # -------- FILTERING ----------
        if "state" in df.columns:
            state = st.selectbox("Select State", df["state"].unique())
            filtered = df[df["state"] == state]
        else:
            filtered = df

        st.subheader("Filtered Dataset")
        st.dataframe(filtered)

        # -------- CHART ----------
        if "district" in df.columns:
            st.subheader("District-wise Biometric Updates")

            chart_data = filtered.groupby("district")["total_updates"].sum()

            fig, ax = plt.subplots()
            chart_data.plot(kind="bar", ax=ax)
            ax.set_title("District-wise Biometric Updates")
            ax.set_xlabel("District")
            ax.set_ylabel("Total Updates")
            plt.xticks(rotation=45)
            plt.tight_layout()

            st.pyplot(fig)

            # -------- INSIGHTS ----------
            st.subheader("Insights")
            st.write(f"Total biometric updates: {chart_data.sum()}")
            st.write(f"Highest update district: {chart_data.idxmax()}")

        else:
            st.warning("District column not found in dataset.")
