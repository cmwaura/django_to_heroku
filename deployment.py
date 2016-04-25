'''
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
|THIS PROJECT IS A DEPLOYMENT TOOL HELPED TO ASSIST DEVELOPERS PUSH THEIR WORK TO SERVERS HOSTED|
|BY HEROKU.                                                                                     |
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|

HOW THIS TOOL WILL WORK
-------------------------
Assuming that you have initialized your git repository and hae been committing your changes, this 
tool is meant to be used right when you are about to deploy. It will handle all the deployment 
details for you as well as save your credential keys to a json file in your current directory. 
It will then add the json file to the gitignore file and change your settings debug to False as well
as set the secret key to its valis os.get(value). Right after deployment it will open the heroku bash
and add the secret key to the config file in heroku for safe keeping.

To summarize all the hooplah.
WSGI.py:
1) add the relevant wsgi line for deployment
2) change the relative settings and this includes but is not limited to 
	1)add staticfile storage keys for amazon web services
	2) save the secret keys as a JSON file and add it to the gitignore
	
3) add the secret information to heroku config menu and  link the information to the settings file.

'''
import os
import codecs

class BaseFile(object):
	'''
	This is the base file that will contain more of the common elements that other classes can and will 
	inherit from. The main purpose of this specific module is just to be the parent module.
	'''
	def __init__(self, filename):
		'''
		initializes the file name where it is located via filename and the path
		'''
		self.path =  os.path.dirname(os.path.abspath("__file__"))
		self.text_file = os.path.join(self.path, filename)
	def open_text_file(self):
		'''
		opens the text file for writing.
		'''
		self.text_file = codecs.open(self.text_file, "w")
		return self.text_file


class WsgiFile(object):
	'''
	This is specific for the WSGI file in the Django structure. At the end of this process, all the details 
	required on the wsgi file will be transfered from the wsgi_text file
	'''
	def __init__(self, directory_tree, text_file="wsgi_text.txt"):
		'''
		Initializing the actual wsgi.py file in the django directory as well as the wsgi_text.txt file 
		which contains the actual commands needed to deploy your project.
		directory_tree = where the file is stored. This for instance if your file lives one folder down,
		it would be "folder/wsgi.py"
		text_file = wsgi_text.txt, text file that is used for comparison
		'''
		self.path =  os.path.dirname(os.path.abspath("__file__"))
		self.wsgi_file = os.path.join(self.path, directory_tree)
		self.text_file = text_file
		
	def open_wsgi_file(self):
		self.open_wsgi = codecs.open(self.wsgi_file).read().splitlines()
		return self.open_wsgi

	def open_wsgitxt_file(self):
		comp_file = codecs.open(self.text_file).read().split('\n')
		return comp_file
	
	def compare_files(self, file1, file2):	
		'''
		this is just an option to compare both files and get all the common objects in the files
		file1 = the wsgi.py file
		file2 = wsgi_text.txt
		'''	
		same = set(file1).intersection(file2)
		same.discard('\n')
		return same

	def contrast_files(self, file1, file2):
		'''
		this is just an option to contrast both files and get all the difference objects in the files
		file1 = the wsgi.py file
		file2 = wsgi_text.txt
		return : difference between both files
		'''
		difference = set(file2).difference(file1)		
		return difference

	def write_to_wsgi(self, difference):
		'''
		takes in the difference between the files and writes it to the wsgi.py file. This ensures that 
		the wsgi deployment settings that lived in wsgi_text is now added to wsgi.py
		'''

		transfer = open(self.wsgi_file, 'a')
		linestr = ''
		if len(difference) > 0:			
			linestr = '\n'.join(difference)
			transfer.write(linestr)
		return transfer	

class ProcFile(BaseFile):
	def __init__(self, **kwargs):
		'''
		initializes a filename called Procfile
		'''
		super(ProcFile, self).__init__(filename="Procfile", **kwargs)
	
	def write_to_file(self, wsgi_directory, astring):
		'''
		takes in the wsgi_directory and writes the Procfile statement fr gunicorn
		it takes in the astring that is either nolog or log
		wsgi_directory:directory where your wsgi file lives
		astring: "log or nolog" for the option of logging
		'''

		cap_log = "web: gunicorn " + wsgi_directory+".wsgi --log-file -"
		if astring:
			if astring == "log":
				self.text_file.write(cap_log)
			elif astring == "nolog":
				self.text_file.write("web: gunicorn " + wsgi_directory+".wsgi")
			else:
				print "there are only two options log/nolog"
		else:
			print "Error: astring option needed to execute."

	def close_proc(self):
		self.text_file.close()

