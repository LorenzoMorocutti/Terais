import subprocess
import numpy as np

a=3
b = 45
script_path = "/home/icub/Desktop/Terais/drawing.py"
#script_path = "/home/icub/Desktop/Terais/prova_sub.py"

res = subprocess.Popen(["python3", script_path, '0'], stdout=subprocess.PIPE)

output = []
output = res.stdout.read()

array = np.fromstring(output.decode(), dtype=float, sep=',')

#b[0] = float(output[0])
#b[1] = int(output[1])
#b[2] = float(output[2])


print(array)


#print(a+b)

