It is an example of standalone app that uses yaml file as cofig, external library, logging, unitests and classes.
There are two demos that work with two different input datasets.

1. Running the ORIGINAL input dataset.

if you wan to run the original input dataset:
[{"Gender": "Male", "HeightCm": 171, "WeightKg": 96 },
{ "Gender": "Male", "HeightCm": 161, "WeightKg": 85 },
{ "Gender": "Male", "HeightCm": 180, "WeightKg": 77 },
{ "Gender": "Female", "HeightCm": 166, "WeightKg": 62},
{"Gender": "Female", "HeightCm": 150, "WeightKg": 70},
{"Gender": "Female", "HeightCm": 167, "WeightKg": 82}]

then you need to type the command in the command line

python BM_DEMO.py .\ORIGINAL_config.yaml  

it will take input data from directory ORIGINAL_input, save the results in the directory ORIGINAL_output
and create the log file called ORIGINAL_errors.


2. Running the extended dataset.

In the directory AD_input I created another input dataset that is an extension of the ORIGINAL one:
[{"Gender": "Male",   "HeightCm": 0, "WeightKg": 96},
 {"Gender": "Male",   "HeightCm": 171, "WeightKg": -100},
 {"Gender": "Male",   "HeightCm": 0, "WeightKg": 0},

 {"Gender": "Male",   "HeightCm": 100, "WeightKg": 18.4},
 {"Gender": "Male",   "HeightCm": 100, "WeightKg": 24.9},
 {"Gender": "Male",   "HeightCm": 100, "WeightKg": 29.9},
 {"Gender": "Female", "HeightCm": 100, "WeightKg": 34.9},
 {"Gender": "Female", "HeightCm": 100, "WeightKg": 39.9},
 {"Gender": "Female", "HeightCm": 100, "WeightKg": 50}, 

 {"Gender": "Male",   "HeightCm": 171, "WeightKg": 96},
 {"Gender": "Male",   "HeightCm": 161, "WeightKg": 85},
 {"Gender": "Male",   "HeightCm": 180, "WeightKg": 77},
 {"Gender": "Female", "HeightCm": 166, "WeightKg": 62},
 {"Gender": "Female", "HeightCm": 150, "WeightKg": 70},
 {"Gender": "Female", "HeightCm": 167, "WeightKg": 82}]

in order to use this input run the same command but with different config:
python BM_DEMO.py .\AD_config.yaml

it will use AD_input, save the results in the directory AD_output
and create the log file called AD_errors.

3. YAML file
you can create another config that is yaml file, for example, with the following keys and values:

input file name: ORIGINAL_input/customer_weight_height.json
weight column: WeightKg 
height column: HeightCm
weight measurement system: kg
height meqasurement system: cm
output path: ORIGINAL_output
output file name: output.csv
output stats file name: stats.csv
output n overweights file name: output_n_overweights.json
log file name: ORIGINAL_errors.log

You can change the measurement system. 
I implemented  "lb", "g" and "kg" for weight and  "cm", "mm", "in", "m" for height. 

4. Test
You can run unittest as following:

python -m unittest discover  .

I could add more tests in unittest that I have implemented in the script.

5. Outputs.

Outputs (see directory ORIGINAL_output and AD_output) contain the following files:
a) output.csv is the output of the first task (see "1) Calculate the BMI (Body Mass Index) using FormUla 1, BMI Category and Health risk 
from Table 1 of the person and add them as 3 new columns");
b) output_n_overweights.json is the output of the second task ("2) Count the total number of overweight people using ranges in the column BMI Category 
of Table 1, c"). Not sure what you mean by " check this is consistent programmatically";
c) stats.csv - is the second part of the second task (see "add any other observations in 
the documentation"). It compute distribution "BMI Category", "Health risk" and "BMI". 
See example for the ORIGINAL input dataset:

BMI Category	 Health risk	BMI min	        BMI mean	BMI max	        count	probability
Moderately obese Medium risk	31.11111111	32.2445568	32.83061455	3	0.5
Normal weight	 Low risk	22.4996371	23.1325346	23.7654321	2	0.333333333
Overweight	 Enhanced risk	29.4022733	29.4022733	29.4022733	1	0.166666667

6. Python notebook

If you like python notebooks you can run the code using BMI_DEMO.ipynb
