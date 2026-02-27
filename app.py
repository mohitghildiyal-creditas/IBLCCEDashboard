import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import datetime

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="IBL Credit Card Activation",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= DESIGN TOKENS (McKinsey × UIEngine) =================
C_NAVY      = "#051C2C"   # McKinsey deep navy
C_BLUE      = "#0065BD"   # McKinsey primary blue
C_SKY       = "#00A3E0"   # UIEngine sky accent
C_BG        = "#F4F6F9"   # UIEngine page background
C_SURFACE   = "#FFFFFF"
C_BORDER    = "#DDE1E7"
C_TEXT      = "#1A1A2E"
C_MUTED     = "#6B7280"
C_GREEN     = "#00875A"
C_AMBER     = "#F59E0B"
C_RED       = "#DC2626"

# ================= GLOBAL CSS =================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background-color: {C_BG};
}}

.block-container {{
    padding-top: 0 !important;
    padding-bottom: 2rem;
    max-width: 100% !important;
}}

/* ---- TOP HEADER BAR ---- */
.dash-header {{
    background: {C_NAVY};
    padding: 18px 40px;
    margin: -1rem -1rem 0 -1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}
.dash-header h1 {{
    color: white;
    font-size: 20px;
    font-weight: 700;
    margin: 0;
    letter-spacing: 0.3px;
}}
.dash-header .sub {{
    color: rgba(255,255,255,0.55);
    font-size: 12px;
    margin-top: 3px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}}
.dash-header .user-badge {{
    background: rgba(255,255,255,0.12);
    color: white;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
}}

/* ---- SECTION DIVIDER ---- */
.section-block {{
    background: {C_SURFACE};
    border: 1px solid {C_BORDER};
    border-radius: 4px;
    padding: 24px 28px;
    margin-bottom: 20px;
}}

/* ---- SECTION TITLE ---- */
.section-title {{
    font-size: 13px;
    font-weight: 700;
    color: {C_NAVY};
    text-transform: uppercase;
    letter-spacing: 1.2px;
    padding-bottom: 10px;
    border-bottom: 2px solid {C_BLUE};
    margin-bottom: 18px;
    display: inline-block;
}}

/* ---- FILTER LABEL ---- */
.filter-label {{
    font-size: 11px;
    font-weight: 600;
    color: {C_MUTED};
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
}}

/* ---- KPI CARD ---- */
.kpi-card {{
    background: {C_SURFACE};
    border: 1px solid {C_BORDER};
    border-top: 3px solid {C_BLUE};
    border-radius: 4px;
    padding: 18px 20px;
    text-align: left;
}}
.kpi-label {{
    font-size: 11px;
    font-weight: 600;
    color: {C_MUTED};
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
}}
.kpi-value {{
    font-size: 28px;
    font-weight: 800;
    color: {C_NAVY};
    line-height: 1;
}}
.kpi-sub {{
    font-size: 12px;
    color: {C_MUTED};
    margin-top: 4px;
}}

/* ---- LOGIN PAGE ---- */
.login-page-bg {{
    position: fixed;
    inset: 0;
    background: linear-gradient(135deg, {C_NAVY} 0%, #0a2d4a 50%, #0d3a5c 100%);
    z-index: -1;
}}
.login-card {{
    background: {C_SURFACE};
    border-radius: 6px;
    padding: 52px 48px 44px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.35), 0 4px 16px rgba(0,0,0,0.15);
}}
.login-brand {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 32px;
}}
.login-brand-dot {{
    width: 10px;
    height: 10px;
    background: {C_SKY};
    border-radius: 50%;
}}
.login-brand-name {{
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    color: {C_MUTED};
    text-transform: uppercase;
}}
.login-title {{
    font-size: 26px;
    font-weight: 800;
    color: {C_NAVY};
    margin-bottom: 6px;
    line-height: 1.2;
}}
.login-sub {{
    font-size: 13px;
    color: {C_MUTED};
    margin-bottom: 32px;
    line-height: 1.5;
}}
.login-divider {{
    height: 1px;
    background: {C_BORDER};
    margin: 28px 0;
}}
.login-footer {{
    font-size: 11px;
    color: {C_MUTED};
    text-align: center;
    margin-top: 20px;
    letter-spacing: 0.3px;
}}

div[data-testid="stDataFrame"] {{
    border: 1px solid {C_BORDER};
    border-radius: 4px;
    overflow: hidden;
}}

/* hide streamlit branding */
#MainMenu, footer, header {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)


