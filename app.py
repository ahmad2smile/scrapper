import requests
import logging
import json

from pageScrapper import getNames
from bs4 import BeautifulSoup
from time import sleep
from configLogger import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

PROGRESS_FILE = "progress.json"


def getLinks():
    with open("links.txt") as links:
        return [link.strip() for link in links]


def appendToFile(name, data):
    with open(f"./data/{name}.txt", "a+", encoding="utf-8") as dataFile:
        dataFile.write(data)


def getPreviousPage(name, link):
    with open(PROGRESS_FILE, "r") as progressLog:
        progress = json.loads(progressLog.read())
        files = progress["files"]

        results = [f for f in files if f["link"] == link]

        linkProgress = results[0] if len(results) > 0 else None

        if linkProgress is None:
            updateLinkPage(name, link, 0)
            return 0
        if bool(linkProgress["isDone"]):
            return None
        return int(linkProgress["page"])


def updateLinkPage(name, link, page, isDone=False):
    with open(PROGRESS_FILE, "r+") as progressLog:
        progress = json.load(progressLog)
        files = progress["files"]
        results = [f for f in files if f["link"] == link]

        linkProgress = results[0] if len(results) > 0 else None

        if linkProgress is None:
            linkProgress = {
                "name": name,
                "page": page,
                "link": link,
                "isDone": isDone
            }

            progress["files"].append(linkProgress)
        else:
            linkProgress["page"] = page
            linkProgress["isDone"] = isDone

        progressLog.seek(0)
        json.dump(progress, progressLog, ensure_ascii=False, indent=4)
        progressLog.truncate()


def generateLinkName(link):
    return link.split(".com/")[-1].replace("/", "_")


def scrape():
    links = getLinks()

    for link in links:
        name = generateLinkName(link)
        previousPage = getPreviousPage(name, link)

        if previousPage is None:
            continue

        page = previousPage

        while True:
            results = getNames(f"{link}?page={page + 1}",
                               ".inventors")  # 1 index based pages

            if results is None:
                break

            updateLinkPage(name, link, page)

            appendToFile(name, "\n".join(results))
            logger.info(f"Link: {name}, Page: {page}")
            page += 1

        page = 0  # Reset for new Link
        logger.info(f"Done with: {name}")
