"""
The Composers: A Duet of Names — Streamlit wrapper.

The whole experience is a static site: flow.html stitches 7 sheets (cover, score,
orchestra, aria, cormac, quiz) via iframes, fetches lookup.json, and plays
audio from assets/. Streamlit's static file server exposes ./static as real files
at /app/static/<path>, so we embed flow.html in a single full-viewport iframe.

Sizing note (the subtle part): each sheet inside flow.html is `height:100vh`. When
flow.html is nested inside Streamlit's component iframe, `100vh` resolves against
THAT iframe's height, not the browser window. So the wrapper must be exactly one
browser-viewport tall and scroll internally; then every sheet == one real screen,
exactly like `python -m http.server`. We pin the component iframe to 100vh with CSS.
"""
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="The Composers · A Duet of Names",
    page_icon="🎼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Strip Streamlit chrome/padding AND force the component iframe to fill the viewport,
# so flow.html's 100vh sheets map to one real screen each.
st.markdown(
    """
    <style>
      #MainMenu, header, footer {visibility: hidden;}
      [data-testid="stHeader"] {display: none;}
      .block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
      [data-testid="stAppViewContainer"] > .main {padding: 0 !important;}
      [data-testid="stAppViewContainer"], [data-testid="stMain"] {overflow: hidden !important;}
      div[data-testid="stVerticalBlock"] {gap: 0 !important;}
      /* the component's own iframe: make it the full viewport */
      [data-testid="stIFrame"], iframe[title="streamlit_component"], .element-container iframe {
        height: 100vh !important;
        width: 100% !important;
        border: 0 !important;
        display: block !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# The inner iframe fills its parent (the component iframe, now 100vh). flow.html
# scrolls internally; scrolling stays on so the reader can move sheet to sheet and
# so the encore's picked state can scroll into view on short viewports.
components.html(
    """
    <style>html,body{margin:0;padding:0;height:100%;overflow:hidden;}</style>
    <iframe src="./app/static/flow.html"
            style="width:100%;height:100vh;border:0;display:block;"
            allow="autoplay" scrolling="yes"></iframe>
    """,
    height=900,          # initial hint; CSS above stretches the frame to 100vh
    scrolling=False,     # inner flow.html owns the scroll
)
