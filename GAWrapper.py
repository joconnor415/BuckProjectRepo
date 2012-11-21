#This can be run in a local machine
import os, stat, subprocess, commands
from pyevolve import G1DBinaryString
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Mutators

#runs genemania function passing in command
def runGeneMania(cmd):
    p = subprocess.call(cmd, shell=True)

#retreive networks from list of networks file
def getNetworks(fileName):
    networks = [network.strip() for network in open(fileName)]
    return networks

#retrieve all true classifiers from file
def retrieveAUROC(fileName):
    f = open(fileName, "r+b")
    for line in f:
        index = line.find("\t-\t")
        if index != -1:
            return float(line[index+3:line.find("\t", index+3, len(line))])
        
#Evaluation Function (Fitness Function) evaluates genome, assigning it a raw score
# objective of this function is to quantify the solutions (individuals, chromosomes)
#iterate through global networks list, if network is set to true add it to list of networks
#pas netwroks list into command to run genemania
def eval_func(chromosome):
    global networks
    networkList = [];
    for i in range(0, len(networks)):
        if chromosome[i] == 1:
            networkList.append(networks[i])
    networkList = ",".join(networkList)
    #800 to little, 
    cmd = "java -Xmx800M -cp GeneMania.jar org.genemania.plugin.apps.CrossValidator " + \
              "--data gmdata-2012-08-02 --organism \"S. Cerevisiae\" --query queryGene.txt " + \
              "--networks " + networkList + " --folds 3 --outfile result.txt"
    runGeneMania(cmd)
    #lastTime = 0;
    #while(os.stat("result.txt")[stat.ST_MTIME] != lastTime):
    #    lastTime = os.stat("result.txt")[stat.ST_MTIME];
    return retrieveAUROC('result.txt')

networks    = getNetworks('S_Cerevisiae_networks.txt')
#evaluating first five networks
networks    = networks[1:5]
print networks
networksNum = len(networks)
genome      = G1DBinaryString.G1DBinaryString(networksNum)

#setting evaluation function
genome.evaluator.set(eval_func)

#G1DBinaryStringMutatorFlip- The classical flip mutator for binary strings
genome.mutator.set(Mutators.G1DBinaryStringMutatorFlip)

#GA Engine. Responsible for evolutionary process. Receives one parameter
ga = GSimpleGA.GSimpleGA(genome)

#Default tournament selector uses the roulette wheel to pick individuals for the pool
#test different selectors
ga.selector.set(Selectors.GTournamentSelector)

#Sets population size, calls setPopulationSize() of GPopulation
ga.setPopulationSize(5)

#Sets the number of generations to evolve
ga.setGenerations(100)

#Do the evolution, with stats dump frequency of 10 generations
ga.evolve(freq_stats=10)

#bestIndividual() returns the population's best individual
best = ga.bestIndividual()

def get_network_list(data=None, organism=None, query=None):
    '''
    Get a list of available biological network by organism type
    '''
    if data is None: data = "gmdata-2012-08-02"
    if organism is None: organism = "H. Sapiens"
    if query is None: query = "yeast.query"
    
    cmd = "java -cp GeneMANIA.jar org.genemania.plugin.apps.QueryRunner --data "+data+" --list-networks \""+organism+"\" "+query
    p = commands.getoutput(cmd)
    
    networks = []
    if p is not None:
        networks = [network for network in p.split('\n')]
        
    print networks
    return networks

# #parse through string and retreive score
# list_of_best_individuals= []
# list_of_best_individuals.append(best)

# #find max in list, return max and delete it from the list
# def get_and_remove_max(list):
#     listMax= list[0]
#     maxIndex=0
#     for i in range (len(list)):
#         if list[i]>listMax:
#             listMax= list[i]
#             maxIndex=i


#     del list[maxIndex]
#     return best

# #store top 5 elements
# def store_top_5(list):
#     top5_list= [5]
#     for i in range len(top5_list):
#         top5_list.append(get_and_remove_max(list))
#     return top5_list

#average for each generation
#def avg_4_each_gen(list):
#total=0
    #for i in range len(list):
       # total+=list[i]
    #return total/ len(list)


