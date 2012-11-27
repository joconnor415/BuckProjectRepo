    #This can be run in a local machine
    import os, stat, subprocess, commands,
    from pyevolve import G1DBinaryString
    from pyevolve import GSimpleGA
    from pyevolve import Selectors
    from pyevolve import Mutators
    from pyevolve import Statistics

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

    #get and print the list of networks
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

    #parse through string and retreive score
    # list_of_best_individuals= []
    # list_of_best_individuals.append(best)

#source code callback function will be executed every generations
def evolve_callback(ga_engine):
    
    #stats lists
    global top5_raw_score, bottom5_raw_score, raw_st_dev_array, raw_ave_arr, raw_var_array, top5_networks, best_individuals
    internal_pop = ga_engine.getPopulation()
    
    #keep track of stats for each generation
    stats= ga_enginge.getStatistics()
    rawMax= st["rawMax"] #max
    rawMin= st["rawMin"] #min
    rawAve= st["rawAve"] #average
    rawDev= st["rawDev"] #standard deviation
    rawVar= st["rawVar"] #variance

    best_individuals.append(ga_engine.bestIndividual())

  #go through each genrations
  for ind in internal_pop:
    if len(top5_raw_score) < 5:
        top5_raw_score.append(rawMax)
        #st_dev_array.append(rawDev)
        top5_networks.append(ind.getBinary())
    if len(bottom5_raw_score) <5:
          bottom5_raw_score.append(rawMin)
          bottom5_networks.append(ind.getBinary())

    raw_st_dev_array.append(rawDev)
    raw_var_array.append(rawVar)
    else:

  for i in range(5):
    if rawMax > top5_raw_score[i]:
        top5__raw_score[i] = rawMax
        top5_networks[i] = ind.getBinary()
    if rawMin < bottom5_raw_score[i]:
        bottom5__raw_score[i] = rawMin
        bottom5_networks[i] = ind.getBinary()
  break

#basic average values in list function
def avg_func(list):
    total=0
    for i in range(len(list)):
        total+=ind
    return total/ len(list)

total_avg_dev= avg_func(st_dev_array)

# def evolve_callback(ga_engine):
#   global top5_raw_score, bottom5_raw_score, st_dev_array, top5_networks, best_individuals
#   internal_pop = ga_engine.getPopulation()
#   best_individuals.append(ga_engine.bestIndividual())
#   for ind in internal_pop:
#     if len(top5_raw_score) < 5:
#         top5_raw_score.append(ind.score)
#         top5_networks.append(ind.getBinary())
#     else:
#   for i in range(5):
#     if ind.score > top5_raw_score[i]:
#         top5__raw_score[i] = ind.score
#         top5_networks[i] = ind.getBinary()
#   break

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
    # def store_top_5(ga_engine):
        #pop= ga_engine.getPopulation()
    #     top5_list= [5]
    #     for i in range len(top5_list):
    #         top5_list.append(get_and_remove_max(list))
    #     return top5_list

    #basic average values in list function

