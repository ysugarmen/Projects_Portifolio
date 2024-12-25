# Amplify API URL and authentication
API_CAMPAIGN_URL = "https://api.outbrain.com/amplify/v0.1/campaigns?extraFields=CustomAudience,Locations,InterestsTargeting,BidBySections,BlockedSites,PlatformTargeting,CampaignOptimization,Scheduling,IABCategories,CampaignPixels"
API_CONVERSION_URL = "https://api.outbrain.com/amplify/v0.1/marketers/0074749fbabdd20da461caca578b8ec365/conversionEvents"
API_BUDGET_URL = "https://api.outbrain.com/amplify/v0.1/marketers/0074749fbabdd20da461caca578b8ec365/budgets?detachedOnly=detachedOnly"
API_KEY = 'MTczMjg3NzYyMzQyOTowNzYwNjM5MjVkMTA0OTk2MzA2NWJkZGE4Y2U5N2I4OWE2ZDAwZDFjMDhiYWI2ZDg5MzZlZTliNzgzNjQzOWU2OnsiY2FsbGVyQXBwbGljYXRpb24iOiJBbWVsaWEiLCJpcEFkZHJlc3MiOiIvMTAuMjEyLjQ0LjEwNDo1MDg4MiIsImJ5cGFzc0FwaUF1dGgiOiJmYWxzZSIsInVzZXJOYW1lIjoiaGFyZWxrQGdtYWlsLmNvbSIsInVzZXJJZCI6IjEwNjcxMzk0IiwiZGF0YVNvdXJjZVR5cGUiOiJNWV9PQl9DT00ifTowMTE0YWYxYWVmYjE4NmFlZDhjZDg1YWE4OTAzODMwNmYxODI5NjIzOWE1ZTQ1YTM5ODZhY2U0MDljMmMwOGJhZGMxOWNiYzZlODhkYTlhYWQyYmY4ODhlYWI4ZmE2MzZjMzFhNzczNjIzMWFlY2ZmZDU4ODM5ZjZiNjkzYjExNQ=='  # Replace with your API key
HEADERS = {
    'Content-Type': 'application/json',
    'OB-TOKEN-V1': API_KEY
}
CAMPAIGNS_DATA_FILE_PATH = "/Users/yonatansugarmen/Desktop/Documents/Outbrain_Campaign_Creation/CampaignsData.xlsx"
PROMOTED_LINKS_DATA_FILE_PATH = "/Users/yonatansugarmen/Desktop/Documents/Outbrain_Campaign_Creation/PromotedLinksData.xlsx"
API_PROMOTED_LINKS_URL = "https://api.outbrain.com/amplify/v0.1/campaigns/"
PROMOTED_LINKS_HEADERS = {
    'Content-Type': 'application/json',
    'AMPLIFY-REQUEST-ID': 'f505a184-dc50-4648-83c8-db8e17c8a466',
    'OB-TOKEN-V1': API_KEY
}

CAMPAIGN_TEMPLATE = {
    'name': None,
    'enabled': True,
    'budgetId': None,
    'targeting': None,
    'suffixTrackingCode': "EMPTY_SUFFIX",
    'feeds': [],
    'startHour': None,
    'onAirType': "StartHour",
    'campaignOptimization': {
        'optimizationType': "MAX_CONVERSION_FULLY_AUTOMATED",
        'targetConversionId': "00e2bd0b1b5f004652b8b25d44be09b576",
    },
    'objective': "Conversions",
    'creativeFormat': "Standard"
}


BUDGET_TEMPLATE = {
 "name": None,
 "amount": 50,
 "startDate": None,
 "endDate": None,
 "runForever": True,
 "pacing": "AUTOMATIC",
 "type": "DAILY"
}

TARGETING_TEMPLATE = {
    "platform": None,
    "language":"en", #const for now
        "locations": [
            "fc4deb5112fb4415a9edacdf4aafb0d8" #const= "US"
        ],
        "operatingSystems": [ #check for more
            "MacOs",
            "Windows"
        ],
        "browsers": [ #check for more
            "Chrome"
        ]
}

PROMOTED_LINK_TEMPLATE = {
    'metaData': None,
    'text': None,
    'url': None,
    'enabled': True,
    'sectionName': 'Search Ads',
    'imageMetadata': {
        'url': None
    },
    'callToAction': 'LEARN_MORE'
}


TEST_CAMPAIGN_DATA = {

    "name": "test - campaign",
    "enabled": True,
    "budgetId": "005842f8752af596d929f7ed016ba41a94",
    "targeting": {
        "platform": [
            "DESKTOP"
        ],
        "language": "en",
        "locations": [
            "fc4deb5112fb4415a9edacdf4aafb0d8"
        ],
        "operatingSystems": [
            "MacOs",
            "Windows"
        ],
        "browsers": [
            "Chrome"
        ]
    },
    "suffixTrackingCode": "EMPTY_SUFFIX",
    "feeds": [],
    "startHour": "12:20 PM",
    "onAirType": "StartHour",
    "campaignOptimization": {
        "optimizationType": "MAX_CONVERSION_FULLY_AUTOMATED",
        "targetConversionId": "00e2bd0b1b5f004652b8b25d44be09b576"
    },
    "objective": "Conversions",
    "creativeFormat": "Standard",
}
