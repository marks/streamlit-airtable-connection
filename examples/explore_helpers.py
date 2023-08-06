from graphviz import Digraph


def create_graph_from_base_schema(base_id, json_data):
    graph = Digraph("G")

    # Extract table names and their relationships
    table_names = {}
    relationships = {}
    field_names = {}
    for table in json_data["tables"]:
        table_id = table["id"]
        table_names[table_id] = table["name"]

        for field in table["fields"]:
            field_id = field["id"]
            field_names[field_id] = field["name"]

            if field["type"] == "multipleRecordLinks":
                linked_table_id = field["options"]["linkedTableId"]
                is_reversed = field["options"]["isReversed"]
                relationship_key = (
                    (table_id, linked_table_id)
                    if is_reversed
                    else (linked_table_id, table_id)
                )
                relationships.setdefault(relationship_key, []).append(field_id)

    # Add nodes and edges to the graph
    for table_id, table_name in table_names.items():
        graph.node(
            table_id,
            label=table_name,
            href=f"https://airtable.com/{base_id}/{table_id}",
            target="_blank",
        )

    for (source_table_id, target_table_id), field_ids in relationships.items():
        edge_label = ", ".join(field_names[field_id] for field_id in field_ids)
        graph.edge(
            source_table_id,
            target_table_id,
            label=edge_label,
            href=f"https://airtable.com/{base_id}/{source_table_id}/{field_ids[0]}",
            target="_blank",
        )

    return graph
