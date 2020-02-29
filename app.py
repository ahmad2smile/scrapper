import requests
import logging

from pageScrapper import getNames, logHere
from bs4 import BeautifulSoup
from time import sleep
from configLogger import setup_logging

setup_logging()

logger = logging.getLogger(__name__)


def getLinks():
    with open("links.txt") as links:
        return [link.strip() for link in links]


def appendToFile(name, data):
    with open("./data/{}.txt".format(name), "a+") as dataFile:
        dataFile.write(data)


def scrape():
    links = getLinks()
    for linkIndex, link in enumerate(links, start=0):
        name = link.split("/")[-1]

        with open("progressLog", "w+") as progressLog:
            page = 1
            while True:
                results = getNames("{}?page={}".format(
                    link, linkIndex), ".inventors")
                progressLog.write("{} {}".format(linkIndex, page))
                if results is None:
                    break
                else:
                    appendToFile(name, "\n".join(results))
                    print("Done page: {}".format(page))
                    page += 1
        logger.info("Done with: {}".format(name))


# scrape()
