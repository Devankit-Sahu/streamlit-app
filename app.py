import pandas as pd
import streamlit as st
import plotly.express as px
# Load your dataset
df = pd.read_csv("state-wise-data.csv")
# set title
st.title('State-wise Enrollment Analysis In Regional Centers')
# selection of university state
selected_university_state = st.sidebar.selectbox("Select University State", df["State of University"].unique())
# selection of university for selected state
selected_university = st.sidebar.selectbox("Select University", df[df["State of University"] == selected_university_state]["Name of University"].unique())
# Sidebar for state selection for selected university
selected_state = st.sidebar.selectbox("Select State of Regional Center", df[df['Name of University'] == selected_university]['State of Regional Center'].unique())
# Filter data based on the selected university and state
filtered_data_state = df[(df['Name of University'] == selected_university) & (df['State of Regional Center'] == selected_state)]
# Get unique districts in the selected state
district_options = filtered_data_state['District of Regional Center'].unique()
# selection of district
selected_district = st.sidebar.selectbox("Select District of Regional Center", district_options)
# Filter data based on the selected university, state, and district
filtered_data = df[(df['Name of University'] == selected_university) & (df['State of Regional Center'] == selected_state) & (df['District of Regional Center'] == selected_district)]

fig_all_universities_pie = px.pie(
    df[df['State of University'] == selected_university_state],
    names='Name of University',
    values='Total Enrolment',
    width=800,
    height=700,
    title=f'Total Enrollment Distribution for All Universities in {selected_university_state}'
)
fig_all_universities_pie.update_layout(margin=dict(l=20, r=20, t=40, b=20))
st.plotly_chart(fig_all_universities_pie)

# Scatter Plot - Compare Education Levels between Two States
selected_states_scatter = st.multiselect("Select States for Comparison", df['State of University'].unique(), default = df["State of University"].unique()[0])
filtered_data_scatter = df[df['State of University'].isin(selected_states_scatter)]

fig_scatter = px.scatter(
    filtered_data_scatter,
    x='Level',
    y='Total Enrolment',
    color='State of University',
    labels={'Total Enrolment': 'Total Enrollment'},
    title='Enrollment Comparison by Education Level between Selected States'
)
st.plotly_chart(fig_scatter)

# Bar Chart - Level-wise Enrollment in Regional States
fig_state_enrollment = px.bar(
    filtered_data,
    x='State of Regional Center',
    y='Total Enrolment',
    color='Level',
    labels={'Total Enrolment': 'Total Enrollment'},
    title=f'Total Enrollment in Regional State ({selected_state}) for {selected_university}'
)
st.plotly_chart(fig_state_enrollment)
# Bar Chart - Level-wise Enrollment in Regional Districts
fig_district_enrollment = px.bar(
    filtered_data,
    x='District of Regional Center',
    y='Total Enrolment',
    color='Level',
    labels={'Total Enrolment': 'Total Enrollment',"Level":"Level of Education"},
    title=f'Total Enrollment in Regional district ({selected_district}) for {selected_university}'
)
st.plotly_chart(fig_district_enrollment)

# Bar Chart - Level-wise Enrollment by Gender in Regional Districts
fig_district_enrollment = px.bar(
    filtered_data,
    x='Level',
    y=['Total Enrolment Male', 'Total Enrolment Female'],
    color_discrete_map={'Total Enrolment Male': 'blue', 'Total Enrolment Female': 'pink'},
    labels={'value': 'Total Enrollment'},
    title=f'Level-wise Enrollment by Gender in {selected_district} for {selected_university}'
)
st.plotly_chart(fig_district_enrollment)

# Bar Chart - Top Universities by Total Enrollment
top_universities = df.groupby('Name of University')['Total Enrolment'].sum().nlargest(10).reset_index()
fig_top_universities = px.bar(top_universities, x='Name of University', y='Total Enrolment',
                              labels={'Total Enrolment': 'Total Enrollment'},
                              title='Top 10 Universities by Total Enrollment')
st.plotly_chart(fig_top_universities)

# print(df["State of University"].unique())
