import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go


def kpi_forecast():
    st.title("📈 Forecast KPI from Uploaded File")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)

            if "date" not in df.columns or "usage_kwh" not in df.columns:
                st.error("CSV must have 'date' and 'usage_kwh' columns.")
                return

            df = df.rename(columns={"date": "ds", "usage_kwh": "y"})
            df["ds"] = pd.to_datetime(df["ds"])

            st.subheader("📊 Uploaded Historical Data")
            st.line_chart(df.set_index("ds")["y"])

            # Train Prophet
            with st.spinner("Training forecasting model..."):
                model = Prophet()
                model.fit(df)

                future = model.make_future_dataframe(periods=365 * 5)  # Next 5 years
                forecast = model.predict(future)

            st.subheader("📈 Forecast for Next 5 Years")
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=forecast["ds"], y=forecast["yhat"], name="Forecasted Usage"
                )
            )
            fig.add_trace(go.Scatter(x=df["ds"], y=df["y"], name="Historical Usage"))
            st.plotly_chart(fig, use_container_width=True)

            # Optional: download forecast
            csv = forecast[["ds", "yhat"]].to_csv(index=False)
            st.download_button(
                "📥 Download Forecast CSV",
                csv,
                file_name="forecast.csv",
                mime="text/csv",
            )

        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
