from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import AddressForm, PhotoForm, SurveyForm
from geopy import geocoders
from app.api_keys import bing_key, zillow_key, google_key
import zillow
import os
import requests
import re
import exifread

# get coordinates from an image file function
def get_coordinates(filepath_str):
    f = open(filepath_str, 'rb')

    # Return Exif tags
    tags = exifread.process_file(f)

    lng_ref_tag_name = "GPS GPSLongitudeRef"
    lng_tag_name = "GPS GPSLongitude"
    lat_ref_tag_name = "GPS GPSLatitudeRef"
    lat_tag_name = "GPS GPSLatitude"

    # Check if these tags are present
    gps_tags = [lng_ref_tag_name,lng_tag_name,lat_tag_name,lat_tag_name]
    for tag in gps_tags:
        if not tag in tags.keys():
            print ("Skipping file. Tag {} not present.".format(tag))
            return None
    #converting to values to be used
    convert = lambda ratio: float(ratio.num)/float(ratio.den)

    lng_ref_val = tags[lng_ref_tag_name].values
    lng_coord_val = [convert(c) for c in tags[lng_tag_name].values]

    lat_ref_val = tags[lat_ref_tag_name].values
    lat_coord_val = [convert(c) for c in tags[lat_tag_name].values]

    lng_coord = sum([c/60**i for i,c in enumerate(lng_coord_val)])
    lng_coord *= (-1)**(lng_ref_val=="W")

    lat_coord = sum([c/60**i for i,c in enumerate(lat_coord_val)])
    lat_coord *= (-1)**(lat_ref_val=="S")
    #grabbing the heading (cardinal direction photo was taken in)
    heading = tags['GPS GPSImgDirection'].values[0].num / tags['GPS GPSImgDirection'].values[0].den

    return [(lat_coord, lng_coord), heading]


#get lat_long from an image file function
def latlong_to_address(img_path_str):
# run get_coordinates function for lat, long
    coords = get_coordinates(img_path_str)[0]

#instantiate bing geocoder
    bing_locator = geocoders.Bing(bing_key)
    #pulling address from bing locator
    address = bing_locator.reverse(coords).raw

    return address


# Pull Zillow value function
def zillow_pull(address):
    #instantiate zillow api
    zillow_api = zillow.ValuationApi()

    # get house and postal code info from dictionary
    house = address['address']['addressLine']
    postal_code = address['address']['postalCode']

    # Grab Zillow price and set to price variable
    try:
        house_data = zillow_api.GetSearchResults(zillow_key, house, postal_code)
        price = house_data.zestimate.amount
    #Error if zillow doesnt have price for property
    except:
        price = 'Zillow does not have price for this address'

    return price
