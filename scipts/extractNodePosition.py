import numpy as np
from odbAccess import*
import sys
# import os

# name of the odb file
odbName = sys.argv[1]

# part name
partName = sys.argv[2]

# step name
if len(sys.argv) > 3:
    stepName = sys.argv[3]
else:
    stepName = "Step-1"

# frame No.
if len(sys.argv) > 4:
    frameId = int(sys.argv[4])
else:
    frameId = -1

# ====================================================
odb = openOdb(path=odbName)
assembly = odb.rootAssembly
ins = assembly.instances
# print(ins)

iName = partName.upper()
part = assembly.instances[iName]

coordinates_inital = np.zeros((len(part.nodes), 3))
# node_Labels = [] 
# print(len(part.nodes))
for node in part.nodes:
    # coordinates_inital.append(node.coordinates)
    coordinates_inital[node.label-1] = node.coordinates
    # node_Labels.append(node.label)
np.savetxt('./tempData/position_0.csv', coordinates_inital, delimiter=',')

eleIdList = []
for ele in part.elements:
    Ids = ele.connectivity
    eleIdList.append(Ids)
np.savetxt('./tempData/elementsIds.csv', eleIdList, fmt="%d",  delimiter=',')


varialeList = ["U", "UR", "V", "VR"]

step1 = odb.steps[stepName]
Frame = step1.frames[frameId]


# *****************************************************
# node_Labels = (55,56,57,58) 
# node_set = part.NodeSetFromNodeLabels(name='node-label-set',nodeLabels=node_Labels)
# local_dis_values = dis_field.getSubset(region=node_set) 

varArrayDict = {}
for i in range(len(varialeList)):
    variableName = varialeList[i]
    var = Frame.fieldOutputs[variableName]
    # var = Frame.fieldOutputs[variableName].getSubset(region=node_set)
    # varDict[variableName] = var.values
    tmpVar = np.zeros_like(coordinates_inital)
    # print(type(var))
    # print(var)
    # print(type(var.values))
    # print(len(var.values))
    # print(var.values[0])
    # exit()
    for v in var.values:
        # print(type(var.values))
        # print(type(v.instance))
        # print(v.instance)
        # tmpVar.append(v.dataDouble)
        if v.instance and v.instance.name == iName:
            # print(v)
            # print(v.instance)
            # exit()
            tmpVar[v.nodeLabel-1] = v.data
    varArrayDict[variableName] = tmpVar
    # exit()

# print(len(coordinates_inital))
# print(len(varArrayDict['U']))
# print(len(varArrayDict['UR']))

temp_coordinates_inital = np.array(coordinates_inital)
temp_DISP = varArrayDict["U"]
varArrayDict["DefCoor"] = temp_coordinates_inital + temp_DISP
# np.savetxt('position_1.csv', coordinates_deformed, delimiter=',')

for varName, varArray in varArrayDict.items():
    fname = "./tempData/" + varName + ".csv"
    np.savetxt(fname, varArray, delimiter=",")
    print("num of " + varName + ": ", len(varArray))

odb.close
