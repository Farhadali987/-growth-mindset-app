
import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS for background animation
st.markdown(
    """
    <style>
    @keyframes gradientBg {
        0% { background-color: #2b2b2b; }
        50% { background-color: #1a1a1a; }
        100% { background-color: #000000; }
    }
    .stApp {
        animation: gradientBg 5s infinite alternate;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Datasweeper Sterling Integrator by Farhad Ali Laghari")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization. This project is for Quarter 3!")

uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine="openpyxl")
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        st.write(f"### Preview of {file.name}")
        st.dataframe(df.head())

        st.subheader(f"Data Cleaning Options for {file.name}")
        if st.checkbox(f"Enable cleaning for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates ({file.name})"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed!")

            with col2:
                if st.button(f"Fill missing values ({file.name})"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing values filled!")

        st.subheader(f"Select Columns to Keep for {file.name}")
        columns = st.multiselect(f"Choose columns ({file.name})", df.columns, default=df.columns)
        df = df[columns]

        st.subheader(f"Data Visualization for {file.name}")
        if st.checkbox(f"Show visualization ({file.name})"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        st.subheader(f"Conversion Options for {file.name}")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine="openpyxl")
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            buffer.seek(0)
            st.download_button(
                label=f"📥 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

            st.success(f"🎉 {file.name} processed successfully!")
