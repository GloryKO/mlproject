import numpy as np
import pandas as pd
import sys
import os
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import  Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from utils import save_object

from exception import CustomException
from logger import logging

class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')

class DataTranformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    
    def get_data_transformer_obj(self):
        try:
            numerical_columns = ["writing_score","reading_score"] #gets all the numerical features 
            categorical_columns =["gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course"]#gets the categorical features
           
            num_pipeline = Pipeline(
                steps =[("imputer",SimpleImputer(strategy="median")),
                        ("sclaer", StandardScaler())
                        ] #handle missing data
                )
            
            cat_pipelines = Pipeline(
                steps =[("imputer",SimpleImputer(strategy="most_frequent"))]
                        ("one_hot_encoder",OneHotEncoder())
                        ("sclaer", StandardScaler())
                )
            logging.info("Numerical and Categorical encoding completed")

            #get the column transformer to combine both numerical and categorical columns
            preprocessor = ColumnTransformer([

                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipeline",cat_pipelines,categorical_columns)

            ])
            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
    

    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("read training data and test data completed")

            preprocessing_obj = self.get_data_transformer_obj()
            target_column_name = "maths_score"
            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df =train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df =test_df[target_column_name]
            
            logging.info(f"Applying preprocessing object on training and testing dataframe")    
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved Preprocessing object")
            save_object(self.data_transformation_config.preprocessor_obj_file_path,preprocessing_obj)

            return (train_arr,test_arr,self.data_transformation_config.preprocessor_obj_file_path)
        
        except Exception as e:
            raise CustomException(e,sys)    
            


