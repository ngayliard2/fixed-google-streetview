### **ImageGEO: A collaboration between New Light Technologies and General Assembly's Team Street View**

[New Light Technologies](https://www.newlight.com/) (NLT) is an organization founded in 2003 which provides comprehensive information technology solutions for clients in government, commercial, and non-profit sectors, including FEMA (the Federal Emergency Management Agency), the U.S. Census Bureau, and The World Bank.

[Ran Goldblatt](https://www.linkedin.com/in/ran-goldblatt-34365886/), our contact with NLT, is a remote sensing scientist and senior consultant. He has a background in geographic information systems (GIS) and leverages this knowledge when solving problems facing various agencies.

Team Street View is a data science-based team at [General Assembly](https://generalassemb.ly/) (GA). We draw our experiences from a diversity of backgrounds and industry experiences and are collaborating with NLT on a specific task of interest for which we have created a framework and concept for the ImageGEO tool.

Our team is [Hussain Burhani](https://www.linkedin.com/in/hussain-burhani/), [Nick Gayliard](https://www.linkedin.com/in/nick-gayliard/), [Maurie Kathan](https://www.linkedin.com/in/maurie-kathan-17b67040/), and [Zack Stern](https://www.linkedin.com/in/zachary-j-stern/).


###
**Problem statement**

During the recovery phase immediately following a disaster, the Federal Emergency Management Agency (FEMA) performs damage assessment "on the ground" to assess the level of damage caused to residential parcels and to critical infrastructure. To assure an accurate estimation of the damage, it is important to understand the condition of the structures prior to the event.

To help and guide the damage assessment efforts following a disaster and to assist the surveyors identify the structures of interest, this tool (a web-app or a mobile app) will expect to get, as an input, a list of addresses, and retrieve screenshots of the structures from Google Street View. The tool will also include a damage assessment form, which, in addition to relevant information about the level of damage to the structures, will also provide a pre-event photo of the assessed structure.


###
**Usage scenario**

Samantha is a disaster assessment agent at FEMA heading to the field, days after a disaster. Her office is short on resources and all she has with her is a smart phone. Yet she has been tasked to quickly scan the disaster zone and assess the damage to residential property.

She jumps out of her truck, starts walking the street, and sees the first house in disrepair. She pulls out her phone, opens the ImageGEO app, and takes a photograph facing the house. Upon taking the photograph she sees a page displaying the photo she took, the image of the home prior to the disaster, a map location, a value estimate of the house, as well as pertinent information regarding number of stories, bedrooms, and square footage, to give the complete summary of that particular property.

At the backend, each photograph she takes is stored, along with the summary information, and available to be accessed at a later time or when web connectivity is available again. However, ideally, even with limited web connectivity, a low-resolution image can be uploaded directly in real-time to the disaster response team at the home office. This data can be aggregated to assess total damage and real-time statistics can be relayed to appropriate agencies for assessment, disaster management, and appropriation purposes.

In addition, the information collated can be sent to insurance companies, the tool made accessible for crowd-sourcing to allow individuals to self-report information, or simply be used through entering address information to gather pre-disaster summaries for the property.

![Alt Text](./Images/website_gif.gif)

###
**Under the hood**

Currently, ImageGEO is in its development stage, built as a web app using Python, associated APIs, and the Flask/Dash web framework. Two different instances have been developed showcasing the variations in user experience, to use in future A/B testing.

The basic steps that we are using in both Flask and Dash are:

<span style="text-decoration:underline;">Step one: Loading data</span>

There are two formats to collect location information from users. First, an address can simply be entered into the tool as a text input by the user. The second, and ideal interface, is to use the app is by uploading photos that contain exif data (also known as metadata).  The app can accept single photos or batch process a folder of photos.  The photo upload and information gathering process takes place using the following steps.

<span style="text-decoration:underline;">Step two: Extracting location data from smartphone photos:</span>

We extract the [exif](https://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/EXIF.html) data from photographs using an existing Python library called [exifread](https://pypi.org/project/ExifRead/). The pertinent information that is most useful for geolocation include internal parameters called GPS-Longitude, GPS-Latitude, and GPS-ImgDirection. For the app to work, as intended, location services for the phones internal photo app must be active.  Additionally, the heading direction data is key to pinpointing the house that the user is facing in the field.   

<span style="text-decoration:underline;">Step three: Getting the address from location data</span>

The exif data is formatted we call the Google Street View API based using location and heading from the previous step.The Google streetview photo is saved to a local directory.

We use the [geopy](https://geopy.readthedocs.io/en/stable/) library to connect to the  [Bing Maps](https://www.bing.com/maps) api and convert our convert the latitude and longitude information to valid street address of a particular house.

<span style="text-decoration:underline;">Step four: Pull Zillow information for the property</span>

With the address of the house we can now query a host of databases for summary information for the home. We specifically query the Zillow API to pull Zillow property price estimate and other basic information to summarize pre and post disaster information on the property of interest.

<span style="text-decoration:underline;">Web-deployment:</span>

Input: The ImageGEO tool is built in two different instances, one primarily using the Flask framework and the other Dash. A page first accepts a photo image to be uploaded or an address (if already known). We also ask some basic questions of the assessor about the damage to the property in the form of some multiple choice and open ended questions.

Output: We are using the above functionality to return side by side photos of pre and post disaster pictures, the Google Street View photo, as well as the address and summary information, including valuation/pricing, from Zillow.

For the second implementation that we developed using the Dash framework, a table of information is created that displays all the collected information (lat, lon, address, street view image file location, address of the property and Zillow estimate.  That same information is also placed on a map.  The pins on the map can be hovered over to view the address and zillow price information or the pin can be clicked on to display the street view photo that was collected.  

##
**Library Requirements**  
flask, geopy, zillow, exifread, flask_wtf, wtforms, dash, geopy, folium, base64, IPython.display

In order to run you also must have an api key for GoogleStreetView, Bing and Zillow. All are free and open to public.


###
**Data**

ImageGEO is currently deployed as a concept and is in development.

The photo tool captures

*   Input image (photo taken by agent)
*   Google Street View photo
*   Address of the property
*   Property Latitude and Longitude
*   Zillow Price Estimate
*   User imputed information
    *   Disaster identifier
    *   Main Building Damaged/Undamaged
    *   Outer Building Damaged/Undamaged
    *   Exterior Damage Yes/No
    *   Interior Damage Yes/No
    *   Percentage of Damage

The Address tool captures

*   Google Street View photo
*   Address of the property
*   Property Latitude and Longitude
*   Zillow Price Estimate

The Dash tool captures

*   Input image (photo taken by agent)
*   Google Street View photo
*   Address of the property
*   Property Latitude and Longitude
*   Zillow Price Estimate

###
**Further improvements**

*   Deploy as a stand-alone app
*   Cross-platform functionality. The photo capture currently only works with Iphones.
*   Collaborate with UX/Web-dev teams to enhance user experience
*   SQL Integration
*   Build in better error handling for location mismatch
    *   Using image matching to confirm that the photo matches the google street view that is being pulled.
    *   Incorporating heading into street address query, so that we make sure it is getting the address from the correct side of the street.
*   Formal collaborations with Zillow and Google corporate citizenship teams
*   Adding satellite image integration into image output
*   Currently this only works if there is a google street view for that property prior. This is a consideration that needs to be thought about. Perhaps using alternative mapping tools in that situation.

###
**Summary**

[Slideset](./slides/teamstreetview_slides.pdf) presented at General Assembly on January 18, 2019.

*   Inspiration
*   Usage scenario
*   Live demonstration
*   Under the hood
*   Further improvements
*   Takeaways
