"""
Master theme for Odoo Mini HR Pro v2
Odoo 18 / Zoho People inspired design system
"""

COLORS = {
    "primary":      "#714B67",
    "primary_dark": "#5a3c52",
    "primary_light":"#875A7B",
    "secondary":    "#875A7B",
    "bg":           "#F6F7FB",
    "surface":      "#FFFFFF",
    "sidebar_bg":   "#1E1128",
    "sidebar_item": "#2d1a38",
    "sidebar_hover":"#714B67",
    "success":      "#28C76F",
    "warning":      "#FF9F43",
    "danger":       "#EA5455",
    "info":         "#00CFE8",
    "text":         "#2D3748",
    "text_muted":   "#718096",
    "border":       "#E2E8F0",
    "shadow":       "rgba(113,75,103,0.10)",
}

MONTH_NAMES = [
    'يناير','فبراير','مارس','إبريل','مايو','يونيو',
    'يوليو','أغسطس','سبتمبر','أكتوبر','نوفمبر','ديسمبر'
]


def inject_global_css():
    """Inject full global CSS — call once from app.py."""
    import streamlit as st
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after {{
    font-family: 'Cairo', 'Segoe UI', Arial, sans-serif !important;
    box-sizing: border-box;
}}

html, body, .stApp {{
    direction: rtl !important;
    background: {COLORS['bg']} !important;
    color: {COLORS['text']} !important;
}}

/* ═══ HIDE STREAMLIT CHROME ═══ */
#MainMenu, footer, .stDeployButton {{visibility: hidden;}}
header[data-testid="stHeader"] {{background: transparent !important; min-height: 0; display:none;}}
[data-testid="stToolbar"] {{display:none;}}
[data-testid="stDecoration"] {{display:none;}}

/* ═══ HIDE double-arrow collapse button (all known selectors) ═══ */
[data-testid="collapsedControl"],
button[data-testid="baseButton-headerNoPadding"],
[data-testid="stSidebarCollapsedControl"],
button[aria-label="Close sidebar"],
button[aria-label="Open sidebar"],
.st-emotion-cache-1cypcdb,
button[kind="header"] {{
    display: none !important;
}}

/* ═══ SIDEBAR ═══ */
section[data-testid="stSidebar"] {{
    background: {COLORS['sidebar_bg']} !important;
    border-left: none !important;
    border-right: none !important;
    padding: 0 !important;
    width: 265px !important;
    min-width: 265px !important;
    max-width: 265px !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.3) !important;
    transition: width 0.3s ease, min-width 0.3s ease !important;
}}
section[data-testid="stSidebar"] > div:first-child {{
    padding: 0 !important;
}}
section[data-testid="stSidebar"] * {{
    color: #e2d6ea !important;
}}

/* ── Nav list ── */
section[data-testid="stSidebar"] .stRadio > div {{
    gap: 2px !important;
    flex-direction: column;
}}
/* Hide the radio group label ("القائمة") */
section[data-testid="stSidebar"] .stRadio > label {{
    display: none !important;
}}
section[data-testid="stSidebar"] .stRadio label {{
    display: flex !important;
    align-items: center !important;
    padding: 11px 16px !important;
    margin: 2px 8px !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    color: #b8a5c8 !important;
    transition: background 0.2s ease, color 0.2s ease, box-shadow 0.2s ease !important;
    background: transparent !important;
    gap: 10px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}}
