import logging


logging.basicConfig(
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s:%(message)s",
)


def main():
    logging.info(' sample text ')


main()
