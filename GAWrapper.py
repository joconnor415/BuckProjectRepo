#This can be run in a local machine
import os, stat, subprocess
from pyevolve import G1DBinaryString
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Mutators

def runGeneMania(cmd):
    p = subprocess.call(cmd, shell=True)
    
def getNetworks(fileName):
    networks = [network.strip() for network in open(fileName)]
    return networks

def retrieveAUROC(fileName):
    f = open(fileName, "r+b")
    for line in f:
        index = line.find("\t-\t")
        if index != -1:
            return float(line[index+3:line.find("\t", index+3, len(line))])
        

def eval_func(chromosome):
    global networks
    networkList = [];
    for i in range(0, len(networks)):
        if chromosome[i] == 1:
            networkList.append(networks[i])
    networkList = ",".join(networkList)
    cmd = "java -Xmx800M -cp GeneMania.jar org.genemania.plugin.apps.CrossValidator " + \
              "--data gmdata-2012-08-02 --organism \"S. Cerevisiae\" --query queryGene.txt " + \
              "--networks " + networkList + " --folds 3 --outfile result.txt"
    runGeneMania(cmd)
    lastTime = 0;
    #while(os.stat("result.txt")[stat.ST_MTIME] != lastTime):
    #    lastTime = os.stat("result.txt")[stat.ST_MTIME];
    return retrieveAUROC('result.txt')

networks    = getNetworks('S_Cerevisiae_networks.txt')
networks    = networks[1:5]
print networks
networksNum = len(networks)
genome      = G1DBinaryString.G1DBinaryString(networksNum)

genome.evaluator.set(eval_func)
genome.mutator.set(Mutators.G1DBinaryStringMutatorFlip)

ga = GSimpleGA.GSimpleGA(genome)
ga.selector.set(Selectors.GTournamentSelector)
ga.setPopulationSize(5)
ga.setGenerations(100)

ga.evolve(freq_stats=10)
best = ga.bestIndividual()

print best

