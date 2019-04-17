import os
import pydicom #needs to be installed - doesn't usually come with the python installation - pip install pydicom

class RenameImages:


	'''

	This is the class constructor. It initializes the object of the class Rename Images

	@param - 
	rootdir - here the rootdir is the root of the directory in which your patient images are in

	'''
	def __init__(self, rootdir):

		self.rootdir = rootdir

	'''
	This function renames all the dicom files header data in the root directory
	The root directory in this example case was - 
	rootdir = '/Users/souvik/Documents/NU/Lectures/Spring2019/EECS338/Data/FirstDownload/SWEDDfilteredSPECT/PPMI'

	@params - none


	@returns - 
	this method doesn't return anything

	'''
	def rename_images(self):


		'''
		Patient names have been de identified in our case
		Need to find the tag corresponding to the patient name and id
		'''
		#it is helpful to first load the image (say in a var d) and then use d.dir("anystringyouwanttofindintag")
		#this lets us view all the tags

		#iterate through subject folders. Such as 3102,3103,3109 etc...
		for filename in os.listdir(self.rootdir):

			subject_dir = self.rootdir + '/' + filename

			#save the jubject name for the reference later
			subject_name = filename


		    #iterate through the directories till the subdirectories and get all the files names
			for subdir, dirs, files in os.walk(subject_dir):


				#we iterate through all the files - in our case we had just one file per directory
				#but it doesn't matter
			    for file in files:
			    	name, ext = os.path.splitext(file)
			    	if ext != ('.dcm'):
			    		continue
			    	file_name =  (os.path.join(subdir, file))
			    	curr_image = pydicom.dcmread(file_name)
			    	curr_patient_name = curr_image.PatientName
			    	curr_patient_id = curr_image.PatientName
			    	curr_patient_name_change = subject_name
			    	curr_patient_id_change = curr_patient_name_change+'_BL'
			    	curr_image.PatientName = curr_patient_name_change
			    	curr_image.PatientID = curr_patient_id_change
			    	print(curr_patient_name," - name changed to - ",curr_patient_name_change)
			    	print(curr_patient_id," - id changed to - ",curr_patient_id_change)
			    	print('')
			    	curr_image.save_as(file_name)


	'''
	This function checks what the names and ids of the images are currently

	@params - none
	'''
	def check_names(self):

		#iterate through the directories till the subdirectories and get all the files names
		for subdir, dirs, files in os.walk(self.rootdir):
            

			#we iterate through all the files - in our case we had just one file per directory
			#but it doesn't matter
		    for file in files:
		    	name, ext = os.path.splitext(file)
		    	if ext != ('.dcm'):
		    		continue
		    	file_name =  (os.path.join(subdir, file))
		    	curr_image = pydicom.dcmread(file_name)
		    	print("Name of current image - ", curr_image.PatientName)
		    	print("Id of current image - ", curr_image.PatientID)
		    	print('')


    



