import math
import csv
import numpy

def loop(inputFile='.dat'):
    vals = ["1", "2.5", "5", "7.5", "10", "11.25", "12.5","13.75","15","17.5","20","22.5","25","27.5","30","32.5","35","37.5","40","42.5","45","47.5","50","55","60","65","70","75","80","85","90","95","100"]
   # vals = ["1", "2.5", "5", "7.5", "10"]
    overall = [["Beam energy","mean","beta", "mode"]]
    for v in vals:
        totalDistance = 0.
        counter = 0
        start_x = 0
        start_y = 0
        start_z = 0
        allDistances = []
        rangeDistances = []
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
                            if float(v) > 10:
                                rangeDistances.append(round(thisDistance / 1000, 1))
                            else:
                                rangeDistances.append(round(thisDistance / 1000, 2))
                        elif float(words[6]) == float(v):
                            start_x = float(words[0])
                            start_y = float(words[1])
                            start_z = float(words[2])

        f.close()
        std_numpy = numpy.std(allDistances)
        beta = (std_numpy * math.sqrt(6))/math.pi
        mean_numpy = numpy.mean(allDistances)
        mode = max(set(rangeDistances), key=rangeDistances.count)
     #   meanDistance = totalDistance / counter
        overall.append([v, mean_numpy, beta, mode])

    f = open('./mean+mode-distances.csv', 'wb')
  #  f = open('./low-mode.csv', 'wb')
    writer = csv.writer(f)
    writer.writerows(overall)
    f.close()

if __name__ == "__main__":
    loop()