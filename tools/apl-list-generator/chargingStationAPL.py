#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 10:24:33 2019

@author: aborami
"""
import requests, json

jsonFileName = "launchRequest.json"



def getLogoSmall(name):
    name = name.lower()
    name = name.split(" ")[0]
    if name in "blink":
        return "https://apl-resources-skill.s3.amazonaws.com/blink.png"
    if name in "chargepoint":
        return "https://apl-resources-skill.s3.amazonaws.com/chargePoint.jpg"
    if name in "evgo":
        return "https://apl-resources-skill.s3.amazonaws.com/evgo.png"

    
def getLogoLarge(name):
    name = name.lower()
    name = name.split(" ")[0]
    if name in "blink":
        return "https://apl-resources-skill.s3.amazonaws.com/blink.png"
    if name in "chargepoint":
        return "https://apl-resources-skill.s3.amazonaws.com/chargePoint.jpg"
    if name in "evgo":
        return "https://apl-resources-skill.s3.amazonaws.com/evgo.png"

    
def load_apl_document(file_path):
    with open(file_path) as f:
        return json.load(f)


def updateJSON_APL_Document(json_file):
    if ".json" in json_file:
        returned_JSON = load_apl_document("./" + json_file)
    else:
        returned_JSON = load_apl_document("./" + json_file + ".json")
        json_file = json_file + ".json"
    
    assert (len(listItems_textContent_primaryText_text) == \
            len(listItems_textContent_secondaryText_text) == \
            len(listItems_textContent_tertiaryText_text)==\
            len(listItems_image_sources_small)== \
            len(listItems_image_sources_large)), "size input mismatch for the list details"
    
    numberOfElements = len(listItems_textContent_primaryText_text)
            
    returned_JSON["listTemplate1Metadata"]["title"] = title
    returned_JSON["listTemplate1Metadata"]["logoUrl"] = skill_logo
    returned_JSON["listTemplate1Metadata"]["backgroundImage"]["sources"][0]["url"] = sources_small_url
    returned_JSON["listTemplate1Metadata"]["backgroundImage"]["sources"][1]["url"] = sources_large_url
    returned_JSON["listTemplate1ListData"]["totalNumberOfItems"] = numberOfElements
    
    for index in range(numberOfElements):
        returned_JSON["listTemplate1ListData"]["listPage"]["listItems"][index]["listItemIdentifier"] = listItems_textContent_primaryText_text[index].lower()
        returned_JSON["listTemplate1ListData"]["listPage"]["listItems"][index]["textContent"]["primaryText"]["text"] = listItems_textContent_primaryText_text[index]
        returned_JSON["listTemplate1ListData"]["listPage"]["listItems"][index]["textContent"]["secondaryText"]["text"]= listItems_textContent_secondaryText_text[index]
        returned_JSON["listTemplate1ListData"]["listPage"]["listItems"][index]["textContent"]["tertiaryText"]["text"]= listItems_textContent_tertiaryText_text[index]
        returned_JSON["listTemplate1ListData"]["listPage"]["listItems"][index]["image"]["sources"][0]["url"] = listItems_image_sources_small[index]
        returned_JSON["listTemplate1ListData"]["listPage"]["listItems"][index]["image"]["sources"][1]["url"] = listItems_image_sources_large[index]

    with open(json_file, 'w', encoding='utf-8') as outfile:
        json.dump(returned_JSON, outfile, ensure_ascii=False, indent=2)
        
        
    
def chargingStationAPL_Info(jsonResponse):

    lengthOfResponse = len(jsonResponse["fuel_stations"])  
    # title, logo, and background image details
    title = "Charging Stations Nearby"
    sources_small_url = "https://d2o906d8ln7ui1.cloudfront.net/images/LT1_Background.png"
    sources_large_url = "https://d2o906d8ln7ui1.cloudfront.net/images/LT1_Background.png"
    skill_logo = "https://apl-resources-skill.s3.amazonaws.com/mainLogo.jpg"
    
    listItems_textContent_primaryText_text = []
    listItems_textContent_secondaryText_text = []
    listItems_textContent_tertiaryText_text = []
    listItems_image_sources_small = []
    listItems_image_sources_large = []
    
    for index in range(lengthOfResponse):
        #main name of the items
        listItems_textContent_primaryText_text.append(
                jsonResponse["fuel_stations"][index]["station_name"] +
                " -  " + 
                jsonResponse["fuel_stations"][index]["ev_network"])
        
        # secondary name of the items
        listItems_textContent_secondaryText_text.append(
                "distance: %g miles" % jsonResponse["fuel_stations"][index]["distance"])
        
        
        # teritiary name of the items
        listItems_textContent_tertiaryText_text.append(jsonResponse["fuel_stations"][index]["ev_pricing"])
        
        # items image links
        listItems_image_sources_small.append(getLogoSmall(jsonResponse["fuel_stations"][index]["ev_network"]))   
        listItems_image_sources_large.append(getLogoLarge(jsonResponse["fuel_stations"][index]["ev_network"]))

    return (title, sources_small_url, sources_large_url, skill_logo, listItems_textContent_primaryText_text,\
            listItems_textContent_secondaryText_text, listItems_textContent_tertiaryText_text,\
            listItems_image_sources_small, listItems_image_sources_large)



link = "https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?fuel_type=ELEC&latitude=37.517309&longitude=-122.049265&limit=4&ev_connector_type=J1772&api_key=Sg4vfBlIiOk6hFUNYk8BYZU0h1MDwieRjBzK2s9j"
API_Response = requests.get(link)
jsonResponse = API_Response.json()

title, sources_small_url, sources_large_url, skill_logo, listItems_textContent_primaryText_text,\
                listItems_textContent_secondaryText_text, listItems_textContent_tertiaryText_text, \
                listItems_image_sources_small, listItems_image_sources_large = chargingStationAPL_Info(jsonResponse)


updateJSON_APL_Document("./" + jsonFileName)