section[data-testid="stSidebar"] .stRadio label:hover {{
    background: rgba(113,75,103,0.35) !important;
    color: #fff !important;
}}
section[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {{
    font-size: 13.5px !important;
    color: inherit !important;
    margin: 0 !important;
}}
/* Hide radio circle bullets entirely */
section[data-testid="stSidebar"] .stRadio input[type="radio"] {{
    display: none !important;
}}
section[data-testid="stSidebar"] .stRadio div[data-testid="stRadioGroup"] > label > div:first-child {{
    display: none !important;
}}
section[data-testid="stSidebar"] .stRadio div[data-baseweb="radio"] {{
    display: none !important;
}}

/* ═══ RESPONSIVE — hide sidebar on narrow screens ═══ */
@media (max-width: 768px) {{
    section[data-testid="stSidebar"] {{
        width: 0 !important;
        min-width: 0 !important;
        overflow: hidden !important;
    }}
    .main .block-container {{
        padding: 0.75rem !important;
    }}
}}

/* ═══ MAIN CONTENT ═══ */
.main .block-container {{
    padding: 1.5rem 2rem 2rem !important;
    max-width: 100% !important;
    background: {COLORS['bg']};
}}

/* ═══ BUTTONS ═══ */
.stButton > button {{
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 8px 20px !important;
    transition: all 0.2s ease !important;
    border: none !important;
}}
.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_light']} 100%) !important;
    color: #fff !important;
    box-shadow: 0 4px 15px {COLORS['shadow']} !important;
}}
.stButton > button[kind="primary"]:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px {COLORS['shadow']} !important;
    opacity: 0.92 !important;
}}
.stButton > button[kind="secondary"] {{
    background: #fff !important;
    color: {COLORS['primary']} !important;
    border: 1.5px solid {COLORS['primary']} !important;
}}
.stButton > button[kind="secondary"]:hover {{
    background: {COLORS['primary']}11 !important;
    transform: translateY(-1px) !important;
}}

/* ═══ INPUTS ═══ */
.stTextInput input, .stNumberInput input, .stTextArea textarea,
.stSelectbox select, [data-baseweb="input"] input {{
    border-radius: 8px !important;
    border: 1.5px solid {COLORS['border']} !important;
    padding: 8px 12px !important;
    background: #fff !important;
    font-size: 14px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}}
.stTextInput input:focus, .stNumberInput input:focus,
.stTextArea textarea:focus {{
    border-color: {COLORS['primary']} !important;
    box-shadow: 0 0 0 3px {COLORS['primary']}22 !important;
    outline: none !important;
}}
.stTextInput label, .stNumberInput label, .stTextArea label,
.stSelectbox label, .stDateInput label, .stMultiSelect label {{
    font-weight: 600 !important;
    font-size: 13px !important;
    color: {COLORS['text']} !important;
    margin-bottom: 4px !important;
}}
[data-baseweb="select"] {{
    border-radius: 8px !important;
}}

/* ═══ TABS ═══ */
.stTabs [data-baseweb="tab-list"] {{
    background: {COLORS['surface']} !important;
    border-radius: 12px !important;
    padding: 5px !important;
    gap: 3px !important;
    border-bottom: none !important;
    box-shadow: 0 2px 12px {COLORS['shadow']} !important;
    margin-bottom: 20px !important;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 9px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 9px 20px !important;
    color: {COLORS['text_muted']} !important;
    border: none !important;
    transition: all 0.2s !important;
}}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['primary_light']}) !important;
    color: #fff !important;
    box-shadow: 0 4px 12px {COLORS['shadow']} !important;
}}
.stTabs [data-baseweb="tab-panel"] {{
    padding: 0 !important;
}}

/* ═══ DATAFRAME ═══ */
.stDataFrame {{
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 2px 16px {COLORS['shadow']} !important;
    border: 1px solid {COLORS['border']} !important;
}}
.stDataFrame table {{
    font-size: 13px !important;
}}
.stDataFrame thead tr th {{
    background: {COLORS['primary']}10 !important;
    font-weight: 700 !important;
    color: {COLORS['primary']} !important;
}}

/* ═══ METRICS ═══ */
[data-testid="metric-container"] {{
    background: {COLORS['surface']} !important;
    border-radius: 12px !important;
    padding: 16px !important;
    border: 1px solid {COLORS['border']} !important;
    box-shadow: 0 2px 10px {COLORS['shadow']} !important;
}}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {{
    font-size: 13px !important;
    color: {COLORS['text_muted']} !important;
    font-weight: 600 !important;
}}
[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    font-size: 26px !important;
    font-weight: 800 !important;
    color: {COLORS['primary']} !important;
}}