# ================================================================
# AUTH
# ================================================================
USERS = {"admin": "admin@7860"}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

def login_page():
    # Full-page dark background
    st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(135deg, {C_NAVY} 0%, #0a2d4a 50%, #0d3a5c 100%) !important; }}
    .block-container {{ padding-top: 0 !important; }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)

    col = st.columns([1, 1.1, 1])[1]
    with col:
        st.markdown(f"""
        <div class="login-card">
            <div class="login-brand">
                <div class="login-brand-dot"></div>
                <div class="login-brand-name">IndusInd Bank &nbsp;·&nbsp; Creditas</div>
            </div>
            <div class="login-title">Welcome back</div>
            <div class="login-sub">Sign in to access the Credit Card<br>Activation Analytics Dashboard</div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Sign In →", use_container_width=True, type="primary")

            if submitted:
                if username in USERS and USERS[username] == password:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        st.markdown(f"""
        <div class="login-footer">
            © {datetime.date.today().year} IndusInd Bank · Confidential
        </div>
        """, unsafe_allow_html=True)


if not st.session_state.authenticated:
    login_page()
    st.stop()


# ================================================================
# HEADER BAR
# ================================================================
st.markdown(f"""
<div class="dash-header">
  <div>
    <div style="display:flex;align-items:center;gap:14px;">
      <div style="background:{C_BLUE};color:white;font-size:11px;font-weight:700;
                  letter-spacing:1px;padding:6px 10px;border-radius:2px;">IBL BANK</div>
      <div>
        <div class="dash-header" style="background:transparent;padding:0;margin:0;">
          <h1 style="color:white;font-size:18px;font-weight:700;margin:0;">
            Credit Card Activation Dashboard
          </h1>
        </div>
        <div class="sub">Performance Analytics & Monitoring</div>
      </div>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:12px;">
    <div style="color:rgba(255,255,255,0.55);font-size:12px;">
      {datetime.date.today().strftime("%d %b %Y")}
    </div>
    <div class="user-badge">&#9679; {st.session_state.username.upper()}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Logout button
with st.sidebar:
    st.markdown(f"### Signed in as **{st.session_state.username}**")
    if st.button("Sign Out", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)


# ================================================================
# HELPER: chart layout defaults
# ================================================================
CHART_LAYOUT = dict(
    template="simple_white",
    plot_bgcolor=C_SURFACE,
    paper_bgcolor=C_SURFACE,
    font=dict(family="Inter, sans-serif", color=C_TEXT, size=12),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                font=dict(size=11)),
    margin=dict(l=0, r=10, t=10, b=10),
)

TABLE_HEADER_STYLE = [
    {"selector": "th", "props": [
        ("background-color", C_NAVY), ("color", "white"),
        ("font-weight", "700"), ("text-align", "center"),
        ("padding", "10px 14px"), ("font-size", "12px"),
        ("letter-spacing", "0.5px"), ("text-transform", "uppercase"),
    ]},
    {"selector": "td", "props": [
        ("padding", "9px 14px"), ("border-bottom", f"1px solid {C_BORDER}"),
        ("font-size", "13px"),
    ]},
    {"selector": "tr:last-child td", "props": [
        ("background-color", "#EEF3FB"), ("font-weight", "700"),
    ]},
    {"selector": "tr:hover td", "props": [
        ("background-color", "#F0F7FF"),
    ]},
]


# ================================================================
# SECTION 1 : MONTHLY ACTIVATION SUMMARY
# ================================================================
st.markdown('<div class="section-title">Monthly Activation Summary</div>', unsafe_allow_html=True)

data = {
    "Month":     ["Jul'25", "Aug'25", "Sep'25", "Nov'25", "Dec'25"],
    "Sourced":   [65622, 60691, 45932, 45257, 33801],
    "Activated": [59243, 55731, 37846, 41670, 30805],
}
df_summary = pd.DataFrame(data)
df_summary["Activated %"] = round((df_summary["Activated"] / df_summary["Sourced"]) * 100, 2)

col1, col2 = st.columns([1, 1.7])

with col1:
    styled = df_summary.style\
        .format({"Sourced": "{:,.0f}", "Activated": "{:,.0f}", "Activated %": "{:.2f}%"})\
        .set_properties(**{"text-align": "center", "font-size": "13px"})\
        .set_table_styles(TABLE_HEADER_STYLE)\
        .hide(axis="index")
    st.dataframe(styled, width="stretch", hide_index=True, height=230)

with col2:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_summary["Month"], y=df_summary["Sourced"], name="Sourced",
        marker_color=C_NAVY, marker_line_width=0,
        text=df_summary["Sourced"].apply(lambda x: f"{x:,.0f}"),
        textposition="outside", textfont=dict(size=10, color=C_NAVY),
    ))
    fig.add_trace(go.Bar(
        x=df_summary["Month"], y=df_summary["Activated"], name="Activated",
        marker_color=C_BLUE, marker_line_width=0,
        text=df_summary["Activated"].apply(lambda x: f"{x:,.0f}"),
        textposition="outside", textfont=dict(size=10, color=C_BLUE),
    ))
    fig.add_trace(go.Scatter(
        x=df_summary["Month"], y=df_summary["Activated %"],
        name="Activation %", mode="lines+markers+text", yaxis="y2",
        line=dict(color=C_SKY, width=2.5),
        marker=dict(size=7, color=C_SKY),
        text=df_summary["Activated %"].apply(lambda x: f"{x}%"),
        textposition="top center", textfont=dict(size=10, color=C_SKY),
    ))
    fig.update_layout(
        barmode="group", height=300,
        yaxis=dict(title="Volume", title_font=dict(size=11), tickfont=dict(size=10), gridcolor="#F0F0F0"),
        yaxis2=dict(title="Activation %", overlaying="y", side="right",
                    range=[85, 100], ticksuffix="%", title_font=dict(size=11), tickfont=dict(size=10)),
        **CHART_LAYOUT
    )
    st.plotly_chart(fig, width="stretch")


