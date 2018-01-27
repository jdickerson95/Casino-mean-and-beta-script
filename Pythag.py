import math
import csv
import numpy

def loop(inputFile='.dat'):
    vals = ["32.5","37.5","42.5","47.5"]
    overall = [["Beam energy","mean","beta"]]
    for v in vals:
        totalDistance = 0.
        counter = 0
        start_x = 0
        start_y = 0
        start_z = 0
        allDistances = []
        f = open(v + inputFile, 'r')
        for line in f:
            words = line.strip().split()
            isint = True
            if len(words) > 0:
                try:
                    first = float(words[0])
                except ValueError:
                    isint = False
                if isint == True:
                    if len(words) > 6:
                        if float(words[6]) <= 0.05:
                            thisDistance = math.sqrt((float(words[0])-start_x) ** 2 + (float(words[1])-start_y) ** 2 + (float(words[2])-start_z) ** 2)
                           # totalDistance += thisDistance
                            allDistances.append(thisDistance/1000)
                            counter += 1
                        elif float(words[6]) == float(v):
                            start_x = float(words[0])
                            start_y = float(words[1])
                            start_z = float(words[2])

        f.close()
        std_numpy = numpy.std(allDistances)
        beta = (std_numpy * math.sqrt(6))/math.pi
        mean_numpy = numpy.mean(allDistances)
     #   meanDistance = totalDistance / counter
        overall.append([v, mean_numpy, beta])

    f = open('./mean-distances.csv', 'wb')
    writer = csv.writer(f)
    writer.writerows(overall)
    f.close()

if __name__ == "__main__":
    loop()