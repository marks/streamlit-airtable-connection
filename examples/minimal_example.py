import streamlit as st
from streamlit_airtable import AirtableConnection

# Create connection
conn = st.experimental_connection("your_connection_name", type=AirtableConnection)

# Retrieve base schema
base_schema = conn.get_base_schema()
with st.expander("Base schema"):
    st.json(base_schema)

# Get the first table's ID
first_table = base_schema["tables"][0]
st.markdown(f"First table ID: `{first_table['id']}` (named `{first_table['name']}`)")

# Retrieve all records for the first table (pyAirtable) paginates automatically
table_records = conn.get_full_table(first_table["id"])
st.markdown(f"{len(table_records)} records retrieved")
st.dataframe(table_records)
