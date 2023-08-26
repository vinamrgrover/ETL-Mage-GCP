from google.cloud import bigquery
import pandas_gbq

@data_exporter
def bigquery_export(df_list):
    dataset_id = 'airbnb_reviews'
    client = bigquery.Client()
    
    dataset_ref = client.dataset(dataset_id = dataset_id)
    dataset = client.get_dataset(dataset_ref)

    tables = client.list_tables(dataset)
    table_ids = ['personalproject-394720.airbnb_reviews.' + tbl.table_id for tbl in tables]

    for df, table_id in zip(df_list, table_ids):
        print(table_id)
        pandas_gbq.to_gbq(df, destination_table = table_id, if_exists = 'replace', api_method = 'load_csv')


