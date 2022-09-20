from ASDM.ASDM.Engine import Structure
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
pd.options.display.max_columns = 100

model = Structure(from_xmile='Elective Recovery Model.stmx')

# Name the app

st.title('Elective Recovery Model')

model.clear_last_run()

# Variables
st.subheader('Slide the Slider to Vary The Proportion of Patients Awaiting Routine Treatment')
routine_adjustment = st.slider("Routine treatment", 1, 100, 1)
st.subheader('Slide the Slider to Vary The Proportion of Patients Awaiting Urgent Treatment')
urgent_adjustment = st.slider("Urgent treatment", 1, 100, 1)

# Edit Stock
model.add_stock(name='Routine treatment', equation={'nosubscript': str(routine_adjustment)}, x=0, y=0, non_negative=True)
model.add_stock(name='Urgent treatment', equation={'nosubscript': str(urgent_adjustment)}, x=0, y=0, non_negative=True)

# Run Model
model.simulate()

# Create the Model

df_outcome = model.export_simulation_result()

df_backlog = df_outcome[['Total waiting for diagnostics or treatment','Waiting 6mths for treatment','Waiting 6 to 12mths for treatment','Waiting 12 to 24mths for treatment','Waiting over 24mths for treatment']]

# Then plot

st.subheader('Time Series Of Backlog')
st.line_chart(df_backlog)