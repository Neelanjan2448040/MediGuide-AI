import streamlit as st
import os
import pandas as pd
import plotly.express as px
from datetime import datetime
import random
from config.config import DATA_DIR
from models.llm import get_llm
from utils.rag_manager import RAGManager
from utils.search_manager import SearchManager
from database.db_manager import DBManager
import streamlit.components.v1 as components

# Page Config
st.set_page_config(page_title="MediGuide AI", page_icon="🧬", layout="wide")

# CORE DASHBOARD CSS
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; font-family: 'Inter', sans-serif; }
    section[data-testid="stSidebar"] { background-color: #161B22 !important; border-right: 1px solid #30363D; }
    .sidebar-brand { font-size: 24px; font-weight: 800; color: #E91E63; margin-bottom: 30px; }
    .stat-box { background-color: transparent; margin-bottom: 20px; }
    .stat-val { font-size: 36px; font-weight: 800; color: white; line-height: 1; }
    .stat-lab { font-size: 13px; color: #8B949E; margin-top: 4px; }
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; border-bottom: 1px solid #30363D; }
    .user-msg { background-color: #21262D; border: 1px solid #30363D; border-radius: 10px; padding: 12px 16px; margin: 10px 0; max-width: 85%; align-self: flex-end; }
    .bot-msg { background-color: transparent; border: 1px solid #30363D; border-radius: 10px; padding: 12px 16px; margin: 10px 0; max-width: 90%; }
    .suggestion-box { background-color: #111927; border-left: 4px solid #1E88E5; padding: 15px; border-radius: 8px; margin: 20px 0; }
    .emergency-alert { background-color: #111927; color: #8B949E; border: 1px solid #30363D; padding: 10px 15px; border-radius: 8px; margin-bottom: 20px; font-size: 13px; }
    .critical-alert { 
        background-color: #FF0000 !important; 
        color: white !important; 
        border: 4px solid white !important; 
        padding: 20px !important; 
        border-radius: 12px !important; 
        margin: 20px 0 !important; 
        font-weight: 900 !important; 
        font-size: 20px !important;
        text-align: center !important;
        box-shadow: 0 0 30px rgba(255,0,0,0.8);
    }
    .action-bar { background-color: #161B22; border: 1px solid #30363D; border-radius: 8px; padding: 12px; margin: 15px 0; display: flex; align-items: center; justify-content: space-between; }
    .disclaimer-text { font-size: 11px; color: #8B949E; text-align: center; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 1. State Hub
if 'user_name' not in st.session_state: st.session_state.user_name = None
if 'chat_session' not in st.session_state: st.session_state.chat_session = []
if 'emergency_flag' not in st.session_state: st.session_state.emergency_flag = False
if 'health_tip' not in st.session_state: st.session_state.health_tip = "💡 Hydration tip: Drink 500ml water immediately after waking up."

# 2. Managers
db = DBManager()
rag = RAGManager()
search = SearchManager()

# --- Sidebar ---
with st.sidebar:
    st.markdown('<div class="sidebar-brand">🧬 MediGuide AI</div>', unsafe_allow_html=True)
    if not st.session_state.user_name:
        st.write("### New Session")
        u_input = st.text_input("Identify your Name", placeholder="e.g. Neelanjan")
        if st.button("Start AI Assistance"):
            if u_input:
                st.session_state.user_name = u_input
                history = db.get_chat_history(u_input)
                if history: st.session_state.chat_session = [{"role": r, "content": c} for r, c in history]
                else:
                    msg = f"Welcome {u_input}."
                    st.session_state.chat_session.append({"role": "bot", "content": msg})
                    db.save_chat_message(u_input, "bot", msg)
                st.rerun()
    else:
        st.success(f"Logged in: **{st.session_state.user_name}**")
        if st.button("Logout / Switch"):
            st.session_state.user_name = None
            st.session_state.chat_session = []
            st.session_state.emergency_flag = False
            st.rerun()

    st.divider()
    up_file = st.file_uploader("Upload Medical PDF", type=["pdf"])
    if up_file:
        f_path = os.path.join(DATA_DIR, up_file.name)
        with open(f_path, "wb") as f: f.write(up_file.getbuffer())
        with st.spinner("Analyzing..."): rag.process_document(f_path)

    st.divider()
    q_all = db.get_query_stats(); a_all = db.get_appointment_stats()
    u_all = db.get_total_users_count(); d_all = len(os.listdir(DATA_DIR)) if os.path.exists(DATA_DIR) else 0
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(f'<div class="stat-box"><div class="stat-val">{q_all}</div><div class="stat-lab">Queries</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-box"><div class="stat-val">{d_all}</div><div class="stat-lab">Documents</div></div>', unsafe_allow_html=True)
    with col_s2:
        st.markdown(f'<div class="stat-box"><div class="stat-val">{a_all}</div><div class="stat-lab">Appointments</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-box"><div class="stat-val">{u_all}</div><div class="stat-lab">Active Users</div></div>', unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
st.markdown('<h1 style="font-size: 38px; font-weight: 800;">🧬 MediGuide AI - Intelligent Health Assistant</h1>', unsafe_allow_html=True)

# THE CRITICAL ALERT
if st.session_state.emergency_flag:
    st.markdown("""
    <div class='critical-alert'>
        🚨 MEDICAL EMERGENCY DETECTED 🚨<br>
        <b>ACTION:</b> Call emergency services or visit the nearest ER immediately.
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔴 DISMISS WARNING"):
        st.session_state.emergency_flag = False
        st.rerun()

tabs = st.tabs(["💬 Chat Intelligence", "📅 Consultations", "📈 Analytics", "⚙️ Control Center"])

if st.session_state.user_name:
    # --- CHAT TAB ---
    with tabs[0]:
        st.markdown("<div class='emergency-alert'>📝 NOTICE: This is an AI assistant, not a doctor. In case of emergency, seek professional help.</div>", unsafe_allow_html=True)
        
        # Toolbar (Mode selection restored)
        st.markdown('<div class="action-bar">', unsafe_allow_html=True)
        m_col1, m_col2 = st.columns([7, 3])
        with m_col1:
            mode = st.radio("Response Mode", ["Concise", "Detailed", "Explain Like I'm 10"], horizontal=True, key="mode_radio")
        with m_col2:
            if st.button("🗑️ Clear My Memory"):
                db.clear_history_for_user(st.session_state.user_name)
                st.session_state.chat_session = []
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Quick Prompts
        st.markdown("""
        <div class="suggestion-box">
            <span style="color: #1E88E5; font-weight: 700;">💡 QUICK PROMPTS:</span>
            <div class="sugg-bullet">• What are the symptoms of dengue?</div>
            <div class="sugg-bullet">• What should I eat and avoid during high fever?</div>
            <div class="sugg-bullet">• How to improve heart health naturally?</div>
        </div>
        """, unsafe_allow_html=True)

        history_box = st.container(height=450)
        with history_box:
            for msg in st.session_state.chat_session:
                prefix = "👤 You" if msg['role'] == 'user' else "🧬 MediGuide"
                st.markdown(f'<div class="{"user-msg" if msg["role"] == "user" else "bot-msg"}"><b>{prefix}</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

        u_in = st.chat_input("How can I assist you with your health today?")
        if u_in:
            u_lower = u_in.lower()
            # 1. ULTRA-ROBUST EMERGENCY DETECTION (ENGLISH ONLY)
            EMG_PATTERNS = [
                "chest pain", "heart pain", "heart attack", "breathing difficulty", "heavy chest", "stroke", "seizure", "poison",
                "emergency", "ambulance", "911", "hospital", "er", "choking", "unconscious", "bleeding"
            ]
            is_urgent = (any(c in u_lower for c in ["chest", "heart"]) and any(p in u_lower for p in ["pain", "attack", "heavy", "trouble"]))
            if any(k in u_lower for k in EMG_PATTERNS) or is_urgent:
                st.session_state.emergency_flag = True
            
            st.session_state.chat_session.append({"role": "user", "content": u_in})
            db.save_chat_message(st.session_state.user_name, "user", u_in)
            
            ctx = rag.retrieve_context(u_in)
            if not ctx: ctx = [search.search_web(u_in)]
            llm = get_llm()
            
            if mode == "Concise":
                detail_instruction = "Provide a direct, factual answer. Use (i), (ii) pointers. No lengthy intros."
            elif mode == "Detailed":
                detail_instruction = "Provide a comprehensive medical guide with WHAT TO EAT and WHAT TO AVOID using (i), (ii) pointers."
            else:
                detail_instruction = "Explain like a friendly story for a 10-year-old using (i), (ii) pointers."

            prompt = f"Identify as Professional Medical Assistant MediGuide AI. Query: {u_in}. Context: {ctx}. {detail_instruction}. Rules: Answer strictly in English. NO Hinglish or Hindi. Address the user politely by their name, {st.session_state.user_name}. NEVER use 'I' when describing the user's symptoms. Use (i)(ii) pointers."
            resp = llm.invoke(prompt).content.replace("**", "").replace("*", "").strip()
            
            st.session_state.chat_session.append({"role": "bot", "content": resp})
            db.save_chat_message(st.session_state.user_name, "bot", resp)
            st.rerun()

    # --- CONSULT TAB ---
    with tabs[1]:
        st.write("### 📅 Consultation Management")
        with st.form("book"):
            d = st.date_input("Select Date", min_value=datetime.today())
            t = st.selectbox("Select Time", ["10:00 AM", "01:00 PM", "04:00 PM"])
            res = st.text_area("Reason")
            if st.form_submit_button("Book Appointment"):
                db.add_appointment(st.session_state.user_name, str(d), t, res)
                st.success("Booked!")

    # --- ANALYTICS ---
    with tabs[2]:
        st.write("### 📈 Intelligent Insights Dashboard")
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1: st.metric("Engagement", f"{q_all} Queries")
        with m_col2: st.metric("Active Users", f"{u_all}")
        with m_col3: st.metric("Knowledge Records", f"{d_all} Files")
        st.divider()
        v1, v2 = st.columns(2)
        with v1:
            topics = db.get_top_topics()
            if topics:
                tdf = pd.DataFrame(topics, columns=["Topic", "Mentions"])
                fig = px.pie(tdf, values='Mentions', names='Topic', hole=.4, title="User Interest Share")
                st.plotly_chart(fig, use_container_width=True)
        with v2:
            st.plotly_chart(px.bar(x=["Engage", "Consults", "Records"], y=[q_all, a_all, d_all], title="Operational Volume", color_discrete_sequence=['#E91E63']), use_container_width=True)
        st.divider()
        st.write("#### 📑 Recent Consultation Registry")
        apps = db.conn.execute("SELECT user_name, date, time, reason FROM appointments ORDER BY id DESC LIMIT 5").fetchall()
        if apps:
            adf = pd.DataFrame(apps, columns=["Patient", "Date", "Time", "Diagnosis/Reason"])
            st.table(adf)

    # --- CONTROL ---
    with tabs[3]:
        st.write("### ⚙️ Control Center")
        if st.button("Reset Everything"):
            if os.path.exists("database/mediguide.db"): os.remove("database/mediguide.db")
            st.rerun()

else:
    st.info("👈 Please enter your name in the sidebar to start.")
    st.markdown("### 🛠️ System Capabilities")
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown('<div class="suggestion-box"><b>🧠 Intelligent Diagnosis</b><br>Real-time symptom analysis and guidance.</div>', unsafe_allow_html=True)
        st.markdown('<div class="suggestion-box"><b>📂 Knowledge Base</b><br>Analyze medical records and PDFs.</div>', unsafe_allow_html=True)
    with f2:
        st.markdown('<div class="suggestion-box"><b>🌐 Global Access</b><br>Anytime, anywhere secure health assistance.</div>', unsafe_allow_html=True)
        st.markdown('<div class="suggestion-box"><b>📊 Advanced Analytics</b><br>Track health trends and performance.</div>', unsafe_allow_html=True)
    with f3:
        st.markdown('<div class="suggestion-box"><b>🚨 Emergency Guard</b><br>Multilingual detection for critical symptoms.</div>', unsafe_allow_html=True)
        st.markdown('<div class="suggestion-box"><b>📅 Care Scheduling</b><br>Manage appointments and consultations.</div>', unsafe_allow_html=True)

st.markdown('<p class="disclaimer-text">MediGuide AI is for informational purposes only. In case of emergency, call 911 or visit an ER.</p>', unsafe_allow_html=True)
