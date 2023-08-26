import pandas as pd
from google.cloud import storage


@data_loader
def load_data_from_bucket() -> pd.DataFrame:

    client = storage.Client()
    bucket = client.bucket('mage-etl-bucket')

    df = pd.read_csv('gs://mage-etl-bucket/Airbnb_Data.csv')
    return df

