from ASDM.ASDM.Engine import Structure
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

model = Structure(from_xmile='Elective Recovery Model.stmx')

# Name the app

st.title('Elective Recovery Model')

# Variables
st.subheader('Slide the Slider to Vary The starting proportion of patients waiting over 24mths for treatment')
long_wait = st.slider("Waiting over 24mths for treatment", 1, 1000, 1)

st.subheader('Number of Weeks to Run the Model For')
sim_time = st.slider("Simulation Time", 1, 500, 1)

# Edit Stock
model.add_stock(name='Waiting over 24mths for treatment', equation={'nosubscript': str(long_wait)}, x=0, y=0, non_negative=True)
# model.add_aux(name='Average pre COVID wait for diagnostics', equation={'nosubscript': str(per_urg_less_six)})

# Run Model
model.clear_last_run()
model.simulate(simulation_time=sim_time, dt=0.25)

# Create the Model

df_outcome = model.export_simulation_result()

df_demand = df_outcome[['Routine treatment', 'Urgent treatment']]
df_backlog = df_outcome[['Total waiting for diagnostics or treatment','Waiting 6 to 12mths for treatment','Waiting 12 to 24mths for treatment','Waiting over 24mths for treatment']]

# Then plot

st.subheader('Estimated Backlog in Weeks')
st.line_chart(df_backlog)

st.subheader('Demand for Urgent and Routine Treatment')
st.line_chart(df_demand)