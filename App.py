import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 設定網頁標題與寬螢幕
st.set_page_config(page_title="Finance Master 2026", page_icon="💎", layout="wide")

# ==================== 1. 初始化資料庫 ====================
# 初始化資產與負債（可於網站後台動態修改）
if "assets" not in st.session_state:
    st.session_state.assets = {"恆生銀行帳戶": 150000.0, "股票證券戶": 350000.0}
if "liabilities" not in st.session_state:
    st.session_state.liabilities = {"渣打信用卡": 12500.0, "其他負債": 200000.0}

# 完美承接你現有的預算配置 (Budget Tracker 基礎設定)
if "budget" not in st.session_state:
    st.session_state.budget = {
        "飲食": 3000.0, "租金": 7700.0, "交通": 1700.0, "化妝品": 1000.0,
        "家用品": 500.0, "娛樂": 700.0, "園藝": 300.0, "電費": 1000.0,
        "貓用品": 500.0, "其他": 500.0
    }

# 初始化流水帳明細（承接你原有的欄位結構）
if "logs" not in st.session_state:
    st.session_state.logs = [
        {"日期": "2026/05/16", "分類": "飲食", "子分類": "外食", "項目": "Dinner", "金額": 79.2, "帳戶/備註": "初始紀錄"},
        {"日期": "2026/05/16", "分類": "飲食", "子分類": "食材", "項目": "面包", "金額": 69.0, "帳戶/備註": "初始紀錄"},
        {"日期": "2026/05/17", "分類": "園藝", "子分類": "花與花盆", "項目": "花同花盤", "金額": 105.0, "帳戶/備註": "初始紀錄"}
    ]

# ==================== 2. 核心財務引擎計算 ====================
# 計算資產淨值
total_assets = sum(st.session_state.assets.values())
total_liabilities = sum(st.session_state.liabilities.values())
net_worth = total_assets - total_liabilities

# 根據流水帳動態統計各分類目前的「實際已使用金額」
df_current_logs = pd.DataFrame(st.session_state.logs)
actual_spent_map = {cat: 0.0 for cat in st.session_state.budget.keys()}

if not df_current_logs.empty and "分類" in df_current_logs.columns and "金額" in df_current_logs.columns:
    # 確保金額是數字格式
    df_current_logs["金額"] = pd.to_numeric(df_current_logs["金額"], errors='coerce').fillna(0.0)
    # 計算各分類的支出總和
    for cat in actual_spent_map.keys():
        actual_spent_map[cat] = float(df_current_logs[df_current_logs["分類"] == cat]["金額"].sum())

total_actual_expense = sum(actual_spent_map.values())

# ==================== 3. 網頁儀表板主介面 ====================
st.title("💎 FINANCE TRACKER MASTER PLAN 2026")
st.caption("✨ 100% 完美相容你現有的 Excel 記帳格式系統")
st.markdown("---")

# 頂部三大看板（串聯你的真實身家）
col1, col2, col3 = st.columns(3)
col1.metric("👑 當前淨身家 (Net Worth)", f"${net_worth:,.2f}")
col2.metric("🟢 本月實際總支出", f"${total_actual_expense:,.2f}")
col3.metric("🔴 總負債庫存", f"${total_liabilities:,.2f}")
st.markdown("---")

# 建立分頁
tab_dashboard, tab_input, tab_upload, tab_settings = st.tabs([
    "📊 財務總覽 & 預算監控", 
    "💸 每日單筆記帳", 
    "📤 批量上載你既 Excel 表",
    "⚙️ 後台系統管理"
])

