import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.feature_extraction import DictVectorizer
from src.exception import CustomException
from src.logger import logging
import os
from src.utilis import saved_obj
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', "preprocessor.pkl")
    dict_vectorizer_obj_file_path = os.path.join('artifacts', "dict_vectorizer.pkl")
class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_columns = ['age', 'education', 'cigsperday', 'totchol', 'bmi', 'heartrate', 'glucose']
            categorical_columns = ['male', 'currentsmoker', 'bpmeds', 'prevalentstroke', 'prevalenthyp', 'diabetes']

            num_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="mean")),
                ("scaler", StandardScaler())
            ])

            cat_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder", OneHotEncoder(handle_unknown="ignore")),
                ("scaler", StandardScaler(with_mean=False))
            ])

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            logging.info("Reading train and test datasets")
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            # Standardize column names
            train_df.columns = [col.lower() for col in train_df.columns]
            test_df.columns = [col.lower() for col in test_df.columns]

            logging.info("Standardizing column names and validating data")
            target_column_name = "tenyearchd"
            numerical_columns = ['age', 'education', 'cigsperday', 'totchol', 'bmi', 'heartrate', 'glucose']
            categorical_columns = ['male', 'currentsmoker', 'bpmeds', 'prevalentstroke', 'prevalenthyp', 'diabetes']

            # Validate columns
            # missing_columns = [col for col in numerical_columns + categorical_columns + [target_column_name] if col not in train_df.columns]
            # if missing_columns:
            #     raise CustomException(f"Missing columns in training data: {missing_columns}", sys)

            logging.info("Obtaining preprocessing object")
            preprocessing_obj = self.get_data_transformer_object()

            # Separate features and target
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            # Transform features
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            # Save objects
            logging.info("Saving preprocessing object and DictVectorizer")
            saved_obj(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (
                np.c_[input_feature_train_arr, target_feature_train_df.to_numpy()],
                np.c_[input_feature_test_arr, target_feature_test_df.to_numpy()],
                self.data_transformation_config.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomException(e, sys)

