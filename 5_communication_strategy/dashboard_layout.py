"""
Layout and UI component module for the HCICS Dashboard.

Module contents:
    - setup_page: Configures Streamlit page settings and injects global CSS.
    - render_header: Creates the custom HTML branded header.
    - render_sidebar: Builds the navigation sidebar with metrics and findings.
    - render_footer: Creates the professional HTML footer.
    - create_anchor: Helper function for creating navigation anchor points.

Handles the visual styling, CSS injection, and structural HTML components
to ensure a professional and responsive user interface.

Created on 05-11-25
@author: Abdulrahman Sirelkhatim
"""

import streamlit as st
import streamlit.components.v1 as components
from config import load_logo

LOGO_PIL, LOGO_BASE64_URI = load_logo()
LOGO_FALLBACK_TEXT = "HCICS"


def setup_page():
    """
    Initializes the Streamlit page configuration and global styles.

    Steps:
        1. Sets page metadata (title, icon, layout) via `st.set_page_config`.
        2. Injects custom CSS to override Streamlit defaults for:
            - Sidebar styling and transitions.
            - Metric box styling.
            - Button gradients and hover effects.
            - Typography and section headers.
        3. Initializes session state for navigation tracking.
    """
    st.set_page_config(
        page_title="HCICS Dashboard | Sudan IDP Crisis Analysis",
        page_icon="assets/logo.png",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            "Get Help": "https://github.com/yourusername/hcics",
            "Report a bug": "https://github.com/yourusername/hcics/issues",
            "About": """
            **Humanitarian Crisis Intelligence & Communication System**

            Geospatial analysis of IDP vulnerability in Sudan.
            Developed for MIT Emerging Talent Program.
            """,
        },
    )

    st.markdown(
        """
    <style>
    * {
        font-family: 'Inter', Arial, sans-serif;
    }

    .main {
    background: linear-gradient(135deg,
        #f8fafc 0%,
        #e0e7ff 25%,
        #dbeafe 50%,
        #e0e7ff 75%,
        #f8fafc 100%);
    min-height: 100vh;
    }

    [data-testid="stSidebar"] {
        background: #1f2937;
        padding-top: 2rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border-right: 4px solid #3b82f6;
    }

    [data-testid="stSidebar"] * {
        color: #e5e7eb !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #f9fafb !important;
        border-bottom: 1px solid rgba(59, 130, 246, 0.2);
        padding-bottom: 0.5rem;
        margin-bottom: 1rem !important;
    }

    .nav-link {
        display: block;
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        color: #e5e7eb !important;
        text-decoration: none !important;
        border-radius: 8px;
        transition: all 0.3s ease;
        border-left: 4px solid transparent;
        font-weight: 500;
    }

    .nav-link:hover {
        background: rgba(59, 130, 246, 0.15);
        border-left-color: #3b82f6;
        transform: translateX(5px);
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
        text-decoration: none !important;
    }

    [data-testid="stSidebar"] [data-testid="stImage"] {
        display: flex;
        justify-content: center;
    }
    [data-testid="stSidebar"] [data-testid="stImage"] > div {
        margin: 0 auto;
    }

    .sidebar-metric-box {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(96, 165, 250, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.75rem 0;
        transition: all 0.3s ease;
        cursor: default;
    }
    .sidebar-metric-box:hover {
        background: rgba(59, 130, 246, 0.2) !important;
        transform: translateX(5px) !important;
        border-color: rgba(96, 165, 250, 0.5) !important;
    }
    .sidebar-metric-label {
        color: #94a3b8;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }
    .sidebar-metric-value {
        color: #60a5fa;
        font-size: 1.75rem;
        font-weight: 700;
    }
    .sidebar-metric-help {
        color: #cbd5e1;
        font-size: 0.75rem;
        margin-top: 0.25rem;
    }

    .sidebar-findings-box {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
        border: 1px solid rgba(96, 165, 250, 0.4);
        border-radius: 12px;
        padding: 1.25rem;
        margin: 1rem 0;
    }
    .sidebar-finding-item {
        color: #e2e8f0;
        font-size: 0.95rem;
        line-height: 1.8;
        margin-bottom: 0.75rem;
    }

    .section-header {
        color: #1e3a8a;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #3b82f6;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e40af;
    }

    .stAlert {
        border-radius: 8px;
        border-left-width: 4px;
    }

    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.25rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4) !important;
    }

    .stDownloadButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
    }

    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 50%, #db2777 100%) !important;
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6) !important;
    }

    .stButton > button:active,
    .stDownloadButton > button:active {
        transform: translateY(0) scale(0.98) !important;
    }

    .streamlit-expanderHeader {
        font-weight: 600;
        color: #1e40af;
    }

    .element-container {
        animation: fadeInUp 0.6s ease-out;
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .anchor {
        display: block;
        height: 80px;
        margin-top: -80px;
        visibility: hidden;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    if "current_section" not in st.session_state:
        st.session_state.current_section = "home"


def render_header():
    """
    Render professional dashboard header with logo and branding using custom HTML.
    """
    logo_src = LOGO_BASE64_URI if LOGO_BASE64_URI else ""
    HEADER_LOGO_SIZE = 90

    logo_content = (
        f'<img src="{logo_src}" alt="Project Logo" class="header-logo">'
        if logo_src
        else f'<div class="header-logo header-logo-fallback">{LOGO_FALLBACK_TEXT}</div>'
    )

    components.html(
        f"""
    <style>
        * {{
            box-sizing: border-box;
        }}

        .header-container {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border-radius: 16px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            padding: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1.5rem;
            border-bottom: 4px solid #3b82f6;
            margin-bottom: 2rem;
        }}

        .header-logo {{
            width: {HEADER_LOGO_SIZE}px;
            height: {HEADER_LOGO_SIZE}px;
            border-radius: 50%;
            object-fit: cover;
            background: white;
            flex-shrink: 0;
            box-shadow: 0 4px 10px rgba(59, 130, 246, 0.5);
        }}

        .header-logo-fallback {{
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #3b82f6;
            color: white;
            font-size: 1.5rem;
            font-weight: bold;
        }}

        .header-content {{
            flex: 1;
            min-width: 0;
            overflow: visible;
        }}

        .header-title {{
            color: #1e40af;
            margin: 0 0 0.25rem 0;
            font-size: 2.2rem;
            font-weight: 700;
            line-height: 1.2;
        }}

        .header-subtitle {{
            color: #475569;
            font-size: 1.1rem;
            margin: 0 0 0.5rem 0;
            font-weight: 500;
            line-height: 1.3;
        }}

        .header-meta {{
            color: #64748b;
            font-size: 0.9rem;
            margin: 0;
            line-height: 1.5;
            display: block;
        }}

        /* Mobile Responsive Styles */
        @media (max-width: 768px) {{
            .header-container {{
                flex-direction: column;
                text-align: center;
                padding: 1.25rem;
                gap: 1rem;
            }}

            .header-logo {{
                width: 70px;
                height: 70px;
            }}

            .header-content {{
                width: 100%;
            }}

            .header-title {{
                font-size: 1.5rem;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }}

            .header-subtitle {{
                font-size: 0.95rem;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }}

            .header-meta {{
                font-size: 0.8rem;
                word-wrap: break-word;
                overflow-wrap: break-word;
                white-space: normal;
            }}
        }}

        @media (max-width: 480px) {{
            .header-container {{
                padding: 1rem 0.75rem;
            }}

            .header-title {{
                font-size: 1.3rem;
            }}

            .header-subtitle {{
                font-size: 0.85rem;
            }}

            .header-meta {{
                font-size: 0.75rem;
                line-height: 1.6;
            }}

            .header-logo {{
                width: 60px;
                height: 60px;
            }}
        }}
    </style>

    <div class="header-container">
        {logo_content}

        <div class="header-content">
            <h1 class="header-title">HCICS Dashboard</h1>
            <p class="header-subtitle">
                Humanitarian Crisis Intelligence & Communication System
            </p>
            <p class="header-meta">
                🔍 Geospatial Analysis · 🇸🇩 Sudan IDP Crisis · 🎓 MIT Emerging Talent
            </p>
        </div>
    </div>
    """,
        height=230,
    )


def render_sidebar():
    """
    Constructs the sidebar navigation and summary section.

    Steps:
        1. Displays the logo and project title.
        2. Generates navigation links using HTML anchors.
        3. Renders specific metric boxes for quick stats (Localities, IDPs, Facilities).
        4. Displays a "Key Findings" box with bulleted insights.
        5. Adds credits and attribution footer to the sidebar.
    """
    LOGO_SIZE = 150

    with st.sidebar:
        st.markdown(
            """
        <div style="text-align: center; margin-bottom: 1.5rem; display: flex; flex-direction: column; align-items: center;">
        """,
            unsafe_allow_html=True,
        )
        if LOGO_PIL:
            st.image(LOGO_PIL, width=LOGO_SIZE)
        else:
            st.markdown(
                f"""
            <img src="https://placehold.co/{LOGO_SIZE}x{LOGO_SIZE}/3b82f6/ffffff?text={LOGO_FALLBACK_TEXT}" alt="Logo"
                 style="width: {LOGO_SIZE}px; height: {LOGO_SIZE}px; border-radius: 10px; margin-bottom: 0.5rem; border: 2px solid white;">
            """,
                unsafe_allow_html=True,
            )
        st.markdown("### 📍 Quick Navigation")

        nav_sections = [
            ("Overview", "#overview"),
            ("Key Indicators", "#key-indicators"),
            ("Vulnerability Map", "#vulnerability-map"),
            ("Top 5 Localities", "#top-5-localities"),
            ("Vulnerability Drivers", "#vulnerability-drivers"),
            ("Regional Comparison", "#regional-comparison"),
            ("Statistical Validation", "#statistical-validation"),
            ("Methodology", "#methodology"),
            ("Downloads", "#downloads"),
        ]

        for label, anchor in nav_sections:
            st.markdown(
                f'<a href="{anchor}" class="nav-link">{label}</a>',
                unsafe_allow_html=True,
            )

        st.markdown("### 📊 Dashboard Stats")

        metrics = [
            ("Localities Analyzed", "181", "Total localities in assessment"),
            ("Total IDPs", "6.55M", "Internally displaced persons"),
            ("Health Facilities", "1,126", "Mapped facilities"),
            ("Critical Facilities", "238", "Hospitals and clinics"),
        ]

        for label, value, help_text in metrics:
            st.markdown(
                f"""
                <div class='sidebar-metric-box'>
                    <div class='sidebar-metric-label'>{label}</div>
                    <div class='sidebar-metric-value'>{value}</div>
                    <div class='sidebar-metric-help'>{help_text}</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        st.markdown("### 🔍 Key Findings")

        st.markdown(
            """
        <div class='sidebar-findings-box'>
            <div class='sidebar-finding-item'>
                <strong style='color: #60a5fa;'>•</strong> 86% of localities exceed 20km hospital access
            </div>
            <div class='sidebar-finding-item'>
                <strong style='color: #60a5fa;'>•</strong> River Nile dominates top 5 vulnerable localities
            </div>
            <div class='sidebar-finding-item'>
                <strong style='color: #60a5fa;'>•</strong> Mean distance: 88.1km (17.6× WHO max)
            </div>
            <div class='sidebar-finding-item'>
                <strong style='color: #60a5fa;'>•</strong> Darfur paradox: Lower vulnerability vs non-Darfur
            </div>
            <div class='sidebar-finding-item'>
                <strong style='color: #60a5fa;'>•</strong> 94.6% ML accuracy validates methodology
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div style="text-align: center; font-size: 0.85rem; color: #cbd5e1; margin-top: 2rem;">
            <p style="margin-bottom: 0.5rem;">
                <strong>🎓 MIT Emerging Talent</strong><br>
                Capstone Project 2025
            </p>
            <p style="margin-bottom: 0.5rem;">
                <strong>Developer:</strong><br>
                Abdulrahman Sirelkhatim
            </p>
            <p style="font-size: 0.75rem; color: #94a3b8;">
                Open Source · Humanitarian Use
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )


def render_footer():
    """
    Renders the application footer with credits and licensing info.

    Steps:
        1. Constructs a comprehensive HTML footer container.
        2. Includes data source citations (IOM DTM, OSM, OCHA).
        3. Displays project credits (MIT Emerging Talent).
        4. Styles with a distinct dark gradient background.
    """
    logo_src = LOGO_BASE64_URI if LOGO_BASE64_URI else ""
    logo_content = (
        f'<img src="{logo_src}" alt="Project Logo" class="footer-logo">'
        if logo_src
        else f'<div class="footer-logo footer-logo-fallback">{LOGO_FALLBACK_TEXT}</div>'
    )

    components.html(
        f"""
    <style>
        .footer-container {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            padding: 2.5rem 1.5rem;
            margin-top: 3rem;
            border-radius: 20px 20px 0 0;
            text-align: center;
            color: white;
        }}

        .footer-logo {{
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid white;
            margin: 0 auto 1rem;
            display: block;
        }}

        .footer-logo-fallback {{
            background-color: white;
            color: #1e3a8a;
            font-size: 1.25rem;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .footer-title {{
            margin: 0 0 0.5rem 0;
            font-size: 1.5rem;
            font-weight: 600;
            line-height: 1.3;
        }}

        .footer-description {{
            opacity: 0.9;
            margin-bottom: 1.5rem;
            font-size: 1rem;
            line-height: 1.4;
        }}

        .footer-data-sources {{
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            display: inline-block;
            margin-bottom: 1rem;
            font-size: 0.95rem;
        }}

        .footer-badge {{
            background: rgba(251, 191, 36, 0.3);
            border: 1px solid rgba(251, 191, 36, 0.5);
            border-radius: 20px;
            padding: 0.5rem 1.25rem;
            color: #fcd34d;
            display: inline-block;
            margin-bottom: 1rem;
            font-size: 0.9rem;
        }}

        .footer-developer {{
            margin: 1rem 0;
            font-size: 1rem;
        }}

        .footer-copyright {{
            font-size: 0.85rem;
            opacity: 0.7;
            margin-top: 1.5rem;
        }}

        @media (max-width: 768px) {{
            .footer-container {{
                padding: 2rem 1rem;
            }}

            .footer-title {{
                font-size: 1.2rem;
                padding: 0 0.5rem;
            }}

            .footer-description {{
                font-size: 0.9rem;
                padding: 0 0.5rem;
            }}

            .footer-data-sources,
            .footer-badge {{
                font-size: 0.85rem;
                padding: 0.6rem 1rem;
                margin: 0.5rem 0.25rem;
                display: block;
                max-width: 90%;
                margin-left: auto;
                margin-right: auto;
            }}

            .footer-developer {{
                font-size: 0.9rem;
            }}

            .footer-logo {{
                width: 50px;
                height: 50px;
            }}
        }}

        @media (max-width: 480px) {{
            .footer-container {{
                padding: 1.5rem 0.75rem;
            }}

            .footer-title {{
                font-size: 1rem;
                line-height: 1.4;
            }}

            .footer-description {{
                font-size: 0.85rem;
            }}

            .footer-data-sources,
            .footer-badge {{
                font-size: 0.8rem;
                padding: 0.5rem 0.75rem;
            }}

            .footer-developer {{
                font-size: 0.85rem;
            }}

            .footer-copyright {{
                font-size: 0.75rem;
            }}
        }}
    </style>

    <div class="footer-container">
        {logo_content}

        <h3 class="footer-title">
            Humanitarian Crisis Intelligence & Communication System
        </h3>

        <p class="footer-description">
            Data-driven insights for humanitarian response in Sudan
        </p>

        <div class="footer-data-sources">
            📊 <strong>Data Sources:</strong> IOM DTM · HOT OSM · OCHA COD-AB
        </div>

        <div class="footer-badge">
            🎓 MIT Emerging Talent · Capstone Project 2025
        </div>

        <p class="footer-developer">
            <strong>Developed by:</strong> Abdulrahman Sirelkhatim
        </p>

        <p class="footer-copyright">
            © 2025 All Rights Reserved
        </p>
    </div>
    """,
        height=500,
    )


def create_anchor(anchor_id: str):
    """
    Creates an invisible HTML anchor for internal page navigation.

    Steps:
        1. Generates an empty HTML div with the specified ID.
        2. Adjusts negative margin to account for fixed headers (if any).
        3. Injects the HTML to allow sidebar links to jump to this section.

    Args:
        anchor_id (str): The unique identifier for the HTML element.
    """
    st.markdown(f'<div class="anchor" id="{anchor_id}"></div>', unsafe_allow_html=True)
