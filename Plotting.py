import math
import csv
import numpy
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from scipy import stats
from scipy.special import gamma as gammaf
from scipy.stats import gumbel_l
from scipy.stats import gumbel_r



def loop(inputFile='.dat'):
   # vals = ["1","5", "10", "15", "20", "30", "40", "50", "100"]
    vals = ["20"]
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
        std_numpy = numpy.std(allDistances, ddof=1)
        var = std_numpy ** 2
        beta = (std_numpy * math.sqrt(6))/math.pi

        mean_numpy = numpy.mean(allDistances)

        mode = max(set(rangeDistances), key=rangeDistances.count)
        length = len(allDistances)
        PDF = [None] * length
        PDFGumbel = [None] * length
        PDFGumbelEst = [None] * length
        pdf_manual_beta = [None] * length
       # PDFGenLog = [None] * length
        plt.figure(counter)
        n, bins, patches = plt.hist(allDistances,20,normed=1)
        allDistances.sort()
        median = (allDistances[(length/2)-1] + allDistances[length/2])/2
        the_max = max(allDistances)

        #manual beta
        alpha1, beta1, loc, scale = stats.beta.fit(allDistances)
       # alpha1 = mean_numpy ** 2 * (1 - mean_numpy) / var - mean_numpy
        #alpha1 = 246.2
      #  alpha1 = (mean_numpy*(2*mode - the_max))/(the_max*(mode-mean_numpy))
       # beta1 = alpha1 * (1 - mean_numpy) / mean_numpy
       # beta1 = 15.2
       # beta1 = (alpha1*(the_max-mean_numpy))/mean_numpy
        denominator = (gammaf(alpha1)* gammaf(beta1))/ gammaf(alpha1 + beta1)
        #loc = -65.0
        #scale = 74.4

        for x in range(len(allDistances)):
            m = (allDistances[x]-loc)/scale
            pdf_manual_beta[x] = (1/scale) * ((m**(alpha1 - 1)) * ((1-((m))**(beta1-1))) / denominator)
            '''
            #work out Gayther dist

            z = (allDistances[x]-mean_numpy)/beta
            PDF[x] = ((1/beta)*(math.exp((z-math.exp(z)))))
            
            #work out gumbel
            z = (allDistances[x] - mode) / beta
            PDFGumbel[x] = ((1 / beta) * (math.exp(-(z + math.exp(-z)))))
            #z = (allDistances[x] - (mean_numpy - beta+0/5772)) / beta
            #PDFGumbelEst[x] = ((1 / beta) * (math.exp(-(z + math.exp(-z)))))

            
            #work out genlog
            PDFGenLog[x] = (median * math.exp(-allDistances[x]))/((1+math.exp(-allDistances[x]))**(median+1))

            # gamma
            ag, bg, cg = stats.gamma.fit(allDistances)
            pdf_gamma = stats.gamma.pdf(allDistances, ag, bg, cg)
            green_line = plt.plot(allDistances, pdf_gamma, color = 'g', label="Gamma")

            
            '''

           # gumbel_l
        agl, bgl = gumbel_l.fit(allDistances)
        print(agl)
        print(bgl)
        # pdf_gumbel_l = gumbel_l.pdf(allDistances, agl, bgl)
        pdf_gumbel_best = gumbel_l.pdf(allDistances, agl, bgl)
        pdf_gumbel_l = [None] * length
        for x in range(len(allDistances)):
            #z = (allDistances[x]-agl)/bgl
            #pdf_gumbel_l[x] = (1/bgl) * math.exp(-(z + math.exp(-z)))
            #agl = mean_numpy
            z = (allDistances[x] - agl)/bgl
            pdf_gumbel_l[x] = (1/bgl) * math.exp(z - math.exp(z))


        magenta_line, = plt.plot(allDistances, pdf_gumbel_l, color = 'm', label="gumbel_l")
        blue_line, = plt.plot(allDistances, pdf_gumbel_best, color = 'b', label="gumbel_best")
        '''
        #gumbel_r
        agr, bgr = gumbel_r.fit(allDistances)
        pdf_gumbel_r = gumbel_r.pdf(allDistances, agr, bgr)
        cyan_line, = plt.plot(allDistances, pdf_gumbel_r, color='c', label="gumbel_r")

        #gamma
        ag, bg, cg = stats.gamma.fit(allDistances)
        pdf_gamma = stats.gamma.pdf(allDistances, ag, bg, cg)

        #beta
        ab, bb, cb, db = stats.beta.fit(allDistances)
        print(ab)
        print(bb)
        print(cb)
        print(db)
        pdf_beta = stats.beta.pdf(allDistances, ab, bb, cb, db)
        yellow_line, = plt.plot(allDistances, pdf_beta, color = 'y', label="Beta")

        #normal
        pdf_g = stats.norm.pdf(allDistances, mean_numpy, std_numpy)  # now get theoretical values in our interval
        black_line, = plt.plot(allDistances, pdf_g, color='k', label="Norm")  # plot it

        #manual beta
        '''


       # red_line, = plt.plot(allDistances, PDF, color='r', label='Gayther')
        red_line, = plt.plot(allDistances, pdf_manual_beta, color='r', label='manual beta')
       # blue_line, = plt.plot(allDistances, PDFGumbel, color = 'b', label='Gumbel')
     #   green_line, = plt.plot(allDistances, PDFGenLog, color = 'g', label='GenLog')
      #  green_line, = plt.plot(allDistances, PDFGumbelEst, color='b', label='GumbelEst')

      #  green_line, = plt.plot(allDistances, pdf_gamma, color = 'g', label="Gamma")
      #  plt.legend(handles=[blue_line, red_line, green_line])
      #  plt.legend(handles=[black_line, green_line, cyan_line, magenta_line, yellow_line, red_line])
        plt.legend(handles=[magenta_line, blue_line, red_line])
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