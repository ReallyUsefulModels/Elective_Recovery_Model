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
st.subheader('Slide the Slider to Vary The Percent increase in diagnostic capacity post COVID')
diagnostic_capacity_increase = st.slider("Percent increase in diagnostic capacity post COVID", 1, 100, 1)

# Edit Stock
# model.add_stock(name='Percent increase in diagnostic capacity post COVID', equation={'nosubscript': str(diagnostic_capacity_increase)}, x=0, y=0, non_negative=True)
model.add_aux(name='Percent increase in diagnostic capacity post COVID', equation={'nosubscript': str(diagnostic_capacity_increase)})

# Run Model
model.simulate()

# Create the Model

df_outcome = model.export_simulation_result()

df_backlog = df_outcome[['Total waiting for diagnostics or treatment','Waiting 6mths for treatment','Waiting 6 to 12mths for treatment','Waiting 12 to 24mths for treatment','Waiting over 24mths for treatment']]

# Then plot

st.subheader('Number Waiting By Month')
st.line_chart(df_backlog)