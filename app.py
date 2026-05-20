"""Netflix Data Analysis — Streamlit Dashboard.

Multi-page app with sidebar navigation. Loads and cleans the Netflix titles
dataset once (cached), then exposes Overview / Cleaning / EDA / Filter /
Insights pages with interactive Plotly charts.

Run locally:
    streamlit run app.py
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

DATA_PATH = Path(__file__).parent / "data" / "netflix_titles.csv"

st.set_page_config(
    page_title="Netflix Data Analysis Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------- Data loading & cleaning ----------

@st.cache_data(show_spinner="Loading and cleaning Netflix dataset…")
def load_data(path: str | Path) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Return (clean_df, raw_df, cleaning_report).

    cleaning_report carries the numbers shown on the Cleaning page so we
    don't have to recompute them across reruns.
    """
    raw = pd.read_csv(path)
    df = raw.copy()

    missing_before = df.isna().sum()
    rows_before = len(df)

    df = df.drop_duplicates().copy()
    duplicates_removed = rows_before - len(df)

    df.columns = (
        df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("-", "_")
    )

    for col in ["director", "cast", "country", "rating"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown").replace("", "Unknown")

    df["date_added"] = pd.to_datetime(
        df["date_added"].astype(str).str.strip(), errors="coerce"
    )
    df = df.dropna(subset=["date_added"]).copy()
    df["year_added"] = df["date_added"].dt.year.astype(int)
    df["month_added"] = df["date_added"].dt.month.astype(int)

    df["duration"] = df["duration"].fillna("").astype(str)
    split = df["duration"].str.extract(
        r"(?P<duration_value>\d+)\s*(?P<duration_unit>[A-Za-z]+)?"
    )
    df["duration_value"] = pd.to_numeric(split["duration_value"], errors="coerce")
    df["duration_unit"] = split["duration_unit"].fillna("").str.lower().str.rstrip("s")

    missing_after = df.isna().sum()
    report = {
        "rows_before": rows_before,
        "rows_after": len(df),
        "duplicates_removed": duplicates_removed,
        "missing_before": missing_before,
        "missing_after": missing_after,
    }
    return df, raw, report


if not DATA_PATH.exists():
    st.error(
        f"Dataset not found at `{DATA_PATH}`. "
        "Run the generator at `data/generate_dataset.py` or place the original "
        "`netflix_titles.csv` in the `data/` folder."
    )
    st.stop()

try:
    df, raw_df, report = load_data(DATA_PATH)
except Exception as exc:  # pragma: no cover — surface load failures to the UI
    st.error(f"Failed to load dataset: {exc}")
    st.stop()


# ---------- Sidebar navigation ----------

st.sidebar.title("🎬 Netflix Dashboard")
st.sidebar.caption("DawoodTech — Week 2")
page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Overview",
        "🧹 Data Cleaning",
        "📊 EDA & Analysis",
        "🔍 Filter & Explore",
        "💡 Insights",
    ],
)
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Rows:** {len(df):,}  \n**Columns:** {df.shape[1]}")


# ---------- Pages ----------

