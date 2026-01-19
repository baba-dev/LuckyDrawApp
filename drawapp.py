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
    initial_sidebar_state="collasped"
)

# --- CUSTOM CSS ---
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

    /* CUSTOM BOXES FOR TEASER DRAWS */
    .side-draw-box {
        border: 2px solid #444; 
        background-color: #1e1e1e;
        padding: 10px; 
        border-radius: 8px;
        text-align: center;
        margin-bottom: 15px; 
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        opacity: 0.9;
        animation: fadeIn 1s;
    }
    
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 0.9; }
    }

    .side-draw-title {
        color: #aaaaaa;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 2px;
    }
    .side-draw-name {
        color: #ffffff;
        font-size: 18px; 
        font-weight: bold;
    }
    
    /* MAIN WINNER TITLE */
    .final-winner-title {
        font-size: 30px;
        font-weight: 800;
        color: #FFD700; /* Gold */
        text-align: center;
        margin-bottom: 20px;
        text-transform: uppercase;
        animation: popIn 1s;
    }
    
    @keyframes popIn {
        0% { transform: scale(0.5); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
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
if 'selected_csv_path' not in st.session_state:
    st.session_state.selected_csv_path = None
if 'animation_complete' not in st.session_state:
    st.session_state.animation_complete = False

def submitted():
    st.session_state.submitted = True

# --- HELPER FUNCTION FOR HTML BOX ---
def get_teaser_html(idx, name):
    return f"""
    <div class="side-draw-box">
        <div class="side-draw-title">Lucky Pick #{idx} (Teaser)</div>
        <div class="side-draw-name">{name}</div>
    </div>
    """

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://aiwamediagroup.com/wp-content/uploads/2024/05/AiwaMediaGroup-980x393.webp", use_column_width=True)
    st.markdown("---")
    st.title("💎 Al Masa Mall")
    
    with st.expander("📝 Draw Guidelines", expanded=True):
        st.info("""
        **Prize Structure:**
        * 🏆 **1 Official Winner:** (Main Screen)
        * ✨ **4 Teaser Draws:** (Left Side - For visual excitement only)
        
        **Prize:**
        * Apple iPhone 17 Pro
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
    m2.metric("Official Winners", "1 Person")
    m3.metric("Status", "READY", delta="Online")
    st.markdown("---")

    # --- BUTTON SECTION ---
    if st.session_state.current_step == 0:
        b_col1, b_col2, b_col3 = st.columns([1, 2, 1])
        with b_col2:
            if st.button("🎲 START GRAND DRAW 🎲", type="primary"):
                # Pre-calculate winners immediately
                num_to_select = min(5, len(draw_data))
                selected_winners = draw_data.sample(n=num_to_select)
                
                # Assign ranks
                ranks = []
                for i in range(num_to_select - 1):
                    ranks.append(f"Teaser #{i+1} (No Prize)")
                if num_to_select > 0:
                    ranks.append("🏆 OFFICIAL WINNER 🏆")
                selected_winners['Status'] = ranks
                
                st.session_state.winners_list = selected_winners
                st.session_state.current_step = 1
                st.session_state.animation_complete = False # Reset animation flag
                st.rerun()

    # --- RESULTS DISPLAY WITH ANIMATION ---
    if st.session_state.current_step == 1:
        
        winners = st.session_state.winners_list
        grand_winner = winners.iloc[-1]
        teasers = winners.iloc[:-1]

        # --- PREPARE LAYOUT GRID ---
        col_left, col_right = st.columns([1, 2.5])
        
        # Create empty placeholders for animation
        with col_left:
            st.markdown("<br>", unsafe_allow_html=True)
            teaser_placeholders = []
            for i in range(4):
                teaser_placeholders.append(st.empty())
                
        with col_right:
            title_placeholder = st.empty()
            card_placeholder = st.empty()
            celebration_placeholder = st.empty()

        # --- ANIMATION SEQUENCE (Only runs if not already done) ---
        if not st.session_state.animation_complete:
            
            # 1. Reveal Teasers One by One
            for idx, (p_holder, teaser_row) in enumerate(zip(teaser_placeholders, teasers.itertuples())):
                time.sleep(1.5) # Suspense delay
                
                # Show Toast
                st.toast(f"Teaser #{idx+1}: {teaser_row.Full_Name}", icon="🎲")
                
                # Render HTML Box
                p_holder.markdown(get_teaser_html(idx+1, teaser_row.Full_Name), unsafe_allow_html=True)
            
            # 2. Reveal Grand Winner
            time.sleep(2)
            st.toast("Selecting Grand Winner...", icon="🔄")
            time.sleep(1.5)
            
            title_placeholder.markdown('<div class="final-winner-title">Final Draw Winner</div>', unsafe_allow_html=True)
            
            st.toast(f"WINNER: {grand_winner['Full_Name']}", icon="🏆")
            st.balloons()
            
            # Render Card
            with card_placeholder:
                card(
                    title=grand_winner['Full_Name'],
                    text=f"Prize: iPhone 17 Pro\n\nInvoice: {grand_winner['Invoice_ID']}\nMobile: {grand_winner['Mobile_No']}",
                    image="https://img.freepik.com/free-vector/blue-neon-frame-dark-background_53876-113902.jpg",
                    styles={
                        "card": {
                            "width": "100%", 
                            "height": "500px",
                            "border-radius": "15px",
                            "box-shadow": "0 0 40px rgba(255, 215, 0, 0.6)"
                        },
                        "title": {
                            "font-family": "sans-serif", "font-size": "35px", "font-weight": "bold"
                        },
                        "text": {
                            "font-family": "sans-serif", "font-size": "20px"
                        }
                    }
                )
            celebration_placeholder.markdown("<h2 style='text-align: center; color: #FFD700;'>🎉 WE HAVE A WINNER! 🎉</h2>", unsafe_allow_html=True)
            
            # Mark animation as complete so it doesn't re-run on simple interactions
            st.session_state.animation_complete = True
            st.snow()

        else:
            # --- STATIC VIEW (After Animation) ---
            # If we just refresh the page, show everything instantly without waiting
            
            # Fill Left
            for idx, (p_holder, teaser_row) in enumerate(zip(teaser_placeholders, teasers.itertuples())):
                p_holder.markdown(get_teaser_html(idx+1, teaser_row.Full_Name), unsafe_allow_html=True)
            
            # Fill Right
            title_placeholder.markdown('<div class="final-winner-title">Final Draw Winner</div>', unsafe_allow_html=True)
            with card_placeholder:
                card(
                    title=grand_winner['Full_Name'],
                    text=f"Prize: iPhone 17 Pro\n\nInvoice: {grand_winner['Invoice_ID']}\nMobile: {grand_winner['Mobile_No']}",
                    image="https://img.freepik.com/free-vector/blue-neon-frame-dark-background_53876-113902.jpg",
                    styles={
                        "card": {
                            "width": "100%", "height": "500px", "border-radius": "15px", "box-shadow": "0 0 40px rgba(255, 215, 0, 0.6)"
                        },
                        "title": {
                            "font-family": "sans-serif", "font-size": "35px", "font-weight": "bold"
                        },
                        "text": {
                            "font-family": "sans-serif", "font-size": "20px"
                        }
                    }
                )
            celebration_placeholder.markdown("<h2 style='text-align: center; color: #FFD700;'>🎉 WE HAVE A WINNER! 🎉</h2>", unsafe_allow_html=True)

        # --- AUDIT DATA ---
        st.write("---")
        with st.expander("📂 View Elaborated Audit Data", expanded=True):
            st.markdown("### 📋 Official Results Ledger")
            
            display_df = winners.copy()
            cols_to_show = ['Status', 'Full_Name', 'Invoice_ID', 'Mobile_No']
            valid_cols = [c for c in cols_to_show if c in display_df.columns]
            
            st.dataframe(
                display_df[valid_cols],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Status": st.column_config.TextColumn("Result Category", width="medium"),
                    "Full_Name": st.column_config.TextColumn("Participant Name", width="large"),
                    "Invoice_ID": "Invoice Ref",
                    "Mobile_No": "Contact"
                }
            )
            
        if st.button("Start New Draw"):
            st.session_state.current_step = 0
            st.session_state.winners_list = None
            st.session_state.animation_complete = False
            st.rerun()
