import numpy as np
import vtk
from mylib.tranformation import rotation2d

def addPoints(nodes, pd=None):
    if pd == None:
        polydata = vtk.vtkPolyData()
    else:
        polydata = pd
    pts = vtk.vtkPoints()
    for i in range(len(nodes)):
        p = nodes[i]
        pts.InsertNextPoint(tuple(p))
    polydata.SetPoints(pts)
    return polydata
    
def addVertex(pd, nodes=None):
    vtx = vtk.vtkCellArray()
    if nodes == None:
        for i in range(pd.GetNumberOfPoints()):
            vtx.InsertNextCell(1)
            vtx.InsertCellPoint(i)
    else:
        pts = vtk.vtkPoints()
        for i in range(len(nodes)):
            p = nodes[i]
            pId = pts.InsertNextPoint(p)
            vtx.InsertNextCell(1)
            vtx.InsertCellPoint(pId)
        pd.SetPoints(pts)
    pd.SetVerts(vtx)

def setPoints(nodes, pd) -> None:
    '''replace the points of a polydata obj with new points'''
    if not pd.GetNumberOfPoints() == len(nodes):
        print("nodes number(%d) =/= pd.points number(%d)\nthe nodes cannot match the Polydata"%(len(nodes), pd.GetNumberOfPoints()))
        exit(1)
    for i in range(len(nodes)):
        p = tuple(nodes[i])
        pd.GetPoints().SetPoint(i, p)

def addPolys(elementIds, pd, polyType) -> None:
    '''add polys to the polydata obj
    line    : polyType="Line" or 2
    triangle: polyType="Tri" or 3
    quad    : polyType="Quad" or 4
    '''
    pType = 0
    if polyType == "Line":
        pType = 2
    elif polyType == "Tri":
        pType = 3
    elif polyType == "Quad":
        pType = 4
    else:
        pType = len(elementIds[0])
    if not (0 < pType <= 4):
        print("polyType is wrong!")
        exit(1)

    cellArray = vtk.vtkCellArray()
    for i in range(len(elementIds)):
        Ids = elementIds[i]
        if pType == 2:
            poly = vtk.vtkLine()
        elif pType == 3:
            poly = vtk.Triangle()
            poly.GetPointIds().SetNumberOfIds(pType)
        elif pType == 4:
            poly = vtk.vtkQuad()
            poly.GetPointIds().SetNumberOfIds(pType)
        for j in range(pType):
            poly.GetPointIds().SetId(j, int(Ids[j])-1)
        cellArray.InsertNextCell(poly)
    if pType == 2:
        pd.SetLines(cellArray)
    else:
        pd.SetPolys(cellArray)

def addNodeVariable(varArray, pd, varName) -> None:
    if not pd.GetNumberOfPoints() == len(varArray):
        print( "variable-array number(%d) =/= pd.points number(%d)\n\
            the variable-array cannot match the Polydata"%(len(varArray), pd.GetNumberOfPoints()))
        exit(1)

    dim = len(varArray.shape)
    varVec = vtk.vtkFloatArray()
    varVec.SetName(varName)
    if dim == 1:
        varVec.SetNumberOfComponents(dim)
    elif dim == 2:
        varVec.SetNumberOfComponents(3)
    else:
        print("check dim of var!")
        exit(1)

    for i in range(len(varArray)):
        v = varArray[i]
        if dim == 1:
            varVec.InsertValue(i, v)
        elif len(v) == 3:
            varVec.InsertTuple3(i, v[0], v[1], v[2])
        else:
            print("check dim of var!")
            exit(1)

    pd.GetPointData().AddArray(varVec)


def norm(vector:np.array):
    return np.linalg.norm(vector)

def normalize(vector:np.array):
    return vector/norm(vector)

# generate centers
def calcCenterAreaNormal(nodes, eleIds, mesh_factor=1):
    elesNum = len(eleIds)
    eleType = len(eleIds[0])
    centerCoordinates = np.zeros((elesNum, 3))
    areaArray = np.zeros(elesNum)
    normalArray = np.zeros_like(centerCoordinates)
    for i in range(elesNum):
        nIds = eleIds[i]
        # center
        tmpC = np.zeros((eleType,3))
        for j in range(eleType):
            tmpC[j] = nodes[nIds[j]-1]
        centerCoordinates[i] = np.mean(tmpC, 0)

        # normal
        v1 = nodes[nIds[1]-1] - nodes[nIds[0]-1]
        v2 = nodes[nIds[2]-1] - nodes[nIds[0]-1]
        normal = np.cross(v1, v2)
        normalArray[i] = normalize(normal)

        # area
        vAC = nodes[nIds[2]-1] - nodes[nIds[0]-1]
        vBD = nodes[nIds[3]-1] - nodes[nIds[1]-1]
        cosTheta = np.dot(vAC, vBD) / norm(vAC) / norm(vBD)
        sinTheta = np.sqrt(1 - cosTheta**2)
        areaArray[i] = 0.5 * norm(vAC) * norm(vBD) * sinTheta / mesh_factor

    return centerCoordinates, areaArray, normalArray


# compute variables of elements
def calcVariableOfElements(varArr, eleIds):
    elesNum = len(eleIds)
    nIdsNum = len(eleIds[0])
    varType = len(varArr.shape)

    if varType == 1:  # scalar
        varCenerArr = np.zeros(elesNum)
    elif varType == 2:
        varCenerArr = np.zeros((elesNum, 3))
    else:
        print("check dim of var!")
        exit(1)

    for i in range(elesNum):
        nIds = eleIds[i]
        if varType == 1:
            tmpC = np.zeros(nIdsNum)
        elif varType == 2:
            tmpC = np.zeros((nIdsNum,3))
        else:
            print("check dim of var!")
            exit(1)
        for j in range(nIdsNum):
            tmpC[j] = varArr[nIds[j]-1]
        varCenerArr[i] = np.mean(tmpC,0)
    return varCenerArr


# output data files
def output(fileName, data) -> None:
    with open(fileName, 'w', newline='') as f:
        for i in range(len(data)):
            p = data[i]
            if len(data.shape) == 3:
                row = '%.8f \t%.8f \t%.8f'%(p[0],p[1],p[2])
            elif len(data.shape) == 1:
                row = '%.8f \t%.8f \t%.8f'%(p,0,0)
            if i < len(data)-1:
                row += "\n"
            f.write(row)

def outputNodesDeformed(fileName, data)-> None:
    with open(fileName, 'w', newline='') as f:
        for i in range(len(data)):
                n = list(data[i])
                row = '\t%d,\t%.8f, \t%.8f, \t%.8f\n'%(i+1, n[0],n[1],n[2])
                f.write(row)

def rotateNodes(nodes, axis:str, degree):
    newNodes = nodes.copy()
    for i in range(len(nodes)):
        nn = nodes[i]
        indices = [0,0]
        if axis == "x":
            # y, z
            indices[0] = 1
            indices[1] = 2
        elif axis == "y": 
            # z, x
            indices[0] = 2
            indices[1] = 0
        elif axis == "z":
            # x, y
            indices[0] = 0
            indices[1] = 1
        i0, i1 = indices[0],indices[1]
        newNodes[i][i0] ,newNodes[i][i1] =\
            rotation2d(nn[i0],nn[i1], angle=degree)
    return newNodes
        

