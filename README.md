# 🎬 Netflix Data Analysis Dashboard

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

End-to-end data analysis project on the Netflix titles catalog — cleaning,
EDA, six static visualizations, and an interactive Streamlit dashboard.

Built for **DawoodTech — Week 2 Internship**.

---

## 🎯 Objective

Take a raw Netflix titles CSV and turn it into something useful:

- Clean the messy real-world fields (missing values, mixed-format durations,
  string dates).
- Surface the headline patterns in the catalog — what countries / genres /
  ratings dominate, and how the catalog grew over time.
- Ship an interactive dashboard a non-technical stakeholder can actually
  click through.

---

## 📦 Dataset

- **Source:** [dsrscientist/dataset1 — netflix_titles.csv](https://raw.githubusercontent.com/dsrscientist/dataset1/master/netflix_titles.csv)
  (with a synthetic-fallback generator at `data/generate_dataset.py` for
  cases where the upstream URL is unreachable).
- **Rows after cleaning:** ~1500
- **Columns:** `show_id`, `type`, `title`, `director`, `cast`, `country`,
  `date_added`, `release_year`, `rating`, `duration`, `listed_in`,
  `description` — plus `year_added`, `month_added`, `duration_value`,
  `duration_unit` derived during cleaning.

---

## ✨ Features

- 📓 Reproducible Jupyter notebook covering loading → cleaning → analysis → insights.
- 🖼️ Six publication-quality PNG visualizations (Matplotlib + Seaborn).
- 📊 Interactive Streamlit dashboard with five sidebar-navigated pages.
- 🔍 Filter & download — slice by Type, Rating, Country, Year and export CSV.
- 💡 Styled insight cards summarising the five+ key findings.
- ⚡ `@st.cache_data` for fast page switching.

---

## 🧰 Tech Stack

| Layer        | Tools                                          |
|--------------|------------------------------------------------|
| Data         | pandas, numpy                                  |
| Static viz   | matplotlib, seaborn                            |
| Interactive  | plotly, streamlit                              |
| Notebook     | jupyter                                        |
| Utilities    | requests, openpyxl                             |

---

## 📂 Folder Structure

```
ds-week2-netflix-analysis/
├── data/
│   ├── netflix_titles.csv          # main dataset
│   └── generate_dataset.py         # synthetic fallback
├── notebook/
│   └── analysis.ipynb              # full EDA notebook
├── visualizations/
│   ├── 01_top_countries.png
│   ├── 02_movies_vs_tv.png
│   ├── 03_yearly_trend.png
│   ├── 04_movie_duration_hist.png
│   ├── 05_correlation_heatmap.png
│   └── 06_top_genres.png
├── screenshots/                    # dashboard screenshots
├── app.py                          # Streamlit dashboard
├── requirements.txt
└── README.md
```

---

## 🚀 Installation & Run

```bash
# 1. Clone
git clone https://github.com/arsid69/ds-week2-netflix-analysis.git
cd ds-week2-netflix-analysis

# 2. (Optional) virtualenv
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Only if data/netflix_titles.csv is missing)
python data/generate_dataset.py

# 5. Run the notebook
jupyter notebook notebook/analysis.ipynb

# 6. Launch the dashboard
streamlit run app.py
```

The dashboard opens at <http://localhost:8501>.

---

## 📸 Screenshots

> Drop dashboard screenshots into `screenshots/` and reference them here.

| Page              | Preview                                   |
|-------------------|-------------------------------------------|
| Overview          | `screenshots/overview.png`                |
| Data Cleaning     | `screenshots/cleaning.png`                |
| EDA & Analysis    | `screenshots/eda.png`                     |
| Filter & Explore  | `screenshots/filter.png`                  |
| Insights          | `screenshots/insights.png`                |

---

## 🔗 Links

- **Repository:** <https://github.com/arsid69/ds-week2-netflix-analysis>
- **Program:** DawoodTech Internship — Week 2 Data Analysis

---

## 📝 License

MIT — free to use, fork, and adapt.
