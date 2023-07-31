from streamlit_airtable import AirtableConnection
import streamlit as st
import pandas as pd

st.image("https://airtable.com/favicon.ico")
st.markdown("## Airtable `st.experimental_connection` example")

st.markdown("----")
st.markdown("### Connect to Airtable")
with st.echo():
    conn = st.experimental_connection("your_connection_name", type=AirtableConnection)

st.markdown("### Get the base's schema (list of tables)")
with st.echo():
    base_schema = conn.get_base_schema()

    # Display the full base schema
    with st.expander("Full base schema (all tables)"):
        st.json(base_schema)

    # Display a list of tables to the right of the number of tables
    col1, col2 = st.columns(2)
    # Show the number of tables in the base
    col1.metric(label="Number of tables", value=len(base_schema["tables"]))
    # Create a dataframe of the table names and ids; and display number of
    tables_df = [(table["name"], table["id"]) for table in base_schema["tables"]]
    col2.dataframe(pd.DataFrame(tables_df, columns=["Table Name", "Table ID"]))

    # Show the full schema for each table
    for table_schema in base_schema["tables"]:
        with st.expander(
            f"Table schema for '{table_schema['name']}' ({table_schema['id']})"
        ):
            col1, col2 = st.columns(2)
            col1.metric(label="Number of fields", value=len(table_schema["fields"]))
            col2.metric(label="Number of views", value=len(table_schema["views"]))

            # Show the full table_schema
            st.json(table_schema)

st.markdown("### Retrieve records for each table (default 'json' cell format)")
st.markdown(
    "In this example, the first 10 records for each table are retrieved and displayed. Remove or increase `max_records` to retrieve more records.",
)
st.markdown(
    "The [Airtable list records API](https://airtable.com/developers/web/api/list-records) defaults to `json` cell formatting so some complex field types may show values that are different from what you see in the Airtable UI/CSV exports.",
)
with st.echo():
    for table in base_schema["tables"]:
        with st.expander(
            f"First 10 records of '{table['name']}' table with `json` cell format"
        ):
            st.dataframe(conn.query(table["id"], max_records=10))

st.markdown("### Retrieve records for each table ('string' cell format)")
st.markdown(
    "In this example, we ask the [Airtable API list records API](https://airtable.com/developers/web/api/list-records) to return the records in `string` cell format. This will return the same values you see in the Airtable UI and when you export as CSV. When specifying `string` cell format, time zone and user locale must also be included."
)
with st.echo():
    for table in base_schema["tables"]:
        with st.expander(
            f"First 10 records of '{table['name']}' table with `string` cell format"
        ):
            st.dataframe(
                conn.query(
                    table["id"],
                    max_records=10,
                    cell_format="string",
                    time_zone="America/Los_Angeles",
                    user_locale="en-us",
                )
            )
