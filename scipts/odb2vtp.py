import numpy as np
from mylib.myPolyData import save_polydata
import os
from HelpfulFunction import *

def odb2vtp(script, args, polyType):   
    abaqus = os.environ.get("ABAQUS_BAT_PATH", "abaqus")
    print(f"{abaqus} python {script} {args}")

    os.system(f"{abaqus} python {script} {args}")

    pos0 = np.loadtxt("./tempData/position_0.csv", delimiter=',')
    pos1 = np.loadtxt("./tempData/DefCoor.csv", delimiter=',')
    
    outputNodesDeformed("./tempData/DefNodesInp.txt", pos1)

    eles = np.loadtxt("./tempData/elementsIds.csv", dtype=int, delimiter=',')

    # pos0 = rotateNodes(pos0,"x", 90)
    # pos1 = rotateNodes(pos1,"x", 90)

    U = np.loadtxt("./tempData/U.csv", delimiter=',')
    UR = np.loadtxt("./tempData/UR.csv", delimiter=',')
    V = np.loadtxt("./tempData/V.csv", delimiter=',')
    VR = np.loadtxt("./tempData/VR.csv", delimiter=',')

    pd = addPoints(pos0)
    addPolys(eles, pd, polyType)
    save_polydata(pd, "pos0.vtp")

    setPoints(pos1, pd)
    addNodeVariable(U, pd, "displacement")
    addNodeVariable(UR, pd, "displacement-rotation")
    addNodeVariable(V, pd, "velocity")
    addNodeVariable(VR, pd, "velocity-rotation")
    save_polydata(pd, "pos1.vtp")


def data2particle():
    pos0 = np.loadtxt("./tempData/position_0.csv", delimiter=',')
    pos1 = np.loadtxt("./tempData/DefCoor.csv", delimiter=',')
    eles = np.loadtxt("./tempData/elementsIds.csv", dtype=int, delimiter=',')

    U = np.loadtxt("./tempData/U.csv", delimiter=',')
    UR = np.loadtxt("./tempData/UR.csv", delimiter=',')
    V = np.loadtxt("./tempData/V.csv", delimiter=',')
    VR = np.loadtxt("./tempData/VR.csv", delimiter=',')

    meshfactor = 1
    Pos0, Area0, Normal0 = calcCenterAreaNormal(pos0, eles, meshfactor)
    pd0 = addPoints(Pos0)
    addVertex(pd0)
    addNodeVariable(Normal0,pd0, "Normal")
    addNodeVariable(Area0, pd0, "Area")
    save_polydata(pd0, "particle0.vtp")

    Pos1, Area1, Normal1 = calcCenterAreaNormal(pos1, eles, meshfactor)
    U1 = calcVariableOfElements(U, eles)
    UR1 = calcVariableOfElements(UR, eles)
    V1 = calcVariableOfElements(V, eles)
    VR1 = calcVariableOfElements(VR, eles)

    pd1 = addPoints(Pos1)
    addVertex(pd1)
    addNodeVariable(Area1, pd1, "Area")
    addNodeVariable(Normal1, pd1,"Normal")
    addNodeVariable(U1, pd1, "displacement")
    addNodeVariable(UR1, pd1, "displacement-rotation")
    addNodeVariable(V1, pd1, "velocity")
    addNodeVariable(VR1, pd1, "velocity-rotation")
    save_polydata(pd1, "particle1.vtp")



if __name__ == "__main__":
    data2particle()

