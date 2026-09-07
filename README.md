# 🎬 Reels Insight

An end-to-end data analytics project that transforms Reels data into meaningful insights using Python, Pandas, SQL, and an interactive Streamlit dashboard.

## Overview

This project analyzes Reels-related data through a complete data analytics workflow — data preparation → data cleaning → exploratory analysis → SQL analysis → visualization → interactive dashboard.

The project contains four Jupyter notebooks for data processing and analysis, CSV/database files for storing the data, and a Streamlit application for presenting the final insights.

## Tech Stack

| Layer                | Tool                                |
| -------------------- | ----------------------------------- |
| Language             | Python 3                            |
| Data Analysis        | `pandas`                            |
| Numerical Processing | `numpy`                             |
| Data Visualization   | `matplotlib` / `seaborn` / `plotly` |
| Database             | **SQLite**                          |
| SQL                  | SQL queries                         |
| Dashboard            | `streamlit`                         |
| Notebooks            | Jupyter (`.ipynb`)                  |

## Project Structure

```text
Reels-Insight/
├── notebooks/          # Jupyter notebooks
│   ├── 01_*.ipynb
│   ├── 02_*.ipynb
│   ├── 03_*.ipynb
│   └── 04_*.ipynb
├── data/               # CSV files and database
│   ├── *.csv
│   └── *.db
├── app.py              # Streamlit dashboard
├── requirements.txt    # Python dependencies
└── README.md
```

## Data Pipeline

The project follows an end-to-end analytics workflow:

```text
Raw Reels Data
      ↓
Data Loading
      ↓
Data Cleaning & Preprocessing
      ↓
Exploratory Data Analysis
      ↓
SQL Analysis
      ↓
Insight Generation
      ↓
Streamlit Dashboard
```

### Data Preparation

The notebooks are used to:

1. Load and inspect the Reels dataset.
2. Analyze data types and dataset structure.
3. Identify and handle missing values.
4. Check and remove duplicate records where required.
5. Clean and transform the data.
6. Perform Exploratory Data Analysis (EDA).
7. Prepare data for SQL analysis and dashboard visualization.

Run the notebooks in order using VS Code or Jupyter.

## Database

The project uses **SQLite** for storing and querying the processed data.

SQLite was selected because it is lightweight, requires no separate database server, and integrates easily with Python.

The database supports SQL-based analysis and provides data for the Streamlit dashboard.

## SQL Analysis

SQL is used to perform analytical queries and identify useful patterns from the Reels dataset.

The analysis covers:

* Filtering using `WHERE`
* Sorting using `ORDER BY`
* Aggregations using `COUNT`, `SUM`, `AVG`, `MIN`, and `MAX`
* `GROUP BY`
* `HAVING`
* `JOIN`s
* Subqueries
* Ranking and comparison queries

## Dashboard

The final analysis is presented through an interactive **Streamlit** dashboard.

### Dashboard Features

* Dataset overview
* Key performance metrics
* Interactive filters
* Data visualizations
* Reels performance analysis
* Analytical data tables


## Key Concepts Demonstrated

* Python programming
* Pandas data manipulation
* Data cleaning and preprocessing
* Exploratory Data Analysis (EDA)
* SQL querying
* SQLite database
* Data visualization
* Jupyter notebooks
* Streamlit dashboard development
* Data-driven insights

## Project Objective

The main objective of **Reels Insight** is to transform raw Reels data into meaningful analytical insights and present those insights through an interactive dashboard.

This project demonstrates an end-to-end data analytics workflow from raw data to final visualization.

## Author

Built as a data analytics portfolio project covering Python, data preprocessing, exploratory data analysis, SQL, SQLite, visualization, and Streamlit dashboard development.
