from ASDM.ASDM.Engine import Structure
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
pd.options.display.max_columns = 100

model = Structure(from_xmile='Elective Recovery Model.stmx')

model.clear_last_run()
model.simulate()

# Name the app

st.title('Elective Recovery Model')

# Create the Model

df_outcome = model.export_simulation_result()
print(df_outcome)

df_backlog = df_outcome[['Waiting 12 to 24mths for treatment','Total waiting for diagnostics or treatment','Routine treatment','Urgent treatment']]

# Then plot

st.subheader('Time Series Of Backlog')
st.line_chart(df_backlog)