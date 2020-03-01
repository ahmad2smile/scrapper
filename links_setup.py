import logging

from progress_setup import getLinkPreviousPage, updateLinkPage, queue_progress_data
from page_scrapper import getNamesInPage
from files_setup import appendToFile

logger = logging.getLogger(__name__)


def getLinks():
    with open("links.txt") as links:
        return [link.strip() for link in links]


def generateLinkName(link):
    return link.split(".com/")[-1].replace("/", "_")


def start_link(link):
    name = generateLinkName(link)
    previousPage = getLinkPreviousPage(name, link)

    if previousPage is None:
        return None

    page = previousPage

    while True:
        results = getNamesInPage(f"{link}?page={page + 1}",
                                 ".inventors")  # 1 index based pages

        if results is None:
            break

        queue_progress_data(name, link, page, False)

        updateLinkPage()

        appendToFile(name, "\n".join(results))
        logger.info(f"Link: {name}, Page: {page}")
        page += 1

    queue_progress_data(name, link, page, True)
    page = 0  # Reset for new Link
    logger.info(f"Done with: {name}")
