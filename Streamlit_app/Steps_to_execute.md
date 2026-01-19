# Streamlit App: Run Guide

Follow these steps to clone and run the Streamlit frontend locally.

## Prerequisites

- Python 3.10+ installed
- Git installed

## (1) Clone the repository

# From the folder where you want the project
git clone <https://github.com/Tishasimejiya/Internship.gitl>
cd Internship/Streamlit_app


## (2) Create and activate a virtual environment (recommended)

`
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate


## (3) Install dependencies

The requirements file lives in the frontend folder and is spelled `requirnments.txt`:

cd Frontend
pip install -r requirnments.txt


## (4) Run the Streamlit app

streamlit run app.py


## (5) Stop the app

Press `Ctrl+C` in the terminal running Streamlit.
