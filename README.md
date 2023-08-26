# ETL-Mage-GCP

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



Further, the following script is executed in BigQuery, to create the required Dimension Tables and Fact Tables.

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

## 3. Setting up Mage on VM Instance
