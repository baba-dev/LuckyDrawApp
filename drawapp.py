import streamlit as st
import pandas as pd
import os
import time
from streamlit_card import card

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Al Masa Mall: Multi-Draw System",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR THE LAYOUT ---
st.markdown("""
    <style>
    /* Hide Streamlit default menu/footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Center titles */
    h1, h2, h3 {
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* START BUTTON STYLE */
    .stButton button {
        font-size: 24px !important;
        font-weight: bold !important;
        padding: 15px 30px !important;
        width: 100%;
    }

    /* CUSTOM BOXES FOR SIDE DRAWS (Draw 1 & 2) */
    .side-draw-box {
        border: 2px solid #4CAF50; /* Green Border */
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    }
    .side-draw-title {
        color: #aaaaaa;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    .side-draw-name {
        color: #ffffff;
        font-size: 22px;
        font-weight: bold;
    }
    
    /* MAIN WINNER TITLE */
    .final-winner-title {
        font-size: 30px;
        font-weight: 800;
        color: #FFD700; /* Gold */
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'winners_list' not in st.session_state:
    st.session_state.winners_list = None

def submitted():
    st.session_state.submitted = True

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://aiwamediagroup.com/wp-content/uploads/2024/05/AiwaMediaGroup-980x393.webp", use_column_width=True)
    st.markdown("---")
    st.title("💎 Al Masa Mall")
    
    with st.expander("📝 Draw Guidelines", expanded=True):
        st.info("""
        **System Logic:**
        * Each shuffle pulls **3 Unique Winners**.
        * **Winner 1:** Runner Up (Left Top)
        * **Winner 2:** Runner Up (Left Bottom)
        * **Winner 3:** Grand Prize (Main Screen)
        """)
    st.caption("© 2026 Al Masa Event Management")

# --- MAIN APP ---
st.title("✨ 2026 WINTER GRAND DRAW ✨")
st.write("---") 

# STEP 1: DATA UPLOAD
if not st.session_state.submitted:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("Step 1: Upload Participant Data")
        uploaded_file = st.file_uploader("Upload CSV", type="csv")
        
        if not os.path.exists("dataset"):
            os.makedirs("dataset")
            
        csv_files = [f for f in os.listdir("dataset") if f.endswith(".csv")]
        selected_csv = st.selectbox("Or Select Existing File", csv_files if csv_files else ["No CSV files found"])

        if st.button("🚀 Load Data"):
            if uploaded_file:
                with open(os.path.join("dataset", uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.session_state.selected_csv_path = os.path.join("dataset", uploaded_file.name)
                submitted()
                st.rerun()
            elif selected_csv != "No CSV files found":
                st.session_state.selected_csv_path = os.path.join("dataset", selected_csv)
                submitted()
                st.rerun()

# STEP 2: DRAW DASHBOARD
else:
    # Load Data
    draw_data = pd.read_csv(st.session_state.selected_csv_path)
    draw_data.columns = draw_data.columns.str.strip()
    total_participants = len(draw_data)

    # Metrics Bar
    m1, m2, m3 = st.columns(3)
    m1.metric("Participants", f"{total_participants:,}")
    m2.metric("Grand Prize", "iPhone 17 Pro")
    m3.metric("Status", "READY", delta="Online")
    st.markdown("---")

    # --- BUTTON SECTION ---
    # Only show button if we aren't showing results yet
    if st.session_state.current_step == 0:
        b_col1, b_col2, b_col3 = st.columns([1, 2, 1])
        with b_col2:
            if st.button("🎲 SHUFFLE & DRAW (3 WINNERS) 🎲", type="primary"):
                st.session_state.current_step = 1
                st.rerun()

    # --- ANIMATION & PROCESSING ---
    if st.session_state.current_step == 1:
        with st.container():
            st.write("## 🔄 Extracting 3 Random Winners...")
            progress = st.progress(0)
            
            # Dramatic delay loop
            for i in range(100):
                time.sleep(0.02)
                progress.progress(i + 1)
            
            # --- SELECTION LOGIC (RANDOM) ---
            # We need 3 unique people
            num_to_select = min(3, len(draw_data))
            
            # This selects 3 completely random rows
            selected_winners = draw_data.sample(n=num_to_select)
            
            # Assign ranks based on the order they were picked
            # Row 0 -> Draw 1 (Left Top)
            # Row 1 -> Draw 2 (Left Bottom)
            # Row 2 -> Grand Winner (Right Main)
            
            # Add a 'Rank' column for the Audit view
            ranks = []
            if num_to_select >= 1: ranks.append("Runner Up (Draw 1)")
            if num_to_select >= 2: ranks.append("Runner Up (Draw 2)")
            if num_to_select >= 3: ranks.append("GRAND WINNER")
            
            selected_winners['Draw_Rank'] = ranks
            
            # Save to session state so it persists
            st.session_state.winners_list = selected_winners
            st.session_state.current_step = 2
            st.rerun()

    # --- RESULTS DISPLAY (LAYOUT MATCHING MS PAINT) ---
    if st.session_state.current_step == 2:
        st.balloons()
        
        winners = st.session_state.winners_list
        
        # Safe access to winners (handling case if file had < 3 people)
        w1 = winners.iloc[0] if len(winners) > 0 else None
        w2 = winners.iloc[1] if len(winners) > 1 else None
        w3 = winners.iloc[2] if len(winners) > 2 else None

        # --- THE LAYOUT GRID ---
        # Left Column (1 part) | Right Column (2.5 parts)
        col_left, col_right = st.columns([1, 2.5])
        
        # --- LEFT SIDE (Draw 1 & 2) ---
        with col_left:
            st.markdown("<br>", unsafe_allow_html=True) # Spacer
            
            # Draw 1 Box
            if w1 is not None:
                st.markdown(f"""
                <div class="side-draw-box">
                    <div class="side-draw-title">Draw 1 Result</div>
                    <div class="side-draw-name">{w1['Full_Name']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True) # Spacer between boxes
            
            # Draw 2 Box
            if w2 is not None:
                st.markdown(f"""
                <div class="side-draw-box">
                    <div class="side-draw-title">Draw 2 Result</div>
                    <div class="side-draw-name">{w2['Full_Name']}</div>
                </div>
                """, unsafe_allow_html=True)

        # --- RIGHT SIDE (Main Winner) ---
        with col_right:
            if w3 is not None:
                st.markdown('<div class="final-winner-title">Final Draw Winner</div>', unsafe_allow_html=True)
                
                # The Big Card
                card(
                    title="iPhone 17 Pro",
                    text=f"WINNER: {w3['Full_Name']}\n\nInvoice: {w3['Invoice_ID']}\nMobile: {w3['Mobile_No']}",
                    image="https://img.freepik.com/free-vector/blue-neon-frame-dark-background_53876-113902.jpg",
                    styles={
                        "card": {
                            "width": "100%", 
                            "height": "500px",
                            "border-radius": "15px",
                            "box-shadow": "0 0 30px rgba(255, 215, 0, 0.3)"
                        },
                        "text": {
                            "font-family": "sans-serif",
                            "font-size": "24px"
                        }
                    }
                )
                st.markdown("<h2 style='text-align: center; color: #4CAF50;'>🎉 WE HAVE A WINNER! 🎉</h2>", unsafe_allow_html=True)

        # --- ELABORATED AUDIT DATA ---
        st.write("---")
        with st.expander("📂 View Elaborated Audit Data", expanded=True):
            st.markdown("### 📋 Official Results Ledger")
            
            # Clean up the dataframe for display
            display_df = winners.copy()
            
            # Select relevant columns only (adjust these names based on your actual CSV columns)
            # Assuming standard columns like 'Full_Name', 'Invoice_ID', 'Mobile_No' exist
            cols_to_show = ['Draw_Rank', 'Full_Name', 'Invoice_ID', 'Mobile_No']
            
            # Filter to exist columns only
            valid_cols = [c for c in cols_to_show if c in display_df.columns]
            
            st.dataframe(
                display_df[valid_cols],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Draw_Rank": st.column_config.TextColumn("Prize Category", width="medium"),
                    "Full_Name": st.column_config.TextColumn("Winner Name", width="large"),
                    "Invoice_ID": "Invoice Ref",
                    "Mobile_No": "Contact"
                }
            )
            
        # Reset Button
        if st.button("Start New Draw"):
            st.session_state.current_step = 0
            st.session_state.winners_list = None
            st.rerun()
