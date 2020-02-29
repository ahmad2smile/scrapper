import requests
import logging

from pageScrapper import getNames
from bs4 import BeautifulSoup
from time import sleep
from configLogger import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

PROGRESS_FILE = "progressLog"


def getLinks():
    with open("links.txt") as links:
        return [link.strip() for link in links]


def appendToFile(name, data):
    with open(f"./data/{name}.txt", "a+", encoding="utf-8") as dataFile:
        dataFile.write(data)


def getPreviousProgress():
    with open(PROGRESS_FILE, "r") as progressLog:
        line = progressLog.readline()
        if len(line) == 0:
            return [0, 1]
        return [int(x) for x in line.split(" ")]


def saveNewProgress(linkIndex, page):
    with open(PROGRESS_FILE, "w") as progressLog:
        progressLog.truncate()
        progressLog.write(f"{linkIndex} {page}")


def scrape():
    links = getLinks()

    previousLinkIndex, previousPage = getPreviousProgress()
    page = previousPage + 1  # Pages are 1 indexed

    for linkIndex, link in enumerate(links[previousLinkIndex:]):
        name = link.split("/")[-1]

        while True:
            results = getNames(f"{link}?page={page}", ".inventors")

            if results is None:
                break

            saveNewProgress(linkIndex + previousLinkIndex, page)

            appendToFile(name, "\n".join(results))
            logger.info(f"Link: {name}, Page: {page}")
            page += 1

        page = 1  # Reset for new Link
        logger.info(f"Done with: {name}")


scrape()
