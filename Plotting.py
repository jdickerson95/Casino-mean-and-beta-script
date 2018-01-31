import math
import csv
import numpy
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

def loop(inputFile='.dat'):
 #   vals = ["5", "10", "15", "20", "30", "40", "50", "100"]
    vals = ["1", "2.5"]
    overall = [["Beam energy", "mean", "beta"]]
    counter = 0
    for v in vals:
        totalDistance = 0.
        start_x = 0
        start_y = 0
        start_z = 0
        allDistances = []
        rangeDistances = []
        counter += 1
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
                            thisDistance = math.sqrt(
                                (float(words[0]) - start_x) ** 2 + (float(words[1]) - start_y) ** 2 + (
                                float(words[2]) - start_z) ** 2)
                            # totalDistance += thisDistance
                            allDistances.append(thisDistance / 1000)
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
        PDF = [None] * len(allDistances)
        PDFGumbel = [None] * len(allDistances)
        plt.figure(counter)
        n, bins, patches = plt.hist(allDistances, normed=1)
        allDistances.sort()
        for x in range(len(allDistances)):

            #work out Gayther dist
            z = (allDistances[x]-mean_numpy)/beta
            PDF[x] = ((1/beta)*(math.exp(z-math.exp(z))))

            #work out gumbel
            z = (allDistances[x] - mode) / beta
            PDFGumbel[x] = ((1 / beta) * (math.exp(z - math.exp(z))))

        red_line, = plt.plot(allDistances, PDF, color='r', label='Gayther')
        blue_line, = plt.plot(allDistances, PDFGumbel, color = 'b', label='Gumbel')

        plt.legend(handles=[blue_line, red_line])
        plt.xlabel('Path length')
        plt.ylabel('Probability density')
        plt.title(v + 'keV')
    plt.show()
    #   meanDistance = totalDistance / counter
    '''
    overall.append([v, mean_numpy, beta])

    f = open('./mean-distances.csv', 'wb')
    writer = csv.writer(f)
    writer.writerows(overall)
    f.close()
    '''

if __name__ == "__main__":
    loop()