/* ═══ ALERTS ═══ */
.stAlert {{
    border-radius: 10px !important;
    border: none !important;
    font-size: 14px !important;
}}

/* ═══ FORMS ═══ */
[data-testid="stForm"] {{
    background: {COLORS['surface']} !important;
    border-radius: 14px !important;
    padding: 24px !important;
    border: 1px solid {COLORS['border']} !important;
    box-shadow: 0 2px 12px {COLORS['shadow']} !important;
}}

/* ═══ EXPANDER ═══ */
.streamlit-expanderHeader {{
    background: {COLORS['surface']} !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    border: 1px solid {COLORS['border']} !important;
    transition: all 0.2s !important;
}}
.streamlit-expanderHeader:hover {{
    border-color: {COLORS['primary']} !important;
    background: {COLORS['primary']}08 !important;
}}

/* ═══ ANIMATIONS ═══ */
@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to   {{ opacity: 1; }}
}}
@keyframes slideInRight {{
    from {{ opacity: 0; transform: translateX(20px); }}
    to   {{ opacity: 1; transform: translateX(0); }}
}}
@keyframes pulse-glow {{
    0%, 100% {{ box-shadow: 0 0 0 0 rgba(113,75,103,0.3); }}
    50%       {{ box-shadow: 0 0 0 8px rgba(113,75,103,0); }}
}}

.fade-in-up  {{ animation: fadeInUp  0.45s ease both; }}
.fade-in     {{ animation: fadeIn    0.3s ease both; }}
.slide-in    {{ animation: slideInRight 0.4s ease both; }}

/* ═══ SCROLLBAR ═══ */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: {COLORS['bg']}; border-radius: 3px; }}
::-webkit-scrollbar-thumb {{
    background: {COLORS['primary']}55;
    border-radius: 3px;
}}
::-webkit-scrollbar-thumb:hover {{ background: {COLORS['primary']}; }}

/* ═══ COLUMN GAPS ═══ */
[data-testid="column"] {{ padding: 0 6px !important; }}

/* ═══ FILE UPLOADER ═══ */
[data-testid="stFileUploaderDropzone"] {{
    border-radius: 12px !important;
    border: 2px dashed {COLORS['primary']}55 !important;
    background: {COLORS['primary']}05 !important;
    transition: all 0.2s !important;
}}
[data-testid="stFileUploaderDropzone"]:hover {{
    border-color: {COLORS['primary']} !important;
    background: {COLORS['primary']}10 !important;
}}

/* ═══ DATE INPUT ═══ */
.stDateInput input {{
    border-radius: 8px !important;
    border: 1.5px solid {COLORS['border']} !important;
}}

/* ═══ SPINNER ═══ */
.stSpinner > div {{
    border-top-color: {COLORS['primary']} !important;
}}

/* ═══ DOWNLOAD BUTTON ═══ */
[data-testid="stDownloadButton"] > button {{
    background: linear-gradient(135deg, {COLORS['success']}, #20a55a) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}}

/* ═══ PROGRESS BAR ═══ */
.stProgress > div > div > div {{
    background: linear-gradient(90deg, {COLORS['primary']}, {COLORS['primary_light']}) !important;
    border-radius: 4px !important;
}}

/* ═══ SIDEBAR DIVIDER ═══ */
.sidebar-divider {{
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    margin: 8px 16px;
}}

/* ═══ KPI CARD HOVER ═══ */
.kpi-hover:hover {{
    transform: translateY(-4px) !important;
    box-shadow: 0 12px 35px rgba(0,0,0,0.15) !important;
}}

/* Card hover effect */
.emp-card:hover {{
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 28px {COLORS['shadow']} !important;
    border-color: {COLORS['primary']}44 !important;
}}

/* Section separator */
.section-sep {{
    height: 1px;
    background: {COLORS['border']};
    margin: 20px 0;
}}
</style>
""", unsafe_allow_html=True)
