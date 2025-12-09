import streamlit as st
import streamlit.components.v1 as components
import random
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="COSMIC COMMAND: FINAL",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 1. STABLE PARTY POPPER ENGINE (JAVASCRIPT) ---
def trigger_party_mode():
    # This uses a professional library to blast confetti without glitches
    components.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
            var duration = 3 * 1000;
            var animationEnd = Date.now() + duration;
            var defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 9999 };

            function randomInOut(min, max) { return Math.random() * (max - min) + min; }

            var interval = setInterval(function() {
              var timeLeft = animationEnd - Date.now();
              if (timeLeft <= 0) { return clearInterval(interval); }
              
              var particleCount = 50 * (timeLeft / duration);
              confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInOut(0.1, 0.3), y: Math.random() - 0.2 } }));
              confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInOut(0.7, 0.9), y: Math.random() - 0.2 } }));
            }, 250);
        </script>
        """,
        height=0, width=0 # Invisible container
    )

# --- 2. SOUND ENGINE ---
def play_sound(sound_type):
    if not st.session_state.get('sound_on', True): return

    sounds = {
        "start": "https://www.soundjay.com/buttons/button-10.mp3", # Initiating
        "win": "https://www.soundjay.com/misc/success-bell-01.mp3", # Excellent/Unlocked
        "error": "https://www.soundjay.com/buttons/button-42.mp3"   # Fail
    }
    if sound_type in sounds:
        st.markdown(f"""
            <audio autoplay>
                <source src="{sounds[sound_type]}" type="audio/mp3">
            </audio>
            """, unsafe_allow_html=True)

# --- 3. CSS STYLING (GLITCH FIX) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;700&display=swap');

    /* BACKGROUND */
    .stApp {
        background-color: #050508;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px);
        background-size: 550px 550px, 350px 350px;
        animation: star-move 120s linear infinite;
    }
    @keyframes star-move {
        from { background-position: 0 0, 40px 60px; }
        to { background-position: 1000px 1000px, 1040px 1060px; }
    }

    /* FONTS */
    h1, h2, h3 { font-family: 'Orbitron', sans-serif !important; text-shadow: 0 0 10px rgba(0, 240, 255, 0.6); }
    div, p, button, span, li { font-family: 'Rajdhani', sans-serif !important; font-weight: 700; letter-spacing: 1px; }

    /* --- FIX FOR THE TEXT GLITCH --- */
    /* This forces icons to use the correct symbol font instead of your custom font */
    .material-icons, .st-emotion-cache-1pbqdg3, .st-emotion-cache-10trblm, i {
        font-family: sans-serif !important; 
    }

    /* NEON DISPLAY */
    .cosmic-display {
        background: linear-gradient(135deg, rgba(10, 10, 20, 0.95), rgba(0, 20, 30, 0.95));
        border: 2px solid #00f0ff;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.2);
    }
    
    /* WINNER TEXT */
    .winner-text {
        color: #39ff14 !important;
        font-size: 42px !important;
        font-weight: 900 !important;
        text-shadow: 0 0 20px #39ff14;
        animation: pulse 0.5s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    /* BUTTONS */
    div.stButton > button {
        background: #0a0a0f;
        color: #00f0ff;
        border: 1px solid #00f0ff;
        width: 100%;
        border-radius: 5px;
        padding: 12px;
        font-size: 18px;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        background: #00f0ff;
        color: black;
        box-shadow: 0 0 20px #00f0ff;
    }

    /* SLIDER VISIBILITY FIX */
    div[data-testid="stThumbValue"] { font-family: 'Rajdhani', sans-serif !important; font-size: 14px; }
    div[role="slider"] { background-color: #00f0ff !important; border: 2px solid white; height: 20px; width: 20px; }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 4. STATE ---
if 'game_active' not in st.session_state: st.session_state.game_active = False
if 'target' not in st.session_state: st.session_state.target = 50
if 'fuel' not in st.session_state: st.session_state.fuel = 100
if 'msg_main' not in st.session_state: st.session_state.msg_main = "SYSTEM ONLINE"
if 'msg_sub' not in st.session_state: st.session_state.msg_sub = "READY TO START"
if 'color' not in st.session_state: st.session_state.color = "#00f0ff"
if 'input_type' not in st.session_state: st.session_state.input_type = "SLIDER"
if 'intel_txt' not in st.session_state: st.session_state.intel_txt = ""
if 'sound' not in st.session_state: st.session_state.sound = None
if 'mode' not in st.session_state: st.session_state.mode = "EXPLORATION"
if 'max_val' not in st.session_state: st.session_state.max_val = 100
if 'sound_on' not in st.session_state: st.session_state.sound_on = True
if 'trigger_party' not in st.session_state: st.session_state.trigger_party = False

# --- 5. LOGIC ---
def start_game(mode):
    st.session_state.game_active = True
    st.session_state.mode = mode
    
    if mode == "EXPLORATION": st.session_state.max_val = 100
    elif mode == "SURVIVAL": st.session_state.max_val = 100
    elif mode == "QUANTUM": st.session_state.max_val = 150

    st.session_state.target = random.randint(1, st.session_state.max_val)
    st.session_state.fuel = 100
    st.session_state.msg_main = "INITIATING..."
    st.session_state.msg_sub = "ENTER FREQUENCY"
    st.session_state.color = "#00f0ff"
    st.session_state.intel_txt = ""
    st.session_state.sound = "start"
    st.session_state.trigger_party = False

def get_feedback(guess, target):
    diff = abs(target - guess)
    if diff == 0: return "EXCELLENT!", "#39ff14", "win"
    elif diff <= 4: return "CRITICAL (BURNING HOT!!)", "#ff073a", "scan"
    elif diff <= 12: return "VERY CLOSE (HOT)", "#ff4500", "scan"
    elif diff <= 25: return "SIGNAL DETECTED (WARM)", "#ffd700", "scan"
    elif diff <= 40: return "WEAK SIGNAL (COOL)", "#00bfff", "scan"
    else: return "NO SIGNAL (FAR)", "#bf00ff", "error"

def scan(guess):
    # INSTANT WIN CHECK
    if guess == st.session_state.target:
        st.session_state.msg_main = "TARGET UNLOCKED!"
        st.session_state.msg_sub = f"EXCELLENT WORK. NUMBER WAS {st.session_state.target}"
        st.session_state.color = "#39ff14"
        st.session_state.sound = "win"
        st.session_state.trigger_party = True
        return

    # Delay only on non-wins
    with st.spinner("ANALYZING..."):
        time.sleep(0.15) 

    # Low Cost Scanning
    cost = 2
    if st.session_state.mode == "SURVIVAL": cost = 5
    st.session_state.fuel -= cost

    # Loss Check
    if st.session_state.fuel <= 0:
        st.session_state.msg_main = "MISSION FAILED"
        st.session_state.msg_sub = f"HIDDEN TARGET WAS: {st.session_state.target}"
        st.session_state.color = "#ff0000"
        st.session_state.sound = "error"
        return

    # Feedback
    main, col, snd = get_feedback(guess, st.session_state.target)
    
    if guess < st.session_state.target: sub = "TRY HIGHER ↑"
    elif guess > st.session_state.target: sub = "TRY LOWER ↓"
    else: sub = ""

    st.session_state.msg_main = main
    st.session_state.msg_sub = sub
    st.session_state.color = col
    # No sound on normal scans

def buy_intel():
    if st.session_state.fuel >= 10:
        st.session_state.fuel -= 10
        tgt = st.session_state.target
        parity = "EVEN" if tgt % 2 == 0 else "ODD"
        sector = "1-50" if tgt <= 50 else "51-100"
        if st.session_state.max_val > 100 and tgt > 100: sector = "101-150"
        st.session_state.intel_txt = f"💡 INTEL: Number is {parity} & in Sector {sector}"
    else:
        st.session_state.intel_txt = "❌ NOT ENOUGH FUEL (Need 10%)"
        st.session_state.sound = "error"

# --- 6. UI RENDERING ---

# SIDEBAR (Clear Mission Brief)
with st.sidebar:
    st.markdown("## 🚀 MENU")
    st.session_state.sound_on = st.toggle("🔊 SOUNDS", value=True)
    st.write("---")
    if st.button("🔄 RESTART GAME"):
        st.session_state.game_active = False
        st.session_state.sound = "start"
        st.rerun()

    st.markdown("### 📝 MISSION BRIEF")
    st.info("""
    **OBJECTIVE:** Find the hidden number before you run out of fuel.
    
    **INSTRUCTIONS:**
    1. **Scan:** Use the slider/keypad to guess.
    2. **Feedback:** "Hot" means close, "Cold" means far.
    3. **Win:** Get "Target Unlocked!"
    """)

# MAIN SCREEN
if st.session_state.sound:
    play_sound(st.session_state.sound)
    st.session_state.sound = None

# PARTY POPPER TRIGGER
if st.session_state.trigger_party:
    trigger_party_mode()
    st.session_state.trigger_party = False

st.markdown("<h1 style='text-align:center; color:#00f0ff;'>COSMIC COMMAND</h1>", unsafe_allow_html=True)

if not st.session_state.game_active:
    # START SCREEN
    st.markdown("<h3 style='text-align:center; color:#666;'>SELECT DIFFICULTY</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("EXPLORE (EASY)"): start_game("EXPLORATION")
    if c2.button("SURVIVAL (HARD)"): start_game("SURVIVAL")
    if c3.button("QUANTUM (CHAOS)"): start_game("QUANTUM")

else:
    # GAME SCREEN
    if "UNLOCKED" in st.session_state.msg_main:
        st.markdown(f"""
        <div class='cosmic-display' style='border-color: #39ff14; box-shadow: 0 0 40px #39ff14;'>
            <div class='winner-text'>YOU GUESSED IT RIGHT!</div>
            <div style='color: #fff; letter-spacing: 2px; margin-top: 10px; font-size: 20px;'>{st.session_state.msg_sub}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='cosmic-display' style='border-color: {st.session_state.color};'>
            <h2 style='color: {st.session_state.color}; margin:0; font-size:36px;'>{st.session_state.msg_main}</h2>
            <p style='color: #aaa; margin-top:5px; font-size:18px;'>{st.session_state.msg_sub}</p>
        </div>
        """, unsafe_allow_html=True)

    fuel_pct = max(0, st.session_state.fuel) / 100.0
    st.progress(fuel_pct)
    st.caption(f"HYPERFUEL: {max(0, st.session_state.fuel)}%")

    if st.session_state.fuel > 0 and "UNLOCKED" not in st.session_state.msg_main:
        st.write("---")
        
        c_tog1, c_tog2 = st.columns(2)
        if c_tog1.button("🎚️ SLIDER"): st.session_state.input_type = "SLIDER"
        if c_tog2.button("⌨️ KEYPAD"): st.session_state.input_type = "KEYPAD"
        st.write("")
        
        guess = 50
        if st.session_state.input_type == "SLIDER":
            guess = st.slider("TUNING FREQUENCY", 1, st.session_state.max_val, 50)
        else:
            guess = st.number_input("ENTER COORDINATES", 1, st.session_state.max_val, 50)

        st.write("")
        c_act1, c_act2 = st.columns([2,1])
        with c_act1:
            if st.button("INITIATE SCAN", type="primary"):
                scan(guess)
        with c_act2:
            if st.button("BUY INTEL (-10)"):
                buy_intel()

        if st.session_state.intel_txt:
            st.info(st.session_state.intel_txt)
            
    else:
        st.write("---")
        if st.button("🔄 REBOOT SYSTEM (PLAY AGAIN)"):
            st.session_state.game_active = False
            st.session_state.sound = "start"
            st.rerun()