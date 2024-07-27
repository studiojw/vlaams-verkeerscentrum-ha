"""Helper functions for the Verkeerscentrum API."""

import re

from bs4 import BeautifulSoup


def extract_trajectory_id(element: BeautifulSoup) -> str:
    """Extract the trajectory id from the element."""
    details_element = element.find("div", class_="details")
    if details_element is None:
        return None
    return details_element.find("a")["href"].split("/account/traject-")[-1]


def extract_title(element):
    """Extract the title from the element."""
    if element.find(name="h3") is None:
        return None
    return element.find(name="h3").text.strip()


def extract_description(element):
    """Extract the description from the element."""
    if element.find("div", class_="points") is None:
        return None
    return element.find("div", class_="points").text.strip()


def extract_actual_travel_time(element):
    """Extract the actual travel time from the element."""
    regex = r"(\d+) min\."
    travel_time_element = element.find("span", class_="actual-travel-time")
    if travel_time_element is None:
        return None
    match = re.search(regex, travel_time_element.text)
    if match:
        d = int(match.group(1))
    return d


def extract_delay(element):
    """Extract the delay from the element."""
    regex = r"(\d+) min\. vertraging"
    delay_element = element.find("span", class_="text-danger")
    if delay_element is None:
        return None
    match = re.search(regex, delay_element.text)
    if match:
        d = int(match.group(1))
    return d
