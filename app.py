import streamlit as st
import streamlit.components.v1 as components
import random
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="COSMIC COMMAND",
    page_icon="🚀",
    layout="centered",
    # "collapsed" makes the sidebar hidden until you click the arrow to slide it out
    initial_sidebar_state="collapsed" 
)

# --- 1. JAVASCRIPT PARTY POPPER ---
def trigger_party():
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
        height=0, width=0
    )

# --- 2. SOUND ENGINE ---
def play_sound(sound_name):
    # Check the toggle state from the sidebar
    if not st.session_state.get('sound_enabled', True): return

    sounds = {
        "start": "https://www.soundjay.com/buttons/button-10.mp3",
        "win": "https://www.soundjay.com/misc/success-bell-01.mp3",
        "error": "https://www.soundjay.com/buttons/button-42.mp3"
    }
    if sound_name in sounds:
        st.markdown(f"""
            <audio autoplay>
                <source src="{sounds[sound_name]}" type="audio/mp3">
            </audio>
            """, unsafe_allow_html=True)

# --- 3. CSS STYLING ---
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
    }

    /* SIDEBAR STYLING */
    section[data-testid="stSidebar"] {
        background-color: #0a0a10;
        border-right: 1px solid #00f0ff;
    }

    /* NEON TEXT HEADERS */
    h1, h2, h3 { 
        font-family: 'Orbitron', sans-serif !important; 
        color: #00f0ff !important;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.6); 
    }
    
    /* GAME DISPLAY BOX */
    .cosmic-display {
        background: rgba(20, 20, 30, 0.9);
        border: 2px solid #00f0ff;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* WINNER TEXT */
    .winner-text {
        color: #39ff14 !important;
        font-size: 35px !important;
        font-weight: 900 !important;
        font-family: 'Orbitron', sans-serif !important;
        text-shadow: 0 0 20px #39ff14;
    }

    /* HIDE HEADER/FOOTER */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 4. SESSION STATE ---
if 'game_active' not in st.session_state: st.session_state.game_active = False
if 'target' not in st.session_state: st.session_state.target = 50
if 'fuel' not in st.session_state: st.session_state.fuel = 100
if 'msg_main' not in st.session_state: st.session_state.msg_main = "SYSTEM ONLINE"
if 'msg_sub' not in st.session_state: st.session_state.msg_sub = "READY TO START"
if 'color' not in st.session_state: st.session_state.color = "#00f0ff"
if 'intel_txt' not in st.session_state: st.session_state.intel_txt = ""
if 'sound' not in st.session_state: st.session_state.sound = None
if 'mode' not in st.session_state: st.session_state.mode = "EXPLORATION"
if 'max_val' not in st.session_state: st.session_state.max_val = 100
if 'sound_enabled' not in st.session_state: st.session_state.sound_enabled = True
if 'trigger_party' not in st.session_state: st.session_state.trigger_party = False

# --- 5. GAME FUNCTIONS ---
def start_game(mode):
    st.session_state.game_active = True
    st.session_state.mode = mode
    
    if mode == "EXPLORATION": st.session_state.max_val = 100
    elif mode == "SURVIVAL": st.session_state.max_val = 100
    elif mode == "QUANTUM": st.session_state.max_val = 150

    st.session_state.target = random.randint(1, st.session_state.max_val)
    st.session_state.fuel = 100
    st.session_state.msg_main = "SCANNER INITIALIZED"
    st.session_state.msg_sub = "ENTER FREQUENCY"
    st.session_state.color = "#00f0ff"
    st.session_state.intel_txt = ""
    st.session_state.sound = "start"
    st.session_state.trigger_party = False

def get_feedback(guess, target):
    diff = abs(target - guess)
    if diff == 0: return "SUCCESS!", "#39ff14", "win"
    elif diff <= 4: return "CRITICAL (HOT!!)", "#ff073a", "scan"
    elif diff <= 12: return "VERY CLOSE (HOT)", "#ff4500", "scan"
    elif diff <= 25: return "SIGNAL DETECTED (WARM)", "#ffd700", "scan"
    elif diff <= 40: return "WEAK SIGNAL (COOL)", "#00bfff", "scan"
    else: return "NO SIGNAL (FAR)", "#bf00ff", "error"

def scan(guess):
    if guess == st.session_state.target:
        st.session_state.msg_main = "YOU GUESSED IT RIGHT!"
        st.session_state.msg_sub = f"TARGET LOCKED: {st.session_state.target} // EXCELLENT WORK"
        st.session_state.color = "#39ff14"
        st.session_state.sound = "win"
        st.session_state.trigger_party = True
        return

    with st.spinner("SCANNING..."):
        time.sleep(0.15) 

    cost = 2
    if st.session_state.mode == "SURVIVAL": cost = 5
    st.session_state.fuel -= cost

    if st.session_state.fuel <= 0:
        st.session_state.msg_main = "MISSION FAILED"
        st.session_state.msg_sub = f"HIDDEN TARGET WAS: {st.session_state.target}"
        st.session_state.color = "#ff0000"
        st.session_state.sound = "error"
        return

    main, col, snd = get_feedback(guess, st.session_state.target)
    
    if guess < st.session_state.target: sub = "TRY HIGHER ↑"
    elif guess > st.session_state.target: sub = "TRY LOWER ↓"
    else: sub = ""

    st.session_state.msg_main = main
    st.session_state.msg_sub = sub
    st.session_state.color = col

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

# --- 6. LAYOUT ---

# --- THE "OPTION SLIDER" (SIDEBAR) ---
# This is the menu sliding from the left
with st.sidebar:
    st.header("⚙️ OPTIONS")
    
    # SOUND TOGGLE
    st.session_state.sound_enabled = st.toggle("🔊 Sound Effects", value=True)
    
    st.write("---")
    
    # RESTART
    if st.button("🔄 RESTART GAME", use_container_width=True):
        st.session_state.game_active = False
        st.session_state.sound = "start"
        st.rerun()

    # INSTRUCTION PANEL
    st.header("📝 INSTRUCTIONS")
    st.info("""
    **OBJECTIVE:** Find the secret number.
    
    1. **Scan:** Use the main slider or keypad.
    2. **Signals:**
       - 🔴 **Hot:** Very close.
       - 🔵 **Cold:** Far away.
    3. **Fuel:** Scans cost fuel. Don't run out!
    4. **Win:** Unlock the target to celebrate!
    """)

# --- MAIN GAME SCREEN ---

if st.session_state.sound:
    play_sound(st.session_state.sound)
    st.session_state.sound = None

if st.session_state.trigger_party:
    trigger_party()
    st.session_state.trigger_party = False

st.title("COSMIC COMMAND")

if not st.session_state.game_active:
    st.subheader("SELECT DIFFICULTY")
    c1, c2, c3 = st.columns(3)
    if c1.button("EXPLORE (EASY)", use_container_width=True): start_game("EXPLORATION")
    if c2.button("SURVIVAL (HARD)", use_container_width=True): start_game("SURVIVAL")
    if c3.button("QUANTUM (CHAOS)", use_container_width=True): start_game("QUANTUM")

else:
    # DISPLAY
    if "RIGHT" in st.session_state.msg_main:
        st.markdown(f"""
        <div class='cosmic-display' style='border-color: #39ff14; box-shadow: 0 0 30px #39ff14;'>
            <div class='winner-text'>{st.session_state.msg_main}</div>
            <div style='color: white; margin-top: 10px;'>{st.session_state.msg_sub}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='cosmic-display' style='border-color: {st.session_state.color};'>
            <h2 style='color: {st.session_state.color}; margin:0;'>{st.session_state.msg_main}</h2>
            <p style='color: #ccc; margin-top:5px; font-size: 18px;'>{st.session_state.msg_sub}</p>
        </div>
        """, unsafe_allow_html=True)

    # FUEL
    st.progress(max(0, st.session_state.fuel) / 100.0)
    st.caption(f"HYPERFUEL: {max(0, st.session_state.fuel)}%")

    if st.session_state.fuel > 0 and "RIGHT" not in st.session_state.msg_main:
        st.write("---")
        
        # INPUT SWITCHER
        input_mode = st.radio("SELECT INPUT:", ["SLIDER", "KEYPAD"], horizontal=True)
        
        st.write("")
        
        # GAME INPUT SLIDER
        guess = 50
        if input_mode == "SLIDER":
            guess = st.slider("TUNING FREQUENCY", 1, st.session_state.max_val, 50)
        else:
            guess = st.number_input("ENTER COORDINATES", 1, st.session_state.max_val, 50)

        st.write("")
        
        # BUTTONS
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("INITIATE SCAN", type="primary", use_container_width=True):
                scan(guess)
        with col2:
            if st.button("BUY INTEL (-10)", use_container_width=True):
                buy_intel()

        # INTEL MESSAGE
        if st.session_state.intel_txt:
            st.info(st.session_state.intel_txt)
            
    else:
        st.write("---")
        if st.button("🔄 PLAY AGAIN", type="primary", use_container_width=True):
            st.session_state.game_active = False
            st.session_state.sound = "start"
            st.rerun()