import logging
import os


class Logger:
    def __init__(self, name, level):

        name = f"{name}.log"
        os.makedirs(os.path.join("/", "app/invoice-app", "logs"), exist_ok=True)

        file_path = os.path.join("/", "app/invoice-app", "logs", name)
        print(f"Attempting to create log at: {file_path}")


        logger = logging.getLogger(name)
        logger.setLevel(level)

        if not logger.hasHandlers():
            formatter = logging.Formatter(
                "%(asctime)s: %(name)s: [%(levelname)s]: %(message)s"
            )

            file_handler = logging.FileHandler(file_path)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
        
        
        self.logger = logger