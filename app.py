import streamlit as st
import random
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="COSMIC COMMAND: DIRECTOR'S CUT",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 1. SOUND ENGINE (WEB) ---
def play_sound(sound_type):
    sounds = {
        "scan": "https://www.soundjay.com/buttons/beep-01a.mp3",
        "win": "https://www.soundjay.com/misc/success-bell-01.mp3",
        "error": "https://www.soundjay.com/buttons/button-10.mp3",
        "ping": "https://www.soundjay.com/buttons/button-30.mp3" 
    }
    if sound_type in sounds:
        # Invisible audio player
        st.markdown(f"""
            <audio autoplay>
                <source src="{sounds[sound_type]}" type="audio/mp3">
            </audio>
            """, unsafe_allow_html=True)

# --- 2. ADVANCED CSS (FIXED & POLISHED) ---
st.markdown("""
    <style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');

    /* ANIMATED STARFIELD BACKGROUND */
    .stApp {
        background-color: #050508;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px);
        background-size: 550px 550px, 350px 350px;
        background-position: 0 0, 40px 60px;
        animation: star-move 100s linear infinite;
    }
    @keyframes star-move {
        from { background-position: 0 0, 40px 60px; }
        to { background-position: 1000px 1000px, 1040px 1060px; }
    }

    /* TYPOGRAPHY - TARGETED TO AVOID BREAKING ICONS */
    h1, h2, h3, h4, .big-font {
        font-family: 'Orbitron', sans-serif !important;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.6);
    }
    p, div, label, input, button {
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 700;
        letter-spacing: 1px;
    }

    /* NEON DISPLAY BOX */
    .cosmic-display {
        background: linear-gradient(135deg, rgba(10, 10, 20, 0.95), rgba(0, 20, 30, 0.95));
        border: 2px solid #00f0ff;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.15), inset 0 0 20px rgba(0, 240, 255, 0.05);
    }

    /* MODE SELECTION CARDS */
    .mode-card {
        border: 1px solid #333;
        background: rgba(20, 20, 25, 0.8);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
        transition: 0.3s;
    }
    .mode-card:hover {
        border-color: #00f0ff;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
    }

    /* CUSTOM BUTTONS */
    div.stButton > button {
        background: #0a0a0f;
        color: #00f0ff;
        border: 1px solid #00f0ff;
        width: 100%;
        border-radius: 4px;
        padding: 10px;
        font-size: 16px;
        text-transform: uppercase;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        background: #00f0ff;
        color: #000;
        font-weight: bold;
        box-shadow: 0 0 15px #00f0ff;
    }

    /* HIDE DEFAULT HEADER/FOOTER */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'game_active' not in st.session_state: st.session_state.game_active = False
if 'target' not in st.session_state: st.session_state.target = 50
if 'fuel' not in st.session_state: st.session_state.fuel = 100
if 'message' not in st.session_state: st.session_state.message = "SYSTEM STANDBY"
if 'feedback_color' not in st.session_state: st.session_state.feedback_color = "#444"
if 'input_method' not in st.session_state: st.session_state.input_method = "SLIDER"
if 'hint_text' not in st.session_state: st.session_state.hint_text = ""
if 'sound_trigger' not in st.session_state: st.session_state.sound_trigger = None
if 'mode' not in st.session_state: st.session_state.mode = "EXPLORATION"
if 'max_val' not in st.session_state: st.session_state.max_val = 100

# --- 4. GAME LOGIC ---
def start_game(mode):
    st.session_state.game_active = True
    st.session_state.mode = mode
    
    # Mode Config
    if mode == "EXPLORATION":
        st.session_state.max_val = 100
        drain = 5
    elif mode == "SURVIVAL":
        st.session_state.max_val = 100
        drain = 10
    elif mode == "QUANTUM":
        st.session_state.max_val = 150
        drain = 8

    st.session_state.target = random.randint(1, st.session_state.max_val)
    st.session_state.fuel = 100
    st.session_state.message = "SCANNER INITIALIZED"
    st.session_state.feedback_color = "#00f0ff"
    st.session_state.hint_text = ""
    st.session_state.sound_trigger = "scan"

def get_feedback(guess, target):
    diff = abs(target - guess)
    if diff == 0: return "TARGET LOCKED!", "#39ff14", "win"
    elif diff <= 2: return "CRITICAL (HOT!!)", "#ff073a", "scan"
    elif diff <= 5: return "HIGH SIGNAL (HOT)", "#ff4500", "scan"
    elif diff <= 10: return "DETECTING (WARM)", "#ffd700", "scan"
    elif diff <= 20: return "WEAK SIGNAL (COOL)", "#00bfff", "scan"
    else: return "NO SIGNAL (FAR)", "#bf00ff", "error"

def scan_target(guess):
    # Suspense Animation
    with st.spinner("CALCULATING TRAJECTORY..."):
        time.sleep(0.4) # Small delay for "Juice"
        
    drain = 5
    if st.session_state.mode == "SURVIVAL": drain = 10
    if st.session_state.mode == "QUANTUM": drain = 8
    
    st.session_state.fuel -= drain
    
    # Check Win
    if guess == st.session_state.target:
        st.session_state.message = f"TARGET LOCKED: {st.session_state.target}"
        st.session_state.feedback_color = "#39ff14"
        st.session_state.sound_trigger = "win"
        st.balloons()
        return

    # Check Loss
    if st.session_state.fuel <= 0:
        st.session_state.message = f"FAILED. TARGET WAS {st.session_state.target}"
        st.session_state.feedback_color = "#ff0000"
        st.session_state.sound_trigger = "error"
        return

    # Feedback
    msg, color, sound = get_feedback(guess, st.session_state.target)
    
    if guess < st.session_state.target: direction = "(TOO LOW)"
    elif guess > st.session_state.target: direction = "(TOO HIGH)"
    else: direction = ""

    st.session_state.message = f"{msg} {direction}"
    st.session_state.feedback_color = color
    st.session_state.sound_trigger = sound

def buy_intel():
    if st.session_state.fuel >= 15:
        st.session_state.fuel -= 15
        tgt = st.session_state.target
        low = max(1, tgt - random.randint(5,15))
        high = min(st.session_state.max_val, tgt + random.randint(5,15))
        st.session_state.hint_text = f"🤖 INTEL: Target is between {low} and {high}"
        st.session_state.sound_trigger = "ping"
    else:
        st.session_state.hint_text = "❌ ERROR: Insufficient Fuel for Intel"
        st.session_state.sound_trigger = "error"

# --- 5. UI RENDERING ---

# Trigger Sound
if st.session_state.sound_trigger:
    play_sound(st.session_state.sound_trigger)
    st.session_state.sound_trigger = None

# Title
st.markdown("<h1 style='text-align:center; color:#00f0ff;'>COSMIC COMMAND</h1>", unsafe_allow_html=True)

if not st.session_state.game_active:
    # --- MENU SCREEN (IMPROVED) ---
    st.markdown("<h3 style='text-align:center; color:#888; margin-bottom: 30px;'>SELECT MISSION PROTOCOL</h3>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <div class='mode-card'>
            <h3 style='color:#00f0ff'>EXPLORATION</h3>
            <p style='color:#ccc; font-size:12px;'>Standard Training.<br>Range: 1-100<br>Fuel Drain: Low</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("LAUNCH ALPHA"): start_game("EXPLORATION")

    with c2:
        st.markdown("""
        <div class='mode-card'>
            <h3 style='color:#ffaa00'>SURVIVAL</h3>
            <p style='color:#ccc; font-size:12px;'>High Stakes.<br>Range: 1-100<br>Fuel Drain: HIGH</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("LAUNCH BETA"): start_game("SURVIVAL")

    with c3:
        st.markdown("""
        <div class='mode-card'>
            <h3 style='color:#bf00ff'>QUANTUM</h3>
            <p style='color:#ccc; font-size:12px;'>Unstable Physics.<br>Range: 1-150<br>Fuel Drain: Medium</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("LAUNCH OMEGA"): start_game("QUANTUM")

else:
    # --- GAME SCREEN ---
    
    # 1. Main Monitor
    st.markdown(f"""
    <div class='cosmic-display' style='border-color: {st.session_state.feedback_color};'>
        <h4 style='color: #888; margin: 0; font-size: 14px; letter-spacing: 2px;'>SIGNAL MONITOR</h4>
        <h2 style='color: {st.session_state.feedback_color}; font-size: 36px; margin: 10px 0;'>
            {st.session_state.message}
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # 2. Status Bar
    fuel_pct = max(0, st.session_state.fuel) / 100.0
    st.progress(fuel_pct)
    c_stat1, c_stat2 = st.columns([1, 1])
    with c_stat1:
        st.caption(f"🔋 HYPERFUEL: {max(0, st.session_state.fuel)}%")
    with c_stat2:
        st.caption(f"📡 MODE: {st.session_state.mode}")
    
    # 3. Game Controls (Only if alive)
    if st.session_state.fuel > 0 and "LOCKED" not in st.session_state.message:
        st.write("---")
        
        # Centering Layout using Columns
        c_pad1, c_main, c_pad2 = st.columns([1, 3, 1])
        
        with c_main:
            # Input Switcher
            tabs = st.tabs(["🎚️ SLIDER", "⌨️ KEYPAD"])
            
            with tabs[0]:
                guess_slider = st.slider("FREQUENCY TUNER", 1, st.session_state.max_val, 50)
                if st.button("INITIATE SCAN (SLIDER)", type="primary"):
                    scan_target(guess_slider)
            
            with tabs[1]:
                guess_key = st.number_input("ENTER COORDINATES", 1, st.session_state.max_val, 50)
                if st.button("INITIATE SCAN (KEYPAD)", type="primary"):
                    scan_target(guess_key)

        st.write("---")
        
        # Bottom Actions
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("💰 BUY INTEL (-15)"):
                buy_intel()
        with c_b2:
            if st.button("🛑 ABORT MISSION"):
                st.session_state.game_active = False
                st.rerun()

        # Hints
        if st.session_state.hint_text:
            st.warning(st.session_state.hint_text)
            
    else:
        # Game Over / Restart
        st.write("---")
        if st.button("🔄 REBOOT SYSTEM (PLAY AGAIN)"):
            st.session_state.game_active = False
            st.rerun()