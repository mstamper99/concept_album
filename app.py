import streamlit as st
import pandas as pd
from urllib.parse import quote

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="🎧 Concept Album Explorer",
    layout="wide",
    page_icon="🎶"
)

st.title("🎧 Concept Album Explorer")
st.markdown(
"""
Discover 70 years of concept albums that turned music into storytelling.  
Filter by genre, artist, or era — then tap any title to play it instantly on YouTube Music.
---
"""
)

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    return pd.read_csv("concept_albums.csv")

df = load_data()

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("🔍 Filters")
genre = st.sidebar.selectbox("Genre", ["All"] + sorted(df["Genre"].unique()))
artist = st.sidebar.selectbox("Artist", ["All"] + sorted(df["Artist"].unique()))
era = st.sidebar.selectbox("Era", ["All"] + sorted(df["Era"].unique()))

filtered = df[
    ((df["Genre"] == genre) | (genre == "All")) &
    ((df["Artist"] == artist) | (artist == "All")) &
    ((df["Era"] == era) | (era == "All"))
].reset_index(drop=True)

st.sidebar.write(f"🎵 **{len(filtered)} albums found**")

# ---------- MAIN TABLE ----------
col1, col2 = st.columns([2, 3])

with col1:
    st.markdown("### Albums Found")
    st.dataframe(
        filtered[["Artist", "Album", "Genre", "Era"]],
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.markdown("### 🎬 Preview and Play")
    if len(filtered) > 0:
        selected = st.selectbox(
            "Choose an album to preview:",
            filtered["Album"].tolist()
        )
        row = filtered[filtered["Album"] == selected].iloc[0]
        art_url = (
            f"https://img.youtube.com/vi/"
            f"{quote(row['Artist'] + ' ' + row['Album']).replace('%20','+')}/hqdefault.jpg"
        )
        st.image(art_url, width=300, caption=f"{row['Artist']} – {row['Album']}")
        st.markdown(f"**Genre:** {row['Genre']} | **Era:** {row['Era']}")
        st.markdown(
            f"[▶ Listen on YouTube Music]({row['Link']})",
            unsafe_allow_html=True
        )
    else:
        st.info("No albums match this filter set.")

# ---------- FOOTER ----------
st.markdown("---")
st.caption(
    "Data compiled January 2026 • Built with Streamlit Cloud • Curated from Rolling Stone, Wikipedia & uDiscover Music concept‑album lists."
)