# ================================================================
# SECTION 2 : DAY-WISE ACTIVATION SUMMARY
# ================================================================
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
st.markdown(f'<div style="height:2px;background:linear-gradient(90deg,{C_BLUE},transparent);margin-bottom:20px;"></div>', unsafe_allow_html=True)

csv_path = "data/dec-feb.csv"

if os.path.exists(csv_path):
    df_external = pd.read_csv(csv_path)
    df_external["AccountOpeningDate"] = pd.to_datetime(df_external["AccountOpeningDate"]).dt.date
    df_external["ReceivedDate"]       = pd.to_datetime(df_external["ReceivedDate"]).dt.date
    mask = df_external["ReceivedDate"] < df_external["AccountOpeningDate"]
    df_external.loc[mask, "ReceivedDate"] = df_external.loc[mask, "AccountOpeningDate"]

    def fmt_month(m):
        try:
            return datetime.datetime.strptime(str(int(m)), "%Y%m").strftime("%b'%y")
        except:
            return str(m)
    df_external["MonthYearLabel"] = df_external["MonthYear"].apply(fmt_month)

    # ---- Filters row ----
    st.markdown('<div class="section-title">Day-wise Activation Summary</div>', unsafe_allow_html=True)

    fa, fb = st.columns([1, 2])
    with fa:
        desc_options = ["All"] + sorted(df_external["ProductDesc"].dropna().unique().tolist())
        product_filter = st.selectbox("Product", options=desc_options, index=0, key="product_select")

    with fb:
        st.markdown('<div class="filter-label">Month Year</div>', unsafe_allow_html=True)
        month_label_map   = dict(zip(df_external["MonthYearLabel"], df_external["MonthYear"]))
        month_num_to_label = {v: k for k, v in month_label_map.items()}
        _my_order = df_external[["MonthYearLabel","MonthYear"]].drop_duplicates().dropna().sort_values("MonthYear")
        month_labels_sorted = _my_order["MonthYearLabel"].tolist()
        latest_month_label  = month_num_to_label.get(df_external["MonthYear"].max())
        month_filter_labels = st.pills("month_year", options=month_labels_sorted,
                                       default=[latest_month_label] if latest_month_label else None,
                                       selection_mode="multi", label_visibility="collapsed", key="month_pills")
        month_filter = [month_label_map[l] for l in month_filter_labels] if month_filter_labels else []

    df_filtered = df_external.copy()
    if product_filter != "All":
        df_filtered = df_filtered[df_filtered["ProductDesc"] == product_filter]
    if month_filter:
        df_filtered = df_filtered[df_filtered["MonthYear"].isin(month_filter)]

    # ---- Toggle row ----
    c1, c2, c3 = st.columns([2, 3, 2])
    with c1:
        st.markdown('<div class="filter-label">Date View</div>', unsafe_allow_html=True)
        date_view = st.pills("date_view", ["Account Opening Date", "Received Date"],
                             default="Account Opening Date", selection_mode="single",
                             label_visibility="collapsed", key="date_view_pills")
    with c2:
        st.markdown('<div class="filter-label">Activation View</div>', unsafe_allow_html=True)
        activation_view = st.pills("activation_view",
                                   ["Overall Activated", "Creditas Activated", "Bank Activated"],
                                   default="Overall Activated", selection_mode="single",
                                   label_visibility="collapsed", key="act_view_pills")
    with c3:
        st.markdown('<div class="filter-label">Metric</div>', unsafe_allow_html=True)
        view_mode = st.pills("view_mode", ["Count", "Activation %"],
                             default="Count", selection_mode="single",
                             label_visibility="collapsed", key="view_mode_pills")

    if activation_view == "Creditas Activated":
        df_act = df_filtered[df_filtered["CreditasActivated"] == 1].copy()
    elif activation_view == "Bank Activated":
        df_act = df_filtered[df_filtered["BankActivated"] == 1].copy()
    else:
        df_act = df_filtered[df_filtered["OverallActivated"] == 1].copy()

    day_cols_all = [c for c in df_act.columns if c.startswith("Day")]

    if date_view == "Received Date":
        date_col = "ReceivedDate"
        # Shift Day columns: Day_N from AccountOpeningDate → Day_{N-offset} from ReceivedDate
        # offset = (ReceivedDate - AccountOpeningDate).days (can be positive/negative)
        df_rd = df_act.copy()
        df_rd["_aod"] = pd.to_datetime(df_rd["AccountOpeningDate"])
        df_rd["_rcd"] = pd.to_datetime(df_rd["ReceivedDate"])
        df_rd["_offset"] = (df_rd["_rcd"] - df_rd["_aod"]).dt.days.fillna(0).astype(int)
        # Extract numeric day indices
        import re as _re
        day_idx_map = {c: int(_re.search(r'\d+', c).group()) for c in day_cols_all if _re.search(r'\d+', c)}
        # Melt to long, shift, re-pivot
        df_melt = df_rd.melt(
            id_vars=["ReceivedDate", "_offset"],
            value_vars=list(day_idx_map.keys()),
            var_name="_day_col", value_name="_cnt"
        )
        df_melt["_new_day"] = df_melt["_day_col"].map(day_idx_map) - df_melt["_offset"]
        df_melt = df_melt[df_melt["_new_day"] >= 0]
        if len(df_melt) > 0:
            df_pivot = df_melt.groupby(["ReceivedDate", "_new_day"])["_cnt"].sum().unstack("_new_day").fillna(0)
            df_pivot.columns = [f"Day{int(c)}" for c in df_pivot.columns]
            df_pivot = df_pivot.reset_index()
        else:
            df_pivot = pd.DataFrame(columns=["ReceivedDate"])
        # Add Total_CUID
        df_cuid_base = df_filtered.groupby("ReceivedDate", as_index=False)["Total_CUID"].sum()
        df_grouped = df_pivot.merge(df_cuid_base, on="ReceivedDate", how="left").sort_values("ReceivedDate")
        # Add Total_Activation
        act_grp = df_act.groupby("ReceivedDate", as_index=False)["Total_Activation"].sum()
        df_grouped = df_grouped.merge(act_grp, on="ReceivedDate", how="left")
    else:
        date_col = "AccountOpeningDate"
        df_cuid_base = df_filtered.groupby(date_col, as_index=False)["Total_CUID"].sum()
        numeric_cols = df_act.select_dtypes(include="number").columns
        df_grouped = df_act.groupby(date_col, as_index=False)[numeric_cols].sum().sort_values(date_col)
        df_grouped = df_grouped.drop(columns=["Total_CUID"], errors="ignore").merge(df_cuid_base, on=date_col, how="left")

    cols_remove = ["CreditasActivated","BankActivated","OverallActivated","MonthYear","MonthYearLabel",
                   "ProductCode","ProductDesc","ReceivedDate","ActivationDate","BankActivatedDate",
                   "OverallActivatedDate","AccountOpeningDate"]
    cols_remove = [c for c in cols_remove if c != date_col]
    df_display = df_grouped.drop(columns=cols_remove, errors="ignore")

    priority = [date_col, "Total_CUID"]
    df_display = df_display[priority + [c for c in df_display.columns if c not in priority]]
    df_display[date_col] = df_display[date_col].astype(str)

    day_columns = [c for c in df_display.columns if c.startswith("Day")]
    metric_cols = df_display.select_dtypes(include="number").columns
    raw_totals  = df_display.head(100)[metric_cols].sum()

    if view_mode == "Activation %":
        df_view = df_display.copy()
        for col in day_columns:
            df_view[col] = (df_view[col] / df_view["Total_Activation"].replace(0, 1)) * 100
        df_view[day_columns] = df_view[day_columns].round(2)
        for col in day_columns:
            df_view[col] = df_view[col].astype(str) + "%"
        denom = raw_totals.get("Total_Activation", 1) or 1
        total_row = raw_totals.copy().astype(object)
        total_row[date_col] = "Total"
        for col in day_columns:
            total_row[col] = f"{round(raw_totals[col]/denom*100,2)}%"
    else:
        df_view = df_display.copy()
        total_row = raw_totals.copy().astype(object)
        total_row[date_col] = "Total"

    df_with_total = pd.concat([df_view.head(100), pd.DataFrame([total_row])], ignore_index=True)
    st.dataframe(df_with_total, width="stretch", hide_index=True)

