import os

import requests


def scrape_linkedin_profile(linkedin_profile_url: str) -> dict:
    """
    scrape information from Linkedin Profiles,
    manually scrape information from a linkedin in profile
    """

    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    header_dict = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}

    response = requests.get(
        api_endpoint, params={"url": linkedin_profile_url}, headers=header_dict
    )
    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", None) and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
    return data
