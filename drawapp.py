import streamlit as st
import pandas as pd
import os
import random
import time
from streamlit_card import card as card


def submitted():
    st.session_state.submitted = True


# Set page configuration
st.set_page_config(
    page_title="Al Masa Mall: Lucky Draw App",
    page_icon=":tada:",
    layout="wide"
)

# Sidebar Initialization
with st.sidebar:
    st.image("https://aiwamediagroup.com/wp-content/uploads/2024/05/AiwaMediaGroup-980x393.webp")
    st.header(" **Al Masa Mall: Lucky Draw:tada:**", divider='rainbow')
    with st.expander("2026 Al Masa Draw Guidelines", expanded=True):
        st.write("""
                *   Required Details: Name, Instagram ID, Invoice & Mobile Number.
                *   Draw Prizes:
                    * Winner 1: Apple iPhone 17 Pro
                    * Winner 2: Apple iPhone 17
                *   Draw Winners: 2
                *   Extra Shake Enabled: Yes
                *   Social Media Requirement: Yes
                """)
    with st.expander("Al Masa Mall - Previous Draws:"):
        st.write("""
                *   Grand New Year Draw : 2024
                *   Eid ul Fitr Draw    : 2023
                *   National Day Draw   : 2022
                *   New Year Draw       : 2022
                """)

# Step 1: Data Upload
with st.container():
    st.subheader("Step 1 : Upload Data For Lucky Draw:", divider='rainbow')
    uploaded_file = st.file_uploader("Upload CSV Dataset", type="csv")

    csv_files = [f for f in os.listdir("dataset") if f.endswith(".csv")]

    selected_csv = st.selectbox("Select a CSV File", csv_files if csv_files else ["No CSV files found"])

    num_winners = 1  # Hardcoded number of winners

    if not uploaded_file and selected_csv == "No CSV files found":
        st.warning("Please upload or select a CSV dataset first.")
        st.stop()

    process_button = st.button("Process CSV")
    if process_button:
        submitted()
    if uploaded_file is not None and process_button:
        with open(os.path.join("dataset", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("CSV file uploaded successfully!")
        selected_csv = uploaded_file.name

# Step 2: Data Analysis
if 'submitted' in st.session_state and st.session_state.submitted:
    if selected_csv and selected_csv != "No CSV files found":
        with st.spinner("Loading Data..."):
            draw_data = pd.read_csv(os.path.join("dataset", selected_csv))
            draw_data.columns = draw_data.columns.str.strip()

        totalParticipants = draw_data.shape[0]

        if "slider_val" not in st.session_state:
            st.session_state.slider_val = 0
        if "checkbox_val" not in st.session_state:
            st.session_state.checkbox_val = False
        st.session_state.current_step = 1

        with st.container():
            st.subheader("Step 2 : Data Analytics:", divider='rainbow')
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.dataframe(draw_data.head(279))
            with col2:
                col2.metric("Total Participants", totalParticipants)
                col2.metric("Prize 1", "Apple iPhone 17 Pro")
                # col2.metric("Prize 2", "Samsung S23")
                col2.metric("Social Media Verified", "Verified")

            with col3:
                with st.form("customset"):
                    st.write("Setup For Draw:")
                    slider_val = st.slider("Variance", key="slider")
                    checkbox_val = st.checkbox("Extra Shake", key="checkbox")
                    st.checkbox("Use container width", value=True, key="use_container_width")
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        st.session_state.slider_val = slider_val
                        st.session_state.checkbox_val = checkbox_val
                        st.session_state.current_step = 2

            with st.container():
                if st.session_state.current_step == 2:
                    with st.spinner("Drawing Winners..."):
                        st.toast('Verifying Participants')
                        time.sleep(2)
                        st.toast('Scrambling the data.')
                        time.sleep(2)
                        st.toast('Finding Good People.')
                        time.sleep(2)
                        st.toast('Winner Data is Ready', icon='🎉')

                        # if st.session_state.checkbox_val:
                        #     winner_s24_ultra = draw_data.iloc[[9]]  # 10th participant (index 9)
                        #     remaining_data = draw_data.drop(index=9)
                        #     winner_s23 = remaining_data.sample(n=1)
                        #     winners = pd.concat([winner_s24_ultra, winner_s23])
                        # else:
                        #     winners = draw_data.sample(n=num_winners)
                        # New Code Block (Paste this)
                        if st.session_state.checkbox_val:
                            # RIGGED: Only select the 10th participant (Index 9)
                            winners = draw_data.iloc[[9]]
                        else:
                            # FAIR: Select 1 random winner
                            winners = draw_data.sample(n=num_winners)
                    
                    st.subheader("Step 3 : Congratulations to the Winners:", divider='rainbow')
                    st.balloons()
                    time.sleep(1)
                    st.balloons()

                    prizes = ["Apple iPhone 17 Pro", "Apple iPhone 17"]
                    cols = st.columns(num_winners)

                    for i, (winner_data, prize) in enumerate(zip(winners.itertuples(index=False), prizes)):
                        with cols[i]:
                            card(
                                f"Winner {i + 1} - {prize}",
                                f"Congrats {winner_data.Full_Name}, Mobile: {winner_data.Mobile_No}, Invoice: {winner_data.Invoice_ID}",
                                image="https://img.freepik.com/free-vector/blue-neon-frame-dark-background_53876-113902.jpg",
                                styles={"card": {"width": "100%", "height": "300px"}}
                            )

                    st.dataframe(winners, use_container_width=st.session_state.use_container_width)
                    time.sleep(10)
                    st.success('Al Masa 2026 Winter Draw is Now Over!', icon="✅")
                    st.snow()



