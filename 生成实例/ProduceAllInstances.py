# this script has to be execute with this command line:
# python produceAllInstances.py

import os.path

# the directory to put the instances
dirInstances = "instances"

# the directory where the generator can be found
dirGenerator = "./"

# list of instance parameters to produce
# of course you can change this list
listRho = [-0.2]
listM   = [2]
listN   = [20,50]
listD   = [0.8]

# number of instance per tuple of parameters
nbInst = 1

# create the directory of instances if necessary
if not os.path.isdir(dirInstances):
    os.mkdir(dirInstances)

# Go to produce all the instances. 
# It can take a lot of time (hours) if there is a lot of large instances !
for M in listM:
    for N in listN:
        for d in listD:
            for r in listRho:
                for n in range(nbInst):
                    name = "mubqp_" + str(r) + "_" + str(M) + "_" + str(N) + "_" + str(d) + "_" + str(n) + ".dat"
                        
                    if r > (-1.0 / (M - 1)):
                        command_line = "R --slave --no-restore --file=" + dirGenerator + "mubqpGenerator.R --args " + str(r) + " " + str(M) + " " + str(N) + " " + str(d) + " " + str(n) + " " + dirInstances + "/" + name
                        print("执行命令:",command_line)
                        os.system(command_line)