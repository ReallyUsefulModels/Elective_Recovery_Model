import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from ASDM.ASDM import Structure

# Function to load the model
def load_model(model_path):
    try:
        model = Structure(from_xmile=model_path)
    except FileNotFoundError:
        st.error(f"File {model_path} not found.")
        return None
    return model

# Function to run the simulation
def run_simulation(model, weeks):
    # Set the simulation specs in weeks
    model.sim_specs['initial_time'] = 0
    model.sim_specs['current_time'] = 0
    model.sim_specs['dt'] = 1
    model.sim_specs['simulation_time'] = weeks
    model.sim_specs['time_units'] = 'Weeks'

    # Clear the previous run
    model.clear_last_run()

    # Run the simulation
    model.simulate()

    # Get the results
    results = model.export_simulation_result()
    results_df = pd.DataFrame.from_dict(results)

    # Return the specific columns required for plotting
    columns_to_plot = [
        "Waiting_more_than_12mths",
        "Waiting_6_to_12mths_for_treatment",
        "Waiting_12_to_24mths_for_treatment",
        "13wk_wait_for_urgent_treatment",
        "Total_waiting_for_diagnostics_or_treatment"
    ]
    return results_df["Weeks"], results_df[columns_to_plot]

# Streamlit App
st.title('NHS Elective Recovery Model')
st.subheader('Modeling the elective recovery in the NHS')

# Load the model
model = load_model('models/Elective Recovery Model.stmx')

# Check if the model is successfully loaded
if model is not None:
    # Add Streamlit components for user inputs (e.g., sliders, number input)
    weeks_to_simulate = st.slider("Select the number of weeks to simulate:", min_value=1, max_value=104, value=52)

    # Run the simulation and get the results
    x_values, y_values = run_simulation(model, weeks_to_simulate)

    # Create the plot
    fig = go.Figure()
    for column in y_values.columns:
        fig.add_trace(go.Scatter(x=x_values, y=y_values[column], mode='lines', name=column))

    # Update the plot layout
    fig.update_layout(title_text='Elective Recovery in the NHS',
                      xaxis_title='Weeks',
                      yaxis_title='Number of Patients (log scale)',  # Update the y-axis label
                      xaxis_type='linear',  # Set the x-axis scale to linear
                      yaxis_type='log',  # Set the y-axis scale to logarithmic
                      legend=dict(orientation='h', x=0.5, y=-0.15),  # Move legend to the bottom
                      margin=dict(l=50, r=50, t=50, b=50))  # Add margins for better display

    # Display the plot
    st.plotly_chart(fig)