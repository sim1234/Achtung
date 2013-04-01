# coding: utf-8

import threading, select, socket, time, sys, math, bz2
import cPickle as pickle


class SubProces(threading.Thread):
            def __init__(self, function, lag = 0, maxduration = 0, *args, **kwargs):
                threading.Thread.__init__(self)
                self.function = function
                self.result = None
                self.running = 2
                self.a = args
                self.k = kwargs
                self.lag = lag / 1000.0
                self.stoper = None
                self.start()
                #if maxduration:
                #    self.stoper = SubProces(self.stop, maxduration, 0)
                    
          
            def run(self):
                self.running = 1
                if self.lag:
                    time.sleep(self.lag)
                self.result = self.function(*self.a, **self.k)
                #if self.stoper:
                #    self.stoper.stop()
                self.running = 0
                
            
            def stop(self):
                if self.running:
                    self.running = 0
                    #if self.stoper:
                    #    self.stoper.stop()
                    self.join()
                    self.join(0)
                    self.join(1)
                
            def get_result(self):
                if self.running:
                    raise RuntimeError("Function didn't finish yet!")
                else:
                    return self.result

def async(f):
    def ff(*args, **kwargs):
        return SubProces(f, 0, 0, *args, **kwargs)
    return ff

def async_wl(lag = 0, maxduration = 0):
    def dec(f):
        def ff(*args, **kwargs):
            return SubProces(f, lag, maxduration, *args, **kwargs)
        return ff
    return dec

def fill_to(v, ln, f = " "):
    if len(v) > ln:
        return v[:ln]
    return v + f * (ln - len(v))

def lans():
    li = []
    for x in socket.gethostbyname_ex(socket.gethostname()):
        if x:
            l = x[0].split(".")
            if len(l) == 4:
                li.append(l[0] + "." + l[1] + "." + l[2] + ".")
    ll = []
    for x in li:
        for i in xrange(0, 256):
            ll.append(x + str(i))
    #ll.pop(ll.index(socket.gethostbyname(socket.gethostname())))
    return ll

@async
def try_connect(ip, port, handshakestr):
    r = ""
    c = MyClient(handshakestr = handshakestr)
    #c.sock.settimeout(10)
    try:
        if c.connect(ip, port):
            r = ip
        else:
            raise Exception()
    except Exception as e:
        print e
    c.close()
    del c
    time.sleep(1)
    return r
        
def search_serv_async(port, handshakestr, pool = 256):
    li = []
    ll = []
    #print lans()
    #for x in lans()[180:190]:
    ln = lans()
    lc = 0
    while len(ll) < pool and lc < len(ln):
            ll.append(try_connect(ln[lc], port, handshakestr))
            lc += 1
            time.sleep(0.001)
    while len(ll):
        x = 0
        while x < len(ll):
            try:
                res = ll[x].get_result()
                if res and not res in li:
                    li.append(res)
                ll.pop(x)
                continue
            except Exception:
                pass
            x += 1
        while len(ll) < pool and lc < len(ln):
            ll.append(try_connect(ln[lc], port, handshakestr))
            #print "added", ln[lc]
            lc += 1
            time.sleep(0.001)
        time.sleep(0.5)
    return li

def search_serv(port, handshakestr):
    li = []
    
    for ip in lans()[180:190]:
        c = MyClient(handshakestr = handshakestr)
        c.sock.settimeout(1)
        try:
            if c.connect(ip, port):
                li.append(ip)
        except Exception:
            pass
        
        c.close()
        #del c.sock
    return li
        

class PContainer(object):
    def __init__(self, info = [], content = None):
        self.i = info
        self.c = content
        
    def SetI(self, info):
        self.i = info
        
    def SetC(self, content):
        self.c = content
    
    def Set(self, info, content):
        self.i = info
        self.c = content
        
    def Get(self):
        return self.i, self.c
    
class PMessage(object):
    
    def __init__(self, msg = ""):
        self.m = str(msg)
        
    def Set(self, msg):
        self.m = str(msg)
        
    def Get(self):
        return self.m
    
class PChange(PContainer):
    
    def __init__(self, name, delta = 0):
        self.i = name
        self.c = delta
        
    def Set(self, delta, name = ""):
        self.c = delta
        if name:
            self.i = name
        
    def Set2(self, old, new, name = ""):
        self.c = new - old
        if name:
            self.i = name


