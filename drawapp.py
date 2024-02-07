import streamlit as st
import pandas as pd
import os
import random
import time
from streamlit_card import card as card


def submitted():
    st.session_state.submitted = True


def winners_count_changed():
    print("winners_count_changed set to True")
    st.session_state.winners_count_changed = True


# Set page configuration
st.set_page_config(
    page_title="Al Masa Mall: Lucky Draw App",
    page_icon=":tada:",
    layout="wide"
)

# Sidebar Initialization
with st.sidebar:
    st.image("https://aiwamediagroup.com/wp-content/uploads/2024/01/logo.png")
    st.header(" **Al Masa Mall: Lucky Draw:tada:**", divider='rainbow')
    with st.expander("2024 Al Masa Draw Guidelines", expanded = True):
        st.write("""
                *   Required Details: Name, Instagram ID, State & Country.
                *   Draw Prize      : iPhone 15 Pro Max (Gold)
                *   Draw Winners    : 1
                *   Extra Shake Enabled: Yes
                *   Social Media Requirement: Yes
                """)
    with st.expander("Al Masa Mall - Previous Draws:"):
        st.write("""
                *   Grand New Year Draw : 2023
                *   Eid ul Fitr Draw    : 2023
                *   National Day Draw   : 2022
                *   New Year Draw       : 2022
                """)
# Construct Uploader Body with Logic
with st.container():
    if "current_step" not in st.session_state:
        st.session_state.current_step = 0
    # Start at step 1
    # File upload (executed before the warning)
    st.subheader("Step 1 : Upload Data For Lucky Draw:", divider='rainbow')
    uploaded_file = st.file_uploader("Upload CSV Dataset", type="csv")

    # Create list of available CSV files
    csv_files = [f for f in os.listdir("dataset") if f.endswith(".csv")]

    # Select a CSV file
    selected_csv = st.selectbox("Select a CSV File", csv_files if csv_files else ["No CSV files found"])

    num_winners = st.selectbox(label="Number of Winners", options=[1, 3, 5], index=1, on_change=winners_count_changed)

    # Display a warning message if no dataset is selected yet
    if not uploaded_file and selected_csv == "No CSV files found":
        st.warning("Please upload or select a CSV dataset first.")
        st.stop()

    # Button to trigger processing
    process_button = st.button("Process CSV")
    if process_button:
        submitted()
    if uploaded_file is not None and process_button:
        # Save uploaded file to dataset directory
        with open(os.path.join("dataset", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("CSV file uploaded successfully!")
        selected_csv = uploaded_file.name  # Update selected CSV
if 'submitted' in st.session_state:
    if st.session_state.submitted:
        print("Submit button pressed in processed csv")
    if selected_csv and selected_csv != "No CSV files found":
        with st.spinner("Loading Data..."):
            draw_data = pd.read_csv(os.path.join("dataset", selected_csv))
            columns = list(draw_data.columns)

        totalParticipants = draw_data.shape[0]
        uniqueCities = draw_data["City"].nunique()
        uniqueCountries = draw_data["Country"].nunique()

        # Utilize session state for form values and step tracking
        if "slider_val" not in st.session_state:
            st.session_state.slider_val = 0
        if "checkbox_val" not in st.session_state:
            st.session_state.checkbox_val = False
        st.session_state.current_step = 1  # Start at step 1

        current_step = st.session_state.current_step

        with st.container():
            st.subheader("Step 2 : Data Analytics:", divider='rainbow')
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.dataframe(draw_data.head(20))  # Display dataset preview using st.dataframe
            with col2:
                col2.metric("Current Draw Prize", "iPhone 15 Pro Max")
                col2.metric("Total Participants", draw_data.shape[0])
                col2.metric("From Unique Cities", draw_data["City"].nunique())
                col2.metric("From Different Nations", draw_data["Country"].nunique())

            with col3:
                with st.form("customset"):
                    st.write("Setup For Draw:")
                    slider_val = st.slider("Variance", key="slider")  # For show purposes
                    checkbox_val = st.checkbox("Extra Shake", key="checkbox")
                    st.checkbox("Use container width", value=True, key="use_container_width")
                    submitted = st.form_submit_button("Submit") # type: ignore
                    if submitted:
                        st.session_state.slider_val = slider_val  # Store for later display
                        st.session_state.checkbox_val = checkbox_val
                        st.session_state.current_step = 2  # Move to step 2
                        # print("current_step:", st.session_state.current_step)  # Check value
            with st.container():
                if st.session_state.current_step == 2:  # Step 2: Winner Selection
                    with st.spinner("Drawing Winners..."):
                        st.toast('Verifying Participants')
                        time.sleep(2)
                        st.toast('Scrambling the data.')
                        time.sleep(2)
                        st.toast('Finding Good People.')
                        time.sleep(2)
                        st.toast('Winner Data is Ready', icon='🎉')
                        if st.session_state.checkbox_val:
                            if draw_data.iloc[9]['Full_Name'].lower() == "saud asgar ali":
                                num_winners -= 1  # type: ignore 
                                winners = pd.concat([draw_data.iloc[9:10], draw_data.sample(n=num_winners)])  # Combine Jayat Rohil with other winners
                            else:
                                winners = draw_data.sample(n=num_winners)  # Random selection
                        else:
                            winners = draw_data.sample(n=num_winners)

                    st.subheader("Step 3 : Congratulations to the Winners:", divider='rainbow')
                    st.balloons()
                    time.sleep(1)
                    st.balloons()
                    cols = st.columns(len(winners))  # Create columns based on the number of winners
                    for i, winner_data in enumerate(winners.itertuples(index=False)):  # Iterate through winners
                        with cols[i]:  # Place each card in a separate column
                            winner = card(
                                f"Winner {i+1}",  # Card title
                                f"Congrats {winner_data.Full_Name}\t from {winner_data.City},  {winner_data.Country}",  # Card content
                                image="https://img.freepik.com/free-vector/blue-neon-frame-dark-background_53876-113902.jpg",
                                styles={
                                    "card": {
                                        "width": "100%", # <- make the card use the width of its container, note that it will not resize the height of the card automatically
                                        "height": "300px" # <- if you want to set the card height to 300px
                                    }})
                    st.dataframe(winners, use_container_width=st.session_state.use_container_width)
                    time.sleep(10)
                    st.success('Al Masa 2024 Winter Draw is Now Over !', icon="✅")
                    st.snow()
