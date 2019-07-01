# quick apl list generator



## Steps to reproduce:

1. <launchRequest.json> must be present in the directory
2. Fill the info in the APL_Info_List.py (lines 5 to 42)
3. Run the script.
4. <launchRequest.json> will update accordingly and is ready to be used in the skill directive



## Legend

```python
# title, logo, and background image details
title = "List of charging stations"
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
listItems_image_sources_small = ["https://d2o906d8ln7ui1.cloudfront.net/images/sm_gouda.png",\
"https://d2o906d8ln7ui1.cloudfront.net/images/sm_gouda.png",\                                "https://d2o906d8ln7ui1.cloudfront.net/images/sm_gouda.png",\                                 "https://d2o906d8ln7ui1.cloudfront.net/images/sm_gouda.png"]


listItems_image_sources_large = ["https://d2o906d8ln7ui1.cloudfront.net/images/sm_gouda.png", \                                 "https://d2o906d8ln7ui1.cloudfront.net/images/sm_gouda.png", \                                 "https://d2o906d8ln7ui1.cloudfront.net/images/sm_gouda.png", \                                 "https://d2o906d8ln7ui1.cloudfront.net/images/sm_gouda.png"]

```



![Image description](apl_template.png)