class MyClient(threading.Thread):
    
    def __init__(self, sock = None, fn = None, handshakestr = "MySocketServer"):
        threading.Thread.__init__(self)
        self.running = 0
        self.handshakestr = handshakestr
        self.select_timeout= 0.01
        self.fn = fn
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
            self.running = 1
        self.sock.settimeout(5)
        self.ev = []
        self.ev_op = 0
        self.msg = []
        self.msg_op = 0
        
    def connect(self, host, port):
        #self.sock.settimeout(0.5)
        try:
            self.sock.connect((host, port))
            self.running = 1
            #print "Connected to " + str(host) + ":" + str(port) + "."
        except socket.error as e:
            print "Couldn't connect to " + str(host) + ":" + str(port)+ ".", e
            self.close()
            return 0
        return self.hand_shake()
        
        
    def hand_shake(self):
        self.p_send(self.handshakestr)
        if not self.p_recv() == self.handshakestr:
            self.close()
            return 0
            #raise TypeError("Remote socket not in my type")
        return 1 
        
    def start(self):
        if self.running:
            threading.Thread.start(self)
        else:
            raise RuntimeError("Socket not connected")
    
    def add_event(self, event):
        while self.ev_op:
            time.sleep(0.001)
        self.ev_op = 1
        self.ev.append(event)
        self.ev_op = 0
    
    def pop_event(self, p = -1):
        while self.ev_op:
            time.sleep(0.001)
        self.ev_op = 1
        r = self.ev.pop(p)
        self.ev_op = 0
        return r
    
    def add_msg(self, msg):
        while self.msg_op:
            time.sleep(0.001)
        self.msg_op = 1
        self.msg.append(str(msg))
        self.msg_op = 0
    
    def pop_msg(self, p = -1):
        while self.msg_op:
            time.sleep(0.001)
        self.msg_op = 1
        r = self.msg.pop(p)
        self.msg_op = 0
        return r
    
    def run(self):
        #print "Socket running"
        while self.running:
            inputready, outputready, exceptready = select.select([self.sock],[],[], self.select_timeout)
            for s in inputready: 
                if s == self.sock:
                    d = self.p_recv()
                    if self.fn and d:
                        d = self.fn(self, d)
                    if d:
                        self.add_event(d)
            #print "Socket event"
            while len(self.msg):
                m = self.pop_msg(0)
                self.p_send(m)
        self.close()
        #print "Socket closed"

    def p_send(self, msg):
        try:
            msg = str(len(msg)) + ";" + msg
            while self.running and len(msg):
                sent = self.sock.send(msg)
                if sent == 0:
                    raise Exception("Socket connection broken")
                msg = msg[sent:]
            return 1
        except Exception as e:
            print "Couldn't send data.", e
            self.close()
            return 0

    def p_recv(self):
        try:
            data = ""
            while self.running and not ";" in data:
                d = self.sock.recv(1)
                if d == None:
                    raise Exception("No response")
                data += d
            l = int(data[:-1] or 0)
            data = ""
            while self.running and len(data) < l:
                d = self.sock.recv(l - len(data))
                if d == None:
                    raise Exception("No response")
                data += d
            return data
        except Exception as e:
            print "Couldn't recive data.", e
            self.close()
            return None
    
    def send(self, msg):
        self.add_msg(str(msg))
        
    def recv(self, wait = False):
        while wait and self.running and not len(self.ev):
            time.sleep(0.05)
        if len(self.ev):
            return self.pop_event(0)
        return None
    
    def decode(self, msg):
        try:
            return pickle.loads(msg)
        except Exception:
            try:
                return pickle.loads(bz2.decompress(msg))
            except Exception:
                pass
            raise
        
    def code(self, obj, protocol = 2, compress = 0): # 0-9 (9 to best compression)
        c = pickle.dumps(obj, protocol)
        if compress:
            return bz2.compress(c, compress)
        return c
    
    def close(self):
        self.running = 0
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        try:
            self.sock.close()
        except Exception:
            pass
        #self.join(1)
        #self.join(0)



         
    
class Server(threading.Thread): 
    def __init__(self, handshakestr = "MySocketServer"): 
        threading.Thread.__init__(self)
        self.handshakestr = handshakestr 
        self.host = socket.gethostbyname(socket.gethostname()) #"localhost"
        self.port = 666
        self.backlog = 5
        self.size = 1024
        self.select_timeout= 0.01
        self.server = None
        self.threads = []
        self.running = 0
 
    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host, self.port)) 
            self.server.listen(5)
            self.running = 1
            print "Server started!"
        except socket.error as e:
            if self.server: 
                self.server.close() 
            print "Could not open socket:", e 
            self.running = 0
            raise
 
    @async
    def try_add_client(self, sock):
        c = MyClient(sock, self.response, self.handshakestr)
        t = c.sock.gettimeout()
        c.sock.settimeout(2)
        if c.hand_shake():
            c.sock.settimeout(t)
            c.start()
            self.threads.append(c)
        else:
            c.close()
            print "Server: some connection attempt"
 
    def run(self): 
        self.open_socket()
        while self.running:
            inputready, outputready, exceptready = select.select([self.server],[],[], self.select_timeout)
            for s in inputready: 
                if s == self.server:
                    self.try_add_client(self.server.accept()[0])
            #print "Server event"
            x = 0
            while x < len(self.threads):
                if not self.threads[x].running:
                    self.threads.pop(x)
                    print "Thread", x, "died."
                    continue
                x += 1

        self.server.close()
        for c in self.threads:
            c.close()
        self.running = 0
        print "Server exited!"
    
    def stop(self):
        self.running = 0
        #self.join(1)
        #self.join(0)
        
    def response(self, p, e):
        p.send("You said:" + e)
 
 
    
