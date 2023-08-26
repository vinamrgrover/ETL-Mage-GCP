# ETL-Mage-GCP
## Architecture Diagram




![ezgif-1-b00367ea6f](https://github.com/vinamrgrover/ETL-Mage-GCP/assets/100070155/3e7d5851-11d1-402f-9e7b-51cce60eff27)


## Description

An ETL Pipeline built on Google Cloud Platform (GCP). First, an Airbnb dataset from kaggle is loaded into GCS Bucket. 

Then, a Dimensional Model (Star Schema) is built and the Data is Transformed and loaded into BigQuery. Further, a Looker Dashboard is built for analysis. 

This process is orchestrated by Mage, a modern ETL tool.

## Workflow 

The Dataset used in this project is based on Listing Reviews on Airbnb.
Download the Dataset used in this project [here](https://www.kaggle.com/datasets/arianazmoudeh/airbnbopendata)

### 1. Loading the Dataset

First, a GCS Bucket is created, then the [dataset](https://www.kaggle.com/datasets/arianazmoudeh/airbnbopendata) is loaded in Bucket.

<img width="1224" alt="Screenshot 2023-08-26 at 10 06 34 PM" src="https://github.com/vinamrgrover/ETL-Mage-GCP/assets/100070155/3b53d74c-000c-439d-b7e1-ec7a41ab1548">

### 2. Building Dimensional Model (Star Schema)

After setting up the Data source, a Star Schema Dimensional Model is built in BigQuery Console.

Here's the Model Overview:

![Screen Recording 2023-08-26 at 10 21 43 PM](https://github.com/vinamrgrover/ETL-Mage-GCP/assets/100070155/d2d440f0-2a2d-40a5-b05a-b14658d17f83)

Next, BigQuery Dataset named **airbnb_reviews** is created. 

Further, the following script is executed in BigQuery, to create the required Dimension Tables and Fact Tables under **airbnb_reviews**:

```
CREATE OR REPLACE TABLE airbnb_reviews.DIM_DATE(
  date_key INT NOT NULL,
  last_review_day INT,
  last_review_month INT,
  last_review_year INT,
  PRIMARY KEY (date_key) NOT ENFORCED
);

CREATE OR REPLACE TABLE airbnb_reviews.DIM_LOCATION(
  location_key INT NOT NULL,
  latitude NUMERIC,
  longitude NUMERIC,
  country STRING(30),
  country_code STRING(2),
  PRIMARY KEY (location_key) NOT ENFORCED
);

CREATE OR REPLACE TABLE airbnb_reviews.DIM_HOST(
  host_key INT NOT NULL,
  host_id INT,
  host_name STRING(30),
  isVerified BOOL,
  licence STRING,
  PRIMARY KEY (host_key) NOT ENFORCED
);

CREATE OR REPLACE TABLE airbnb_reviews.DIM_LISTING(
  listing_key INT NOT NULL,
  listing_id INT,
  listing_name STRING,
  listing_house_rules STRING,
  neighbourhood_group STRING,
  neighbourhood STRING,
  cancellation_policy STRING,
  room_type STRING,
  isInstantBookable BOOL,
  PRIMARY KEY (listing_key) NOT ENFORCED
);


CREATE OR REPLACE TABLE airbnb_reviews.FACT_PRICE(
  listing_key INT,
  location_key INT,
  host_key INT,
  date_key INT,
  price INT,
  service_fee INT,
  FOREIGN KEY (listing_key) REFERENCES airbnb_reviews.DIM_LISTING (listing_key) NOT ENFORCED,
  FOREIGN KEY (location_key) REFERENCES airbnb_reviews.DIM_LOCATION (location_key) NOT ENFORCED,
  FOREIGN KEY (host_key) REFERENCES airbnb_reviews.DIM_HOST (host_key) NOT ENFORCED,
  FOREIGN KEY (date_key) REFERENCES airbnb_reviews.DIM_DATE (date_key) NOT ENFORCED
);

CREATE OR REPLACE TABLE airbnb_reviews.FACT_REVIEWS(
  listing_key INT,
  location_key INT,
  host_key INT,
  date_key INT,
  review_count INT,
  review_per_month NUMERIC,
  review_rate_number INT,
  FOREIGN KEY (listing_key) REFERENCES airbnb_reviews.DIM_LISTING (listing_key) NOT ENFORCED,
  FOREIGN KEY (location_key) REFERENCES airbnb_reviews.DIM_LOCATION (location_key) NOT ENFORCED,
  FOREIGN KEY (host_key) REFERENCES airbnb_reviews.DIM_HOST (host_key) NOT ENFORCED,
  FOREIGN KEY (date_key) REFERENCES airbnb_reviews.DIM_DATE (date_key) NOT ENFORCED
);

CREATE OR REPLACE TABLE airbnb_reviews.FACT_LISTING_INFO(
  listing_key INT,
  location_key INT,
  host_key INT,
  date_key INT,
  minimum_nights INT,
  host_listings_count INT,
  days_available INT,
  FOREIGN KEY (listing_key) REFERENCES airbnb_reviews.DIM_LISTING (listing_key) NOT ENFORCED,
  FOREIGN KEY (location_key) REFERENCES airbnb_reviews.DIM_LOCATION (location_key) NOT ENFORCED,
  FOREIGN KEY (host_key) REFERENCES airbnb_reviews.DIM_HOST (host_key) NOT ENFORCED,
  FOREIGN KEY (date_key) REFERENCES airbnb_reviews.DIM_DATE (date_key) NOT ENFORCED
);

```
<img width="988" alt="Screenshot 2023-08-26 at 11 28 11 PM" src="https://github.com/vinamrgrover/ETL-Mage-GCP/assets/100070155/d47eb2ef-91a6-4fc2-ac19-1e6df7af7695">

## 3. Setting up Mage on VM Instance and populating BigQuery Tables

Further, on VM Instance, Mage is set up and the following scripts are used for Data Loader, Transformer, and Data Exporter respectively:

[gcs_load.py](https://github.com/vinamrgrover/ETL-Mage-GCP/blob/main/bigquery_export.py)

[generating_dataframes.py](https://github.com/vinamrgrover/ETL-Mage-GCP/blob/main/generating_dataframes.py)

[bigquery_export.py](https://github.com/vinamrgrover/ETL-Mage-GCP/blob/main/generating_dataframes.py)

Here's the Mage UI's overview:

<img width="1438" alt="Screenshot 2023-08-26 at 11 15 08 PM" src="https://github.com/vinamrgrover/ETL-Mage-GCP/assets/100070155/5d5283a8-60b4-451a-b3cb-79bf06473e70">

Next, the ETL Process is triggered and Data is Exported into Bigquery Tables.

The following Query is Executed in BigQuery Console to create a table for further analysis:



```
CREATE OR REPLACE TABLE airbnb_reviews.TBL_REVIEWS_LOOKER AS(
  SELECT
    h.host_name,
    h.isVerified,
    l.listing_name,
    l.neighbourhood, 
    l.room_type,
    l.isInstantBookable,
    n.latitude,
    n.longitude,
    n.country, 
    d.last_review_month,
    d.construction_year,
    p.price,
    p.service_fee,
    r.review_count,
    r.review_rate_number,
    i.minimum_nights,
    i.host_listings_count,
    i.days_available
  FROM airbnb_reviews.DIM_HOST h
  LEFT JOIN airbnb_reviews.FACT_PRICE p
  ON h.host_key = p.host_key
  LEFT JOIN airbnb_reviews.FACT_REVIEWS r
  ON p.host_key = r.host_key
  LEFT JOIN airbnb_reviews.FACT_LISTING_INFO i
  ON r.host_key = i.host_key
  LEFT JOIN airbnb_reviews.DIM_LISTING l
  ON i.listing_key = l.listing_key
  LEFT JOIN airbnb_reviews.DIM_LOCATION n
  ON i.location_key = n.location_key
  LEFT JOIN airbnb_reviews.DIM_DATE d
  ON i.date_key = d.date_key
  ORDER BY l.listing_id
);
```


### 4. Creating a Dashboard with Looker Studio

Next, a Dashboard is created by using the BigQuery table created in the previous step:

<img width="1440" alt="Screenshot 2023-08-26 at 11 32 01 PM" src="https://github.com/vinamrgrover/ETL-Mage-GCP/assets/100070155/fad637d8-dead-4bb5-841d-eda72781fae1">


