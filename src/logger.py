import logging
import os
from datetime import datetime

log_dir=os.path.join(os.getcwd(),'logs')
os.makedirs(log_dir,exist_ok=True)
log_file=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_path=os.path.join(log_dir,log_file)
logging.basicConfig(
    filename=log_path,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)