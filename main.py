import logging


from screen import generate_screen 
from datetime import datetime
from pathlib import Path

def get_logger():
    now = datetime.now()
    LOG_EXEC_DIR = Path("./logs").joinpath(
        str(now.year), str(now.month), str(now.day)
    )
    LOG_EXEC_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE_NAME = "log_file.log"
    LOG_FILE = LOG_EXEC_DIR.joinpath(LOG_FILE_NAME)

    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
        level=logging.ERROR,
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=LOG_FILE,
        filemode='a'
    )

    # esse handler exibi as mensagens de log no console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Adiciona o handler ao logger
    logger = logging.getLogger('gerenciador_recursos')
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)

    return logger


logger = get_logger()

if __name__ == '__main__':
    generate_screen(logger)