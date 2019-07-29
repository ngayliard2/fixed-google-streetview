import exifread

import requests
import re

import os
import pandas as pd
import numpy as np
from geopy import geocoders
import folium
from folium import IFrame
import base64

from IPython.display import Image
import zillow

import time

# In[13]:


#use this folder to input photos '../images/Test_exif_pics/'


# In[31]:


def files_to_process():
    """List the files in the upload directory."""
    img_files = []


    for filename in os.listdir('./uploads/'):
        path = os.path.join('./uploads/', filename)
        if os.path.isfile(path):
            img_files.append(f'./uploads/{filename}')
    for file in img_files:
        if '.DS' in file:
            img_files.remove(file)

    return img_files




files_to_process()



#taken from repo documentation:
def get_coordinates(filepath_str):


    f = open(filepath_str, 'rb')

    # Return Exif tags
    tags = exifread.process_file(f)
    #Exif tags
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
    #grabbing the heading
    heading = tags['GPS GPSImgDirection'].values[0].num / tags['GPS GPSImgDirection'].values[0].den
    return (lat_coord, lng_coord, heading)


#image return
def image_return(img_list):
    #making a list of the houses
    houses = []
    #looping though uploaded images
    for img in img_list:
        #house dictionary
        house = {}
        #pull the coordinates from the get coordinates function
        coords = get_coordinates(img)
        #defining 'address' as coordinates
        address = f'+{coords[0]},{coords[1]}'
        heading = coords[2]
        #url to query api, plug your api key in place of (your_key_here)
        url = f'https://maps.googleapis.com/maps/api/streetview?size=300x600&location={address}&heading={heading}&key={your_key_here}'
        #img pulled from api
        img = requests.get(url)
        #writing the file name into a file path
        filelist = re.findall(r'\w+', address)
        filename = ''.join(filelist)
        final_path = f'./SVphotos//{filename}.jpg'
        #write it into path
        open(final_path, 'wb').write(img.content)
        #add information to 'house' dictionary
        house['street_view'] = final_path
        house['Lat'] = coords[0]
        house['Lon'] = coords[1]
        house['heading'] = heading
        #adding house to houses list
        houses.append(house)

    return houses


# In[35]:


def latlong_to_address(img_list):
    # run get_coordinates function for lat, long
    addresses = []
    #add your api keys here to use this function
    bing_key = 'your_key_here'
    zillow_key = 'your_key_here'
    #instantiating the zillow api
    zillow_api = zillow.ValuationApi()

    for img in img_list:
        #get address from Lat/lon
        coords = get_coordinates(img)


        #instantiate bing geocoder
        bing_locator = geocoders.Bing(bing_key)
        #pulling mailing address from bing
        address = bing_locator.reverse(coords).raw
        street_address = address['name']
        house = address['address']['addressLine']
        postal_code = address['address']['postalCode']
        #zillow api call
        try:
            #attempt to pull a price from the zillow api
            house_data = zillow_api.GetSearchResults(zillow_key, house, postal_code)
            price = house_data.zestimate.amount
        except:
            #if no zillow price leave empty
            price='$__'

        #add zillow price to address
        addresses.append(f'{street_address}: ${price}')
        #sleep so that we are not pinging api in too rapid of sucession
        time.sleep(.5)
    return addresses


def map_objects():
    #build map with folium library
    map = folium.Map(tiles='Stamen Toner', location=[df['Lat'][0], df['Lon'][0]], zoom_start=10,)
    #build the map based on the address we collected in our dataframe
    for lat,lon,sv_photo,address in zip(df['Lat'],df['Lon'],df['street_view'],df['address_price']):


        encoded = base64.b64encode(open(sv_photo, 'rb').read()).decode()


        #building html for the map
        html = '<img src="data:image/jpeg;base64,{}" >'.format
        resolution, width, height = 75, 50, 25
        iframe = IFrame(html(encoded), width=300, height=600)
        popup = folium.Popup(iframe, max_width=1000)
        #defining marker parameters
        icon = folium.Icon(color="red", icon="home")
        marker = folium.Marker(location=[lat, lon], popup=popup, icon=icon,tooltip=address)
        #add marker to mapp
        marker.add_to(map)
    #save map data
    map.save('multi_map_200.html')
#create dataframe
def final_df():
    batch_list = files_to_process()
    if len(batch_list) > 0:

        df = pd.DataFrame(image_return(batch_list))
        df['address_price']=latlong_to_address(batch_list)
        df.to_csv('../csvs/add_data1',index=False)

        return df
    else:
        pass




df = final_df()
map_objects()
