import pandas as pd
import config
import requests
from datetime import datetime


def main(campaigns_file_path, promoted_links_file_path, logger):
    logs = []
    logger.info("Starting Outbrain Campaign Creation")
    logs.append("Starting Outbrain Campaign Creation")
    
    config.CAMPAIGNS_DATA_FILE_PATH = campaigns_file_path
    config.PROMOTED_LINKS_DATA_FILE_PATH = promoted_links_file_path
    
    campaigns_dataframes, campaigns_dict = import_campaigns_data(config.CAMPAIGNS_DATA_FILE_PATH)
    campaigns_dict = create_campaigns(campaigns_dataframes, campaigns_dict, logger, logs)
    
    promoted_links_df = pd.read_excel(config.PROMOTED_LINKS_DATA_FILE_PATH)
    for campaign, campaign_id in campaigns_dict.items():
        filtered_rows = promoted_links_df[promoted_links_df['Campaign Name'] == campaign]
        create_promoted_links(campaign_id, filtered_rows, logger, logs)
    
    logs.append("Outbrain Campaign Creation Completed")
    logger.info("Outbrain Campaign Creation Completed")
    
    # Filter relevant logs
    relevant_logs = [log for log in logs if "Campaign" in log or "Promoted Link" in log]
    return relevant_logs



def create_campaigns(campaigns_dataframes, campaigns_dict, logger, logs):
    for campaign in campaigns_dataframes:
        response = requests.post(config.API_CAMPAIGN_URL, json=campaign, headers=config.HEADERS)
        log_message = f"Campaign '{campaign['name']}': {response.status_code} - {response.text}"
        logger.info(log_message)
        logs.append(log_message)
        if response.status_code == 200:
            campaigns_dict[campaign['name']] = response.json()['id']
        else:
            error_message = f"Error creating campaign '{campaign['name']}': {response.text}"
            logger.error(error_message)
            logs.append(error_message)
    return campaigns_dict


def import_campaigns_data(excel_file_path):
    df = pd.read_excel(excel_file_path)
    df = df.fillna('')
    campaigns_dataframes = []
    campaigns_dict = {}
    for _, row in df.iterrows():
        new_campaign = config.CAMPAIGN_TEMPLATE.copy()
        campaign_name = row['Campaign Name']
        new_campaign['name'] = campaign_name
        budget_start_date = datetime.now().strftime('%Y-%m-%d')
        budget_end_date = None
        budget_id = create_budget_object(campaign_name, budget_start_date, budget_end_date)
        if not budget_id:
            print(f"Error creating budget for campaign {campaign_name}")
            continue
        new_campaign['budgetId'] = budget_id
        platform_value = row['Platforms']
        platform_list = [platform.strip() for platform in platform_value.split(',')]
        new_campaign['targeting'] = create_targeting_object(platform_list)
        new_campaign['startHour'] = datetime.now().strftime('%I:%M %p')
        campaigns_dict[campaign_name] = None
        campaigns_dataframes.append(new_campaign)
    return campaigns_dataframes, campaigns_dict


def create_budget_object(campaign_name, start_date, end_date):
    new_budget = config.BUDGET_TEMPLATE.copy()
    new_budget['name'] = campaign_name + '_budget'
    new_budget['startDate'] = start_date
    new_budget['endDate'] = end_date
    response = requests.post(config.API_BUDGET_URL, json=new_budget, headers=config.HEADERS)
    if response.status_code == 200:
        budget_id = response.json()['id']
        print(f"Budget {new_budget['name']} created")
        return budget_id
    else:
        print(f"Error creating budget: {new_budget['name']} - {response.status_code}: {response.text}")
        return None


def create_targeting_object(platform_list):
    new_targeting = config.TARGETING_TEMPLATE.copy()
    new_targeting['platform'] = platform_list
    return new_targeting


def create_promoted_links(campaign_id, promoted_links_df, logger, logs):
    for _, row in promoted_links_df.iterrows():
        new_promoted_link = config.PROMOTED_LINK_TEMPLATE.copy()
        new_promoted_link['metaData'] = row['adName']
        new_promoted_link['text'] = row['text']
        new_promoted_link['url'] = row['url']
        new_promoted_link['imageMetadata']['url'] = row['picture file']
        request_url = config.API_PROMOTED_LINKS_URL + f'{campaign_id}/promotedLinks'
        response = requests.post(request_url, json=new_promoted_link, headers=config.PROMOTED_LINKS_HEADERS)
        log_message = f"Promoted Link '{new_promoted_link['text']}': {response.status_code} - {response.text}"
        logger.info(log_message)
        logs.append(log_message)
