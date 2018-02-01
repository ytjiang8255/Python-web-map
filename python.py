#! -*- coding:utf-8 -*-
#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import sep, curdir
import subprocess


#当前代码不需要修改这个URL，由于HTTPServer的第一个参数若填入''就会自动去找到这个IP

URL = ''
PORT = 8000

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path= "/test.html"
        try:
            SendReply = False
            Reply_data = 'NONE'

            if self.path.endswith(".html"):
                mimetype = 'text/html'
                SendReply = True

            if self.path.endswith(".jpg") or self.path.endswith(".PNG"):
                mimetype = 'text/image'
                SendReply = True

            if "do_action" in self.path :
                mimetype = 'text/command'
                Reply_data = do_action(self.path)
                print (Reply_data)
                SendReply = True

            
            #print self.path
            if SendReply == True :
                self.send_response(200)#如果正确返回200
                self.send_header('Content-type', mimetype) #定义下处理的文件的类型
                #self.send_header('Set-Cookie',Set_cookies)
                self.end_headers()#结束处理

                if Reply_data != 'NONE' :
                    self.wfile.write(Reply_data)
                else:
                    f = open(curdir + sep + self.path)  # 获取客户端输入的页面文件名称
                    self.wfile.write(f.read())#通过wfile将下载的页面传给客户
                    f.close() #关闭
        except IOError:
            self.send_error(404, 'file not found: %s'%self.path)

def main():
    try:
       server=HTTPServer(('',PORT),MyHandler) #启动服务
       print ('server start with ' + URL + ':' + str(PORT))

       server.serve_forever()# 一直运行
    except KeyboardInterrupt:
        print ('shutdong  doen server')
        server.socket.close()

def do_action(type):
    return_Code = 'NONE'
    if type == "/do_action=upper_left" :
        print ('do upper_left')
        return_Code = make_thread(['top', '-n', '1'])

    elif type == "/do_action=up":
        print ('do up')
        return_Code = make_thread(['ls', '-l'])

    elif type == "/do_action=upper_right":
        print ('do upper_right')
        return_Code = make_thread(['ls', '-l'])

    elif type == "/do_action=left":
        print ('do left')
        return_Code = make_thread(['ls', '-l'])

    elif type == "/do_action=riki":
        print ('do menu')
        return_Code = make_thread(['ls', '-l'])

    elif type == "/do_action=right":
        print ('do right')
        return_Code = make_thread(['ls', '-l'])

    elif type == "/do_action=lower_left":
        print ('do lower_left')
        return_Code = make_thread(['ls', '-l'])

    elif type == "/do_action=down":
        print ('do down')
        return_Code = make_thread(['ls', '-l'])

    elif type == "/do_action=lower_right":
        print ('do lower_right')
        return_Code = make_thread(['ls', '-l'])

    elif type == "do_action=keyboard":
        print ('do_action=keyboard')
        return_Code = make_thread(['rosrun teleop_twist_keyboard teleop_twist_keyboard.py'])

    else:
        print ('No such command')

    return return_Code


def make_thread(tumple):
    proc = subprocess.Popen(tumple, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout_value = proc.communicate()
    print (stdout_value[0])
    # proc.kill()
    return stdout_value


if __name__=='__main__':
     main()