def page_overview() -> None:
    st.title("🏠 Overview")
    st.write("A quick snapshot of the Netflix titles dataset after cleaning.")

    movies_n = int((df["type"] == "Movie").sum())
    tv_n = int((df["type"] == "TV Show").sum())
    countries_n = int(
        df["country"].str.split(", ").explode().str.strip().replace("Unknown", np.nan).dropna().nunique()
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total titles", f"{len(df):,}")
    c2.metric("Movies", f"{movies_n:,}")
    c3.metric("TV Shows", f"{tv_n:,}")
    c4.metric("Countries covered", f"{countries_n:,}")

    st.subheader("Dataset preview")
    st.dataframe(df.head(50), use_container_width=True)

    st.subheader("Shape & schema")
    cols = st.columns(2)
    with cols[0]:
        st.write("**Shape**")
        st.write({"rows": len(df), "columns": df.shape[1]})
    with cols[1]:
        st.write("**Dtypes**")
        st.write(df.dtypes.astype(str).to_dict())


def page_cleaning() -> None:
    st.title("🧹 Data Cleaning")
    st.write(
        "Step-by-step record of what changed between the raw CSV and the "
        "cleaned analytical frame."
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Rows (before)", f"{report['rows_before']:,}")
    c2.metric("Rows (after)", f"{report['rows_after']:,}")
    c3.metric("Duplicates removed", f"{report['duplicates_removed']:,}")

    st.subheader("Missing values — before vs after")
    missing_tbl = pd.concat(
        [report["missing_before"].rename("missing_before"),
         report["missing_after"].rename("missing_after")],
        axis=1,
    ).fillna(0).astype(int)
    st.dataframe(missing_tbl, use_container_width=True)

    st.subheader("Cleaning steps applied")
    st.markdown(
        """
        - Dropped exact duplicate rows.
        - Normalised column names to snake_case.
        - Filled missing `director`, `cast`, `country`, `rating` with `Unknown`
          (losing those rows would discard ~10% of the data).
        - Dropped rows with unparseable `date_added` — they can't contribute
          to any time-series view.
        - Parsed `date_added` to `datetime`, derived `year_added` / `month_added`.
        - Split `duration` into numeric `duration_value` and textual
          `duration_unit` (min / season).
        """
    )

    st.subheader("Dtypes after cleaning")
    st.dataframe(df.dtypes.astype(str).rename("dtype").to_frame(), use_container_width=True)


def page_eda() -> None:
    st.title("📊 EDA & Analysis")
    st.write("All charts below are interactive — hover, zoom, export.")

    # 1. Movies vs TV Shows (pie)
    type_counts = df["type"].value_counts().reset_index()
    type_counts.columns = ["type", "count"]
    fig1 = px.pie(
        type_counts, values="count", names="type", hole=0.45,
        title="Movies vs TV Shows",
        color_discrete_sequence=["#E50914", "#221f1f"],
    )
    st.plotly_chart(fig1, use_container_width=True)

    # 2. Top 10 countries (bar)
    country_series = (
        df["country"].str.split(", ").explode().str.strip()
    )
    country_series = country_series[country_series != "Unknown"]
    top_countries = country_series.value_counts().head(10).reset_index()
    top_countries.columns = ["country", "count"]
    fig2 = px.bar(
        top_countries, x="count", y="country", orientation="h",
        title="Top 10 Countries by Content",
        color="count", color_continuous_scale="Viridis",
    )
    fig2.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig2, use_container_width=True)

    # 3. Yearly content trend (line)
    yearly = df.groupby("year_added").size().reset_index(name="count")
    fig3 = px.line(
        yearly, x="year_added", y="count", markers=True,
        title="Netflix Content Added per Year",
        color_discrete_sequence=["#E50914"],
    )
    st.plotly_chart(fig3, use_container_width=True)

    # 4. Movie duration histogram
    movies = df[(df["type"] == "Movie") & (df["duration_unit"] == "min")]
    fig4 = px.histogram(
        movies, x="duration_value", nbins=30,
        title="Movie Duration Distribution (minutes)",
        color_discrete_sequence=["#564d4d"],
    )
    fig4.update_layout(xaxis_title="Duration (minutes)", yaxis_title="Count")
    st.plotly_chart(fig4, use_container_width=True)

    # 5. Correlation heatmap
    corr = df[["release_year", "year_added", "month_added", "duration_value"]].corr()
    fig5 = px.imshow(
        corr, text_auto=".2f", aspect="auto", color_continuous_scale="RdBu_r",
        title="Correlation — Numeric Columns", zmin=-1, zmax=1,
    )
    st.plotly_chart(fig5, use_container_width=True)

    # 6. Top 10 genres (horizontal bar)
    genre_series = df["listed_in"].str.split(", ").explode().str.strip()
    top_genres = genre_series.value_counts().head(10).reset_index()
    top_genres.columns = ["genre", "count"]
    fig6 = px.bar(
        top_genres, x="count", y="genre", orientation="h",
        title="Top 10 Genres on Netflix",
        color="count", color_continuous_scale="Magma",
    )
    fig6.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig6, use_container_width=True)


