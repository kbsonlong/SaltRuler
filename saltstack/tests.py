import commands
cmd = 'curl  -F "filename=@%s" %s  -w %s  -o /dev/null' % ('/data/www/remove_img_20170329.txt','http://192.168.234.167:10003','%{http_code}')

result = commands.getstatusoutput(cmd)
if result[0] == 0:
    http_code = 200