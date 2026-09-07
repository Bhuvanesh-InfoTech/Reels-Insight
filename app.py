"""
Reel Insights — TMDB Movie Industry Analytics
Streamlit dashboard: Filters | Dashboard | Query Explorer
"""

import base64
import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DB_PATH = Path(__file__).parent / "data" / "movies.db"

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Reel Insights | TMDB Analytics",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# THEME / BACKGROUND (generated SVG film-reel pattern, no external assets)
# ----------------------------------------------------------------------------
FILM_PATTERN_SVG = """
<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'>
  <rect width='160' height='160' fill='none'/>
  <circle cx='20' cy='20' r='6' fill='%23d4af37' fill-opacity='0.05'/>
  <circle cx='100' cy='20' r='6' fill='%23d4af37' fill-opacity='0.05'/>
  <circle cx='60' cy='60' r='6' fill='%23d4af37' fill-opacity='0.05'/>
  <circle cx='140' cy='60' r='6' fill='%23d4af37' fill-opacity='0.05'/>
  <circle cx='20' cy='100' r='6' fill='%23d4af37' fill-opacity='0.05'/>
  <circle cx='100' cy='100' r='6' fill='%23d4af37' fill-opacity='0.05'/>
  <circle cx='60' cy='140' r='6' fill='%23d4af37' fill-opacity='0.05'/>
  <circle cx='140' cy='140' r='6' fill='%23d4af37' fill-opacity='0.05'/>
</svg>
"""
FILM_PATTERN_B64 = base64.b64encode(FILM_PATTERN_SVG.encode()).decode()

CUSTOM_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Manrope:wght@400;500;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'Manrope', sans-serif;
}}

