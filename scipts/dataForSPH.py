from odb2vtp import*



def main():
    script = "./extractNodePosition.py"

    # path_root = "./test/"
    # path_root = "F:/ZAY/Projects/SPH/abaqus/balloon/balloon_shell_validation/"
    path_root = "F:/ZAY/Projects/SPH/abaqus/beam_element/beam_paper/"

    jobNo = 180
    # jobNo = 1

    polyType = "Line"
    # polyType = "Quad"

    args = path_root+"Job-%d.odb"%jobNo
    
    # args += " part-1-1"
    # args += " part-2-1"
    # args += " balloon-1"
    args += " beam-1"
    
    # args += " Step-3"
    
    # args += " 32"
    odb2vtp(script, args, polyType)

    # data for sph
    # data2particle()


if __name__ == "__main__":
    main()