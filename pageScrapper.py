from bs4 import BeautifulSoup
from time import sleep
import requests
import logging

logger = logging.getLogger(__name__)


NOT_FOUND_MSG_SELECTOR = ".wrapper"
NOT_FOUND_MESSAGE = "There are no patents for this"


def getAllTags(page, selector):
    if "." in selector:
        return page.find_all(class_=selector.replace(".", ""))
    elif "#" in selector:
        return page.find_all(id=selector.replace("#", ""))
    return page.find_all(selector)


def isNotFound(page):
    for tag in getAllTags(page, NOT_FOUND_MSG_SELECTOR):
        if NOT_FOUND_MESSAGE in tag.text:
            return True
    return False


def cleanUpTagText(text):
    return text.replace("Inventors:", "").replace("Inventor:", "").strip()


def getNames(link, selector):
    try:
        response = requests.get(link)

        if response.status_code == 404:
            return None

        response.raise_for_status()

        page = BeautifulSoup(response.content, 'html.parser')

        if isNotFound(page):
            return None

        return [cleanUpTagText(tag.text) for tag in getAllTags(page, selector)]
    except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as error:
        logger.error(f"RequestException: {str(error)}")
        logger.error("Retrying in 5 secons")
        sleep(5)
        getNames(link, selector)
