#coding=utf-8
import sys
try:
    import requests
    def get_down(url, path):
        files = {'file': open(path, 'rb')}
        r = requests.post(url, files=files)
        return r.status_code
except :
    import commands
    def get_down(url, path):
        http_code = ''
        cmd = 'curl  -F "filename=@%s" %s  -w %s  -o /dev/null' % (path, url, '%{http_code}')
        result = commands.getstatusoutput(cmd)
        if result[0] == 0:
            http_code = 200
        return http_code

if __name__ == '__main__':
    url = sys.argv[1]
    path = sys.argv[2]
    http_code = get_down(url,path)
    print http_code
