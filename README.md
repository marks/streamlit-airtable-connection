# Airtable ⚡ Streamlit Connection

This repo includes a `st.experimental_connection` for Airtable which wraps the
popular community created and maintained
[pyAirtable](https://github.com/gtalarico/pyairtable) library.

The initial focus of this connector is on read-only operations: specifically
[listing records](https://airtable.com/developers/web/api/list-records) and
[retrieving the schema](https://airtable.com/developers/web/api/get-base-schema)
of an Airtable base. Write-back support may be added in the future.

### 👀 Live demo w/ AI ✨
A live demo of the code example in  [`examples/explore.py`](./examples/explore.py) can be accessed on Streamlit Cloud at [http://marks-airtable-connection-demo.streamlit.app](http://marks-airtable-connection-demo.streamlit.app). Provide your Open AI API key to be able to ask questions about the data in the selected Airtable table. The underlying data can be viewed and cloned [here](https://airtable.com/appdbRXgibDiQkNQN/shrIO0m8oyeQJTf9T).

---

### Minimal example: retrieve all records from base's first table

_See `examples/` for additional examples_

#### [`.streamlit/secrets.toml`](./examples/.streamlit/secrets.toml.example)

```
[connections.your_connection_name]
personal_access_token = "patXXX" # REQUIRED
base_id = "appXXX" # optional
table_id = "tblXXX" # optional
```

ℹ️ The Airtable
[personal access token](https://airtable.com/developers/web/guides/personal-access-tokens)
you use should have both
[`data.records:read`](https://airtable.com/developers/web/api/scopes#data-records-read)
and
[`schema.bases:read`](https://airtable.com/developers/web/api/scopes#schema-bases-read)
scopes to use all functionality of this connector.

#### [`minimal_example.py`](./examples/minimal_example.py)

```python
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

# Retrieve all records for the first table (pyAirtable paginates automatically)
# (Note you can also pass in parameters supported by pyAirtable
# (https://pyairtable.readthedocs.io/en/stable/api.html#parameters) such as as
# max_records, view, sort, and formula into conn.query() like so:
# table_records = conn.query(first_table["id"], max_records=25, view='viwXXX')
table_records = conn.query(table_id=first_table["id"])
st.markdown(f"{len(table_records)} records retrieved")
st.dataframe(table_records)
```

#### Steps to replicate the minimal example

1. Clone/download this repo
2. Install the connector (`pip install . -e`)
3. Move into the `examples/` dir (`cd examples/`)
4. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml.example`
   and provide your own values
5. Run `streamlit run minimal_example.py`

### Acknowledgements & thank yous

- Streamlit connection examples:
  [Google Sheets](https://github.com/streamlit/gsheets-connection) &
  [DuckDB](https://github.com/streamlit/release-demos/blob/master/1.22/st-experimental-connection/duckdb_connection/connection.py)
- [pyAirtable](https://github.com/gtalarico/pyairtable)
