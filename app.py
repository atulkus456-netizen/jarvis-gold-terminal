import streamlit as st
import google.generativeai as genai
from PIL import Image
import ast

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
st.sidebar.info("⚡ SMC/ICT Core Live Scanner Activated")

st.markdown("<h1>🤖 JARVIS GOLD TERMINAL</h1>", unsafe_allow_html=True)
st.write("---")

# 2. Multi-Upload System
st.subheader("📁 Step 1: Upload Market Structural Screenshots")
uploaded_files = st.file_uploader("Upload up to 5 charts (4H, 1H, 15M, 5M, 1M)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"✔️ {len(uploaded_files)} Screenshots Loaded Successfully into JARVIS Core.")
    st.write("---")
    
    st.markdown("<h2>⚙️ Step 2: Configure Tactical Parameters</h2>", unsafe_allow_html=True)
    
    # Secure API Key Input directly on the web app to avoid GitHub block
    user_api_key = st.text_input("🔑 Enter your Gemini API Key (starts with AIzaSy):", type="password")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        currency = st.radio("Currency:", ["INR 🇮🇳", "USD 💵"])
        trading_type = st.radio("Style:", ["Scalping (5M/1M)", "Intraday (15M/5M/1M)"])
    with col2:
        leverage = st.slider("Leverage:", min_value=1, max_value=15, value=5, step=1)
        capital = st.number_input("Enter Capital:", min_value=100.0, value=9000.0)
    with col3:
        rr_value = st.selectbox("Select Target Risk-Reward (RR) Ratio (1:X):", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], index=2)

    if st.button("🚀 ANALYZE REAL MARKET STRUCTURE"):
        if not user_api_key:
            st.error("Please enter a valid Gemini API Key first!")
        else:
            try:
                with st.spinner("JARVIS Vision AI is processing screenshots..."):
                    genai.configure(api_key=user_api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    img_list = [Image.open(f) for f in uploaded_files]
                    
                    prompt = """
                    You are an institutional XAU/USDT Gold trader analyzing screenshots.
                    Find the current market price visible on the chart axis.
                    Based on SMC/ICT concepts, calculate a trade setup.
                    Return your answer EXACTLY as a valid Python dictionary, nothing else. No backticks, no words, no markdown. 
                    Example format: {"current": 2650.50, "entry": 2645.00, "sl": 2640.00}
                    Make sure the dictionary has exactly these keys: "current", "entry", "sl".
                    """
                    
                    response = model.generate_content([prompt] + img_list)
                    clean_text = response.text.replace("```python", "").replace("```", "").strip()
                    
                    data = ast.literal_eval(clean_text)
                    
                    real_gold_price = float(data["current"])
                    entry_usd = float(data["entry"])
                    sl_usd = float(data["sl"])
                    
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
                st.error(f"Error parsing data: {str(e)}. Please ensure chart prices are fully visible on the right axis and try again.")
else:
    st.info("👋 Welcome Operational Commander. Please upload your market screenshots above to unlock the terminal configuration panel.")
