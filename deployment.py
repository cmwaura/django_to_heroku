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
	1)DEBUG = False
	2)add staticfile storage keys for amazon web services
	3) save the secret keys as a JSON file and add it to the gitignore
	4) Add email settings incase of any marketing to be done and save as a JSON.
3) add the secret information to heroku config menu and  link the information to the settings file.

'''
import os
import codecs

class BaseFile(object):
	def __init__(self, filename):
		self.path =  os.path.dirname(os.path.abspath("__file__"))
		self.text_file = os.path.join(self.path, filename)
	def open_text_file(self):
		self.text_file = codecs.open(self.text_file, "w")
		return self.text_file


class WsgiFile(object):
	def __init__(self, filename, text_file="wsgi_text.txt"):
		# self.command = phrase
		self.path =  os.path.dirname(os.path.abspath("__file__"))
		self.wsgi_file = os.path.join(self.path, filename)
		self.text_file = text_file
		
	def open_wsgi_file(self):
		self.open_wsgi = codecs.open(self.wsgi_file).read().splitlines()
		return self.open_wsgi

	def open_wsgitxt_file(self):
		comp_file = codecs.open(self.text_file).read().split('\n')
		return comp_file
	
	def compare_files(self, file1, file2):		
		same = set(file1).intersection(file2)
		same.discard('\n')
		return same

	def contrast_files(self, file1, file2):
		difference = set(file2).difference(file1)		
		return difference

	def write_to_wsgi(self, difference):
		transfer = open(self.wsgi_file, 'a')
		linestr = ''
		if len(difference) > 0:			
			linestr = '\n'.join(difference)
			transfer.write(linestr)
		return transfer	

class ProcFile(BaseFile):
	def __init__(self, **kwargs):
		super(ProcFile, self).__init__(filename="Procfile", **kwargs)
	
	def write_to_file(self, directory, astring):
		cap_log = "web: gunicorn " + directory+".wsgi --log-file -"
		if astring:
			if astring == "log":
				self.text_file.write(cap_log)
			elif astring == "nolog":
				self.text_file.write("web: gunicorn " + directory+".wsgi")
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

	
	def dict_to_var(self, security_dict):

		for key, val in security_dict.items():
			exec(key + "=val")
	# def django_white()


s = Settings("example/settings.py")
security_dict = s.amazon_storage_var("me", 123, 456)
print security_dict
print s.dict_to_var(security_dict)

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



