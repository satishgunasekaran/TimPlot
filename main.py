import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from date_handler.date_util import convert_all_date_columns 


def get_time_series_plot(data, date_column, value_column, time_interval):
    if time_interval == 'Weekly':
        data_grouped = data.groupby(pd.Grouper(key=date_column, freq='W')).mean()
    elif time_interval == 'Monthly':
        data_grouped = data.groupby(pd.Grouper(key=date_column, freq='M')).mean()
    elif time_interval == 'Yearly':
        data_grouped = data.groupby(pd.Grouper(key=date_column, freq='Y')).mean()
    else:
        data_grouped = data

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_grouped.index, y=data_grouped[value_column], mode='lines+markers', name=value_column))
    fig.update_layout(title=f'Time-Series Analysis ({time_interval})', 
                      xaxis_title=date_column, 
                      yaxis_title=value_column)
    fig.update_layout(showlegend=True)
    return fig

def main():
    st.title("Time-Series Analysis with Plotly")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        
        data = convert_all_date_columns(data)
        
        date_columns = data.select_dtypes(include=['datetime64']).columns
        numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns
        
        if len(date_columns) == 0:
            st.write("No date columns found in the uploaded file. Please upload a file with date columns.")
            return 
        

        st.write("Data Preview:")
        st.dataframe(data.head())

        date_column = st.selectbox("Select the Date Column", date_columns)
        value_column = st.selectbox("Select the Value Column", numerical_columns)

        time_intervals = ['Full Time-Series', 'Weekly', 'Monthly', 'Yearly']
        time_interval = st.radio("Select Time Interval for Analysis:", time_intervals)

        time_series_plot = get_time_series_plot(data, date_column, value_column, time_interval)
        st.plotly_chart(time_series_plot)

if __name__ == "__main__":
    main()
