import math
import csv
import numpy
from scipy.stats import gumbel_l

def loop(inputFile='.dat'):
   # vals = ["1", "2.5", "5", "7.5", "10", "11.25", "12.5","13.75","15","17.5","20","22.5","25","27.5","30","32.5","35","37.5","40","42.5","45","47.5","50","55","60","65","70","75","80","85","90","95","100"]
   # vals = ["10"]
   # vals = ["1", "2","2.5", "3","4","5"]
    vals = ["5", "7.5", "10", "11.25", "12.5","13.75","15","17.5","20","22.5","25","27.5","30","32.5","35","37.5","40","42.5","45","47.5","50","55","60"]
  #  overall = [["Beam energy", "6", "5", "4", "3", "2", "1", "0"]]
    overall = [["Beam energy", "3", "2", "1", "0"]]
    for v in vals:
        totalDistance = 0.
        totalEnergy = 0.
        energyBins = int(round(5 * float(v)))
       # energyBins = 10
        counter = 0
        start_x = 0
        start_y = 0
        start_z = 0
        last_energy = 0
        allDistances = []
        allEnergies = []
        rangeDistances = []
        rangeEnergy = [0.] * energyBins
        overallRangeEnergy = []
        end = False

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
                        if float(words[6]) == float(v): #if this is the start of the track
                            end = False
                            start_x = float(words[0])
                            start_y = float(words[1])
                            start_z = float(words[2])
                            last_energy = float(v)
                        else: #a part of the track
                            if end == False:
                                thisDistance = math.sqrt((float(words[0]) - start_x) ** 2 + (float(words[1]) - start_y) ** 2 + (
                                    float(words[2]) - start_z) ** 2)
                                totalDistance += thisDistance / 1000
                                allDistances.append(totalDistance)
                                thisEnergy = last_energy - float(words[6])
                                allEnergies.append(thisEnergy)
                                #now increment the values
                                last_energy = float(words[6])
                                start_x = float(words[0])
                                start_y = float(words[1])
                                start_z = float(words[2])

                        #if it's at the end of this track
                        if end == False:
                            if float(words[6]) <= 0.05: #if end of track
                                end = True
                                index = 0
                                limit = 1/float(energyBins)
                                for x in range(len(allDistances)):
                                    if (allDistances[x] / totalDistance) > limit: #this not quite right need to start at correct index as atm just puts in second whatever
                                        while (allDistances[x] / totalDistance) > limit:
                                            index += 1
                                            limit += 1/float(energyBins)
                                            if index == energyBins:
                                                index -= 1
                                                break
                                    rangeEnergy[index] += allEnergies[x]

                                overallRangeEnergy.append(rangeEnergy)
                                #now I need to reset everything
                                totalDistance = 0.
                                allDistances = []
                                allEnergies = []
                                rangeEnergy = [0.] * energyBins




                            '''
                        if float(words[6]) <= 0.05: #if end of track
                            thisDistance = math.sqrt((float(words[0])-start_x) ** 2 + (float(words[1])-start_y) ** 2 + (float(words[2])-start_z) ** 2)
                           # totalDistance += thisDistance
                            allDistances.append(thisDistance/1000)
                            if float(v) > 20:
                                rangeDistances.append(round(thisDistance / 1000, 1))
                            else:
                                rangeDistances.append(round(thisDistance / 1000, 2))
                        elif float(words[6]) == float(v):
                            start_x = float(words[0])
                            start_y = float(words[1])
                            start_z = float(words[2])
                                '''
        f.close()
        #Average out the energies
        averageRangeEnergy = []
        length = len(overallRangeEnergy)
        for i in range(energyBins):
            totAverageEnergy = 0
            for j in range(length):
                totAverageEnergy += overallRangeEnergy[j][i]
            averageRangeEnergy.append(totAverageEnergy/length)
        proportionRangeEnergy = []
        totalEnergy = sum(averageRangeEnergy) #should be v-0.05
        '''
        for i in averageRangeEnergy:
            proportionRangeEnergy.append(i/totalEnergy)

        firstProportionRangeEnergy = []
        for i in proportionRangeEnergy:
         #   usedProportionRangeEnergy.append(i) #if all
            if i < 0.2:  #if just start
                firstProportionRangeEnergy.append(i)
         '''
       # std_numpy = numpy.std(allDistances)
       # beta = (std_numpy * math.sqrt(6))/math.pi
       # mean_numpy = numpy.mean(allDistances)
       # mode = max(set(rangeDistances), key=rangeDistances.count)
     #   meanDistance = totalDistance / counter
      #  allDistances.sort()
      #  loc, scale = gumbel_l.fit(allDistances)
        '''
        for i in range(energyBins):
            proportionAlongTrack = (i*(1/float(energyBins)) + (i+1)*(1/float(energyBins)))/2
            overall.append([v, proportionAlongTrack, averageRangeEnergy[i]])
        '''

        proportionAlongTrack = []
        firstAverageEnergy = []
        loopCounter = int(energyBins * (2 / float(v)))-1
       # for i in range(energyBins): #all
      #  for i in range(int(energyBins * (2/float(v)))): #first few points
        for i in range(int(energyBins * (2 / float(v))),int(energyBins - (energyBins * (2 / float(v))))):  # middle few points
            loopCounter += 1
            proportionAlongTrack.append((i*(1/float(energyBins)) + (i+1)*(1/float(energyBins)))/2)
            firstAverageEnergy.append(averageRangeEnergy[loopCounter])


       # x_six, x_five, x_four, x_three, x_two, x_one, x_zero = numpy.polyfit(proportionAlongTrack, firstAverageEnergy, 6)
       # overall.append([v, x_six, x_five, x_four, x_three, x_two, x_one, x_zero])
        x_three, x_two, x_one, x_zero = numpy.polyfit(proportionAlongTrack, firstAverageEnergy, 3)
        overall.append([v, x_three, x_two, x_one, x_zero])

    f = open('./energy-depostion.csv', 'wb')
    # f = open('./low-mode.csv', 'wb')
    writer = csv.writer(f)
    writer.writerows(overall)
    f.close()



if __name__ == "__main__":
    loop()