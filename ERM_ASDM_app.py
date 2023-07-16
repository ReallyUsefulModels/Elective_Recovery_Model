from ASDM.ASDM import Structure
from ASDM.Utilities import plot_time_series
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import time

class PatientFlow(Structure):
    def __init__(self):
        super(PatientFlow, self).__init__()
        self.add_stock("Waiting_list", 100, in_flows=['GP_referrals'], out_flows=['Hospital_admission_rate'])
        self.add_stock("In_hospital", 30, in_flows=['Hospital_admission_rate'], out_flows=['Treatment_completion_rate'])
        self.add_stock("In_community_care", 100, in_flows=['Treatment_completion_rate'], out_flows=['Community_care_leaving_rate'])
        
        self.add_aux("Hospital_bed_capacity", 30)
        self.add_aux("Hospital_bed_vacancy", "Hospital_bed_capacity-In_hospital")
        self.add_aux("p_completion", 0.1)
        self.add_aux("p_leaving", 0.1)

        self.add_flow("GP_referrals", 3)
        self.add_flow(
            "Hospital_admission_rate", 
            "MIN(Waiting_list, MAX(Treatment_completion_rate, Hospital_bed_vacancy))",  # mimicing the non-negative stock behaviour
            )
        self.add_flow(
            "Treatment_completion_rate", 
            "RBINOM(In_hospital, p_completion)", 
            )
        self.add_flow(
            "Community_care_leaving_rate", 
            "RBINOM(In_community_care, p_leaving)", 
            )

        # mapping SD functions to Python functions
        self.custom_functions['MAX'] = max
        self.custom_functions['MIN'] = min


# Streamlit App
st.title('Elective Recovery Model')
st.subheader('Slide the Sliders to the left to Vary The starting proportion of patients waiting over 24mths for treatment and the time to simulate over in weeks')

# Set up your sliders
sim_time = st.sidebar.slider('Number of Weeks to Run the model for', 1, 500, 250)
long_wait = st.sidebar.slider('Waiting over 24mths for treatment at model start', 1, 1000, 150)
shorter_wait = st.sidebar.slider('Waiting 6 to 12mths for treatment at model start', 1, 1000, 400)

# Model Object Created
model = PatientFlow()
model.clear_last_run()
model.simulate(time=20, dt=1)

# Extract the simulation results
results = model.export_simulation_result()
df_outcome = pd.DataFrame(results)

df_demand = df_outcome[['In_hospital', 'In_community_care']]
df_backlog = df_outcome[['Waiting_list']]

# Plot the results
st.subheader('Estimated Backlog in Weeks')
st.line_chart(df_backlog)

if st.checkbox('Show Backlog Dataframe'):
    st.write(df_backlog)

'Calculating Demand...' 

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f'Re-Running the Engine {i+1}')
    bar.progress(i + 1)
    time.sleep(0.1)

'...done!'

st.subheader('Demand for Urgent and Routine Treatment')
st.line_chart(df_demand)

if st.checkbox('Show Treatment Demand DataFrame'):
    st.write(df_demand)