/* Cinematic gradient + pattern background */
.stApp {{
    background:
        radial-gradient(circle at 15% 0%, rgba(212,175,55,0.10) 0%, transparent 45%),
        radial-gradient(circle at 85% 20%, rgba(139,0,199,0.12) 0%, transparent 45%),
        linear-gradient(180deg, #0b0e1a 0%, #12162b 45%, #0b0e1a 100%),
        url("data:image/svg+xml;base64,{FILM_PATTERN_B64}");
    background-size: cover, cover, cover, 160px 160px;
    background-attachment: fixed;
}}

/* Hero banner */
.hero-banner {{
    padding: 2.2rem 2rem;
    border-radius: 20px;
    margin-bottom: 1.6rem;
    background: linear-gradient(120deg, rgba(212,175,55,0.16), rgba(139,0,199,0.14));
    border: 1px solid rgba(212,175,55,0.25);
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
}}
.hero-title {{
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 2.4rem;
    background: linear-gradient(90deg, #f5d97a, #d4af37 40%, #b892ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}}
.hero-subtitle {{
    color: #b8bcd4;
    font-size: 1.02rem;
}}

/* Glass cards */
.glass-card {{
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 1.3rem 1.4rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.25);
    margin-bottom: 1rem;
}}

/* Metric cards */
div[data-testid="stMetric"] {{
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(212,175,55,0.22);
    border-radius: 16px;
    padding: 1rem 1rem 0.6rem 1rem;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 18px rgba(0,0,0,0.25);
}}
div[data-testid="stMetricLabel"] {{
    color: #d4af37 !important;
    font-weight: 600;
}}
div[data-testid="stMetricValue"] {{
    font-family: 'Outfit', sans-serif;
    color: #f5f5f7 !important;
}}

/* Section headers */
.section-header {{
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    font-size: 1.35rem;
    color: #f5f5f7;
    border-left: 4px solid #d4af37;
    padding-left: 0.7rem;
    margin: 1.4rem 0 0.9rem 0;
}}

/* Insight box */
.insight-box {{
    background: linear-gradient(120deg, rgba(212,175,55,0.10), rgba(139,0,199,0.08));
    border-left: 4px solid #d4af37;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    color: #e8e6f0;
    font-size: 0.97rem;
    margin-top: 0.6rem;
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0d1024 0%, #151830 100%);
    border-right: 1px solid rgba(212,175,55,0.15);
}}
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {{
    color: #d4af37 !important;
    font-family: 'Outfit', sans-serif;
}}

/* Buttons */
.stButton>button, .stDownloadButton>button {{
    background: linear-gradient(90deg, #d4af37, #b892ff);
    color: #0b0e1a;
    font-weight: 700;
    border: none;
    border-radius: 10px;
}}

/* Dataframe container */
div[data-testid="stDataFrame"] {{
    border-radius: 12px;
    overflow: hidden;
}}

#MainMenu, footer {{visibility: hidden;}}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

PLOTLY_TEMPLATE = "plotly_dark"
ACCENT_GOLD = "#d4af37"
ACCENT_PURPLE = "#b892ff"


# ----------------------------------------------------------------------------
# DATA LOADING
# ----------------------------------------------------------------------------
@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    movies = pd.read_sql("SELECT * FROM movies", conn, parse_dates=["release_date"])
    genres = pd.read_sql("SELECT * FROM genres", conn)
    movie_genres = pd.read_sql("SELECT * FROM movie_genres", conn)
    cast = pd.read_sql("SELECT * FROM cast", conn)
    crew = pd.read_sql("SELECT * FROM crew", conn)
    movie_keywords = pd.read_sql("SELECT * FROM movie_keywords", conn)
    conn.close()

    movies["budget_known"] = movies["budget_known"].astype(bool)
    movies["revenue_known"] = movies["revenue_known"].astype(bool)
    movies["release_year"] = movies["release_date"].dt.year

    mg_named = movie_genres.merge(genres, on="genre_id")
    return movies, genres, movie_genres, cast, crew, movie_keywords, mg_named


movies, genres, movie_genres, cast, crew, movie_keywords, mg_named = load_data()


@st.cache_resource
def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


conn = get_conn()

# ----------------------------------------------------------------------------
# SESSION STATE DEFAULTS
# ----------------------------------------------------------------------------
min_year, max_year = int(movies["release_year"].min()), int(movies["release_year"].max())
all_genres = sorted(genres["genre_name"].unique().tolist())
all_languages = sorted(movies["original_language"].unique().tolist())

defaults = {
    "f_genres": [],
    "f_year_range": (min_year, max_year),
    "f_min_rating": 0.0,
    "f_language": "All",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def apply_filters(df, mg_named_df):
    out = df.copy()
    if st.session_state["f_genres"]:
        movie_ids = mg_named_df[mg_named_df["genre_name"].isin(st.session_state["f_genres"])]["movie_id"].unique()
        out = out[out["movie_id"].isin(movie_ids)]
    y0, y1 = st.session_state["f_year_range"]
    out = out[(out["release_year"] >= y0) & (out["release_year"] <= y1)]
    out = out[out["vote_average"] >= st.session_state["f_min_rating"]]
    if st.session_state["f_language"] != "All":
        out = out[out["original_language"] == st.session_state["f_language"]]
    return out


filtered_movies = apply_filters(movies, mg_named)

# ----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# ----------------------------------------------------------------------------
st.sidebar.markdown("## 🎬 Reel Insights")
st.sidebar.caption("TMDB Movie Industry Analytics")
page = st.sidebar.radio(
    "Navigate",
    ["🎯 Filters", "📊 Dashboard", "🔍 Query Explorer"],
    label_visibility="collapsed",
)
st.sidebar.markdown("---")
st.sidebar.markdown(
    f"<div style='color:#9a9dbd; font-size:0.85rem;'>Live match count</div>"
    f"<div style='color:{ACCENT_GOLD}; font-family:Outfit; font-size:1.8rem; font-weight:800;'>"
    f"{len(filtered_movies):,} movies</div>",
    unsafe_allow_html=True,
)
st.sidebar.caption(f"out of {len(movies):,} total in database")

# ----------------------------------------------------------------------------
# HERO BANNER
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-title">🎬 Reel Insights</div>
        <div class="hero-subtitle">An end-to-end exploratory analysis of the global movie industry — budgets, box office, cast, and audience reception, powered by TMDB data.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================================
# PAGE 1 — FILTERS
# ============================================================================
if page == "🎯 Filters":
    st.markdown('<div class="section-header">Filter the Catalog</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="glass-card">These filters apply across the Dashboard and Query Explorer pages — set them once here.</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.session_state["f_genres"] = st.multiselect(
            "Genre(s)", options=all_genres, default=st.session_state["f_genres"]
        )
        st.session_state["f_year_range"] = st.slider(
            "Release Year Range",
            min_value=min_year,
            max_value=max_year,
            value=st.session_state["f_year_range"],
        )
    with col2:
        st.session_state["f_language"] = st.selectbox(
            "Original Language",
            options=["All"] + all_languages,
            index=(["All"] + all_languages).index(st.session_state["f_language"]),
        )
        st.session_state["f_min_rating"] = st.slider(
            "Minimum Rating", min_value=0.0, max_value=10.0,
            value=st.session_state["f_min_rating"], step=0.1,
        )

    filtered_movies = apply_filters(movies, mg_named)

    st.markdown('<div class="section-header">Live Match Count</div>', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("Movies Matching Filters", f"{len(filtered_movies):,}")
    m2.metric("Share of Full Catalog", f"{len(filtered_movies) / len(movies):.1%}")
    m3.metric("Avg Rating (filtered)", f"{filtered_movies['vote_average'].mean():.2f}" if len(filtered_movies) else "—")

    st.markdown('<div class="section-header">Preview</div>', unsafe_allow_html=True)
    st.dataframe(
        filtered_movies[["title", "release_date", "original_language", "vote_average", "revenue"]]
        .sort_values("release_date", ascending=False)
        .head(50),
        use_container_width=True,
        hide_index=True,
    )

# ============================================================================
# PAGE 2 — DASHBOARD
# ============================================================================
elif page == "📊 Dashboard":
    fm = filtered_movies

    if len(fm) == 0:
        st.warning("No movies match the current filters. Adjust filters on the Filters page.")
    else:
        fm_genre_ids = mg_named[mg_named["movie_id"].isin(fm["movie_id"])]
        fm_cast = cast[cast["movie_id"].isin(fm["movie_id"])]

        st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Movies", f"{len(fm):,}")
        k2.metric("Genres Represented", f"{fm_genre_ids['genre_name'].nunique()}")
        k3.metric("Total Actors", f"{fm_cast['actor_name'].nunique():,}")
        k4.metric("Average Rating", f"{fm['vote_average'].mean():.2f}")

        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown('<div class="section-header">Top 10 Movies by Revenue</div>', unsafe_allow_html=True)
            top_rev = fm.sort_values("revenue", ascending=False).head(10)
            fig = px.bar(
                top_rev, x="revenue", y="title", orientation="h",
                template=PLOTLY_TEMPLATE, color="revenue",
                color_continuous_scale=["#7a5c00", ACCENT_GOLD],
            )
            fig.update_layout(
                yaxis={"categoryorder": "total ascending"},
                coloraxis_showscale=False,
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            st.markdown('<div class="section-header">Genre Distribution</div>', unsafe_allow_html=True)
            genre_dist = fm_genre_ids["genre_name"].value_counts().reset_index()
            genre_dist.columns = ["genre_name", "count"]
            fig = px.pie(
                genre_dist, names="genre_name", values="count", hole=0.55,
                template=PLOTLY_TEMPLATE,
                color_discrete_sequence=px.colors.sequential.Sunsetdark,
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(font=dict(size=10)),
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="section-header">Budget vs Revenue</div>', unsafe_allow_html=True)
        fin = fm[fm["budget_known"] & fm["revenue_known"]]
        if len(fin) > 0:
            fig = px.scatter(
                fin, x="budget", y="revenue", hover_name="title",
                opacity=0.6, template=PLOTLY_TEMPLATE,
                color="vote_average", color_continuous_scale="Sunsetdark",
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No movies with known budget & revenue in this filtered selection.")

        # Auto-generated insight
        st.markdown('<div class="section-header">Auto-Generated Insight</div>', unsafe_allow_html=True)
        genre_revenue = (
            fm_genre_ids.merge(fm[["movie_id", "revenue"]], on="movie_id")
            .groupby("genre_name")["revenue"].mean().sort_values(ascending=False)
        )
        top_genre = genre_revenue.index[0] if len(genre_revenue) else "N/A"
        top_movie = fm.sort_values("revenue", ascending=False).iloc[0]
        insight_text = (
            f"In this filtered view of <b>{len(fm):,} movies</b>, the highest average-grossing genre is "
            f"<b>{top_genre}</b> (avg revenue ${genre_revenue.iloc[0]:,.0f}). "
            f"The single highest-grossing title is <b>{top_movie['title']}</b> "
            f"(${top_movie['revenue']:,.0f}), and the average audience rating across the selection "
            f"is <b>{fm['vote_average'].mean():.2f}/10</b>."
        )
        st.markdown(f'<div class="insight-box">{insight_text}</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE 3 — QUERY EXPLORER
# ============================================================================
elif page == "🔍 Query Explorer":
    st.markdown('<div class="section-header">Saved Query Explorer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="glass-card">Run any of the 10 core SQL analysis questions directly against the live database.</div>',
        unsafe_allow_html=True,
    )

    SAVED_QUERIES = {
        "Q1 — Action movies released after 2015": """
            SELECT m.title, m.release_date
            FROM movies m
            JOIN movie_genres mg ON m.movie_id = mg.movie_id
            JOIN genres g ON mg.genre_id = g.genre_id
            WHERE g.genre_name = 'Action' AND m.release_date > '2015-12-31'
            ORDER BY m.release_date
        """,
        "Q2 — Top 10 highest-grossing movies (with genres)": """
            SELECT m.title, m.revenue, GROUP_CONCAT(g.genre_name, ', ') AS genres
            FROM movies m
            JOIN movie_genres mg ON m.movie_id = mg.movie_id
            JOIN genres g ON mg.genre_id = g.genre_id
            GROUP BY m.movie_id
            ORDER BY m.revenue DESC
            LIMIT 10
        """,
        "Q3 — Average budget & revenue by genre": """
            SELECT g.genre_name,
                   ROUND(AVG(m.budget), 0) AS avg_budget,
                   ROUND(AVG(m.revenue), 0) AS avg_revenue,
                   COUNT(DISTINCT m.movie_id) AS movie_count
            FROM movies m
            JOIN movie_genres mg ON m.movie_id = mg.movie_id
            JOIN genres g ON mg.genre_id = g.genre_id
            GROUP BY g.genre_name
            ORDER BY avg_revenue DESC
        """,
        "Q4 — Top 10 actors by number of movies": """
            SELECT actor_name, COUNT(DISTINCT movie_id) AS movie_count
            FROM cast
            GROUP BY actor_name
            ORDER BY movie_count DESC
            LIMIT 10
        """,
        "Q5 — Directors with more than 3 movies": """
            SELECT person_name AS director_name, COUNT(DISTINCT movie_id) AS movie_count
            FROM crew
            WHERE job = 'Director'
            GROUP BY person_name
            HAVING COUNT(DISTINCT movie_id) > 3
            ORDER BY movie_count DESC
        """,
        "Q6 — Top 10 most frequent keywords": """
            SELECT keyword_name, COUNT(DISTINCT movie_id) AS movie_count
            FROM movie_keywords
            GROUP BY keyword_name
            ORDER BY movie_count DESC
            LIMIT 10
        """,
        "Q7 — High budget, low revenue movies": """
            SELECT title, budget, revenue
            FROM movies
            WHERE budget > (SELECT AVG(budget) FROM movies WHERE budget > 0)
              AND revenue < (SELECT AVG(revenue) FROM movies WHERE revenue > 0)
              AND budget > 0 AND revenue > 0
            ORDER BY budget DESC
        """,
        "Q9 — Highest-rated genre (min. 20 movies)": """
            SELECT g.genre_name,
                   ROUND(AVG(m.vote_average), 2) AS avg_rating,
                   COUNT(DISTINCT m.movie_id) AS movie_count
            FROM movies m
            JOIN movie_genres mg ON m.movie_id = mg.movie_id
            JOIN genres g ON mg.genre_id = g.genre_id
            GROUP BY g.genre_name
            HAVING COUNT(DISTINCT m.movie_id) >= 20
            ORDER BY avg_rating DESC
        """,
        "Q10 — Top 10 movies by keyword count": """
            SELECT m.title, COUNT(mk.keyword_id) AS keyword_count
            FROM movies m
            JOIN movie_keywords mk ON m.movie_id = mk.movie_id
            GROUP BY m.movie_id
            ORDER BY keyword_count DESC
            LIMIT 10
        """,
    }

    query_choice = st.selectbox("Choose a saved query", list(SAVED_QUERIES.keys()))

    st.markdown("**Actors who worked with a specific director**")
    director_options = sorted(
        crew[crew["job"] == "Director"]["person_name"].value_counts().head(30).index.tolist()
    )
    director_pick = st.selectbox("Director (Q8)", ["— none —"] + director_options)

    if director_pick != "— none —":
        result = pd.read_sql(
            """
            SELECT DISTINCT ca.actor_name
            FROM cast ca
            JOIN crew cr ON ca.movie_id = cr.movie_id
            WHERE cr.job = 'Director' AND cr.person_name = ?
            ORDER BY ca.actor_name
            """,
            conn, params=(director_pick,),
        )
        title_used = f"Q8 — Actors who worked with {director_pick}"
    else:
        result = pd.read_sql(SAVED_QUERIES[query_choice], conn)
        title_used = query_choice

    st.markdown(f'<div class="section-header">{title_used}</div>', unsafe_allow_html=True)
    st.dataframe(result, use_container_width=True, hide_index=True)

    numeric_cols = result.select_dtypes(include="number").columns.tolist()
    label_cols = [c for c in result.columns if c not in numeric_cols]
    if numeric_cols and label_cols and len(result) > 1:
        fig = px.bar(
            result.head(15), x=numeric_cols[0], y=label_cols[0], orientation="h",
            template=PLOTLY_TEMPLATE, color=numeric_cols[0],
            color_continuous_scale=["#7a5c00", ACCENT_GOLD],
        )
        fig.update_layout(
            yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False,
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">Insight</div>', unsafe_allow_html=True)
    if len(result) > 0:
        insight = f"This query returned <b>{len(result):,}</b> rows. "
        if numeric_cols:
            top_row = result.sort_values(numeric_cols[0], ascending=False).iloc[0]
            label = top_row[label_cols[0]] if label_cols else ""
            insight += f"The top result is <b>{label}</b> with {numeric_cols[0].replace('_', ' ')} of <b>{top_row[numeric_cols[0]]:,.2f}</b>."
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="insight-box">No rows returned for this query/filter combination.</div>', unsafe_allow_html=True)
