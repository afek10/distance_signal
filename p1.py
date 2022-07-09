from cmath import nan
import numpy as np
from tabulate import tabulate

DifferenceOfZero = None #It is not possible to calculate the difference of a number from 0, Therefore the difference is defined.
sensorAnomaly = 0.2
arr = np.array([], dtype = np.float64)
arrOfAverages = np.array([], dtype = np.float64)
path = "C:\\Users\\Afek Banyas\\Desktop\\distance_signal.txt"
index = 0
numOfZeros = 0

with open(path) as f: #read file to float64 arr
    for line in f:
        line = line.replace("\n", "").replace(" ", "")
        arr = np.append(arr, np.float64(line))
originalLenArr = len(arr)

for i in arr: #Checking how many times the call 0 was received
    if np.array_equal(i,  np.float64(0)):
        numOfZeros += 1
        #arr = np.delete(arr, index)
        index -= 1
    index += 1

index = 0
for i in arr: #create arr of averages
    AverageOfI = np.float64(0) #The average difference of the reading from the other readings
    indexJ = 0
    if np.array_equal(i,  np.float64(0)): #Prevent division by 0
        AverageOfI = DifferenceOfZero
        arrOfAverages = np.append(arrOfAverages, AverageOfI)
        index += 1
        continue
    for j in arr: #Checks the difference in percentages of each reading versus all other readings
        if index is indexJ:
            indexJ += 1
            continue
        if np.array_equal(j,  np.float64(0)): #Prevent division by 0
            AverageOfI = np.float64(AverageOfI) + np.float64(0)
            indexJ += 1
            continue
        difference = (i / j - 1) * 100
        AverageOfI = np.float64(AverageOfI) + np.float64(difference)
        indexJ += 1
    
    AverageOfI = AverageOfI / (len(arr) - 1 - numOfZeros)
    arrOfAverages = np.append(arrOfAverages, np.float64(AverageOfI))
    index += 1

#Since I do not know the sensor, I estimate that if most of the results 
#are absolute 0 it is a faulty sensor or the sensor is completely touching the object.
if numOfZeros > (len(arr) / 2):
    print("""Most results are 0.
The sensor is probably touching the object
or there is a malfunction in the sensor\n""")
    exit()
elif numOfZeros > 0:
    print('The result "absolute 0" was obtained',numOfZeros ,'times out of',len(arr) ,'readings.',
    "Since most of the results are not absolute 0 the program estimates that",
    "this is an incorrect reading and so we will ignore them.\n")
            
averageDifference = np.float64(0)
for i in arrOfAverages:
    if type(i) is not type(None):
        averageDifference = np.float64(averageDifference) + np.float64(i)

averageDifference = averageDifference / (len(arrOfAverages) - numOfZeros)
maxaverageDifference = averageDifference + sensorAnomaly
minaverageDifference = averageDifference - sensorAnomaly

index = 0
table = [['Before cleaning', 'After cleaning']]

for i in arrOfAverages:
    if type(i) is type(None):
        table += [[str(arr[index]), "False reading"]]
    elif i <= maxaverageDifference and i >= minaverageDifference:
        #print("Vaild reading: ", arr[index])
        table += [[str(arr[index]), str(arr[index])]]
    else:
        #print("False reading: ", arr[index])
        table += [[str(arr[index]), "False reading"]]
    index += 1

print(tabulate(table))