def page_filter() -> None:
    st.title("🔍 Filter & Explore")
    st.write("Slice the catalog and download the filtered subset as CSV.")

    c1, c2, c3, c4 = st.columns(4)
    types = c1.multiselect("Type", sorted(df["type"].dropna().unique()), default=None)
    ratings = c2.multiselect("Rating", sorted(df["rating"].dropna().unique()), default=None)

    country_options = sorted(
        c for c in df["country"].str.split(", ").explode().str.strip().dropna().unique()
        if c and c != "Unknown"
    )
    countries = c3.multiselect("Country", country_options, default=None)

    year_min, year_max = int(df["year_added"].min()), int(df["year_added"].max())
    year_range = c4.slider("Year added", year_min, year_max, (year_min, year_max))

    filtered = df.copy()
    if types:
        filtered = filtered[filtered["type"].isin(types)]
    if ratings:
        filtered = filtered[filtered["rating"].isin(ratings)]
    if countries:
        mask = filtered["country"].apply(
            lambda val: any(c.strip() in countries for c in str(val).split(","))
        )
        filtered = filtered[mask]
    filtered = filtered[filtered["year_added"].between(year_range[0], year_range[1])]

    st.caption(f"{len(filtered):,} of {len(df):,} titles match your filters.")
    st.dataframe(filtered, use_container_width=True)

    csv_bytes = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download filtered data as CSV",
        data=csv_bytes,
        file_name="netflix_filtered.csv",
        mime="text/csv",
        disabled=filtered.empty,
    )


def page_insights() -> None:
    st.title("💡 Key Insights")
    st.markdown(
        """
        <style>
        .insight-card {
            background: linear-gradient(135deg, #221f1f 0%, #3a1414 100%);
            color: #f5f5f5;
            padding: 1rem 1.25rem;
            border-left: 5px solid #E50914;
            border-radius: 6px;
            margin-bottom: 0.75rem;
        }
        .insight-card b { color: #E50914; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    insights = [
        ("Movies dominate the catalog",
         "Roughly 70% of all titles are movies and ~30% are TV shows. "
         "The library is still movie-heavy despite Netflix's push into series."),
        ("US and India lead production",
         "The United States contributes the largest share of titles, followed by "
         "India and the United Kingdom. The top three countries account for a "
         "disproportionate slice of the catalog."),
        ("Catalog growth peaked 2018–2020",
         "Yearly additions ramp sharply from 2015, peak in 2019–2020, then taper — "
         "consistent with Netflix's aggressive originals expansion winding down."),
        ("Mature ratings dominate",
         "TV-MA and TV-14 are the two most common ratings, signalling that "
         "adult-oriented content drives library size more than family content."),
        ("Movies cluster around 90–110 minutes",
         "The duration histogram peaks in the standard feature-film range; very "
         "few movies exceed 150 minutes."),
        ("Weak numeric correlations",
         "`release_year` and `year_added` correlate moderately (newer content gets "
         "added sooner). Other numeric fields show little linear relationship — "
         "most signal in this dataset is categorical."),
    ]
    for title, body in insights:
        st.markdown(
            f"<div class='insight-card'><b>{title}.</b> {body}</div>",
            unsafe_allow_html=True,
        )


PAGES = {
    "🏠 Overview": page_overview,
    "🧹 Data Cleaning": page_cleaning,
    "📊 EDA & Analysis": page_eda,
    "🔍 Filter & Explore": page_filter,
    "💡 Insights": page_insights,
}
PAGES[page]()
