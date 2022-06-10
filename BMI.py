import pandas as pd
import logging
import yaml
import json
import os
import sys

class BMI:
      def __init__(self, config_yaml = None):
          self.yaml_data = self.READ_YAML_FN(config_yaml)

      def MEASUREMENT_SYSTEM_CHECK_FN(self, measurement_type):
          """
          Check if the defiend measurement systems implemented in our script
          weight can be measured in "lb", "g" or "kg" and
          height in "cm", "mm", "in" or "m".
          if we have both unknown weight and height measurement system then output of the function is -5.
          if we have only unknown weight measurement system then output of the function is -5.1.
          if we have only unknown height measurement system then output of the function is -5.2.
          In the case we have know system for both weight and height then output is 0.  
          """
          if   not (str(measurement_type[0]).lower() in ["lb", "g", "kg"]) and not (str(measurement_type[1]).lower() in ["cm", "mm", "in", "m"]):
               logging.error('BMI_FN: unknown weight and height measurement systems: ' + str(measurement_type) )
               error = -5
          elif not (str(measurement_type[0]).lower() in ["lb", "g", "kg"]):
               logging.error('BMI_FN: unknown weight measurement system, weight measurement system: ' + str(measurement_type[0]) )
               error = -5.1
          elif not (str(measurement_type[1]).lower() in ["cm", "mm", "in", "m"]):
               logging.error('BMI_FN: unknown height measurement system, hight  measurement system: ' + str(measurement_type[1]) )
               error = -5.2
          else:
               error = 0
          return error      
 
      def CONVERT_TO_METRIC_SYSTEM_FN(self, weight, height, measurement_type = ["kg", "cm"]):
          """
          based on measurement system we convert weight in kg and height in meter.
          """
          if   str(measurement_type[0]).lower() == "lb":
               weight = weight * 0.45359237
          elif str(measurement_type[0]).lower() == "g":    
               weight = weight / 1000 
          elif str(measurement_type[0]).lower() == "kg":    
                  pass
    
          if   str(measurement_type[1]).lower() == "cm":
               height = height / 100
          elif str(measurement_type[1]).lower() == "mm":
               height = height / 1000
          elif str(measurement_type[1]).lower() == "in":
               height = height * 0.0254 
          elif str(measurement_type[1]).lower() == "m":
               pass
          return weight, height

      def IS_NUMBER_FN(self, x):
          """
          if the input of the function is float or integer then output is True
          and otherwise is False.
          Therefore, it is check is the input is the number or not, for example, string
          """
          if isinstance(x, int) or isinstance(x, float):
             output = True
          else:
             output = False
          return output

 
      def BMI_FN(self, weight, height, measurement_type = ["kg", "cm"]):
          """
          Computation of BMI
          BMI = -1, 1.1 and 1.2 when both weight and height less or equal to 0, only weight is  less or equal to zero  and
          only height is less or equal to zero, respectively.
          BMI = -4, 4.1 and 4.2 when both weight and height are non number, only weight is non number and only height is non number, respectively
          in the normal case BMI = weight / height**2 where weight is megsured in k and height in meters.
          """
          try:
             weight = float(weight)
             height = float(height)
          except:
             a = 1
          
          if self.IS_NUMBER_FN(weight) and self.IS_NUMBER_FN(height): 
             if (weight > 0) and (height > 0):
                 weight, height = self.CONVERT_TO_METRIC_SYSTEM_FN(weight, height, measurement_type)
                 #
                 BMI = weight / height**2
                 #
             else:
               if   (weight <= 0) and (height <= 0):
                     BMI = -1  # if it is BMI = -1 it means it is an error weight or height <= 0 
                     logging.warning('BMI_FN: weight and height are less or equal to zero, weight = ' + str(weight) + ", height = " + str(height))
               elif (weight <= 0):
                     BMI = -1.1 
                     logging.warning('BMI_FN: weight is less or equal to zero, weight = ' + str(weight))
               elif (height <= 0):
                     BMI = -1.2
                     logging.warning('BMI_FN: height is less or equal to zero, height = ' + str(height))
          else:
             if    not(self.IS_NUMBER_FN(weight)) and not(self.IS_NUMBER_FN(height)): 
                   BMI = -4
                   logging.error('BMI_FN: weight is not number, weight = ' + str(weight) + " and height is not number, height = " + str(height))
             elif  not(self.IS_NUMBER_FN(weight)): 
                   BMI = -4.1
                   logging.error('BMI_FN: weight is not number, weight = ' + str(weight) )
             elif  not(self.IS_NUMBER_FN(height)): 
                   BMI = -4.2
                   logging.error('BMI_FN: height is not number, height = ' + str(height) )

          return BMI

      def BMI_CATEGORY_RISK_FN(self, BMI):
          """
          compute BMI category and associated risk.

          """
          if   BMI <= 0:
               bmi_category = "BMI ERROR"
               health_risk  = "BMI ERROR"
          elif BMI <= 18.4:
               bmi_category = "Underweight"
               health_risk  = "Malnutrition risk"
          elif BMI <= 24.9:
               bmi_category = "Normal weight"
               health_risk  = "Low risk"
          elif BMI <= 29.9:
               bmi_category = "Overweight"
               health_risk  = "Enhanced risk"
          elif BMI <= 34.9:
               bmi_category = "Moderately obese"
               health_risk  = "Medium risk"
          elif BMI <= 39.9:
               bmi_category = "Severe obese"
               health_risk  = "High risk"
          else:   
               bmi_category = "Very severe obese"
               health_risk  = "Very high risk"
          return {"BMI Category": bmi_category, "Health risk": health_risk}

      def PEARSON_FEATURES_FN(self, input_df, weight = "WeightKg", height = "HeightCm", measurement_type = ["kg", "cm"]):
          """
          Calculate the BMI (Body Mass Index) using FormUla 1, BMI Category and Health risk 
          from input_df of the person and add them as 3 new columns
          if the unknown measurement system is provided then output is None.
    
          Example of OUTPUT:
          Gender  HeightCm  WeightKg  BMI       BMI Category      Health risk
        0 Male    0           96      -3.000000 BMI ERROR         BMI ERROR
        1 Male    171       -100      -2.000000 BMI ERROR         BMI ERROR
        2 Male    0            0      -1.000000 BMI ERROR         BMI ERROR
        3 Male    171         96      32.830615 Moderately obese  Medium risk
        4 Male    161         85      32.791945 Moderately obese  Medium risk
        5 Male    180         77      23.765432 Normal weight     Low risk
        6 Female  166         62      22.499637 Normal weight     Low risk
        7 Female  150         70      31.111111 Moderately obese  Medium risk
        8 Female  167         82      29.402273 Overweight        Enhanced risk
          """
          error = self.MEASUREMENT_SYSTEM_CHECK_FN(measurement_type)
          if error == 0:
             input_df["BMI"] = input_df.apply(lambda x: self.BMI_FN(x[weight], x[height], measurement_type = measurement_type), axis = 1)
             input_df["BMI Category"] = input_df["BMI"].apply(lambda x:  self.BMI_CATEGORY_RISK_FN(x)["BMI Category"])
             input_df["Health risk" ] = input_df["BMI"].apply(lambda x:  self.BMI_CATEGORY_RISK_FN(x)["Health risk" ])
          else:
             input_df = None
          return input_df

      def STATISTICS_FN(self, input_df):
          """
          Compute the number of customers who is in Overweight category.
          We also compute for every category min, mean and max of BMI, the number of category cases and it probabilities

          Example of OUTPUT:
          Number of overweighted:  1

          BMI Category      Health risk   BMI min    BMI mean   BMI max    count probability
        0 BMI ERROR         BMI ERROR     -3.000000  -2.000000  -1.000000  3     0.333333
        1 Moderately obese  Medium risk   31.111111  32.244557  32.830615  3     0.333333
        2 Normal weight     Low risk      22.499637  23.132535  23.765432  2     0.222222
        3 Overweight        Enhanced risk 29.402273  29.402273  29.402273  1     0.111111
          """
          if input_df is not None:
             overweights = input_df[input_df["BMI Category"] == "Overweight"].copy()
             number_of_over_weighted = len(overweights)
             #
             counts = pd.DataFrame()
             probs  = pd.DataFrame()
             #
             counts    = input_df['BMI Category'].value_counts(dropna=False)
             counts_df = pd.DataFrame({'BMI Category': counts.index, 'count': counts})
             #
             probs    = input_df['BMI Category'].value_counts(normalize=True)
             probs_df = pd.DataFrame({'BMI Category': probs.index, "probability": probs})
             #
             BMI_Category_Health_risk = input_df[["BMI Category", "Health risk"]].drop_duplicates().copy()
             BMI_Category_BMI         = input_df.groupby("BMI Category").agg({"BMI": ["min", "mean", "max"]}).reset_index().copy()
             #
             BMI_Category_BMI_min  = input_df.groupby("BMI Category")["BMI"].min( ).reset_index().rename(columns = {"BMI": "BMI min"})
             BMI_Category_BMI_mean = input_df.groupby("BMI Category")["BMI"].mean().reset_index().rename(columns = {"BMI": "BMI mean"})
             BMI_Category_BMI_max  = input_df.groupby("BMI Category")["BMI"].max( ).reset_index().rename(columns = {"BMI": "BMI max"})
             #
             stats = BMI_Category_Health_risk.merge(BMI_Category_BMI_min, on = 'BMI Category')
             stats = stats.merge(BMI_Category_BMI_mean, on = 'BMI Category')
             stats = stats.merge(BMI_Category_BMI_max,  on = 'BMI Category')
             #
             stats = stats.merge(counts_df, on = 'BMI Category')
             stats = stats.merge(probs_df,  on = 'BMI Category')
          else:
             number_of_over_weighted = None
             stats = None
          #
          return number_of_over_weighted, stats

      def READ_YAML_FN(self, yaml_file_name = None):
          """
          Read yaml file that has configuration settings
          """
          #print("READ_YAML_FN, yaml_file_name: ", yaml_file_name)
          if yaml_file_name is None:
             if len(sys.argv) == 2:
                yaml_file_name = sys.argv[1]
             else:
                yaml_file_name = None
          #      
          if yaml_file_name is not None:       
              try:
                  with open(yaml_file_name) as f:
                       yaml_data = yaml.safe_load(f)
              except:
                 logging.error('READ_YAML_FN: config file is not found, yaml_file_name: ' + str(yaml_file_name) )
                 yaml_data = None
          return yaml_data

      def LOAD_INPUT_FN(self, yaml_data, yaml_input_file_name = 'input file name'):
          """
          Load inouts from JSON file and convert to pandas dataframe
          """
          if  yaml_input_file_name in yaml_data:
              input_file_name = yaml_data[yaml_input_file_name]
              #
              try:
                f = open(input_file_name)
                input_df = json.load(f)
                input_df = pd.DataFrame(input_df)
                if len(input_df) == 0:
                   input_df = None
                   logging.error('LOAD_INPUT_FN: input file is empty, input_file_name: ' + str(input_file_name) ) 
              except:
                logging.error('LOAD_INPUT_FN: input file is not found, input_file_name: ' + str(input_file_name) )
                input_df = None
          else: 
              input_df = None
              logging.error('LOAD_INPUT_FN: yaml file does not have input file name') 
          #
          return input_df


      def CREATE_DIRECTORY_IF_DOES_NOT_EXIST_FN(self, path):
          """
          create output directory if it does not exist
          """
          error = 0
          try:
            # Check whether the specified path exists or not
            isExist = os.path.exists(path)
            if not isExist:
               # Create a new directory because it does not exist 
               os.makedirs(path)
               print("The directory " + str(path) + "is created!")
          except:
              logging.error('CREATE_DIRECTORY_IF_DOES_NOT_EXIST_FN: cannot create directory, path: ' + str(path) )
              error = -1
          return error    
    
      def SAVE_OUTPUTS_FN(self, input_df, n_overweights, stats, output_path, output_file_name, output_n_overweights_file_name, output_stats_file_name):
          """save outputs"""
          error = self.CREATE_DIRECTORY_IF_DOES_NOT_EXIST_FN(output_path)
          try:
            if error != - 1:
               input_df.to_csv(os.path.join(output_path,output_file_name), index = False)
               #
               with open(os.path.join(output_path, output_n_overweights_file_name), 'w') as f:
                    json.dump({"n_overweights": n_overweights}, f)
               #
               stats_file_name = os.path.join(output_path, output_stats_file_name)
               stats.to_csv(stats_file_name, index = False)
          except:
               logging.error('SAVE_IUTPUTS_FN: cannot save outputs in files')
          return error  

      def PROCESSSING_FN(self):
          """
          Main processing function. It perform loading input, compute BMI, BMI Category, Health risk, number of overweight, statistics and save results in output directory 
          """
          #
          yaml_data = self.yaml_data
          #
          error = 0
          #
          if (yaml_data is not None) and ("log file name" in yaml_data):
              logging.basicConfig(filename = yaml_data["log file name"], filemode='w', format='%(name)s - %(levelname)s - %(message)s')
              #
              if  (yaml_data is not None) and ('input file name' in yaml_data):
                  input_df = self.LOAD_INPUT_FN(yaml_data, yaml_input_file_name = 'input file name')
                  #
                  if ('weight measurement system' in yaml_data) and ('height meqasurement system' in yaml_data):
                      if (yaml_data['weight measurement system'] is not None) and (yaml_data['height meqasurement system'] is not None):
                          measurement_type = [yaml_data['weight measurement system'], yaml_data['height meqasurement system'] ]
                      else:
                         measurement_type = None
                         error = -1
                         logging.error('PROCESSSING_FN: measurement system for weight or height is missing in yaml file')
                  else:
                      measurement_type = None
                      error = -2
                      logging.error('PROCESSSING_FN: measurement system for weight or height is missing in yaml file')

                  if ('weight column' in yaml_data) and ('height column' in yaml_data):
                      weight_col = yaml_data['weight column']
                      height_col = yaml_data['height column']
                  else:
                      weight_col = None
                      height_col = None
                      error = -3
                      logging.error('PROCESSSING_FN: weight_col or height_col are not defined in yaml file')   
              #
              if (input_df is not None) and (weight_col is not None) and (height_col is not None) and (measurement_type is not None):
                  if (weight_col in input_df.columns) and (height_col in input_df.columns):
                      input_df = self.PEARSON_FEATURES_FN(input_df, weight = weight_col, height = height_col, measurement_type = measurement_type)
                  else:
                      logging.error('PROCESSSING_FN: there are no weight_col or height_col that are defined in yaml file in the input file')        
              else:
                  print("input_df, weight_col, height_col or measurement_type is None")
              #
              if (input_df is not None):
                  n_overweights, stats = self.STATISTICS_FN(input_df)
                  #
                  if (n_overweights is not None) and (stats is not None):
                      if ("output path" in yaml_data) and ("output file name" in yaml_data) and ("output n overweights file name" in yaml_data) and ("output stats file name" in yaml_data):  
                           output_path                    = yaml_data["output path"]
                           output_file_name               = yaml_data["output file name"] 
                           output_n_overweights_file_name = yaml_data["output n overweights file name"]
                           output_stats_file_name         = yaml_data["output stats file name"]
                           self.SAVE_OUTPUTS_FN(input_df, n_overweights, stats, output_path, output_file_name, output_n_overweights_file_name, output_stats_file_name)
                      else:
                           error = -4
                           logging.error('PROCESSSING_FN: output path, output file, n_ocerweight or stats file name are missing in yaml file')      
          return error