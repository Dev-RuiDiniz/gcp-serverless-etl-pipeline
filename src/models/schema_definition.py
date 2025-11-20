from google.cloud import bigquery


IBGE_STATE_SCHEMA = [
    bigquery.SchemaField("id", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("nome", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("sigla", "STRING", mode="NULLABLE"),
    bigquery.SchemaField(
        "regiao",
        "RECORD",
        mode="NULLABLE",
        fields=[
            bigquery.SchemaField("id", "INT64", mode="NULLABLE"),
            bigquery.SchemaField("nome", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("sigla", "STRING", mode="NULLABLE"),
        ],
    ),
]
