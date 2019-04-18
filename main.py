from rename_dicom import RenameImages
import sys


# Put the root as the argument. Assuming it has subject folders such as 3102,3123 etc
# example : python main.py /Users/mayank/documents/ppmi_swedd_dl_mayank/PPMI

rootdir = sys.argv[1]
# rootdir = "/Users/souvik/Documents/NU/Lectures/Spring2019/EECS338/Data/FirstDownload/SweddDTMRIRAW/PPMI"

#instantiate an object of RenameImages
obj = RenameImages(rootdir)

# obj.check_names()
obj.rename_images()
# obj.check_names()

