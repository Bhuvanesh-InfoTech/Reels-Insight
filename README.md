# 📊 Reels Insight

An end-to-end data analytics and visualization project that analyzes Reels data using Python, Pandas, SQL, and Streamlit — from data preparation and exploratory analysis to an interactive analytics dashboard.

## Overview

Reels Insight is a data analytics project designed to extract meaningful insights from Reels-related data.

The project follows a complete analytics workflow:

**Data → Data Cleaning → Exploratory Data Analysis → SQL Analysis → Streamlit Dashboard**

The analysis is implemented through four Jupyter notebooks, with the processed data stored as CSV/database files and the final insights presented through an interactive Streamlit application.

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3 |
| Data Analysis | `pandas`, `numpy` |
| Data Visualization | `matplotlib`, `seaborn`, `plotly` |
| Database | SQLite |
| SQL | SQL queries |
| Dashboard | `streamlit` |
| Notebooks | Jupyter (`.ipynb`) |

## Project Structure

```text
Reels-Insight/
│
├── data/
│   ├── *.csv
│   └── *.db
│
├── notebooks/
│   ├── 01_*.ipynb
│   ├── 02_*.ipynb
│   ├── 03_*.ipynb
│   └── 04_*.ipynb
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Data Analysis Pipeline

The project is organized into four notebooks that cover the complete data analysis workflow.

### 1. Data Preparation

`notebooks/01_*.ipynb`

- Load the raw Reels data
- Inspect the dataset
- Check data types
- Identify missing values
- Identify duplicate records
- Perform initial data cleaning

### 2. Data Cleaning & Transformation

`notebooks/02_*.ipynb`

- Clean and transform the data
- Handle missing values
- Remove duplicate records
- Convert columns into appropriate data types
- Prepare data for analysis

### 3. Exploratory Data Analysis

`notebooks/03_*.ipynb`

- Analyze important metrics
- Identify trends and patterns
- Perform statistical analysis
- Generate visualizations
- Extract meaningful insights from the dataset

### 4. SQL / Final Analysis

`notebooks/04_*.ipynb`

- Load processed data into the database
- Perform SQL-based analysis
- Use filtering, aggregation, grouping, and joins where required
- Generate analytical results for the dashboard

## Database

The project uses **SQLite** as the database.

SQLite is used because it is lightweight and does not require a separate database server.

The database contains the processed Reels data used for analytical queries and dashboard visualizations.

## Dashboard

The project includes an interactive **Streamlit dashboard** implemented in:

```text
app.py
```

The dashboard provides an easy-to-use interface for exploring the analyzed Reels data and viewing key insights through tables, metrics, and visualizations.

### Run the Dashboard

Create and activate the virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

## Key Analysis

The project focuses on extracting useful insights from Reels data, including:

- Content performance
- Engagement-related metrics
- Views and reach analysis
- Performance comparisons
- Trend analysis
- Data-driven content insights

## Key Features

- 📥 Data loading and preparation
- 🧹 Data cleaning and transformation
- 🔍 Exploratory Data Analysis
- 🗄️ SQLite database integration
- 📊 SQL-based analysis
- 📈 Interactive visualizations
- 🎛️ Streamlit dashboard
- 📋 Analytical tables and KPIs

## How to Run the Project

Clone the repository:

```bash
git clone https://github.com/Bhuvanesh-InfoTech/Reels-Insight.git
```

Navigate to the project directory:

```bash
cd Reels-Insight
```

Create the virtual environment:

```bash
python -m venv venv
```

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit dashboard:

```bash
streamlit run app.py
```

## Author

Built as a data analytics portfolio project demonstrating Python programming, Pandas-based data analysis, SQL, data visualization, SQLite database usage, and Streamlit dashboard development.