#coding=utf-8
import sys
sys.path.append("..")
from SaltRuler.glob_config import glob_config
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi
class   PostHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     }
        )
        self.send_response(200)
        self.end_headers()
        self.wfile.write('Client: %sn ' % str(self.client_address) )
        self.wfile.write('User-agent: %sn' % str(self.headers['user-agent']))
        self.wfile.write('Path: %sn'%self.path)
        self.wfile.write('Form data:n')
        # upload_dir = '../upload/'
        upload_dir = glob_config('ftp','upload_dir')
        for field in form.keys():
            field_item = form[field]
            filename = field_item.filename
            filevalue  = field_item.value
            filesize = len(filevalue)#文件大小(字节)
            with open(upload_dir + '/'+filename.decode('utf-8'),'wb') as f:
                f.write(filevalue)
        return filesize


def main():
    ftp_host = glob_config('ftp', 'host')
    ftp_port = int(glob_config('ftp','port'))
    server = HTTPServer((ftp_host,ftp_port),PostHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()

if __name__=='__main__':
    main()