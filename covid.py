import pandas as pd
import math
import os

#Sve drzave u listi 
df = pd.read_csv("./covid.csv")
drzave = df.Country.unique()

print(df.Date_reported[0])

#distr argument odreduje koriste li se kumulativni slucajevi ili novi slucajevi
#stupac["Cumulative_cases", "Cumulative_deaths"] odreduje koriste li se slucjai smrti ili zaraze
def distribucijaZaDrzavu(drzava, distr, stupac):

    distribuijaCul = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Cumulative
    distribuijaNov = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Novi slucaji


    data = pd.read_csv("./covid.csv")



    data = data[(data["Country"] == drzava) & (data[stupac] > 0)]
    #data = data[ (data["stupac"] > 0)]
    brojRedova = data.shape[0]
   # print(brojRedova)
    #print(data[["Country", "stupac"]])
    #print(data.shape)
    #for col in data.columns: 
     #   print(col) 

    if stupac == "Cumulative_cases":
        for culCase in data.Cumulative_cases:
            prviDigit = int(str(culCase)[:1]) 
            #print(culCase, " ", str(prviDigit))
            distribuijaCul[prviDigit] += 1
    else:
        for culCase in data.Cumulative_deaths:
            prviDigit = int(str(culCase)[:1]) 
            #print(culCase, " ", str(prviDigit))
         

    if stupac == "Cumulative_cases":
        for newCase in data.New_cases:
            if newCase > 0:
                prviDigit = int(str(newCase)[:1]) 
                #print(newCase, " ", str(prviDigit))
                distribuijaNov[prviDigit] += 1
    else:
        for newCase in data.New_deaths:
            if newCase > 0:
                prviDigit = int(str(newCase)[:1]) 
                #print(newCase, " ", str(prviDigit))
                distribuijaNov[prviDigit] += 1

    for x in range(10):
        if brojRedova != 0:
            distribuijaCul[x] = round((distribuijaCul[x] / brojRedova) * 100, 1)
            distribuijaNov[x] = round((distribuijaNov[x] / brojRedova) * 100, 1)
        

    #print(distribuijaCul)
    #print(distribuijaNov) 

    if distr == "cul":
        return distribuijaCul
    else:
        return distribuijaNov



def calculateDeviation(distr):
    distr = distr[1:]
    
    deviacija = 0
    orgDistr = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]

    for x in range(9):
        deviacija += pow(distr[x]/100 - orgDistr[x]/100 ,2)

    deviacija = math.sqrt(deviacija) / 1.03606
    return deviacija

print(distribucijaZaDrzavu("United States of America", "cul", "Cumulative_cases"), 
      calculateDeviation(distribucijaZaDrzavu("United States of America", "cul", "Cumulative_cases")))


avgDev = 0

bar = []
x = 0
pos = 0
for x in range(25):
    bar += "-"

#Racunanje prosjecne devijacije
for drzava in drzave:
    cul = distribucijaZaDrzavu(drzava, "cul", "Cumulative_cases")
    dev = calculateDeviation(cul)
    drzavaInfo = [drzava, cul, round(dev  *100)]
    if drzavaInfo[2] >= 1:
        print(drzavaInfo)
    avgDev += dev
    
    #Progerss bar
    # if x % 9 == 0:
    #     bar[pos] = "#"
    #     pos += 1
    # x += 1
    # clear = lambda: os.system("cls")
    # clear()
    # print(bar)

avgDev = avgDev/(len(drzave))
print(avgDev)


