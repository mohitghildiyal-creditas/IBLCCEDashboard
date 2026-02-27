import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="IBL Credit Card Activation",
    layout="wide"
)

# ================= GLOBAL STYLE =================
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
.section-title {
    font-size: 20px;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 12px;
    letter-spacing: 0.3px;
}
.filter-label {
    font-size: 13px;
    font-weight: 600;
    color: #444;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
div[data-testid="stDataFrame"] {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div style="padding:10px 0 20px 0; border-bottom: 2px solid #f0f0f0; margin-bottom: 24px;">
    <h1 style="margin-bottom:2px; color:#1a1a2e; font-size:28px; font-weight:800;">
        IBL Credit Card Activation
    </h1>
    <p style="color:#888; margin-top:4px; font-size:14px;">
        Centralized Analytics & Performance Monitoring
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SECTION 1 : MONTHLY ACTIVATION SUMMARY
# ============================================================

st.markdown('<div class="section-title">Monthly Activation Summary</div>', unsafe_allow_html=True)

data = {
    "Month": ["Jul'25", "Aug'25", "Sep'25", "Nov'25", "Dec'25"],
    "Sourced": [65622, 60691, 45932, 45257, 33801],
    "Activated": [59243, 55731, 37846, 41670, 30805],
}

df_summary = pd.DataFrame(data)
df_summary["Activated %"] = round(
    (df_summary["Activated"] / df_summary["Sourced"]) * 100, 2
)

col1, col2 = st.columns([1, 1.6])

with col1:
    st.markdown("""
    <style>
    div[data-testid="stDataFrame"] table {
        font-size: 14px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Style the dataframe
    styled = df_summary.style\
        .format({"Sourced": "{:,.0f}", "Activated": "{:,.0f}", "Activated %": "{:.2f}%"})\
        .set_properties(**{
            "text-align": "center",
            "font-size": "14px",
        })\
        .set_table_styles([
            {"selector": "th", "props": [
                ("background-color", "#1a1a2e"),
                ("color", "white"),
                ("font-weight", "700"),
                ("text-align", "center"),
                ("padding", "10px 14px"),
                ("font-size", "13px"),
                ("letter-spacing", "0.4px"),
            ]},
            {"selector": "td", "props": [
                ("padding", "9px 14px"),
                ("border-bottom", "1px solid #f0f0f0"),
            ]},
            {"selector": "tr:hover td", "props": [
                ("background-color", "#f7f9fc"),
            ]},
        ])\
        .hide(axis="index")

    st.dataframe(styled, width="stretch", hide_index=True, height=245)

with col2:
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_summary["Month"],
        y=df_summary["Sourced"],
        name="Sourced",
        marker_color="#2563EB",
        marker_line_width=0,
        text=df_summary["Sourced"].apply(lambda x: f"{x:,.0f}"),
        textposition="outside",
        textfont=dict(size=11, color="#2563EB"),
    ))

    fig.add_trace(go.Bar(
        x=df_summary["Month"],
        y=df_summary["Activated"],
        name="Activated",
        marker_color="#F97316",
        marker_line_width=0,
        text=df_summary["Activated"].apply(lambda x: f"{x:,.0f}"),
        textposition="outside",
        textfont=dict(size=11, color="#F97316"),
    ))

    fig.add_trace(go.Scatter(
        x=df_summary["Month"],
        y=df_summary["Activated %"],
        name="Activation %",
        mode="lines+markers+text",
        yaxis="y2",
        line=dict(color="#16a34a", width=2.5),
        marker=dict(size=7, symbol="circle", color="#16a34a"),
        text=df_summary["Activated %"].apply(lambda x: f"{x}%"),
        textposition="top center",
        textfont=dict(size=11, color="#16a34a"),
    ))

    fig.update_layout(
        barmode="group",
        height=320,
        margin=dict(l=0, r=10, t=10, b=10),
        yaxis=dict(
            title="Volume",
            title_font=dict(size=12, color="#555"),
            tickfont=dict(size=11),
            gridcolor="#f0f0f0",
        ),
        yaxis2=dict(
            title="Activation %",
            title_font=dict(size=12, color="#555"),
            tickfont=dict(size=11),
            overlaying="y",
            side="right",
            range=[85, 100],
            ticksuffix="%",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=12),
        ),
        template="simple_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter, sans-serif"),
    )

    st.plotly_chart(fig, width="stretch")

# ============================================================
# SECTION 2 : FILTERABLE DATA
# ============================================================

st.markdown("---")

csv_path = "data/dec-feb.csv"

if os.path.exists(csv_path):

    df_external = pd.read_csv(csv_path)

    # Fix: ReceivedDate < AccountOpeningDate → set equal to AccountOpeningDate
    df_external["AccountOpeningDate"] = pd.to_datetime(df_external["AccountOpeningDate"]).dt.date
    df_external["ReceivedDate"] = pd.to_datetime(df_external["ReceivedDate"]).dt.date
    mask = df_external["ReceivedDate"] < df_external["AccountOpeningDate"]
    df_external.loc[mask, "ReceivedDate"] = df_external.loc[mask, "AccountOpeningDate"]

    # Format MonthYear as readable string (202512 → Dec'25)
    def fmt_month(m):
        try:
            import datetime
            m = int(m)
            return datetime.datetime.strptime(str(m), "%Y%m").strftime("%b'%y")
        except:
            return str(m)

    df_external["MonthYearLabel"] = df_external["MonthYear"].apply(fmt_month)

    # ================= FILTERS =================
    st.markdown('<div class="section-title">Filters</div>', unsafe_allow_html=True)

    f1, f2 = st.columns([1, 2])

    with f1:
        desc_options = ["All"] + sorted(df_external["ProductDesc"].dropna().unique().tolist())
        product_filter = st.selectbox(
            "Product",
            options=desc_options,
            index=0,
            key="product_select"
        )

    with f2:
        st.markdown('<div class="filter-label">Month Year</div>', unsafe_allow_html=True)
        month_label_map = dict(zip(df_external["MonthYearLabel"], df_external["MonthYear"]))
        month_num_to_label = {v: k for k, v in month_label_map.items()}
        month_labels_sorted = sorted(df_external["MonthYearLabel"].dropna().unique().tolist())
        latest_month_label = month_num_to_label.get(df_external["MonthYear"].max())
        month_filter_labels = st.pills(
            "month_year",
            options=month_labels_sorted,
            default=[latest_month_label] if latest_month_label else None,
            selection_mode="multi",
            label_visibility="collapsed",
            key="month_pills"
        )
        month_filter = [month_label_map[l] for l in month_filter_labels] if month_filter_labels else []

    # ================= APPLY FILTERS =================
    df_filtered = df_external.copy()

    if product_filter and product_filter != "All":
        df_filtered = df_filtered[df_filtered["ProductDesc"] == product_filter]

    if month_filter:
        df_filtered = df_filtered[df_filtered["MonthYear"].isin(month_filter)]

    # ============================================================
    # DAY WISE ACTIVATION SUMMARY
    # ============================================================

    st.markdown("---")
    st.markdown('<div class="section-title" style="margin-top:8px;">Day wise Activation Summary</div>', unsafe_allow_html=True)

    # Row 1: Date view + Activation view + Count/% toggle
    c1, c2, c3 = st.columns([2, 3, 2])

    with c1:
        st.markdown('<div class="filter-label">Date View</div>', unsafe_allow_html=True)
        date_view = st.pills(
            "date_view",
            options=["Account Opening Date", "Received Date"],
            default="Account Opening Date",
            selection_mode="single",
            label_visibility="collapsed",
            key="date_view_pills"
        )

    with c2:
        st.markdown('<div class="filter-label">Activation View</div>', unsafe_allow_html=True)
        activation_view = st.pills(
            "activation_view",
            options=["Overall Activated", "Creditas Activated", "Bank Activated"],
            default="Overall Activated",
            selection_mode="single",
            label_visibility="collapsed",
            key="act_view_pills"
        )

    with c3:
        st.markdown('<div class="filter-label">Metric</div>', unsafe_allow_html=True)
        view_mode = st.pills(
            "view_mode",
            options=["Count", "Activation %"],
            default="Count",
            selection_mode="single",
            label_visibility="collapsed",
            key="view_mode_pills"
        )

    # Apply activation filter
    date_col = "AccountOpeningDate" if date_view == "Account Opening Date" else "ReceivedDate"

    if activation_view == "Creditas Activated":
        df_act = df_filtered[df_filtered["CreditasActivated"] == 1].copy()
    elif activation_view == "Bank Activated":
        df_act = df_filtered[df_filtered["BankActivated"] == 1].copy()
    else:
        df_act = df_filtered[df_filtered["OverallActivated"] == 1].copy()

    # Keep Total_CUID from full filtered set (not activation-filtered) for correct denominator
    numeric_cols_all = df_filtered.select_dtypes(include="number").columns
    df_cuid_base = (
        df_filtered
        .groupby(date_col, as_index=False)["Total_CUID"]
        .sum()
    )

    # Group activated data by selected date column
    numeric_cols = df_act.select_dtypes(include="number").columns
    df_grouped = (
        df_act
        .groupby(date_col, as_index=False)[numeric_cols]
        .sum()
        .sort_values(date_col)
    )

    # Replace Total_CUID with overall (unfiltered by activation)
    df_grouped = df_grouped.drop(columns=["Total_CUID"], errors="ignore")
    df_grouped = df_grouped.merge(df_cuid_base, on=date_col, how="left")

    # Remove unwanted columns
    columns_to_remove = [
        "CreditasActivated", "BankActivated", "OverallActivated",
        "MonthYear", "MonthYearLabel", "ProductCode", "ProductDesc",
        "ReceivedDate", "ActivationDate", "BankActivatedDate", "OverallActivatedDate",
        "AccountOpeningDate",
    ]
    # Keep the selected date column visible, remove the other one
    if date_col == "AccountOpeningDate":
        columns_to_remove = [c for c in columns_to_remove if c != "AccountOpeningDate"]
    else:
        columns_to_remove = [c for c in columns_to_remove if c != "ReceivedDate"]

    df_display = df_grouped.drop(columns=columns_to_remove, errors="ignore")

    # Reorder: date col, Total_CUID first
    priority_cols = [date_col, "Total_CUID"]
    other_cols = [c for c in df_display.columns if c not in priority_cols]
    df_display = df_display[priority_cols + other_cols]

    # Convert date column to string to avoid Arrow mixed-type error in Total row
    df_display[date_col] = df_display[date_col].astype(str)

    day_columns = [col for col in df_display.columns if col.startswith("Day")]

    # Compute raw totals before any formatting
    metric_cols = df_display.select_dtypes(include="number").columns
    raw_totals = df_display.head(100)[metric_cols].sum()

    if view_mode == "Activation %":
        df_view = df_display.copy()
        for col in day_columns:
            df_view[col] = (
                df_view[col] / df_view["Total_Activation"].replace(0, 1)
            ) * 100
        df_view[day_columns] = df_view[day_columns].round(2)
        for col in day_columns:
            df_view[col] = df_view[col].astype(str) + "%"

        total_activation_sum = raw_totals.get("Total_Activation", 1) or 1
        total_row = raw_totals.copy().astype(object)
        total_row[date_col] = "Total"
        for col in day_columns:
            pct = round((raw_totals[col] / total_activation_sum) * 100, 2)
            total_row[col] = f"{pct}%"
    else:
        df_view = df_display.copy()
        total_row = raw_totals.copy().astype(object)
        total_row[date_col] = "Total"

    df_with_total = pd.concat(
        [df_view.head(100), pd.DataFrame([total_row])],
        ignore_index=True
    )

    st.dataframe(df_with_total, width="stretch", hide_index=True)

else:
    st.error(f"CSV file not found at: `{csv_path}`\n\nPlease ensure the file exists at the specified path.")

# ============================================================
# SECTION 3 : CAMPAIGN DATA
# ============================================================

st.markdown("---")
st.markdown('<div class="section-title">Campaign Summary</div>', unsafe_allow_html=True)

camp_path = "data/IBL_CENBL_Campaign_dec_jan_feb.csv"

if os.path.exists(camp_path):

    df_camp = pd.read_csv(camp_path)

    # Parse ScheduleDate and create MonthYear label
    df_camp["ScheduleDate"] = pd.to_datetime(df_camp["ScheduleDate"])
    df_camp["_MonthNum"] = df_camp["ScheduleDate"].dt.strftime("%Y%m").astype(int)
    df_camp["_MonthLabel"] = df_camp["ScheduleDate"].dt.strftime("%b'%y")

    # MonthYear filter — default latest month
    camp_month_map = dict(zip(df_camp["_MonthLabel"], df_camp["_MonthNum"]))
    camp_month_rev = {v: k for k, v in camp_month_map.items()}
    camp_months_sorted = sorted(df_camp["_MonthLabel"].dropna().unique().tolist())
    camp_latest_label = camp_month_rev.get(df_camp["_MonthNum"].max())

    st.markdown('<div class="filter-label">Month Year</div>', unsafe_allow_html=True)
    camp_month_sel = st.pills(
        "camp_month",
        options=camp_months_sorted,
        default=[camp_latest_label] if camp_latest_label else None,
        selection_mode="multi",
        label_visibility="collapsed",
        key="camp_month_pills"
    )
    selected_nums = [camp_month_map[l] for l in camp_month_sel] if camp_month_sel else []

    # Apply filter
    df_camp_f = df_camp.copy()
    if selected_nums:
        df_camp_f = df_camp_f[df_camp_f["_MonthNum"].isin(selected_nums)]

    # Drop noisy / internal columns
    drop_cols = ["Unnamed: 0", "TemplateContent", "LongUrl", "Category",
                 "_MonthNum", "_MonthLabel"]
    df_camp_f = df_camp_f.drop(columns=drop_cols, errors="ignore")

    # Format ScheduleDate cleanly
    df_camp_f["ScheduleDate"] = df_camp_f["ScheduleDate"].dt.strftime("%d-%b-%Y")

    # Build total row
    num_cols = df_camp_f.select_dtypes(include="number").columns.tolist()
    total_row = df_camp_f[num_cols].sum().astype(object)
    total_row["Channel"] = "Total"
    for col in df_camp_f.columns:
        if col not in num_cols and col != "Channel":
            total_row[col] = ""

    df_camp_display = pd.concat(
        [df_camp_f, pd.DataFrame([total_row])],
        ignore_index=True
    )

    st.dataframe(df_camp_display, width="stretch", hide_index=True)

else:
    st.error(f"Campaign CSV not found at: `{camp_path}`")

# ============================================================
# SECTION 4 : PRODUCT-WISE ACTIVATION SUMMARY
# ============================================================

st.markdown("---")
st.markdown('<div class="section-title">Product-wise Activation Summary</div>', unsafe_allow_html=True)

prod_csv = "data/dec-feb.csv"

if os.path.exists(prod_csv):

    df_prod = pd.read_csv(prod_csv)
    df_prod["AccountOpeningDate"] = pd.to_datetime(df_prod["AccountOpeningDate"])
    df_prod["ReceivedDate"] = pd.to_datetime(df_prod["ReceivedDate"])
    mask_p = df_prod["ReceivedDate"] < df_prod["AccountOpeningDate"]
    df_prod.loc[mask_p, "ReceivedDate"] = df_prod.loc[mask_p, "AccountOpeningDate"]

    import datetime
    def fmt_m(m):
        try:
            return datetime.datetime.strptime(str(int(m)), "%Y%m").strftime("%b'%y")
        except:
            return str(m)
    df_prod["_MonthLabel"] = df_prod["MonthYear"].apply(fmt_m)

    # Month filter — default latest
    pm_map = dict(zip(df_prod["_MonthLabel"], df_prod["MonthYear"]))
    pm_rev = {v: k for k, v in pm_map.items()}
    pm_labels = sorted(df_prod["_MonthLabel"].dropna().unique().tolist())
    pm_latest = pm_rev.get(df_prod["MonthYear"].max())

    st.markdown('<div class="filter-label">Month Year</div>', unsafe_allow_html=True)
    prod_month_sel = st.pills(
        "prod_month",
        options=pm_labels,
        default=[pm_latest] if pm_latest else None,
        selection_mode="multi",
        label_visibility="collapsed",
        key="prod_month_pills"
    )
    pm_nums = [pm_map[l] for l in prod_month_sel] if prod_month_sel else []

    df_pf = df_prod.copy()
    if pm_nums:
        df_pf = df_pf[df_pf["MonthYear"].isin(pm_nums)]

    # Aggregate per product
    grp = df_pf.groupby("ProductDesc")

    prod_summary = pd.DataFrame({
        "Product":            grp["ProductDesc"].first().index,
        "Total CUID":         grp["Total_CUID"].sum(),
        "Creditas Activated": grp.apply(lambda x: x.loc[x["CreditasActivated"]==1, "Total_Activation"].sum(), include_groups=False),
        "Bank Activated":     grp.apply(lambda x: x.loc[x["BankActivated"]==1, "Total_CUID"].sum(), include_groups=False),
        "Overall Activated":  grp.apply(lambda x: x.loc[x["OverallActivated"]==1, "Total_CUID"].sum(), include_groups=False),
    }).reset_index(drop=True)

    grand_total_cuid = prod_summary["Total CUID"].sum() or 1

    prod_summary["Allocation %"]         = (prod_summary["Total CUID"]         / grand_total_cuid * 100).round(2)
    prod_summary["Creditas Activation %"] = (prod_summary["Creditas Activated"] / prod_summary["Total CUID"].replace(0, 1) * 100).round(2)
    prod_summary["Bank Activation %"]     = (prod_summary["Bank Activated"]     / prod_summary["Total CUID"].replace(0, 1) * 100).round(2)
    prod_summary["Overall Activation %"]  = (prod_summary["Overall Activated"]  / prod_summary["Total CUID"].replace(0, 1) * 100).round(2)

    # Display columns only
    display_cols = [
        "Product", "Total CUID", "Allocation %",
        "Creditas Activated", "Creditas Activation %",
        "Bank Activated", "Bank Activation %",
        "Overall Activated", "Overall Activation %"
    ]
    prod_summary = prod_summary[display_cols].sort_values("Total CUID", ascending=False)

    # Total row
    total_prod = prod_summary.select_dtypes(include="number").sum().astype(object)
    total_prod["Product"] = "Total"
    total_prod["Allocation %"]          = 100.0
    total_prod["Creditas Activation %"] = round(prod_summary["Creditas Activated"].sum() / grand_total_cuid * 100, 2)
    total_prod["Bank Activation %"]     = round(prod_summary["Bank Activated"].sum()     / grand_total_cuid * 100, 2)
    total_prod["Overall Activation %"]  = round(prod_summary["Overall Activated"].sum()  / grand_total_cuid * 100, 2)

    df_prod_display = pd.concat(
        [prod_summary, pd.DataFrame([total_prod])],
        ignore_index=True
    )

    st.dataframe(df_prod_display, width="stretch", hide_index=True)

else:
    st.error(f"File not found: `{prod_csv}`")
