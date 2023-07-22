import pandas as pd
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
def run_simulation(model, weeks, pre_covid_capacity, post_covid_capacity, percent_negative_test_results, average_pre_covid_wait_for_diagnostics):
    # Set the simulation specs in weeks
    model.sim_specs['initial_time'] = 0
    model.sim_specs['current_time'] = 0
    model.sim_specs['dt'] = 1
    model.sim_specs['simulation_time'] = weeks
    model.sim_specs['time_units'] = 'Weeks'

    # Clear the previous run
    model.clear_last_run()

    # Set the 'Pre_COVID_treatment_capacity' aux equation with the user-defined value for the entire simulation period
    model.aux_equations['Pre_COVID_treatment_capacity'] = pre_covid_capacity

    # Set the 'Post_COVID_increase_in_treatment_capacity' aux equation with the user-defined value for the entire simulation period
    model.aux_equations['Post_COVID_increase_in_treatment_capacity'] = post_covid_capacity

    # Set the 'Percent_negative_test_results' aux equation with the user-defined value for the entire simulation period
    model.aux_equations['Percent_negative_test_results'] = percent_negative_test_results 

    # Set the 'Average_pre_COVID_wait_for_diagnostics' aux equation with the user-defined value for the entire simulation period
    model.aux_equations['Average_pre_COVID_wait_for_diagnostics'] = average_pre_covid_wait_for_diagnostics

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
st.subheader('Modeling the elective recovery in the NHS post-COVID')

# Load the model
model = load_model('models/Elective Recovery Model.stmx')

# Check if the model is successfully loaded
if model is not None:
    # Add Streamlit components for user inputs (e.g., sliders, number input) in the sidebar
    with st.sidebar:
        st.header("Variable Sliders")
        weeks_to_simulate = st.slider("Select the number of weeks to simulate:", min_value=1, max_value=52, value=20)
        use_log_scale = st.checkbox("Use Logarithmic Scale", value=True)
        average_pre_covid_wait_for_diagnostics = st.slider("Average_pre_COVID_wait_for_diagnostics:", min_value=2, max_value=100, value=10)
        pre_covid_capacity = st.slider("Pre-COVID Treatment Capacity:", min_value=1, max_value=13, value=2)
        post_covid_capacity = st.slider("Post-COVID Treatment Capacity Increase:", min_value=1, max_value=10, value=3)
        percent_negative_test_results = st.slider("Percent Negative Test Results:", min_value=10, max_value=40, value=20)

    # Run the simulation and get the results
    x_values, y_values = run_simulation(
        model,
        weeks_to_simulate,
        str(pre_covid_capacity),
        str(post_covid_capacity),
        str(percent_negative_test_results),
        str(average_pre_covid_wait_for_diagnostics),
    )

    # Create the plot
    fig = go.Figure()
    for column in y_values.columns:
        fig.add_trace(go.Scatter(x=x_values, y=y_values[column], mode='lines', name=column))

    # Update the plot layout
    fig.update_layout(title_text='Elective Recovery in the NHS',
                      xaxis_title='Weeks',
                      yaxis_title='Number of Patients (log scale)' if use_log_scale else 'Number of Patients',
                      xaxis_type='linear',  # Set the x-axis scale to linear
                      yaxis_type='log' if use_log_scale else 'linear',  # Toggle y-axis scale based on checkbox
                      legend=dict(orientation='h', x=0, y=-0.15),  # Move legend to the bottom
                      margin=dict(l=50, r=50, t=50, b=50))  # Add margins for better display

    # Display explanatory text before the chart
    st.markdown("This model simulates the post-COVID recovery era for elective treatments in the NHS. It is based on a population of 100,000 people and aims to provide insights into the expected changes in patient numbers for different waiting time categories over time. You can customize the 'Pre-COVID Treatment Capacity,' 'Post-COVID Treatment Capacity Increase,' and 'Percent Negative Test Results' using the sliders below before running each simulation.")
    
    # Display the plot
    st.plotly_chart(fig)

    # Display explanatory text after the chart
    st.markdown("The chart shows how the number of patients in various waiting time categories evolves over the selected number of weeks. It provides insights into the recovery of elective services in the NHS and helps identify areas that may require attention for improvement.")
