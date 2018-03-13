import os

start_point = 101156037
step_point = 2000000
count_instance = 50

for i in range(count_instance):
    print(i)
    os.system("nohup python3 start_parsing.py -number "
        +str(i)+" -start "+ str(start_point - (step_point * i)) + " -end " + str(start_point - step_point - (step_point * i)) + " &")