else:
    st.error(f"Data file not found: `{csv_path}`")


# ================================================================
# SECTION 3 : CAMPAIGN SUMMARY
# ================================================================
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
st.markdown(f'<div style="height:2px;background:linear-gradient(90deg,{C_BLUE},transparent);margin-bottom:20px;"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Campaign Summary</div>', unsafe_allow_html=True)

camp_path = "data/IBL_CENBL_Campaign_dec_jan_feb.csv"
if os.path.exists(camp_path):
    df_camp = pd.read_csv(camp_path)
    df_camp["ScheduleDate"] = pd.to_datetime(df_camp["ScheduleDate"])
    df_camp["_MonthNum"]   = df_camp["ScheduleDate"].dt.strftime("%Y%m").astype(int)
    df_camp["_MonthLabel"] = df_camp["ScheduleDate"].dt.strftime("%b'%y")

    cm_map     = dict(zip(df_camp["_MonthLabel"], df_camp["_MonthNum"]))
    cm_rev     = {v: k for k, v in cm_map.items()}
    _cm_order  = df_camp[["_MonthLabel","_MonthNum"]].drop_duplicates().dropna().sort_values("_MonthNum")
    cm_sorted  = _cm_order["_MonthLabel"].tolist()
    cm_latest  = cm_rev.get(df_camp["_MonthNum"].max())

    st.markdown('<div class="filter-label">Month Year</div>', unsafe_allow_html=True)
    camp_sel = st.pills("camp_month", cm_sorted,
                        default=[cm_latest] if cm_latest else None,
                        selection_mode="multi", label_visibility="collapsed", key="camp_month_pills")
    sel_nums = [cm_map[l] for l in camp_sel] if camp_sel else []

    df_cf = df_camp.copy()
    if sel_nums:
        df_cf = df_cf[df_cf["_MonthNum"].isin(sel_nums)]

    df_cf = df_cf.drop(columns=["Unnamed: 0","TemplateContent","LongUrl","Category","_MonthNum","_MonthLabel"], errors="ignore")
    df_cf["ScheduleDate"] = df_cf["ScheduleDate"].dt.strftime("%d-%b-%Y")

    num_cols_c  = df_cf.select_dtypes(include="number").columns.tolist()
    total_row_c = df_cf[num_cols_c].sum().astype(object)
    total_row_c["Channel"] = "Total"
    for col in df_cf.columns:
        if col not in num_cols_c and col != "Channel":
            total_row_c[col] = ""

    df_camp_display = pd.concat([df_cf, pd.DataFrame([total_row_c])], ignore_index=True)
    st.dataframe(df_camp_display, width="stretch", hide_index=True)

