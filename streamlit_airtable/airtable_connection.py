from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data

from pyairtable import Base, metadata
import pandas as pd


class AirtableConnection(ExperimentalBaseConnection[Base]):
    """Basic st.experimental_connection implementation for DuckDB"""

    # Establish a connection to Airtable using personal access token and base ID
    def _connect(self, **kwargs) -> Base:
        personal_access_token = self._secrets["personal_access_token"]
        base_id = self._secrets["base_id"]
        return Base(personal_access_token, base_id)

    # Get the base schema
    # Uses pyAirtable's metadata.get_base_schema method
    # which calls https://airtable.com/developers/web/api/get-base-schema
    def get_base_schema(self, ttl: int = 3600) -> dict:
        @cache_data(ttl=ttl)
        def _get_base_schema() -> dict:
            base_schema = metadata.get_base_schema(self._instance)
            return base_schema

        return _get_base_schema()

    # Query records from a table using pyAirtable's Table.all method
    # which calls https://airtable.com/developers/web/api/get-records
    # and paginates automatically. Parameters such as max_records, sort, view,
    # formula, and more can be passed in using kwargs and the pyAirtable reference
    # at https://pyairtable.readthedocs.io/en/stable/api.html#parameters
    def query(self, table_id: str, ttl: int = 3600, **kwargs) -> pd.DataFrame:
        @cache_data(ttl=ttl)
        def _query(table_id: str, **kwargs) -> pd.DataFrame:
            table = self._instance.get_table(table_id)
            all_records = table.all(**kwargs)
            all_records_fields = [record["fields"] for record in all_records]
            return pd.DataFrame.from_records(all_records_fields)

        return _query(table_id, **kwargs)
