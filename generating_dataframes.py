import pandas as pd
from typing import Union
from decimal import Decimal
import re



def replace_nullable_int(value) -> Union[int, pd._libs.missing.NAType]: # For int values
    if pd.isna(value):
        return pd.NA
    

    return int(value)

def replace_nullable(value) -> Union[Decimal, pd._libs.missing.NAType]: # For float values
    if pd.isna(value):
        return pd.NA
    
    return value
    

def cast_value(value) -> Union[int, pd._libs.missing.NAType]:
    if type(value) is float:
        try:
            return int(value)
        except ValueError:
            return pd.NA
        
    else:
        numbers = re.findall(r'\d+', str(value))
        try:
            return int(''.join(numbers))
        except ValueError:
            return pd.NA

@transformer
def transform(df : pd.DataFrame):
    df.columns = ['_'.join(col.split()).lower() for col in df.columns]

    df.last_review = pd.to_datetime(
            df.last_review.fillna(0), 
            errors = 'coerce'
    )

    df.construction_year = df.construction_year.apply(lambda year : replace_nullable_int(year))
    df.host_identity_verified = df.host_identity_verified.apply(lambda x : True if x == 'verified' else False)

    df.price = df.price.apply(lambda price : cast_value(price))
    df.service_fee = df.service_fee.apply(lambda fee : cast_value(fee))

    df.number_of_reviews = df.number_of_reviews.apply(lambda review : cast_value(review))
    df.review_rate_number = df.review_rate_number.apply(lambda rate : cast_value(rate))

    df.minimum_nights = df.minimum_nights.apply(lambda nights : cast_value(nights))
    df.calculated_host_listings_count = df.calculated_host_listings_count.apply(lambda listing : cast_value(listing))
    df.availability_365 = df.availability_365.apply(lambda days : cast_value(days))


    DIM_date = pd.DataFrame(
    {
        "date_key" : df.last_review.index,
        "last_review_day" : df.last_review.dt.day,
        "last_review_month" : df.last_review.dt.month,
        "last_review_year" : df.last_review.dt.year,
        "construction_year" : df.construction_year
    }
)

    DIM_location = pd.DataFrame(
    {
        "location_key" : df.index,
        "latitude" : df.lat,
        "longitude" : df.long,
        "country" : df.country,
        "country_code" : df.country_code
    }
)


    DIM_host = pd.DataFrame(
    {
        "host_key" : df.index,
        "host_id" : df.host_id,
        "host_name" : df.host_name,
        "isVerified" : df.host_identity_verified, 
        "license" : df.license
    }
)


    DIM_listing = pd.DataFrame(
    {
        "listing_key" : df.index,
        "listing_id" : df.id,
        "listing_name" : df.name,
        "listing_house_rules" : df.house_rules,
        "neighbourhood_group" : df.neighbourhood_group,
        "neighbourhood" : df.neighbourhood,
        "cancellation_policy" : df.cancellation_policy,
        "room_type" : df.room_type,
        "isInstantBookable" : df.instant_bookable
    }
)

    FACT_price = pd.DataFrame(
    {
        "listing_key" : DIM_listing.listing_key,
        "location_key" : DIM_location.location_key,
        "host_key" : DIM_host.host_key,
        "date_key" : DIM_date.date_key,
        "price" : df.price,
        "service_fee" : df.service_fee
    }
)

    FACT_reviews = pd.DataFrame(
    {
        "listing_key" : DIM_listing.listing_key,
        "location_key" : DIM_location.location_key,
        "host_key" : DIM_host.host_key,
        "date_key" : DIM_date.date_key,
        "review_count" : df.number_of_reviews,
        "reviews_per_month" : df.reviews_per_month,
        "review_rate_number" : df.review_rate_number

    }
)
    FACT_listing_info = pd.DataFrame(
    {
        "listing_key" : DIM_listing.listing_key,
        "location_key" : DIM_location.location_key,
        "host_key" : DIM_host.host_key,
        "date_key" : DIM_date.date_key,
        "minimum_nights" : df.minimum_nights,
        "host_listings_count" : df.calculated_host_listings_count,
        "days_available" : df.availability_365
    }
)
        

    DIM_location[['country', 'country_code']] = DIM_location[['country', 'country_code']].fillna('Unknown')
    DIM_location[['latitude', 'longitude']] = DIM_location[['latitude', 'longitude']].apply(lambda x : round(x, 5))
    DIM_location.latitude = DIM_location.latitude.apply(lambda x : replace_nullable(x))
    DIM_location.longitude = DIM_location.longitude.apply(lambda x : replace_nullable(x))




    DIM_date.last_review_day = DIM_date.last_review_day.apply(lambda day : cast_value(day))
    DIM_date.last_review_month = DIM_date.last_review_month.apply(lambda day : cast_value(day))
    DIM_date.last_review_year = DIM_date.last_review_year.apply(lambda day : cast_value(day))
    
    
    df_list = [DIM_date, DIM_host, DIM_listing, DIM_location, FACT_listing_info, FACT_price, FACT_reviews]

    return df_list


