from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data

from pyairtable import Base, metadata
import pandas as pd


class AirtableConnection(ExperimentalBaseConnection[Base]):
    """Basic st.experimental_connection implementation for DuckDB"""

    def _connect(self, **kwargs) -> Base:
        personal_access_token = self._secrets["personal_access_token"]
        base_id = self._secrets["base_id"]
        return Base(personal_access_token, base_id)

    def get_base_schema(self, ttl: int = 3600, **kwargs) -> dict:
        base_schema = metadata.get_base_schema(self._instance)
        return base_schema

    def get_full_table(self, table_id: str, ttl: int = 3600, **kwargs) -> pd.DataFrame:
        @cache_data(ttl=ttl)
        def _get_full_table(table_id: str, **kwargs) -> pd.DataFrame:
            all_records = self._instance.all(table_id, **kwargs)
            all_records_fields = [record["fields"] for record in all_records]
            return pd.DataFrame.from_records(all_records_fields)

        return _get_full_table(table_id, **kwargs)
