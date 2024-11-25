import os
import sys
from dataclasses import dataclass
import pandas as pd
from sklearn.model_selection import train_test_split
from src.exception import CustomException
from src.logger import logging
from src.components.data_transformation import DataTransformationConfig
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_trainer import  ModelTrainerConfig

@dataclass
class DataIngestionConfig:
    # Paths for storing the data
    train_data_path: str = os.path.join("artifacts", 'train.csv')
    test_data_path: str = os.path.join("artifacts", 'test.csv')
    raw_data_path: str = os.path.join("artifacts", 'data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Started data ingestion process.")
        try:
            # Read the raw data
            df = pd.read_csv(r'D:\Projects\Heart-Disease-Prediction\Heart--Disease-Prediction\notebook\Data\framingham.csv')
            logging.info("Read the dataset as a DataFrame.")
    

            # Create directories for storing data if they don't exist
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            # Save raw data for reproducibility
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info(f"Raw data saved at {self.ingestion_config.raw_data_path}.")

            # Split the dataset into train and test sets
            df_full_train, df_test = train_test_split(df, test_size=0.20, random_state=1)
            df_train, df_val = train_test_split(df_full_train, test_size=0.25, random_state=1)
            logging.info(f"Data split into train ({len(df_train)}), validation ({len(df_val)}), and test ({len(df_test)}) sets.")

            # Save the train and test data
            df_train.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            df_test.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info(f"Train and test data saved at {self.ingestion_config.train_data_path} and {self.ingestion_config.test_data_path}.")

            logging.info("Data ingestion process completed successfully.")

            return self.ingestion_config.train_data_path, self.ingestion_config.test_data_path

        except Exception as e:
            logging.error(f"Error occurred during data ingestion: {str(e)}")
            raise CustomException(e, sys)

if __name__ == '__main__':
    # Data Ingestion
    obj = DataIngestion()
    train_data_path, test_data_path = obj.initiate_data_ingestion()

    # Data Transformation
    data_transformation = DataTransformation()
    train_arr, test_arr, preprocessor_path = data_transformation.initiate_data_transformation(
        train_data_path, test_data_path
    )
    logging.info("Data transformation completed successfully.")

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))
