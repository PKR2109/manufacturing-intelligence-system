# Manufacturing Intelligence System

An interactive analytics tool for analyzing manufacturing production data and identifying defect patterns across machines, shifts, and tools.

## Overview

Manufacturing plants generate large volumes of production data. This tool helps engineers quickly detect patterns and understand the factors contributing to defects.

The system analyzes production datasets and provides visual insights into machine performance, shift impact, and tool-related failures.

## Features

- Production health overview
- Machine defect distribution
- Shift failure heatmap
- Tool performance analysis
- Timeline view of production events
- Automatic natural-language insights

## Technologies Used

- Python
- Pandas
- Streamlit
- Plotly

## How It Works

1. Upload a production dataset (CSV or Excel)
2. The system processes the dataset
3. Visual dashboards reveal failure patterns
4. Insights highlight possible root causes

## Example Insights

- Machine M3 produces the highest number of defects
- Shift C shows increased failure frequency
- Tool T2 appears frequently in defect events

## Use Case

Designed for manufacturing environments to assist engineers in identifying defect trends and operational issues within production lines.

## Run the App

```bash
pip install streamlit pandas plotly
streamlit run app.py