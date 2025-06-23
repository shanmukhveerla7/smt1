import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns


def detect_anomalies(data, column):
    model = IsolationForest(contamination=0.05, random_state=42)
    data["anomaly"] = model.fit_predict(data[[column]])
    return data


def anomaly_detection():
    st.title("🚨 Anomaly Detection")

    uploaded_file = st.file_uploader("📂 Upload CSV File", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File Uploaded Successfully")

        st.write("📊 Preview of Data")
        st.dataframe(df.head())

        numeric_columns = df.select_dtypes(include=["float", "int"]).columns.tolist()

        if numeric_columns:
            selected_column = st.selectbox(
                "📈 Select column to detect anomalies", numeric_columns
            )

            if st.button("🔍 Detect Anomalies"):
                result_df = detect_anomalies(df.copy(), selected_column)

                st.write("📍 Anomaly Flags (-1 = Anomaly, 1 = Normal)")
                st.dataframe(result_df[result_df["anomaly"] == -1])

                # Plot
                fig, ax = plt.subplots()
                sns.scatterplot(
                    data=result_df,
                    x=result_df.index,
                    y=selected_column,
                    hue="anomaly",
                    palette={1: "green", -1: "red"},
                    ax=ax,
                )
                ax.set_title(f"Anomaly Detection on {selected_column}")
                st.pyplot(fig)
        else:
            st.warning("⚠️ No numeric columns available in uploaded file.")
