from odb2vtp import*
from mylib.myfunc import dirCheck


def archBeamData():
    script = "./extractNodePosition.py"

    # path_root = "./test/"
    path_root = "F:/ZAY/Projects/SPH/abaqus/beam_element/beam_paper/"

    jobNo = 186
    polyType = "Line"
    instanceName = "beam-1"

    ofname = "arch-g-750"

    stepNo = 0
    frameNo = 0

    args = path_root + "Job-%d.odb"%jobNo + " " + instanceName
    midName = ""
    filePath = "./arch/Job-%d/"%jobNo
    if stepNo > 0 :
        args += (" Step-%d"%stepNo)
        midName = "-step%d"%(stepNo)
        if frameNo > 0:
            args += (" %d"%frameNo)
            midName = "-step%d-%d"%(stepNo, frameNo)
            filePath += midName
            filePath = dirCheck(filePath)

    odb2vtp(script, args, polyType, ofname, filePath)

def shellBalloonData():
    script = "./extractNodePosition.py"

    # path_root = "./test/"
    path_root = "F:/ZAY/Projects/SPH/abaqus/balloon/balloon_shell_validation/"

    jobNo = 96
    polyType = "Quad"
    instanceName = "balloon-1"
    stepNo = 3
    frameNo = 143

    args = path_root + "Job-%d.odb"%jobNo + " " + instanceName
    midName = ""
    filePath = "./balloon/Job-%d/"%jobNo
    if stepNo > 0 :
        args += (" Step-%d"%stepNo)
        midName = "-step%d"%(stepNo)
        if frameNo > 0:
            args += (" %d"%frameNo)
            midName = "-step%d-%d"%(stepNo, frameNo)
            filePath = "./balloon/Job-%d"%jobNo + midName
            filePath = dirCheck(filePath)

    vtp_path = "./vtp_check/"
    odb2vtp(script, args, polyType, vtpPath=vtp_path)

    # data for sph
    coef = 4
    mesh_factor = ((0.125/coef)**2)
    # a = 
    # mesh_factor = a**2

    data2particle(filePath, midName, mesh_factor, vtp_path)

if __name__ == "__main__":
    archBeamData()
    # shellBalloonData()