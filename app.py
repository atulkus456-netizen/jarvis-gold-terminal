import streamlit as st
import subprocess
import sys
import os

# Automatic Package Installer (Taki requirements.txt ka jhanjhat hi khatam ho jaye)
try:
    import google.generativeai as genai
    from PIL import Image
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai", "Pillow"])
    import google.generativeai as genai
    from PIL import Image

# 1. Premium Dark Theme Configuration
st.set_page_config(page_title="JARVIS Gold Terminal", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d0f12; color: #e0e6ed; }
    .stButton>button { background-color: #ff3b30; color: white; border-radius: 5px; font-weight: bold; width: 100%; box-shadow: 0px 0px 10px #ff3b30;}
    h1 { color: #ff3b30; text-shadow: 0 0 10px #ff3b30; font-family: 'Courier New', Courier, monospace; }
    h2, h3 { color: #007aff; text-shadow: 0 0 5px #007aff; }
    .report-box { border: 2px solid #007aff; padding: 20px; border-radius: 10px; background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.markdown("# 🧠 JARVIS Intelligence")
st.sidebar.info("⚡ SMC/ICT Core Live Scanner Activated\n\n🔑 API Key Status: PRE-CONFIGURED & ACTIVE")

st.markdown("<h1>🤖 JARVIS GOLD TERMINAL</h1>", unsafe_allow_html=True)
st.write("---")

# Pre-configured Gemini API Key (Tumhari Key)
HARDCODED_API_KEY = "AIzaSy" + "AQ.Ab8RN6Lb8HMmUlezqraWRScwCwrmtY3Olmmd-X2xlLMLZshADg"

# 2. Multi-Upload System
st.subheader("📁 Step 1: Upload Market Structural Screenshots")
uploaded_files = st.file_uploader("Upload up to 5 charts (4H, 1H, 15M, 5M, 1M)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"✔️ {len(uploaded_files)} Screenshots Loaded Successfully into JARVIS Core.")
    st.write("---")
    
    st.markdown("<h2>⚙️ Step 2: Configure Tactical Parameters</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        currency = st.radio("Currency:", ["INR 🇮🇳", "USD 💵"])
        trading_type = st.radio("Style:", ["Scalping (5M/1M)", "Intraday (15M/5M/1M)"])
    with col2:
        leverage = st.slider("Leverage:", min_value=1, max_value=15, value=5, step=1)
        capital = st.number_input("Enter Capital:", min_value=100.0, value=9000.0)
    with col3:
        rr_ratio = st.selectbox("Select Target RR:", [f"1:{i}" for i in range(1, 11)], index=2)
        rr_value = int(rr_ratio.split(":"))

    if st.button("🚀 ANALYZE REAL MARKET STRUCTURE"):
        try:
            with st.spinner("JARVIS Vision AI is processing screenshots and extraction logic..."):
                genai.configure(api_key=HARDCODED_API_KEY)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                img_list = [Image.open(f) for f in uploaded_files]
                
                prompt = """
                Analyze these XAU/USDT Gold trading charts. Find the exact current real market price visible on the right axis.
                Based on SMC/ICT (Order Blocks, FVG, Liquidity sweeps), calculate an institutional trade setup.
                Output ONLY the numeric values in exact USD point format (e.g. 2650.50) separated by commas for:
                CurrentPrice, RecommendedEntryPrice, SuggestedStopLoss. 
                Do not write any other words, letters, or explanation. Just give the 3 numbers separated by commas.
                """
                
                response = model.generate_content([prompt] + img_list)
                clean_text = response.text.replace(" ", "").replace("\n", "").strip()
                prices = clean_text.split(",")
                
                real_gold_price = float(prices[0])
                entry_usd = float(prices[1])
                sl_usd = float(prices[2])
                
                # Calculations
                sl_dist = abs(entry_usd - sl_usd)
                if entry_usd > sl_usd:
                    tp_usd = entry_usd + (sl_dist * rr_value)
                else:
                    tp_usd = entry_usd - (sl_dist * rr_value)
                
                usd_inr_rate = 84.0
                capital_usd = capital / usd_inr_rate if "INR" in currency else capital
                risk_usd = capital_usd * 0.01
                
                lot_size = risk_usd / (sl_dist * 100) if sl_dist > 0 else 0.01
                final_lot = max(0.001, min(lot_size, (capital_usd * leverage) / (real_gold_price * 10)))
                
                mult = usd_inr_rate if "INR" in currency else 1.0
                sym = "₹" if "INR" in currency else "$"
                
                st.markdown(f"""
                <div class="report-box">
                    <h3 style='color: #34c759;'>🎯 LIVE MATRIX ACTIVATED ({trading_type.upper()})</h3>
                    <p style='font-size: 18px;'><b>Detected Gold Price from Chart:</b> {sym}{real_gold_price*mult:,.2f}</p>
                    <hr style='border-color: #007aff;'>
                    <table style='width:100%; font-size: 16px; border-collapse: collapse;'>
                        <tr><td><b>🎯 Target Entry Price:</b></td><td style='color: #34c759; font-size: 18px;'><b>{sym}{entry_usd*mult:,.2f}</b></td></tr>
                        <tr><td><b>🛑 Absolute Stop Loss (SL):</b></td><td style='color: #ff3b30; font-size: 18px;'><b>{sym}{sl_usd*mult:,.2f}</b></td></tr>
                        <tr><td><b>💰 Take Profit Target (TP):</b></td><td style='color: #007aff; font-size: 18px;'><b>{sym}{tp_usd*mult:,.2f}</b></td></tr>
                        <tr style='background-color: #1c2128;'><td><b>📊 Recommended Lot Size:</b></td><td style='color: #ffcc00; font-size: 18px;'><b>{final_lot:.3f} Lots</b></td></tr>
                        <tr><td><b>⚠️ Total 1% Risk Allowed:</b></td><td>{sym}{risk_usd*mult:,.2f}</td></tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error("Error: Chart structure complex or right-side price scale not fully clear. Please ensure chart prices are readable.")
else:
    st.info("👋 Welcome Operational Commander. Please upload your market screenshots above to unlock the terminal configuration panel.")
