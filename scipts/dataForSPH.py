from odb2vtp import*
from mylib.myfunc import dirCheck


def archBeamData():
    script = "./extractNodePosition.py"

    # path_root = "./test/"
    path_root = "F:/ZAY/Projects/SPH/abaqus/beam_element/beam_paper/"

    jobNo = 194
    polyType = "Line"
    instanceName = "beam-1"

    # ofname = "beam-follow-load-5k"
    ofname = "arch-3dArchPara-90w"

    stepNo = 0
    frameNo = 0

    args = path_root + "Job-%d.odb"%jobNo + " " + instanceName
    midName = ""
    filePath = "./beam/Job-%d"%jobNo
    if stepNo > 0 :
        args += (" Step-%d"%stepNo)
        midName = "-step%d"%(stepNo)
        if frameNo > 0:
            args += (" %d"%frameNo)
            midName = "-step%d-%d"%(stepNo, frameNo)
            filePath += midName
            filePath = dirCheck(filePath)

    odb2vtp(script, args, polyType, ofname, filePath, False)

def shellBalloonData():
    script = "./extractNodePosition.py"

    # path_root = "./test/"
    path_root = "F:/ZAY/Projects/SPH/abaqus/balloon/balloon_shell_validation/"
    # path_root = "F:/ZAY/Projects/SPH/abaqus/beam_element/forPatent/"

    jobNo = 97
    polyType = "Quad"
    instanceName = "balloon-1"
    # instanceName = "Part-1-1"
    stepNo = 2
    frameNo = 0

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
    # coef = 4
    # mesh_factor = ((0.125/coef)**2)
    a = 0.2
    mesh_factor = a**2

    data2particle(filePath, midName, mesh_factor, vtp_path)

def stentBeamData():
    script = "./extractNodePosition.py"

    path_root = "F:/ZAY/Projects/SPH/abaqus/beam_element/stent_modeling/"
    # path_root = "F:/ZAY/Projects/SPH/abaqus/beam_element/forPatent/"

    jobNo = 97
    polyType = "Line"
    instanceName = "part-1-1"
    stepNo = 0
    frameNo = 0

    ofname = "Job-%d-stent-braided-4k" % jobNo

    stepNo = 0
    frameNo = 0

    args = path_root + "Job-%d.odb"%jobNo + " " + instanceName
    midName = ""
    filePath = "./stent/Job-%d/"%jobNo
    if stepNo > 0 :
        args += (" Step-%d"%stepNo)
        midName = "-step%d"%(stepNo)
        if frameNo > 0:
            args += (" %d"%frameNo)
            midName = "-step%d-%d"%(stepNo, frameNo)
            filePath += midName
            filePath = dirCheck(filePath)

    odb2vtp(script, args, polyType, ofname, filePath, False)



if __name__ == "__main__":
    # archBeamData()
    shellBalloonData()
    # stentBeamData()