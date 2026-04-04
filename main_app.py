import streamlit as st

# Configure the main application
st.set_page_config(
    page_title="Trading Master Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS — permanently fix sidebar open, remove all toggle controls
st.markdown(
    """
    <style>
    /* ── Force sidebar to always be visible and expanded ── */
    section[data-testid="stSidebar"] {
        min-width: 280px !important;
        max-width: 320px !important;
        width: 300px !important;
        transform: none !important;
        position: relative !important;
        transition: none !important;
    }

    /* ── Hide the collapse button (« keyboard_double_arrow_left) ── */
    section[data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"] {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
    }

    /* ── Hide the expand button (» keyboard_double_arrow_right) ── */
    button[data-testid="stExpandSidebarButton"] {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
    }

    /* ── Fallback: hide any other toggle selectors ── */
    button[data-testid="stSidebarCollapseButton"],
    button[data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* ── Ensure the sidebar content container is always visible ── */
    section[data-testid="stSidebar"] > div:first-child {
        width: 100% !important;
    }

    /* ── Style the sidebar for a premium look ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #1a1a2e 50%, #16213e 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.06) !important;
    }

    /* ── Hide default Streamlit branding & Deploy button ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    button[data-testid="stBaseButton-header"] {display: none !important;}
    </style>

    <script>
    // Continuously enforce: remove collapse/expand buttons & keep sidebar open
    const fixSidebar = () => {
        // Remove collapse button inside sidebar
        const sidebar = document.querySelector('section[data-testid="stSidebar"]');
        if (sidebar) {
            sidebar.querySelectorAll('button[data-testid="stBaseButton-headerNoPadding"]').forEach(btn => {
                btn.remove();
            });
            // Force sidebar to stay visible
            sidebar.style.transform = 'none';
            sidebar.style.width = '300px';
            sidebar.style.minWidth = '280px';
            sidebar.style.position = 'relative';
        }

        // Remove expand button
        document.querySelectorAll('button[data-testid="stExpandSidebarButton"]').forEach(btn => {
            btn.remove();
        });
    };

    // Run immediately + on any DOM changes
    fixSidebar();
    const observer = new MutationObserver(fixSidebar);
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """,
    unsafe_allow_html=True
)

# Define pages for navigation
bhavcopy_page = st.Page("apps/bhavcopy.py", title="Bhavcopy Downloader", icon="📈", default=True)
excel_merger_page = st.Page("apps/excel_merger.py", title="Excel Merger", icon="📊")

# Set up the Master Sidepanel Navigation
pg = st.navigation([bhavcopy_page, excel_merger_page])

# Run the selected page
pg.run()