else:
    st.error(f"Campaign file not found: `{camp_path}`")


# ================================================================
# SECTION 4 : PRODUCT-WISE ACTIVATION SUMMARY
# ================================================================
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
st.markdown(f'<div style="height:2px;background:linear-gradient(90deg,{C_BLUE},transparent);margin-bottom:20px;"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Product-wise Activation Summary</div>', unsafe_allow_html=True)

prod_csv = "data/dec-feb.csv"
if os.path.exists(prod_csv):
    df_prod = pd.read_csv(prod_csv)
    df_prod["AccountOpeningDate"] = pd.to_datetime(df_prod["AccountOpeningDate"])
    df_prod["ReceivedDate"]       = pd.to_datetime(df_prod["ReceivedDate"])
    mp = df_prod["ReceivedDate"] < df_prod["AccountOpeningDate"]
    df_prod.loc[mp, "ReceivedDate"] = df_prod.loc[mp, "AccountOpeningDate"]
    df_prod["_MonthLabel"] = df_prod["MonthYear"].apply(fmt_month)

    pm_map    = dict(zip(df_prod["_MonthLabel"], df_prod["MonthYear"]))
    pm_rev    = {v: k for k, v in pm_map.items()}
    _pm_order = df_prod[["_MonthLabel","MonthYear"]].drop_duplicates().dropna().sort_values("MonthYear")
    pm_labels = _pm_order["_MonthLabel"].tolist()
    pm_latest = pm_rev.get(df_prod["MonthYear"].max())

    st.markdown('<div class="filter-label">Month Year</div>', unsafe_allow_html=True)
    prod_sel = st.pills("prod_month", pm_labels,
                        default=[pm_latest] if pm_latest else None,
                        selection_mode="multi", label_visibility="collapsed", key="prod_month_pills")
    pm_nums = [pm_map[l] for l in prod_sel] if prod_sel else []

    df_pf = df_prod.copy()
    if pm_nums:
        df_pf = df_pf[df_pf["MonthYear"].isin(pm_nums)]

    grp = df_pf.groupby("ProductDesc")
    prod_summary = pd.DataFrame({
        "Product":            grp["ProductDesc"].first().index,
        "Total CUID":         grp["Total_CUID"].sum(),
        "Creditas Activated": grp.apply(lambda x: x.loc[x["CreditasActivated"]==1,"Total_Activation"].sum(), include_groups=False),
        "Bank Activated":     grp.apply(lambda x: x.loc[x["BankActivated"]==1,"Total_CUID"].sum(), include_groups=False),
        "Overall Activated":  grp.apply(lambda x: x.loc[x["OverallActivated"]==1,"Total_CUID"].sum(), include_groups=False),
    }).reset_index(drop=True)

    gc = prod_summary["Total CUID"].sum() or 1
    prod_summary["Allocation %"]          = (prod_summary["Total CUID"]         / gc * 100).round(2)
    prod_summary["Creditas Activation %"] = (prod_summary["Creditas Activated"] / prod_summary["Total CUID"].replace(0,1) * 100).round(2)
    prod_summary["Bank Activation %"]     = (prod_summary["Bank Activated"]     / prod_summary["Total CUID"].replace(0,1) * 100).round(2)
    prod_summary["Overall Activation %"]  = (prod_summary["Overall Activated"]  / prod_summary["Total CUID"].replace(0,1) * 100).round(2)

    display_cols = ["Product","Total CUID","Allocation %",
                    "Creditas Activated","Creditas Activation %",
                    "Bank Activated","Bank Activation %",
                    "Overall Activated","Overall Activation %"]
    prod_summary = prod_summary[display_cols].sort_values("Total CUID", ascending=False)

    total_p = prod_summary.select_dtypes(include="number").sum().astype(object)
    total_p["Product"]               = "Total"
    total_p["Allocation %"]          = 100.0
    total_p["Creditas Activation %"] = round(prod_summary["Creditas Activated"].sum() / gc * 100, 2)
    total_p["Bank Activation %"]     = round(prod_summary["Bank Activated"].sum()     / gc * 100, 2)
    total_p["Overall Activation %"]  = round(prod_summary["Overall Activated"].sum()  / gc * 100, 2)

    df_prod_display = pd.concat([prod_summary, pd.DataFrame([total_p])], ignore_index=True)

    styled_prod = df_prod_display.style\
        .format({
            "Total CUID": "{:,.0f}",
            "Allocation %": "{:.2f}%",
            "Creditas Activated": "{:,.0f}", "Creditas Activation %": "{:.2f}%",
            "Bank Activated": "{:,.0f}",     "Bank Activation %": "{:.2f}%",
            "Overall Activated": "{:,.0f}",  "Overall Activation %": "{:.2f}%",
        }, na_rep="")\
        .set_table_styles(TABLE_HEADER_STYLE)\
        .hide(axis="index")

    st.dataframe(styled_prod, width="stretch", hide_index=True)

else:
    st.error(f"File not found: `{prod_csv}`")

# ---- Footer ----
st.markdown(f"""
<div style="margin-top:40px;padding:16px 0;border-top:1px solid {C_BORDER};
            text-align:center;color:{C_MUTED};font-size:11px;letter-spacing:0.5px;">
    IBL BANK · Credit Card Activation Dashboard · Confidential
</div>
""", unsafe_allow_html=True)