# -------------------- TAB 1: 財務總覽 & 預算監控（呈現 🟢🟡🔴 燈號） --------------------
with tab_dashboard:
    chart_col, budget_col = st.columns([1, 1.2])
    
    with chart_col:
        st.subheader("📊 本月支出分類比例")
        if total_actual_expense > 0:
            fig_data = pd.DataFrame(list(actual_spent_map.items()), columns=["分類", "實際支出"])
            fig_data = fig_data[fig_data["實際支出"] > 0]
            fig = px.pie(fig_data, values="實際支出", names="分類", hole=0.4, color_discrete_sequence=px.colors.sequential.Plotly3)
            fig.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("尚無支出數據，請去記帳或上載 Excel 檔案。")
            
    with budget_col:
        st.subheader("🎯 Budget Tracker 預算動態追蹤")
        
        # 建立預算狀態表格
        budget_rows = []
        for cat, b_amount in st.session_state.budget.items():
            a_amount = actual_spent_map.get(cat, 0.0)
            remaining = b_amount - a_amount
            use_rate = (a_amount / b_amount) * 100 if b_amount > 0 else 0.0
            
            # 自動判定 🟢🟡🔴 狀態燈號
            if use_rate >= 100: status_icon = "🔴 已超支"
            elif use_rate >= 80: status_icon = "🟡 預警"
            else: status_icon = "🟢 正常"
            
            budget_rows.append({
                "分類 (Category)": cat,
                "預算 (Budget)": f"${b_amount:,.1f}",
                "已使用 (Actual)": f"${a_amount:,.1f}",
                "剩餘 (Remaining)": f"${remaining:,.1f}",
                "使用率 %": f"{use_rate:.1f}%",
                "狀態": status_icon
            })
        st.dataframe(pd.DataFrame(budget_rows), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("📋 完整的收支明細歷史報表")
    if st.session_state.logs:
        df_display = pd.DataFrame(st.session_state.logs).iloc[::-1] # 最新在最前
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # 支援匯出
        csv_data = pd.DataFrame(st.session_state.logs).to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 匯出當前明細成 CSV 備份", data=csv_data, file_name="Expense_Log_Backup.csv", mime="text/csv")

# -------------------- TAB 2: 每日單筆記帳（完全符合你原有的欄位結構） --------------------
with tab_input:
    st.subheader("📥 填寫單筆日常開銷")
    with st.form("single_log_form", clear_on_submit=True):
        col_i1, col_i2, col_i3 = st.columns(3)
        with col_i1:
            in_date = st.date_input("日期", datetime.now())
            in_cat = st.selectbox("分類", list(st.session_state.budget.keys()))
        with col_i2:
            in_subcat = st.text_input("子分類（例如：外食、零食、日常交通）")
            in_title = st.text_input("項目（例如：元氣、地鐵車費）")
        with col_i3:
            in_amount = st.number_input("金額", min_value=0.0, step=1.0)
            in_acc = st.selectbox("扣款帳戶/備註", list(st.session_state.assets.keys()) + list(st.session_state.liabilities.keys()))
            
        submit_btn = st.form_submit_button("確認記入歷史帳本 🚀")
        if submit_btn and in_amount > 0:
            # 扣減資產餘額
            if in_acc in st.session_state.assets: st.session_state.assets[in_acc] -= in_amount
            elif in_acc in st.session_state.liabilities: st.session_state.liabilities[in_acc] += in_amount
            
            # 寫入
            st.session_state.logs.append({
                "日期": in_date.strftime("%Y/%m/%d"), "分類": in_cat, "子分類": in_subcat, "項目": in_title, "金額": in_amount, "帳戶/備註": in_acc
            })
            st.success(f"成功寫入一筆：{in_title} ${in_amount}")
            st.rerun()

# -------------------- TAB 3: 📤 完美讀取你現有的記帳 Excel 檔案 --------------------
with tab_upload:
    st.subheader("📤 批量上載你原有的 Excel 記帳檔案")
    st.markdown("""
    可以直接把你平常在 iPad 上使用的 **`Finance_Tracker_Master_Plan_2026 - Expense Log`** 表格直接上傳！
    你的 Excel 表格本身已經包含了正確的標題：**`日期 (Date)`**, **`分類`**, **`子分類`**, **`項目`**, **`金額`**, **`備註`**。本系統會完美自動識別！
    """)
    
    upload_file = st.file_uploader("選擇你既 Excel 或 CSV 檔案", type=["csv", "xlsx"])
    
    if upload_file is not None:
        try:
            if upload_file.name.endswith('.csv'):
                df_imported = pd.read_csv(upload_file, encoding='utf-8-sig')
            else:
                df_imported = pd.read_excel(upload_file)
                
            # 欄位自動相容對齊清洗引擎
            # 如果欄位叫 "日期 (Date)"，自動更名為 "日期"
            if "日期 (Date)" in df_imported.columns:
                df_imported = df_imported.rename(columns={"日期 (Date)": "日期"})
            if "備註" in df_imported.columns:
                df_imported = df_imported.rename(columns={"備註": "帳戶/備註"})
                
            # 確保有核心欄位
            required_cols = ["日期", "分類", "項目", "金額"]
            if not all(x in df_imported.columns for x in required_cols):
                st.error("❌ 上傳失敗！表格必須包含：『日期 (Date)』, 『分類』, 『項目』, 『金額』這四個最核心的欄位欄位名稱。")
            else:
                # 清洗金額中的貨幣符號
                df_imported["金額"] = df_imported["金額"].astype(str).str.replace('$', '').str.replace(',', '')
                df_imported["金額"] = pd.to_numeric(df_imported["金額"], errors='coerce').fillna(0.0)
                
                # 清洗空行
                df_imported = df_imported.dropna(subset=["分類", "金額"])
                df_imported = df_imported[df_imported["金額"] > 0]
                
                st.success(f"✅ 成功辨識表格！成功讀取到 {len(df_imported)} 筆記帳數據明細。下方為預覽：")
                st.dataframe(df_imported, use_container_width=True)
                
                if st.button("🔥 確定將上載數據與當前系統合併"):
                    for _, row in df_imported.iterrows():
                        st.session_state.logs.append({
                            "日期": str(row.get("日期")),
                            "分類": str(row.get("分類")),
                            "子分類": str(row.get("子分類", "未分類")),
                            "項目": str(row.get("項目", "批量匯入")),
                            "金額": float(row.get("金額", 0.0)),
                            "帳戶/備註": str(row.get("帳戶/備註", "Excel 批量匯入"))
                        })
                    st.toast("🚀 舊有數據已完美併入！預算與圖表已重新跑好！")
                    st.rerun()
        except Exception as e:
            st.error(f"讀取檔案發生錯誤，請檢查格式。錯誤提示: {e}")

# -------------------- TAB 4: 後台系統管理 --------------------
with tab_settings:
    st.subheader("⚙️ 財務後台賬戶管理")
    
    if st.button("🚨 清空目前所有記帳紀錄（重設系統）", type="primary"):
        st.session_state.logs = []
        st.rerun()
        
    st.markdown("---")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.write("#### 修改資產帳戶初始餘額")
        for k, v in list(st.session_state.assets.items()):
            st.session_state.assets[k] = st.number_input(f"【{k}】目前可用餘額 ($)", value=v, key=f"asset_{k}")
    with col_s2:
        st.write("#### 修改負債帳戶初始欠款")
        for k, v in list(st.session_state.liabilities.items()):
            st.session_state.liabilities[k] = st.number_input(f"【{k}】目前應還欠款 ($)", value=v, key=f"lia_{k}")
