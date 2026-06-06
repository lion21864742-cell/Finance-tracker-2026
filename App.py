import streamlit as st
import pandas as pd
import plotly.express as px

# 設定網頁標題與寬螢幕
st.set_page_config(page_title="Finance Master 2026", page_icon="💎", layout="wide")

# 1. 初始化資料庫（如果網頁第一次打開，給予預設值）
if "assets" not in st.session_state:
    st.session_state.assets = {"富邦銀行帳戶": 150000.0, "中信台股證券戶": 350000.0}
if "liabilities" not in st.session_state:
    st.session_state.liabilities = {"國泰世華信用卡": 12500.0, "信貸學貸": 200000.0}
if "logs" not in st.session_state:
    st.session_state.logs = []

# 計算當前核心财务數據
total_assets = sum(st.session_state.assets.values())
total_liabilities = sum(st.session_state.liabilities.values())
net_worth = total_assets - total_liabilities

# ==================== 網頁主標題 ====================
st.title("💎 FINANCE TRACKER MASTER PLAN 2026")
st.caption("iPad 專屬全動態控制版 — 數據、資產完全在線修改")
st.markdown("---")

# ==================== 頂部三大看板 ====================
col1, col2, col3 = st.columns(3)
col1.metric("👑 當前淨身家 (Net Worth)", f"${net_worth:,.2f}")
col2.metric("🟢 總資產 (Total Assets)", f"${total_assets:,.2f}")
col3.metric("🔴 總負債 (Total Liabilities)", f"${total_liabilities:,.2f}")
st.markdown("---")

# ==================== 分頁架構（將記帳與後台分開） ====================
tab_dashboard, tab_input, tab_settings = st.tabs(["📊 財務總覽 & 圖表", "💸 每日快速記帳", "⚙️ 網站後台（修改資產配置）"])

# -------------------- TAB 1: 財務總覽 & 圖表 --------------------
with tab_dashboard:
    chart_col, log_col = st.columns([1, 1])
    with chart_col:
        st.subheader("🟢 資產配置比例")
        if st.session_state.assets:
            asset_df = pd.DataFrame(list(st.session_state.assets.items()), columns=["帳戶", "金額"])
            fig = px.pie(asset_df, values="金額", names="帳戶", hole=0.4)
            fig.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("目前沒有資產數據，請至後台新增。")
            
    with log_col:
        st.subheader("📜 歷史交易流水")
        if st.session_state.logs:
            st.dataframe(pd.DataFrame(st.session_state.logs).iloc[::-1], use_container_width=True)
        else:
            st.text("暫無記帳紀錄。")

# -------------------- TAB 2: 每日快速記帳 --------------------
with tab_input:
    st.subheader("📥 填寫今日收支")
    all_accounts = list(st.session_state.assets.keys()) + list(st.session_state.liabilities.keys())
    
    if not all_accounts:
        st.warning("⚠️ 請先前往「⚙️ 網站後台」建立至少一個資產或負債帳戶。")
    else:
        with st.form("quick_record", clear_on_submit=True):
            tx_type = st.selectbox("交易類型", ["支出 💸", "收入 📥"])
            title = st.text_input("項目描述", placeholder="例如：晚餐、薪水")
            amount = st.number_input("金額 ($)", min_value=0.0, step=10.0)
            account = st.selectbox("選擇帳戶", all_accounts)
            submit = st.form_submit_button("確認提交 🚀")
            
            if submit and amount > 0:
                if "支出" in tx_type:
                    if account in st.session_state.assets: st.session_state.assets[account] -= amount
                    else: st.session_state.liabilities[account] += amount
                else:
                    if account in st.session_state.assets: st.session_state.assets[account] += amount
                    else: st.session_state.liabilities[account] -= amount
                
                st.session_state.logs.append({"項目": title if title else tx_type, "金額": amount, "帳戶": account})
                st.success("記帳成功！數據已動態更新。")
                st.rerun()

# -------------------- TAB 3: 網站後台（直接修改資產配置） --------------------
with tab_settings:
    st.subheader("🛠️ 帳戶與資產配置管理面板")
    st.markdown("你可以在這裡**直接修改金額**、**新增全新帳戶**或**刪除舊帳戶**。")
    
    edit_col1, edit_col2 = st.columns(2)
    
    # 修改/新增資產
    with edit_col1:
        st.write("### 🟢 資產帳戶管理")
        # 讓用戶直接在網頁上改數字
        for asset_name in list(st.session_state.assets.keys()):
            new_val = st.number_input(f"修改【{asset_name}】餘額", value=st.session_state.assets[asset_name], key=f"edit_{asset_name}")
            st.session_state.assets[asset_name] = new_val
            if st.button(f"❌ 刪除 {asset_name}", key=f"del_{asset_name}"):
                del st.session_state.assets[asset_name]
                st.rerun()
                
        st.markdown("---")
        st.write("#### ➕ 新增全新資產項目")
        new_asset_name = st.text_input("新資產名稱（例如：恆生銀行、現金）", key="add_asset_name")
        new_asset_val = st.number_input("初始金額", min_value=0.0, key="add_asset_val")
        if st.button("確認新增資產 🟢"):
            if new_asset_name:
                st.session_state.assets[new_asset_name] = new_asset_val
                st.success(f"已新增資產：{new_asset_name}")
                st.rerun()

    # 修改/新增負債
    with edit_col2:
        st.write("### 🔴 負債帳戶管理")
        for lia_name in list(st.session_state.liabilities.keys()):
            new_val = st.number_input(f"修改【{lia_name}】欠款", value=st.session_state.liabilities[lia_name], key=f"edit_{lia_name}")
            st.session_state.liabilities[lia_name] = new_val
            if st.button(f"❌ 刪除 {lia_name}", key=f"del_{lia_name}"):
                del st.session_state.liabilities[lia_name]
                st.rerun()
                
        st.markdown("---")
        st.write("#### ➕ 新增全新負債項目")
        new_lia_name = st.text_input("新負債名稱（例如：渣打信用卡、車貸）", key="add_lia_name")
        new_lia_val = st.number_input("初始欠款", min_value=0.0, key="add_lia_val")
        if st.button("確認新增負債 🔴"):
            if new_lia_name:
                st.session_state.liabilities[new_lia_name] = new_lia_val
                st.success(f"已新增負債：{new_lia_name}")
                st.rerun()
