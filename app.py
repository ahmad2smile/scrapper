import multiprocessing as mp

from configLogger import setup_logging
from links_setup import getLinks, start_link

setup_logging()


def main():

    pool = mp.Pool(mp.cpu_count())

    links = getLinks()
    pool.map(start_link, links)
    pool.close()


if __name__ == "__main__":
    main()
