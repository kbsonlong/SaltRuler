#coding:utf-8
import sys
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi
class   PostHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        upload_dir = '/src/salt'      ###配置Salt-Master的file_roots base路径，默认/src/salt
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     }
        )
        self.end_headers()
        self.wfile.write('Client: %sn ' % str(self.client_address) )
        self.wfile.write('User-agent: %sn' % str(self.headers['user-agent']))
        self.wfile.write('Path: %sn'%self.path)
        self.wfile.write('Form data:n')
        try:
            for field in form.keys():
                field_item = form[field]
                filename = field_item.filename
                filevalue  = field_item.value
                filesize = len(filevalue)#文件大小(字节)
                with open(upload_dir + '/'+filename.decode('utf-8'),'wb') as f:
                    f.write(filevalue)
            self.send_response(200,message='filesize: %s' % filesize )
        except Exception as e:
            self.send_response(500,message=e)

def main():
    ftp_host = ''
    if sys.argv[1:]:
        port = int(sys.argv[1])
    else:
        port = 8002
    server = HTTPServer((ftp_host,port),PostHandler)
    print 'Listening port %s' % port
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()

if __name__=='__main__':
    main()