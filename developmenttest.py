from development import *
import unittest

s = Settings("example/settings.py")
security_dict = s.amazon_storage_var("me", 123, 456)
heroku = HerokuConfig()
print heroku.amazon(security_dict)
# print security_dict
# print s.dict_to_var(security_dict, "example/settings.py")
# json_security = s.json_security(security_dict)
# s.save_json_security(json_security)

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
