import streamlit as st
import pandas as pd
import os
import re
from io import BytesIO

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def extract_date(filename):
    # Try common date formats in filename and normalize to DD-MM-YYYY.
    patterns = [
        r'(?P<d>\d{2})-(?P<m>\d{2})-(?P<y>\d{4})',
        r'(?P<d>\d{2})_(?P<m>\d{2})_(?P<y>\d{4})',
        r'(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})',
        r'(?P<y>\d{4})_(?P<m>\d{2})_(?P<d>\d{2})',
        r'(?P<y>\d{4})(?P<m>\d{2})(?P<d>\d{2})',
    ]

    for pat in patterns:
        match = re.search(pat, filename)
        if match:
            y = match.group('y')
            m = match.group('m')
            d = match.group('d')
            return f"{d}-{m}-{y}"

    return "Unknown"




st.title("📊 Excel Merger")
st.markdown("Combine multiple Excel and CSV files into one with automatic date extraction")

# Create two columns
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Upload Files")
    uploaded_files = st.file_uploader(
        "Select one or more Excel/CSV files",
        type=["xlsx", "xls", "csv"],
        accept_multiple_files=True
    )

with col2:
    st.subheader("Instructions")
    st.info("""
    1. Select multiple files
    2. Dates will be extracted from filenames (DD-MM-YYYY format)
    3. Click 'Merge Files' to combine
    4. Download the merged file
    """)

if uploaded_files:
    st.markdown("---")
    st.subheader(f"📁 Files Selected: {len(uploaded_files)}")
    
    # Display selected files
    for i, file in enumerate(uploaded_files, 1):
        col_name, col_date = st.columns([3, 1])
        with col_name:
            st.write(f"{i}. {file.name}")
        with col_date:
            date = extract_date(file.name)
            st.write(f"📅 {date}")
    
    st.markdown("---")
    
    if st.button("🔄 Merge Files", key="merge_button", use_container_width=True):
        try:
            with st.spinner("Processing files..."):
                all_data = []
                
                for file in uploaded_files:
                    # Read file based on extension
                    if file.name.endswith('.csv'):
                        df = pd.read_csv(file)
                    else:
                        df = pd.read_excel(file, engine='openpyxl')
                    
                    # Extract and add date
                    date = extract_date(file.name)
                    df.insert(0, "Date", date)
                    all_data.append(df)
                
                # Combine all dataframes
                combined_df = pd.concat(all_data, ignore_index=True)

                # If UserID exists, aggregate numeric values by Date+UserID
                if 'UserID' in combined_df.columns:
                    group_cols = ['Date', 'UserID']
                    num_cols = [c for c in combined_df.select_dtypes(include='number').columns if c not in group_cols]
                    if num_cols:
                        combined_df = combined_df.groupby(group_cols, as_index=False)[num_cols].sum()

                st.success(f"✅ Successfully merged {len(uploaded_files)} files!")
                
                # Display preview
                st.subheader("📋 Preview of Merged Data")
                st.dataframe(combined_df.head(10), use_container_width=True)
                st.write(f"Total rows: {len(combined_df)} | Total columns: {len(combined_df.columns)}")
                
                # Create download button
                output_buffer = BytesIO()
                combined_df.to_excel(output_buffer, index=False, engine='openpyxl')
                output_buffer.seek(0)
                
                st.download_button(
                    label="⬇️ Download Merged File (Excel)",
                    data=output_buffer,
                    file_name="combined_pnl.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                
                # Also offer CSV download
                csv_buffer = combined_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Download Merged File (CSV)",
                    data=csv_buffer,
                    file_name="combined_pnl.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        except Exception as e:
            st.error(f"❌ Error occurred: {str(e)}")
else:
    st.info("👆 Upload files to get started!")
    
    