import numpy as np
from mylib.myPolyData import save_polydata
from mylib.myfunc import pathCheckAndMakeEmpty,dirCheck
import os
from HelpfulFunction import *

def odb2vtp(script, args, polyType, fileName='', vtpPath='./', outputVariable=True):   
    abaqus = os.environ.get("ABAQUS_BAT_PATH", "abaqus")
    print(f"{abaqus} python {script} {args}")

    os.system(f"{abaqus} python {script} {args}")
    print("Abaqus python is done.")

    pos0 = np.loadtxt("./tempData/position_0.csv", delimiter=',')
    pos1 = np.loadtxt("./tempData/DefCoor.csv", delimiter=',')
    
    outputNodesDeformed("./tempData/DefNodesInp.txt", pos1)

    eles = np.loadtxt("./tempData/elementsIds.csv", dtype=int, delimiter=',')

    # pos0 = rotateNodes(pos0,"y", -90)
    # pos1 = rotateNodes(pos1,"y", -90)

    # pos0 = reflectNodes(pos0, "x")
    # pos1 = reflectNodes(pos1, "x")

    U = np.loadtxt("./tempData/U.csv", delimiter=',')
    if outputVariable:
        UR = np.loadtxt("./tempData/UR.csv", delimiter=',')
        V = np.loadtxt("./tempData/V.csv", delimiter=',')
        VR = np.loadtxt("./tempData/VR.csv", delimiter=',')

    pd = addPoints(pos0)
    addPolys(eles, pd, polyType)
    vtpPath = dirCheck(vtpPath)
    pathCheckAndMakeEmpty(vtpPath)
    if fileName:
        save_polydata(pd, vtpPath + fileName+'_init.vtp')
    else:
        save_polydata(pd, vtpPath + "initial_pos.vtp")

    setPoints(pos1, pd)
    addNodeVariable(U, pd, "Displacement")
    if outputVariable:
        addNodeVariable(UR, pd, "Rotation")
        addNodeVariable(V, pd, "Velocity")
        addNodeVariable(VR, pd, "AngularVeloctiy")
    if fileName:
        save_polydata(pd, vtpPath + fileName+'.vtp')
        # save_polydata(pd, vtpPath + fileName+'.vtp', binary=True)
    else:
        save_polydata(pd, vtpPath + "deformed_pos.vtp")


def data2particle(filePathRoot, midName, meshfactor=1, vtpPath='./'):
    pos0 = np.loadtxt("./tempData/position_0.csv", delimiter=',')
    pos1 = np.loadtxt("./tempData/DefCoor.csv", delimiter=',')
    eles = np.loadtxt("./tempData/elementsIds.csv", dtype=int, delimiter=',')

    U = np.loadtxt("./tempData/U.csv", delimiter=',')
    UR = np.loadtxt("./tempData/UR.csv", delimiter=',')
    V = np.loadtxt("./tempData/V.csv", delimiter=',')
    VR = np.loadtxt("./tempData/VR.csv", delimiter=',')
    print("Data is loaded.")

    Pos0, Area0, Normal0 = calcCenterAreaNormal(pos0, eles, meshfactor)
    pd0 = addPoints(Pos0)
    addVertex(pd0)
    addNodeVariable(Normal0,pd0, "Normal")
    addNodeVariable(Area0, pd0, "Area")

    # output initial data
    filePathRoot = dirCheck(filePathRoot)
    vtpPath = dirCheck(vtpPath)
    pathCheckAndMakeEmpty(filePathRoot)
    save_polydata(pd0, vtpPath + "particle0.vtp")
    output(filePathRoot + "PositionData0.txt", Pos0)
    output(filePathRoot + "NormalData0.txt", Normal0)
    output(filePathRoot + "AreaQuadrangleData0.txt", Area0)
    print("Initial data is done.")

    Pos1, Area1, Normal1 = calcCenterAreaNormal(pos1, eles, meshfactor)
    U1 = calcVariableOfElements(U, eles)
    UR1 = calcVariableOfElements(UR, eles)
    V1 = calcVariableOfElements(V, eles)
    VR1 = calcVariableOfElements(VR, eles)

    pd1 = addPoints(Pos1)
    addVertex(pd1)
    addNodeVariable(Area1, pd1, "Area")
    addNodeVariable(Normal1, pd1,"Normal")
    addNodeVariable(U1, pd1, "Displacement")
    addNodeVariable(UR1, pd1, "Rotation")
    addNodeVariable(V1, pd1, "Velocity")
    addNodeVariable(VR1, pd1, "AngularVelocity")
    save_polydata(pd1, vtpPath + "particle1.vtp")

    output(filePathRoot + "PositionData" + midName + ".txt", Pos1)
    output(filePathRoot + "NormalData" + midName + ".txt", Normal1)
    output(filePathRoot + "AreaQuadrangleData" + midName + ".txt", Area1)
    output(filePathRoot + "Variable-UR" + midName + ".txt", UR1)
    output(filePathRoot + "Variable-V" + midName + ".txt", V1)
    output(filePathRoot + "Variable-VR" + midName + ".txt", VR1)
    print("Deformed data is done.")


if __name__ == "__main__":
    data2particle()