class Settings(BaseFile):
	def __init__(self, directory_tree, **kwargs):
				
		super(Settings, self).__init__(filename=directory_tree, **kwargs)

	def static_storage(self, static_loc):
		'''
		This is the point that you will describe the where you wll store the static files. For instance you may decide that
		amazon is the best place to store your static files or you may choose the django whitenoise for staticfile storage
		static_loc: the location where your static files will be loaded from. 
		So far static_loc supports: 
		Amazon s3 as s3
		Djangowhitenoise as dwn

		'''
		return static_loc.lower()

	def djangowhitenoise(self):
		security_dict={}
		security_dict['STATICFILES_STORAGE'] = 'whitenoise.django.GzipManifestStaticFilesStorage'
		return security_dict
	
	def amazon_storage_var(self, AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY):
		security_dict = {}	
		AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

		security_dict["AWS_S3_CUSTOM_DOMAIN"] = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
		security_dict["STATIC_URL"] = "http://%s/" % AWS_S3_CUSTOM_DOMAIN
		security_dict["STATICFILES_STORAGE"] = 'storages.backends.s3boto.S3BotoStorage'
		security_dict["AWS_STORAGE_BUCKET_NAME"] = AWS_STORAGE_BUCKET_NAME
		security_dict["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID
		security_dict["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY

		return security_dict

	def json_security(self, security_dict):
		import json
		json_sec = json.dumps(security_dict)
		return json_sec

	def save_json_security(self, json_security):
		filename = codecs.open("security_cred.json", "w")
		filename.write(json_security)
		filename.close()
	
	def dict_to_var(self, security_dict, directory_tree):
		settings_file = codecs.open(directory_tree, 'a')
		for key in security_dict:
			if key != "STATICFILES_STORAGE" and key !="STATIC_URL" :
				value ='os.environ.get('+"'"+key+"'"+')'
				settings_file.write(key +" = "+ value + '\n')
			elif key == "STATICFILES_STORAGE":
				settings_file.write("\n")
				value = '{0}{1}{0}'.format("'", security_dict["STATICFILES_STORAGE"])
				settings_file.write(key + " = " + value)
			elif key == "STATIC_URL":
				value = '{0}{1}{0}{2}'.format("'", "http://%s/","% AWS_S3_CUSTOM_DOMAIN")
				settings_file.write(key+ " = " + value+ "\n")
			else:
				print "this error should not occur. Please turn back"			
		settings_file.close()

class GitIgnore(BaseFile):
	def __init__(self, **kwargs):
		super(GitIgnore, self).__init__(filename=".gitignore", **kwargs)

	def open_text_file(self):
		'''
		opens the text file for writing.
		'''
		self.text_file = codecs.open(self.text_file, "a")
		return self.text_file

	def write_to_file(self):
		filelist = ['deployment.py', 'security_cred.json', 'wsgi_text.txt']
		for name in filelist:
			self.text_file.write(name + "\n")
		self.text_file.close()


class HerokuConfig(object):

	def __init__(self, command="heroku config:set"):
		self.command = command


	def amazon(self, amazon_storage_var):
		for key, value in  amazon_storage_var.iteritems():
			print self.command ,key + "=" + str(value)
			os.system(self.command + ' '+key + "=" + str(value))




#------------------testing---------------------------#



g = GitIgnore()
g.open_text_file()
g.write_to_file()
s = Settings("example/settings.py")
security_dict = s.djangowhitenoise()
heroku = HerokuConfig()
heroku.amazon(security_dict)
# print security_dict
print "running"
s.dict_to_var(security_dict, "example/settings.py")
print "ran"
# json_security = s.json_security(security_dict)
# s.save_json_security(json_securityg

# pro = ProcFile()
# pro.open_text_file()
# pro.write_to_file("example", "log")
# pro.close_proc()
# w = WsgiFile('example/wsgi.py')
# filed1 = w.open_wsgi_file()
# filed2= w.open_wsgitxt_file()
# # print w.compare_files(filed1, filed2)
# difference = w.contrast_files(filed1, filed2)
# print difference
# w.write_to_wsgi(difference)
# # w.add_lines(filed)



