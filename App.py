import streamlit as st
import pandas as pd
import plotly.express as px

# 設定深色背景與寬螢幕
st.set_page_config(page_title="Finance 2026", page_icon="💎", layout="wide")

# 初始化數據 (暫存於網頁)
if "assets" not in st.session_state:
    st.session_state.assets = {"富邦銀行帳戶": 150000.0, "中信台股證券戶": 350000.0}
if "liabilities" not in st.session_state:
    st.session_state.liabilities = {"國泰世華信用卡": 12500.0, "信貸學貸": 200000.0}

total_assets = sum(st.session_state.assets.values())
total_liabilities = sum(st.session_state.liabilities.values())
net_worth = total_assets - total_liabilities

st.title("💎 FINANCE TRACKER MASTER PLAN 2026")
st.markdown("---")

# 看板數字
col1, col2, col3 = st.columns(3)
col1.metric("👑 當前淨身家 (Net Worth)", f"${net_worth:,.2f}")
col2.metric("🟢 總資產", f"${total_assets:,.2f}")
col3.metric("🔴 總負債", f"${total_liabilities:,.2f}")

st.markdown("---")

# 互動記帳表單 (Sidebar)
st.sidebar.header("📥 快速記帳")
type_choice = st.sidebar.selectbox("類型", ["支出 💸", "收入 📥"])
title = st.sidebar.text_input("項目名稱", "點心")
amount = st.sidebar.number_input("金額", min_value=0.0, value=150.0)
account = st.sidebar.selectbox("帳戶", list(st.session_state.assets.keys()) + list(st.session_state.liabilities.keys()))

if st.sidebar.button("確認提交 🚀"):
    if "支出" in type_choice:
        if account in st.session_state.assets: st.session_state.assets[account] -= amount
        else: st.session_state.liabilities[account] += amount
    else:
        if account in st.session_state.assets: st.session_state.assets[account] += amount
    st.rerun()

# 圓餅圖
asset_df = pd.DataFrame(list(st.session_state.assets.items()), columns=["帳戶", "金額"])
fig = px.pie(asset_df, values="金額", names="帳戶", hole=0.4, title="🟢 資產配置比例")
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)
