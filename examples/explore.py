from streamlit_airtable import AirtableConnection
import streamlit as st
import pandas as pd
import json
import explore_helpers

# Initiate connection to Airtable using st.experimental_connection
airtable_conn = st.experimental_connection(
    "your_connection_name", type=AirtableConnection
)

# Retrieve list of bases, and create a dict of base id to name
bases_list = airtable_conn.list_bases()
bases_id_to_name = {base["id"]: base["name"] for base in bases_list["bases"]}

# Add a sidebar to select a base
with st.sidebar:
    st.markdown("## Configuration")
    selected_base_id = st.sidebar.selectbox(
        "Which base would you like to explore?",
        options=list(bases_id_to_name.keys()),
        format_func=lambda base_id: bases_id_to_name[base_id],
        help="If you don't see a base in this list, make sure your personal access token has access to it.",
    )
    st.write(f"You selected: `{selected_base_id}`")


# Main content pane
with st.container():
    st.markdown("# Airtable Base Explorer")
    # st.markdown(f"## `{bases_id_to_name[selected_base_id]}`")
    base_schema = airtable_conn.get_base_schema(base_id=selected_base_id)

    st.markdown("### Base schema")

    # Two columns: list of tables and graph of relationships
    col1, col2 = st.columns(2)

    # Show the number and a list of tables in the base
    col1.write(f"**{len(base_schema['tables'])} tables**")
    # Create a dataframe of the table names and ids; and display number of
    tables_df = pd.DataFrame(
        [
            {
                "name": table["name"],
                "id": table["id"],
                "deep_link": f"https://airtable.com/{selected_base_id}/{table['id']}",
            }
            for table in base_schema["tables"]
        ]
    )
    col1.dataframe(
        tables_df,
        column_config={"deep_link": st.column_config.LinkColumn()},
        hide_index=True,
    )

    col1.download_button(
        "Download base schema as JSON",
        json.dumps(base_schema),
        f"base-schema-{selected_base_id}.json",
        "application/json",
    )

    # Show a graph of the relationships between tables
    graph = explore_helpers.create_graph_from_base_schema(selected_base_id, base_schema)
    col2.write(
        f"**Table relationships**\n\nNodes are table names and edges are _field names_ of the linked record fields. Both are clickable links to the Airtable UI for that item."
    )
    col2.graphviz_chart(graph)

    st.divider()
    st.markdown("### Table schemas")

    table_schema_tabs = st.tabs([f"{table['name']}" for table in base_schema["tables"]])

    # Show the full schema for each table in an expander
    for i, table_schema in enumerate(base_schema["tables"]):
        this_tab = table_schema_tabs[i]
        this_tab.write(
            f"**{len(table_schema['fields'])} fields** belonging to table `{table_schema['id']}`:"
        )
        fields_df = pd.DataFrame(
            [
                {
                    "name": item["name"],
                    "id": item["id"],
                    "type": item["type"],
                    "choices": [
                        choice["name"] for choice in item["options"].get("choices", [])
                    ]
                    if item["type"] in ["singleSelect", "multipleSelects"]
                    else None,
                    "linked_table_id": item["options"]["linkedTableId"]
                    if item["type"] in ["multipleRecordLinks"]
                    else None,
                    "deep_link": f"https://airtable.com/{selected_base_id}/{table_schema['id']}/{item['id']}",
                }
                for item in table_schema["fields"]
            ]
        )
        this_tab.dataframe(
            fields_df,
            column_config={"deep_link": st.column_config.LinkColumn()},
            hide_index=True,
        )

        this_tab.download_button(
            "Download list of fields as CSV",
            fields_df.to_csv(index=False).encode("utf-8"),
            f"table-schema-{selected_base_id}-{table_schema['id']}.csv",
            "text/csv",
        )

        this_tab.download_button(
            "Download full table schema as JSON",
            json.dumps(table_schema),
            f"table-schema-{selected_base_id}-{table_schema['id']}.json",
            "application/json",
        )

    # # Display the full base schema
    # with st.expander("Expand to view full base schema (all tables, JSON format)"):
    #     st.json(base_schema)

    st.divider()
    st.markdown("### Base records")

    table_record_tabs = st.tabs([f"{table['name']}" for table in base_schema["tables"]])

    # Show the full schema for each table in an expander
    for i, table_schema in enumerate(base_schema["tables"]):
        this_tab = table_record_tabs[i]
        # st.markdown(
        #     "The following preview is of the first 10 records from the [Airtable list records API](https://airtable.com/developers/web/api/list-records) in `string` cell format. This will return the same values you see in the Airtable UI and when you export as CSV."
        # )

        this_tab.dataframe(
            airtable_conn.query(
                base_id=selected_base_id,
                table_id=table_schema["id"],
                max_records=10,
                cell_format="string",
                time_zone="America/Los_Angeles",
                user_locale="en-us",
            ),
            hide_index=True,
        )
