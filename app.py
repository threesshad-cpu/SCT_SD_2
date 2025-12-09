import streamlit as st
import random
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="COSMIC COMMAND: FINAL",
    page_icon="🛸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 1. SOUND ENGINE ---
def play_sound(sound_type):
    sounds = {
        "scan": "https://www.soundjay.com/buttons/beep-01a.mp3",
        "win": "https://www.soundjay.com/misc/success-bell-01.mp3",
        "error": "https://www.soundjay.com/buttons/button-10.mp3",
        "ping": "https://www.soundjay.com/buttons/button-30.mp3" 
    }
    if sound_type in sounds:
        st.markdown(f"""
            <audio autoplay>
                <source src="{sounds[sound_type]}" type="audio/mp3">
            </audio>
            """, unsafe_allow_html=True)

# --- 2. CSS STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');

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

    h1, h2, h3, h4 {
        font-family: 'Orbitron', sans-serif !important;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.6);
    }
    p, div, label, input, button {
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 700;
        letter-spacing: 1px;
    }

    /* MAIN DISPLAY BOX */
    .cosmic-display {
        background: linear-gradient(135deg, rgba(10, 10, 20, 0.95), rgba(0, 20, 30, 0.95));
        border: 2px solid #00f0ff;
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.15);
    }
    
    /* SEPARATE LINES FOR FEEDBACK */
    .status-main { font-size: 36px; margin-bottom: 5px; }
    .status-sub { font-size: 18px; color: #aaa; letter-spacing: 2px; }

    /* MODE CARDS */
    .mode-card {
        border: 1px solid #333;
        background: rgba(20, 20, 25, 0.8);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
    }

    /* CUSTOM BUTTONS */
    div.stButton > button {
        background: #0a0a0f;
        color: #00f0ff;
        border: 1px solid #00f0ff;
        width: 100%;
        border-radius: 4px;
        padding: 12px;
        font-size: 16px;
        text-transform: uppercase;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        background: #00f0ff;
        color: #000;
        box-shadow: 0 0 15px #00f0ff;
    }

    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. STATE INITIALIZATION ---
if 'game_active' not in st.session_state: st.session_state.game_active = False
if 'target' not in st.session_state: st.session_state.target = 50
if 'fuel' not in st.session_state: st.session_state.fuel = 100
if 'main_msg' not in st.session_state: st.session_state.main_msg = "SYSTEM STANDBY"
if 'sub_msg' not in st.session_state: st.session_state.sub_msg = "AWAITING INPUT"
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
    
    if mode == "EXPLORATION": st.session_state.max_val = 100
    elif mode == "SURVIVAL": st.session_state.max_val = 100
    elif mode == "QUANTUM": st.session_state.max_val = 150

    st.session_state.target = random.randint(1, st.session_state.max_val)
    st.session_state.fuel = 100
    st.session_state.main_msg = "SCANNER READY"
    st.session_state.sub_msg = f"RANGE: 1 - {st.session_state.max_val}"
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
    # Animation Delay
    with st.spinner("CALCULATING..."):
        time.sleep(0.3)

    # Fuel Logic
    drain = 5
    if st.session_state.mode == "SURVIVAL": drain = 10
    st.session_state.fuel -= drain
    
    # Win Check
    if guess == st.session_state.target:
        st.session_state.main_msg = f"TARGET ACQUIRED: {st.session_state.target}"
        st.session_state.sub_msg = "DECRYPTION SUCCESSFUL"
        st.session_state.feedback_color = "#39ff14"
        st.session_state.sound_trigger = "win"
        st.balloons()
        return

    # Loss Check
    if st.session_state.fuel <= 0:
        st.session_state.main_msg = "MISSION FAILED"
        st.session_state.sub_msg = f"TARGET LOST AT FREQUENCY {st.session_state.target}"
        st.session_state.feedback_color = "#ff0000"
        st.session_state.sound_trigger = "error"
        return

    # Feedback Logic
    main_txt, color, sound = get_feedback(guess, st.session_state.target)
    
    # Split Direction into separate clear instruction
    if guess < st.session_state.target: sub_txt = "📉 TOO LOW -> TUNE UP"
    elif guess > st.session_state.target: sub_txt = "📈 TOO HIGH -> TUNE DOWN"
    else: sub_txt = ""

    st.session_state.main_msg = main_txt
    st.session_state.sub_msg = sub_txt
    st.session_state.feedback_color = color
    st.session_state.sound_trigger = sound

def buy_intel():
    if st.session_state.fuel >= 15:
        st.session_state.fuel -= 15
        tgt = st.session_state.target
        
        # Simplified Intel: Parity + Half
        parity = "EVEN" if tgt % 2 == 0 else "ODD"
        sector = "1-50" if tgt <= 50 else "51-100"
        if st.session_state.max_val > 100 and tgt > 100: sector = "101-150"
        
        st.session_state.hint_text = f"🤖 INTEL: Number is {parity} & in Sector {sector}"
        st.session_state.sound_trigger = "ping"
    else:
        st.session_state.hint_text = "❌ ERROR: Insufficient Fuel"
        st.session_state.sound_trigger = "error"

# --- 5. UI RENDER ---

if st.session_state.sound_trigger:
    play_sound(st.session_state.sound_trigger)
    st.session_state.sound_trigger = None

st.markdown("<h1 style='text-align:center; color:#00f0ff;'>COSMIC COMMAND</h1>", unsafe_allow_html=True)

if not st.session_state.game_active:
    # START SCREEN
    st.markdown("<h3 style='text-align:center; color:#888;'>SELECT DIFFICULTY</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='mode-card'><h3 style='color:#00f0ff'>EXPLORE</h3><p style='color:#ccc; font-size:12px;'>Standard<br>1-100</p></div>", unsafe_allow_html=True)
        if st.button("START"): start_game("EXPLORATION")
    with c2:
        st.markdown("<div class='mode-card'><h3 style='color:#ffaa00'>SURVIVAL</h3><p style='color:#ccc; font-size:12px;'>Hard Mode<br>High Drain</p></div>", unsafe_allow_html=True)
        if st.button("START "): start_game("SURVIVAL")
    with c3:
        st.markdown("<div class='mode-card'><h3 style='color:#bf00ff'>QUANTUM</h3><p style='color:#ccc; font-size:12px;'>Chaos<br>1-150</p></div>", unsafe_allow_html=True)
        if st.button("START  "): start_game("QUANTUM")

else:
    # MAIN GAME
    
    # 1. Clean Display (Split Text)
    st.markdown(f"""
    <div class='cosmic-display' style='border-color: {st.session_state.feedback_color};'>
        <div class='status-main' style='color: {st.session_state.feedback_color};'>
            {st.session_state.main_msg}
        </div>
        <div class='status-sub'>
            {st.session_state.sub_msg}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Fuel
    fuel_pct = max(0, st.session_state.fuel) / 100.0
    st.progress(fuel_pct)
    st.caption(f"HYPERFUEL: {max(0, st.session_state.fuel)}%")

    # 3. Game Controls
    if st.session_state.fuel > 0 and "ACQUIRED" not in st.session_state.main_msg:
        st.write("---")
        
        # Toggle Input Method
        c_tog1, c_tog2 = st.columns(2)
        if c_tog1.button("🎚️ USE SLIDER"): st.session_state.input_method = "SLIDER"
        if c_tog2.button("⌨️ USE KEYPAD"): st.session_state.input_method = "KEYPAD"

        # Render ONLY the active input to prevent bugs
        guess = 50
        if st.session_state.input_method == "SLIDER":
            guess = st.slider("FREQUENCY", 1, st.session_state.max_val, 50, key="slider_input")
        else:
            guess = st.number_input("ENTER COORDINATES", 1, st.session_state.max_val, 50, key="keypad_input")
        
        # Action Buttons
        c_act1, c_act2 = st.columns([2, 1])
        with c_act1:
            if st.button("INITIATE SCAN", type="primary"):
                scan_target(guess)
        with c_act2:
            if st.button("BUY INTEL (-15)"):
                buy_intel()

        # Intel/Error Messages
        if st.session_state.hint_text:
            st.info(st.session_state.hint_text)
            
        st.write("")
        if st.button("🛑 ABORT MISSION"):
            st.session_state.game_active = False
            st.rerun()
            
    else:
        # Game Over / Restart
        st.write("---")
        if st.button("🔄 REBOOT SYSTEM"):
            st.session_state.game_active = False
            st.rerun()