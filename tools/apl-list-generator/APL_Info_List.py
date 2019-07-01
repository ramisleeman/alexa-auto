import json

jsonFileName = "launchRequest.json"


# title, logo, and background image details
title = "Calories in 1 Serving of Cheese"
sources_small_url = "https://d2o906d8ln7ui1.cloudfront.net/images/LT1_Background.png"
sources_large_url = "https://d2o906d8ln7ui1.cloudfront.net/images/LT1_Background.png"
skill_logo = "https://d2o906d8ln7ui1.cloudfront.net/images/cheeseskillicon.png"


#main name of the items
listItems_textContent_primaryText_text = ["name1",\
                                          "name2",\
                                          "name3",\
                                          "name4"]

# secondary name of the items
listItems_textContent_secondaryText_text = [ "distance: 1.2 miles"\
                                            ,"distance: 2.2 miles"\
                                            ,"distance: 2.3 miles"\
                                            ,"distance: 3.2 miles"]


# teritiary name of the items
listItems_textContent_tertiaryText_text = ["Free",\
                                           "$3 an hour",\
                                           "Free",\
                                           "$1 an hour"]

# items image links
listItems_image_sources_small = ["https://d2o906d8ln7ui1.cloudfront.net/images/sm_gouda.png", \
                                 "https://d2o906d8ln7ui1.cloudfront.net/images/sm_gouda.png", \
                                 "https://d2o906d8ln7ui1.cloudfront.net/images/sm_gouda.png", \
                                 "https://d2o906d8ln7ui1.cloudfront.net/images/sm_gouda.png"]


listItems_image_sources_large = ["https://d2o906d8ln7ui1.cloudfront.net/images/sm_gouda.png", \
                                 "https://d2o906d8ln7ui1.cloudfront.net/images/sm_gouda.png", \
                                 "https://d2o906d8ln7ui1.cloudfront.net/images/sm_gouda.png", \
                                 "https://d2o906d8ln7ui1.cloudfront.net/images/sm_gouda.png"]



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
        
        
updateJSON_APL_Document("./" + jsonFileName)