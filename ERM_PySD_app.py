# Import Dependencies

import pysd
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
pd.options.display.max_columns = 100

model = pysd.read_xmile('Elective Recovery Model.stmx')

# Name the app

st.title('Elective Recovery Model')

values = model.run()

# Add variables relevant to the model

st.subheader('Enter the Startpoint in terms of the Routine Backlog')
rout_treat_start = st.number_input(label='Routine treatment', min_value=0, max_value=100, value=100)
st.subheader('Enter the Startpoint in terms of the Urgent Backlog')
urg_treat_start = st.number_input(label='Urgent treatment', min_value=0, max_value=100, value=100)
st.subheader('Slide the Slider to Vary The Proportion of Patients Undergoing Diagnostic Tests')
diagnostic_adjustment = st.slider("Undergoing diagnostic tests", 1, 100, 1)

# Create the Model

values = model.run(initial_condition=(0,{'Undergoing diagnostic tests': diagnostic_adjustment}), params={'Routine treatment': rout_treat_start})
df_backlog = values[['Waiting 12 to 24mths for treatment','Total waiting for diagnostics or treatment','Routine treatment','Urgent treatment']]

# Then plot

st.subheader('Backlog over Time')
st.line_chart(df_backlog)