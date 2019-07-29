from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import AddressForm, PhotoForm, SurveyForm
from app.functions import get_coordinates, latlong_to_address, zillow_pull
from app.api_keys import bing_key, zillow_key, google_key
from geopy import geocoders
import zillow
import os
import requests
import re
import exifread
import pandas as pd

@app.route('/')

#creating flask page for photo imput
@app.route('/index', methods=['GET', 'POST'])
def photoaddress():
    #adding a form for imputting a photo
    form = PhotoForm(csrf_enabled = False)
    #When submit has clicked
    if form.validate_on_submit():
        #defininging photo as imputed photo
        photo = form.photo.data
        #create file path
        filename = photo.filename.replace(' ', '')

        basepath = os.path.abspath('app/')

        photo.save(f'/{basepath}/uploads/{filename}')
        upload_filepath = f'/{basepath}/uploads/{filename}'
        # run lat_long / heading function, streetview function, and zillow function

        address = latlong_to_address(f'{basepath}/uploads/{filename}')

        price = zillow_pull(address)
        address = address['name']

        # Set image_url to Google Street View of address

## Get coordinates and pull street view with coords and heading
        coords = get_coordinates(f'{basepath}/uploads/{filename}')

        heading = coords[1]
        coords = coords[0]

        image_url = f'https://maps.googleapis.com/maps/api/streetview?size=600x600&location={coords[0]}, {coords[1]}&heading={heading}&key={google_key}'


        # Image path handling
        image = requests.get(image_url)

        filelist = re.findall(r'\w+', address)
        filename2 = ''.join(filelist)
        final_path = f'{basepath}/uploads/{filename2}.jpg'
        open(f'{final_path}', 'wb').write(image.content)


        # redirect to photo_form page
        return redirect(url_for('surveyform', price = price, address = address, goog_photo = f'{filename2}.jpg', filename = filename, coords = coords, basepath = basepath))

        # return render_template('photo_form.html', form=SurveyForm(), filename = filename, address = address, price = price, goog_photo = f'{filename2}.jpg')

    return render_template('index.html', form=form)

#building text to address page
@app.route('/textaddress', methods=['GET', 'POST'])
def textaddress():
    #adding form that accepts address
    form = AddressForm()

    # text to address and value form
    if form.validate_on_submit():

        address = form.address.data

        # bing address grabber
        bing_locator = geocoders.Bing(bing_key)
        address = bing_locator.geocode(address).raw

        # Zillow call (could be replaced with Zillow function)
        zillow_api = zillow.ValuationApi()
        house = address['address']['addressLine']
        postal_code = address['address']['postalCode']

        house_data = zillow_api.GetSearchResults(zillow_key, house, postal_code)
        price = house_data.zestimate.amount

        # set address back to street address and zip code
        address = address['name']


        ### START GOOGLE STREET VIEW IMAGE HANDLING ###

        # Set image_url to Google Street View of address

        image_url = f'https://maps.googleapis.com/maps/api/streetview?size=600x600&location={address}&key={google_key}'

        # Image write out to uploads folder
        image = requests.get(image_url)

        basepath = os.path.abspath('app/')
        filelist = re.findall(r'\w+', address)
        filename = ''.join(filelist)
        final_path = f'{basepath}/uploads/{filename}.jpg'
        open(f'{final_path}', 'wb').write(image.content)


        # render template with passed variables when form validates
        return render_template('text_form.html', title = 'Output', price = price, address = address, file_path = f'{filename}.jpg', photo = open(f'{final_path}', 'rb'))

    #keep same page with form if form does not validate
    return render_template('textaddress.html', title='Submit Address', form=form)

#routing to the survey form after the image upload
@app.route('/photo_form', methods=['GET', 'POST'])
def surveyform():

    form = SurveyForm(csrf_enabled = False)

    if form.validate_on_submit():
        # data collection form
        notes = form.extranotes.data
        dropdown = form.dropdown.data
        multiple = form.multiple.data
        single = form.singletext.data
        outer = form.outer.data
        exterior = form.exterior.data
        interior = form.interior.data




        # add to csv
        #basepath = os.path.abspath('app/')
        #df = pd.read_csv(f'{basepath}/uploads/house_data.csv')
        #temp_df = pd.DataFrame([[filename, goog_photo, coords, address, price, dropdown, multiple, single, outer, exterior, interior, notes]], columns = df.columns)
        #df = df.append(temp_df)
        #df.to_csv(f'{basepath}/uploads/house_data.csv')


        # unnecessary to redirect, but should be able to
        # return redirect(url_for('testformresponse', dropdown = dropdown, single = single))

        # render template with variables from this form
        return render_template('testformresponse.html', dropdown = dropdown, single = single, multiple = multiple, outer = outer, exterior = exterior, interior = interior, notes = request.args.get('notes'), price = request.args.get('price'), address = request.args.get('address'), goog_photo = request.args.get('goog_photo'), filename = request.args.get('filename'), coords = request.args.get('coords')) # singletext = singletext) #, multiple = multiple)

    # render template with passed variables from photo entry page
    return render_template('photo_form.html', form=form, price = request.args.get('price'), address = request.args.get('address'), goog_photo = request.args.get('goog_photo'), filename = request.args.get('filename'), coords = request.args.get('coords'))


# Build same form page for text address

#@app.route('/text_form', methods=['GET', 'POST'])
#def photo():




# Don't need to make a separate page here, render template works

#@app.route('/testformresponse', methods=['GET', 'POST'])
#def testformresponse():
#    return render_template('testformresponse.html', dropdown = request.args.get('dropdown'), single = request.arges.get('single'), 302)
