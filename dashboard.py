import streamlit as st
import pandas as pd
import plotly.express as px

# Loading the dataset
dataset = pd.read_csv("cleaned_dataset.csv")

#Formatting the configuration to wide
st.set_page_config(layout="wide")

#Setting a title on the side bar
st.sidebar.title("Filter your data here")

select_your_year = st.sidebar.selectbox("Select Year", sorted(dataset["YEAR (DISPLAY)"].dropna().unique(), reverse=True))

#Filter the dataset
filtered_dataset = dataset[dataset["YEAR (DISPLAY)"] == select_your_year]

#Setting the title of the dashboard
st.title("Air Pollution Indicators in Sri Lanka")

#Setting three KPIs
col1, col2, col3 = st.columns(3)
col1.metric(f"Total Indicators in {select_your_year}", len(filtered_dataset["GHO (CODE)"].unique()))
col2.metric(f"Average Value in {select_your_year}", f"{filtered_dataset['Numeric'].mean():.2f}")
col3.metric(f"Max Value in {select_your_year}", f"{filtered_dataset['Numeric'].max():.2f}")

#Setting the subheader on top of the bar chart
st.subheader(f"The top 5 Pollution Indicators in {select_your_year}")

# Group by GHO (DISPLAY) and calculate average Numeric for that year
pollution_by_indicator = (
    filtered_dataset.groupby("GHO (DISPLAY)")["Numeric"]
    .mean()
    .sort_values(ascending=False)
    .head(5)  
    .reset_index()
)

# Horizontal bar chart
fig = px.bar(
    pollution_by_indicator,
    x="Numeric",
    y="GHO (DISPLAY)",
    orientation="h",
    color="Numeric",
    color_continuous_scale="Viridis",
    title=f"Top 5 Pollution Indicators for {select_your_year}",
    width=700,  
    height=400
)


st.plotly_chart(fig)

#Putting two columns to make the following bar charts appear side by side
col1, col2 = st.columns(2)

#Creating a bar chart to compare by gender 
with col1:
    st.subheader(f"Pollution by Gender in {select_your_year}")
    sex_df = filtered_dataset[filtered_dataset["DIMENSION (TYPE)"] == "SEX"]
    if not sex_df.empty:
        sex_grouped = sex_df.groupby("DIMENSION (NAME)")["Numeric"].mean().reset_index()
        fig_sex = px.bar(
            sex_grouped,
            x="DIMENSION (NAME)",
            y="Numeric",
            color="Numeric",
            title="Average Pollution Comparison by Gender",
            color_continuous_scale="Oranges",
            width=600,
            height=350
        )
        st.plotly_chart(fig_sex, use_container_width=False)
    else:
        st.warning("Unfortunately, the selected year does not have gender related")

#Creating a bar chart to compare by residence
with col2:
    st.subheader(f"Pollution by Residence Type in {select_your_year}")
    res_df = filtered_dataset[filtered_dataset["DIMENSION (TYPE)"] == "RESIDENCEAREATYPE"]
    res_grouped = res_df.groupby("DIMENSION (NAME)")["Numeric"].mean().reset_index()
    fig_res = px.bar(
        res_grouped,
        x="DIMENSION (NAME)",
        y="Numeric",
        color="Numeric",
        title="Average Pollution Comparison by Residence Type",
        color_continuous_scale="Purples",
        width=600,
        height=350
    )
    st.plotly_chart(fig_res, use_container_width=False)

