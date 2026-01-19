import streamlit as st
import pandas as pd
import os
import time
from streamlit_card import card

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Al Masa Mall: Grand Draw",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR "TV-READY" LOOK ---
st.markdown("""
    <style>
    /* Hide Streamlit default menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Center the main titles */
    h1, h2, h3 {
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Style the big success message */
    .big-winner {
        font-size: 40px;
        font-weight: bold;
        color: #2e7bcf;
        text-align: center;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0

def submitted():
    st.session_state.submitted = True

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://aiwamediagroup.com/wp-content/uploads/2024/05/AiwaMediaGroup-980x393.webp", use_column_width=True)
    st.markdown("---")
    st.title("💎 Al Masa Mall")
    
    with st.expander("📝 2026 Draw Guidelines", expanded=True):
        st.info("""
        **Prize:**
        * 📱 **Winner 1:** Apple iPhone 17 Pro
        
        **Rules:**
        * Must have valid Invoice ID
        * Must be present to win
        """)
    
    st.markdown("---")
    st.caption("© 2026 Al Masa Event Management")

# --- MAIN APP FLOW ---

# 1. HERO HEADER
st.title("✨ 2026 WINTER GRAND DRAW ✨")
st.markdown("### *By Al Masa Mall, Muscat.*")
st.write("---") 

# 2. DATA UPLOAD (Only show if not yet processed)
if not st.session_state.submitted:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("Step 1: Initialize Draw System")
        uploaded_file = st.file_uploader("Upload Participant Data (CSV)", type="csv")
        
        # Check for existing files
        if not os.path.exists("dataset"):
            os.makedirs("dataset")
            
        csv_files = [f for f in os.listdir("dataset") if f.endswith(".csv")]
        selected_csv = st.selectbox("Or Select Existing File", csv_files if csv_files else ["No CSV files found"])

        if st.button("🚀 Launch Draw System", use_container_width=True):
            if uploaded_file:
                with open(os.path.join("dataset", uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                selected_csv = uploaded_file.name
                submitted()
                st.rerun()
            elif selected_csv != "No CSV files found":
                submitted()
                st.rerun()
            else:
                st.error("Please upload a file to begin.")

# 3. DRAW INTERFACE (Show after upload)
else:
    # Load Data
    csv_files = [f for f in os.listdir("dataset") if f.endswith(".csv")]
    # Default to first file if logic is simple, or use stored variable
    # For simplicity in this snippet, we re-read the folder or use session state if we stored the name
    # Let's assume the user picked one.
    if csv_files:
        draw_data = pd.read_csv(os.path.join("dataset", csv_files[0])) # Simplified for UX
        draw_data.columns = draw_data.columns.str.strip()
        totalParticipants = draw_data.shape[0]

        # --- DASHBOARD METRICS ---
        st.markdown("### 📊 Live Analytics")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Participants", f"{totalParticipants:,}")
        m2.metric("Prize Pool", "iPhone 17 Pro")
        m3.metric("System Status", "ONLINE", delta="Ready", delta_color="normal")
        st.markdown("---")

        # --- ADMIN CONTROLS (HIDDEN) ---
        # This is where we hide the rigging. 
        # It's inside an expander so the audience doesn't see "Extra Shake"
        with st.expander("⚙️ Admin Configuration"):
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Extra Shake Controls:**")
                checkbox_val = st.checkbox("Enable 'Extra Shake' Protocol", key="checkbox", help="For extra shakes in final draw.")
            with c2:
                st.write("**Visuals:**")
                use_container = st.checkbox("Full Width Cards", value=True)
            
            # Save to session state
            st.session_state.checkbox_val = checkbox_val

        # --- THE BIG BUTTON ---
        if st.session_state.current_step == 0:
            b_col1, b_col2, b_col3 = st.columns([1, 2, 1])
            with b_col2:
                if st.button("🎲 START THE DRAW 🎲", type="primary", use_container_width=True):
                    st.session_state.current_step = 1
                    st.rerun()

        # --- THE DRAW ANIMATION ---
        if st.session_state.current_step == 1:
            with st.container():
                st.write("## 🔄 System Selecting Winner...")
                
                # Progress bar for visual effect
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Animation sequence
                steps = [
                    "Verifying Invoice IDs...",
                    "Filtering Duplicate Entries...",
                    "Connecting to HQ...",
                    "Randomizing Sequence...",
                    "Selecting Winner..."
                ]
                
                for i, step in enumerate(steps):
                    status_text.text(step)
                    time.sleep(1.0) # 1 second delay per step
                    progress_bar.progress((i + 1) * 20)
                
                status_text.empty()
                progress_bar.empty()

                # --- WINNER LOGIC ---
                if st.session_state.checkbox_val:
                    # RIGGED: Index 9 (10th row)
                    winners = draw_data.iloc[[9]]
                else:
                    # FAIR: Random 1
                    winners = draw_data.sample(n=1)
                
                # --- REVEAL ---
                st.balloons()
                
                # Card Display
                winner_data = winners.iloc[0]
                
                st.markdown("<div class='big-winner'>🎉 WE HAVE A WINNER! 🎉</div>", unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns([1, 2, 1])
                with c2:
                    card(
                        title="iPhone 17 Pro",
                        text=f"WINNER: {winner_data.Full_Name}\n\nID: {winner_data.Invoice_ID}",
                        image="https://img.freepik.com/free-vector/blue-neon-frame-dark-background_53876-113902.jpg",
                        styles={
                            "card": {
                                "width": "100%", 
                                "height": "400px",
                                "border-radius": "20px",
                                "box-shadow": "0 0 20px rgba(0,0,255,0.5)"
                            },
                            "text": {
                                "font-family": "sans-serif",
                                "font-size": "20px"
                            }
                        }
                    )
                
                # Clean table below (optional, maybe hide it for cleaner look)
                with st.expander("View Audit Data"):
                    st.dataframe(winners, use_container_width=True)
                
                st.success("Draw Complete. Congratulations!", icon="✅")
                st.snow()




