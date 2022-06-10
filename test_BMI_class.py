from BMI import BMI
import unittest
class TestBMI(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestBMI, self).__init__(*args, **kwargs)            
        self.BMI_AD = BMI("AD_config.yaml")
         
    
    # test_MEASUREMENT_SYSTEM_CHECK
    def test_MEASUREMENT_SYSTEM_CHECK_normal_case(self):
        self.assertEqual(self.BMI_AD.MEASUREMENT_SYSTEM_CHECK_FN(measurement_type = ["kg", "cm"]), 0, "MEASUREMENT_SYSTEM_CHECK_FN: incorrect responce, has to be 0")
    def test_MEASUREMENT_SYSTEM_CHECK_unknown_case(self):
        self.assertEqual(self.BMI_AD.MEASUREMENT_SYSTEM_CHECK_FN(measurement_type = ["UNKNOWN", "UNKNOWN"]), -5, "MEASUREMENT_SYSTEM_CHECK_FN: incorrect responce, has to be -5")
    def test_MEASUREMENT_SYSTEM_CHECK_unknown_weight_case(self):
        self.assertEqual(self.BMI_AD.MEASUREMENT_SYSTEM_CHECK_FN(measurement_type = ["UNKNOWN", "cm"]), -5.1, "MEASUREMENT_SYSTEM_CHECK_FN: incorrect responce, has to be -5.1")
    def test_MEASUREMENT_SYSTEM_CHECK_unknown_height_case(self):
        self.assertEqual(self.BMI_AD.MEASUREMENT_SYSTEM_CHECK_FN(measurement_type = ["kg", "UNKNOWN"]), -5.2, "MEASUREMENT_SYSTEM_CHECK_FN: incorrect responce, has to be -5.2")
    #
    # test_CONVERT_TO_METRIC_SYSTEM
    def test_CONVERT_TO_METRIC_SYSTEM_kg_cm(self):
        self.assertEqual(self.BMI_AD.CONVERT_TO_METRIC_SYSTEM_FN(weight = 100, height = 100, measurement_type = ["kg", "cm"]), (100, 1.0), "MEASUREMENT_SYSTEM_CHECK_FN: incorrect responce, has to be (100, 1.0)")
    def test_CONVERT_TO_METRIC_SYSTEM_kg_mm(self):
        self.assertEqual(self.BMI_AD.CONVERT_TO_METRIC_SYSTEM_FN(weight = 100000, height = 1000, measurement_type = ["g", "mm"]), (100, 1.0), "MEASUREMENT_SYSTEM_CHECK_FN: incorrect responce, has to be (100, 1.0)")
    def test_CONVERT_TO_METRIC_SYSTEM_lb_in(self):
        self.assertEqual(self.BMI_AD.CONVERT_TO_METRIC_SYSTEM_FN(weight = 100, height = 100, measurement_type = ["lb", "in"]), (45.359237, 2.54), "MEASUREMENT_SYSTEM_CHECK_FN: incorrect responce, has to be (45.359237, 2.54)")
    def test_CONVERT_TO_METRIC_SYSTEM_lb_in(self):
        self.assertEqual(self.BMI_AD.CONVERT_TO_METRIC_SYSTEM_FN(weight = 100, height = 100, measurement_type = ["kg", "in"]), (100, 2.54), "MEASUREMENT_SYSTEM_CHECK_FN: incorrect responce, has to be (100, 2.54)")

    # test_BMI
    def test_BMI_normal_case(self):
        self.assertEqual(int(self.BMI_AD.BMI_FN(weight = 100, height = 100)), 100, "BMI_FN: incorrect responce, has to be 100")
    def test_BMI_zero_cases(self):
        self.assertEqual(    self.BMI_AD.BMI_FN(weight =   0, height =   0),    -1, "BMI_FN: incorrect responce, has to be  -1")
        self.assertEqual(    self.BMI_AD.BMI_FN(weight =   0, height = 100),  -1.1, "BMI_FN: incorrect responce, has to be  -1.1")
        self.assertEqual(    self.BMI_AD.BMI_FN(weight = 100, height =   0),  -1.2, "BMI_FN: incorrect responce, has to be  -1.2")
    def test_BMI_non_number_cases(self):
        self.assertEqual(self.BMI_AD.BMI_FN(weight = "NOT NUMBER", height =            0), -4.1, "BMI_FN: incorrect responce, has to be -4.1")
        self.assertEqual(self.BMI_AD.BMI_FN(weight =          100, height = "NOT NUMBER"), -4.2, "BMI_FN: incorrect responce, has to be -4.2")
        self.assertEqual(self.BMI_AD.BMI_FN(weight = "NOT NUMBER", height = "NOT NUMBER"),   -4, "BMI_FN: incorrect responce, has to be -4")
    #
    # test_BMI_category_risk
    def test_BMI_category_risk_BMI_ERROR(self):
        self.assertEqual(self.BMI_AD.BMI_CATEGORY_RISK_FN(-1),   {'BMI Category': 'BMI ERROR', 'Health risk': 'BMI ERROR'}, "BMI_CATEGORY_RISK_FN: incorrect responce, has to be {'BMI Category': 'BMI ERROR', 'Health risk': 'BMI ERROR'}")
    def test_BMI_category_risk_Underweight(self):
        self.assertEqual(self.BMI_AD.BMI_CATEGORY_RISK_FN(18.4),   {'BMI Category': 'Underweight', 'Health risk': 'Malnutrition risk'}, "BMI_CATEGORY_RISK_FN: incorrect responce, has to be {'BMI Category': 'Underweight', 'Health risk': 'Malnutrition risk'}")
    def test_BMI_category_risk_Normal_weight(self):
        self.assertEqual(self.BMI_AD.BMI_CATEGORY_RISK_FN(24.9),    {'BMI Category': 'Normal weight', 'Health risk': 'Low risk'}, "BMI_CATEGORY_RISK_FN: incorrect responce, has to be {'BMI Category': 'Normal weight', 'Health risk': 'Low risk'}")
    def test_BMI_category_risk_Overweight(self):
        self.assertEqual(self.BMI_AD.BMI_CATEGORY_RISK_FN(29.9),   {'BMI Category': 'Overweight', 'Health risk': 'Enhanced risk'}, "BMI_CATEGORY_RISK_FN: incorrect responce, has to be {'BMI Category': 'Overweight', 'Health risk': 'Enhanced risk'}")
    def test_BMI_category_risk_Moderately_obese(self):
        self.assertEqual(self.BMI_AD.BMI_CATEGORY_RISK_FN(34.9),   {'BMI Category': 'Moderately obese', 'Health risk': 'Medium risk'}, "BMI_CATEGORY_RISK_FN: incorrect responce, has to be {'BMI Category': 'Moderately obese', 'Health risk': 'Medium risk'}")
    def test_BMI_category_risk_Severe_obese(self):
        self.assertEqual(self.BMI_AD.BMI_CATEGORY_RISK_FN(39.9),   {'BMI Category': 'Severe obese', 'Health risk': 'High risk'}, "BMI_CATEGORY_RISK_FN: incorrect responce, has to be {'BMI Category': 'Severe obese', 'Health risk': 'High risk'}")
    def test_BMI_category_risk_Very_Severe_obese(self):
        self.assertEqual(self.BMI_AD.BMI_CATEGORY_RISK_FN(50),    {'BMI Category': 'Very severe obese', 'Health risk': 'Very high risk'}, "BMI_CATEGORY_RISK_FN: incorrect responce, has to be {'BMI Category': 'Very severe obese', 'Health risk': 'Very high risk'}")
        
# run the test
if __name__ == '__main__':
   unittest.main()