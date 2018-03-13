import os
import argparse


parser = argparse.ArgumentParser(description='run_ins.py')
parser.add_argument('-start', type=int)
parser.add_argument('-step', type=int)
parser.add_argument('-count', type=int)
opt = parser.parse_args()

start_point = opt.start
step_point = opt.step
count_instance = opt.count

for i in range(count_instance):
    print(i)
    os.system("nohup python3 start_parsing.py -number "
        +str(i)+" -start "+ str(start_point - (step_point * i)) + " -end " + str(start_point - step_point - (step_point * i)) + " &")
