import logging

# Configure once
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ],
)


# This is the "Base" function can by used to get a logger in any file
def get_logger(name):
    return logging.getLogger(name)
