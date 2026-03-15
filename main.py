import streamlit as st
from python_helper_file import generate_restaurant_name_and_items
import os
from dotenv import load_dotenv

load_dotenv()
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_API_KEY'] = os.getenv("langchain_api_key")
os.environ['GOOGLE_API_KEY'] = os.getenv("API_KEY")

CUISINE_EMOJIS = {
    "Indian": "🇮🇳", "French": "🇫🇷", "Mexican": "🇲🇽", "Italian": "🇮🇹",
    "American": "🇺🇸", "German": "🇩🇪", "Chinese": "🇨🇳", "Korean": "🇰🇷",
    "Japanese": "🇯🇵", "Thai": "🇹🇭", "Greek": "🇬🇷", "Brazilian": "🇧🇷",
    "Spanish": "🇪🇸", "Vietnamese": "🇻🇳", "Caribbean": "🌴",
}

st.set_page_config(page_title="AI Restaurant Generator", page_icon="🍽️", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Rajdhani', sans-serif;
    }

    .stApp {
        background: #020010;
        background-image:
            radial-gradient(ellipse at 20% 50%, rgba(120, 40, 200, 0.08) 0%, transparent 60%),
            radial-gradient(ellipse at 80% 20%, rgba(0, 200, 255, 0.08) 0%, transparent 60%),
            radial-gradient(ellipse at 50% 80%, rgba(0, 255, 150, 0.05) 0%, transparent 60%);
        min-height: 100vh;
    }

    /* Animated grid background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image:
            linear-gradient(rgba(0,200,255,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,200,255,0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: 0;
    }

    .hero {
        text-align: center;
        padding: 3rem 1rem 1rem;
        position: relative;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(0,200,255,0.08);
        border: 1px solid rgba(0,200,255,0.3);
        color: #00c8ff;
        font-family: 'Orbitron', monospace;
        font-size: 0.65rem;
        letter-spacing: 3px;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        margin-bottom: 1rem;
        text-transform: uppercase;
    }

    .hero h1 {
        font-family: 'Orbitron', monospace;
        font-size: 2.6rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00c8ff 0%, #a855f7 50%, #00ffaa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: 2px;
        line-height: 1.2;
    }

    .hero p {
        color: rgba(180,180,220,0.7);
        font-size: 1rem;
        margin-top: 0.6rem;
        letter-spacing: 1px;
    }

    .cyber-divider {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin: 1.5rem 0;
    }

    .cyber-divider::before, .cyber-divider::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0,200,255,0.4), transparent);
    }

    .cyber-divider span {
        color: rgba(0,200,255,0.5);
        font-family: 'Orbitron', monospace;
        font-size: 0.6rem;
        letter-spacing: 2px;
    }

    /* Restaurant name card */
    .restaurant-card {
        position: relative;
        background: linear-gradient(135deg, rgba(0,200,255,0.05), rgba(168,85,247,0.05));
        border: 1px solid rgba(0,200,255,0.25);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        margin: 1.5rem 0 1rem;
        overflow: hidden;
    }

    .restaurant-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00c8ff, #a855f7, #00ffaa, transparent);
    }

    .restaurant-card::after {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 20px;
        box-shadow: 0 0 40px rgba(0,200,255,0.08), inset 0 0 40px rgba(168,85,247,0.04);
        pointer-events: none;
    }

    .restaurant-card .flag { font-size: 3rem; filter: drop-shadow(0 0 10px rgba(0,200,255,0.4)); }

    .restaurant-card h2 {
        font-family: 'Orbitron', monospace;
        font-size: 1.9rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.8rem 0 0.5rem;
        letter-spacing: 1px;
    }

    .cuisine-tag {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(0,200,255,0.1);
        border: 1px solid rgba(0,200,255,0.3);
        color: #00c8ff;
        border-radius: 30px;
        padding: 0.3rem 1rem;
        font-size: 0.8rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-family: 'Orbitron', monospace;
    }

    /* Menu section */
    .menu-header {
        font-family: 'Orbitron', monospace;
        font-size: 0.75rem;
        letter-spacing: 4px;
        color: rgba(0,200,255,0.6);
        text-align: center;
        text-transform: uppercase;
        margin: 2rem 0 1rem;
    }

    .menu-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 0.75rem;
    }

    .menu-item {
        position: relative;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(168,85,247,0.2);
        border-radius: 14px;
        padding: 1.1rem 0.8rem;
        text-align: center;
        overflow: hidden;
        transition: all 0.3s ease;
    }

    .menu-item::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(168,85,247,0.6), transparent);
    }

    .menu-item:hover {
        border-color: rgba(0,200,255,0.4);
        background: rgba(0,200,255,0.05);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,200,255,0.1);
    }

    .menu-item .icon { font-size: 1.6rem; display: block; margin-bottom: 0.5rem; }

    .menu-item .name {
        color: rgba(220,220,255,0.9);
        font-size: 0.9rem;
        font-weight: 500;
        letter-spacing: 0.5px;
        line-height: 1.3;
    }

    .menu-item .num {
        font-family: 'Orbitron', monospace;
        font-size: 0.6rem;
        color: rgba(168,85,247,0.5);
        letter-spacing: 1px;
        margin-bottom: 0.3rem;
        display: block;
    }

    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 4rem 1rem;
    }

    .empty-state .pulse-ring {
        display: inline-block;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 2px solid rgba(0,200,255,0.3);
        box-shadow: 0 0 20px rgba(0,200,255,0.15), inset 0 0 20px rgba(0,200,255,0.05);
        line-height: 76px;
        font-size: 2rem;
        margin-bottom: 1.5rem;
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 20px rgba(0,200,255,0.15), inset 0 0 20px rgba(0,200,255,0.05); }
        50% { box-shadow: 0 0 35px rgba(0,200,255,0.35), inset 0 0 20px rgba(0,200,255,0.1); }
    }

    .empty-state p {
        color: rgba(180,180,220,0.5);
        font-size: 1rem;
        letter-spacing: 1px;
        line-height: 1.8;
    }

    .empty-state strong { color: rgba(0,200,255,0.8); }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(2,0,16,0.95) !important;
        border-right: 1px solid rgba(0,200,255,0.1) !important;
    }

    section[data-testid="stSidebar"] .stMarkdown p {
        color: rgba(180,180,220,0.7) !important;
    }

    .sidebar-title {
        font-family: 'Orbitron', monospace;
        font-size: 0.65rem;
        letter-spacing: 3px;
        color: rgba(0,200,255,0.6);
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .stSelectbox > div > div {
        background: rgba(0,200,255,0.05) !important;
        border: 1px solid rgba(0,200,255,0.2) !important;
        border-radius: 10px !important;
        color: rgba(220,220,255,0.9) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, rgba(0,200,255,0.15), rgba(168,85,247,0.15)) !important;
        color: #00c8ff !important;
        font-family: 'Orbitron', monospace !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        border: 1px solid rgba(0,200,255,0.4) !important;
        border-radius: 10px !important;
        padding: 0.7rem 1.5rem !important;
        width: 100% !important;
        text-transform: uppercase !important;
        transition: all 0.3s !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(0,200,255,0.25), rgba(168,85,247,0.25)) !important;
        border-color: rgba(0,200,255,0.7) !important;
        box-shadow: 0 0 20px rgba(0,200,255,0.2) !important;
    }

    .powered-by {
        font-family: 'Orbitron', monospace;
        font-size: 0.55rem;
        letter-spacing: 2px;
        color: rgba(168,85,247,0.4);
        text-transform: uppercase;
        text-align: center;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ AI Powered</div>
    <h1>RESTAURANT<br>GENERATOR</h1>
    <p>Select a cuisine · Generate instantly · Explore the future of dining</p>
</div>
<div class="cyber-divider"><span>◆ SYSTEM READY ◆</span></div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<p class="sidebar-title">// Select Cuisine</p>', unsafe_allow_html=True)
    cuisine = st.selectbox("", list(CUISINE_EMOJIS.keys()), label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)
    generate = st.button("⚡ GENERATE")
    st.markdown('<p class="powered-by">Gemini AI · LangChain</p>', unsafe_allow_html=True)

# Output
if generate and cuisine:
    emoji = CUISINE_EMOJIS.get(cuisine, "🍴")
    with st.spinner("Initializing AI sequence..."):
        response = generate_restaurant_name_and_items(cuisine)

    name = response["Restaurant_name"].strip()
    menu_items = [i.strip() for i in response["menu_items"].strip().split(",") if i.strip()]
    food_icons = ["🥘", "🍲", "🥗", "🍜", "🍱", "🥩", "🫕", "🍛"]

    st.markdown(f"""
    <div class="restaurant-card">
        <div class="flag">{emoji}</div>
        <h2>{name}</h2>
        <span class="cuisine-tag">◈ {cuisine} Cuisine</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="menu-header">// Menu Sequence Loaded</p>', unsafe_allow_html=True)

    items_html = '<div class="menu-grid">'
    for i, item in enumerate(menu_items):
        icon = food_icons[i % len(food_icons)]
        items_html += f'<div class="menu-item"><span class="num">ITEM_{i+1:02d}</span><span class="icon">{icon}</span><span class="name">{item}</span></div>'
    items_html += '</div>'
    st.markdown(items_html, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="empty-state">
        <div class="pulse-ring">🍽️</div>
        <p>Select a <strong>cuisine</strong> from the sidebar<br>and hit <strong>GENERATE</strong> to initialize</p>
    </div>
    """, unsafe_allow_html=True)
