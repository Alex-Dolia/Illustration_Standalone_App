from BMI import BMI
import sys 

if __name__ == "__main__":
   print("sys.argv: ", sys.argv, ", len: ", len(sys.argv))
   BMI_AD = BMI()
   BMI_AD.PROCESSSING_FN()