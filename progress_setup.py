import json

from queue import Queue


progressQueue = Queue()

PROGRESS_FILE = "progress.json"


def queue_progress_data(name, link, page, isDone):
    progressQueue.put(json.dumps({"name": name, "link": link,
                                  "page": page, "isDone": isDone}))


def getLinkPreviousPage(name, link):
    with open(PROGRESS_FILE, "r") as progressLog:
        progress = json.loads(progressLog.read())
        files = progress["files"]

        results = [f for f in files if f["link"] == link]

        linkProgress = results[0] if len(results) > 0 else None

        if linkProgress is None:
            queue_progress_data(name, link, 0, False)
            updateLinkPage()
            return 0
        if bool(linkProgress["isDone"]):
            return None
        return int(linkProgress["page"])


def updateLinkPage():
    queueData = json.loads(progressQueue.get())
    name = queueData["name"]
    link = queueData["link"]
    page = queueData["page"]
    isDone = queueData["isDone"]

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
