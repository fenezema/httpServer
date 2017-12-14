import asyncore
import socket
import sys
import threading
import os

def response_files():
	filepath="/home/fenezema/Documents/IsengProject/Progjar/httpServer/server/resources"
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: 255\r\n" \
		"\r\n" \
		"{}".format(os.listdir(filepath))
	return hasil

def response_makedir(namafile):
	dir_path,dir_nama=namafile.split("&")
	if dir_path[-1:]!="/":
		dir_path=dir_path+'/'
	elif dir_path[-1:]=="/":
		dir_path=dir_path
	dir_nama='dir_'+dir_nama
	os.system('mkdir '+dir_path+dir_nama)
	page = open('pages/makedir.html','r').read()
	panjang = len(page)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/html\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, page)
	return hasil
	
def response_downfile(namafile):
	filepath='resources/'+namafile
	files = open(filepath,'r').read()
	panjang = len(files)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: multipart/form-data\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, files)
	return hasil
	
def response_delfile(namafile):
	dir_path,namafile=namafile.split("&")
	if dir_path[0]=='/':
		dir_path=dir_path.replace(dir_path[0],'',1)
	if dir_path[-1:]!='/':
		filepath=dir_path+'/'
	elif dir_path[-1:]=='/':
		filepath=dir_path
	os.system('rm -rf '+filepath+namafile)
	page = open('pages/deletefile.html','r').read()
	panjang = len(page)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/html\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, page)
	return hasil
	
def response_movedir(namafile):
	cmd,namafile=namafile.split(":")
	print cmd
	print namafile
	dir_nama,dir_tujuan=namafile.split("&")
	dir_nama='resources/'+dir_nama
	os.system('mv '+dir_nama+' '+dir_tujuan)
	page = open('pages/movdir.html','r').read()
	panjang = len(page)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/html\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, page)
	return hasil
	
def response_php():
	sub.call(['php','pages/phpinfo.php'])
	page = open('pages/uploadfile.html','r').read()
	panjang = len(page)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/html\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, page)
	return hasil
	
def response_upfile():
	sub.Popen(['php','pages/upload.php'],shell=True,stdout=sub.PIPE)
	page = open('pages/uploadfile.html','r').read()
	panjang = len(page)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/html\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, page)
	return hasil

def response_gambar():
	filegambar = open('gambar.png','r').read()
	panjang = len(filegambar)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: image/png\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, filegambar)
	return hasil

def response_page(url):
	print url
	try:
		cmd,namafile=url.split(":")
		if cmd=="/downloadfile":
			hasil=response_downfile(namafile)
			return hasil
		elif cmd=="/deletefile":
			hasil=response_delfile(namafile)
			return hasil
		elif cmd=="/movedir":
			hasil=response_movedir(namafile)
			return hasil
		elif cmd=="/makedir":
			hasil=response_makedir(namafile)
			return hasil
		elif cmd=="/deldir":
			hasil=response_delfile(namafile)
			return hasil
	except:
		if url=="/":
			page = open('pages/landingpage.html','r').read()
		else:
			filename=url+'.html'
			page = open('pages'+filename,'r').read()
		panjang = len(page)
		hasil = "HTTP/1.1 200 OK\r\n" \
			"Content-Type: text/html\r\n" \
			"Content-Length: {}\r\n" \
			"\r\n" \
			"{}" . format(panjang, page)
		return hasil


class ClientHandler(asyncore.dispatcher):
	def __init__(self, sock):
		asyncore.dispatcher.__init__(self, sock=sock)
		self.request_message = ""
		self.reply_message=""
		return
	def handle_write(self):
		pass
	def handle_close(self):
		pass
     #fungsi melayani client
	def handle_read(self):
		data = self.recv(64)
		data = bytes.decode(data)
		self.request_message = self.request_message+data
		if (self.request_message[-4:]=="\r\n\r\n"):
			baris = self.request_message.split("\r\n")
			baris_request = baris[0]
			print baris_request
		
		method,url,c = baris_request.split(" ")
		if method=="GET":       
			if url=='/favicon.ico':
				respon = response_icon()
			elif url=='/filesavailable':
				respon = response_files()       
			elif url=='/doc':
				respon = response_dokumen()
			elif url=='/filesavailable':
				respon=response_files()
			elif url=='/phpinfo':
				respon=response_php()
			elif '/movedir' in url:
				respon=response_movedir(url)
			else:
				respon = response_page(url)
			self.request_message = ""
			self.send(respon)
			self.close()
		elif method=="POST":
			if url=="/upload.php":
				respon = response_upfile()
			self.request_message = ""
			self.send(respon)
			self.close()



class WebServer(asyncore.dispatcher):
    def __init__(self, host, port):
	asyncore.dispatcher.__init__(self)
	self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
	self.set_reuse_addr()
	self.bind((host, port))
	self.listen(5)
    def handle_connect(self):
	pass
    def handle_expt(self):
	self.close()
    def handle_read(self):
	pass
    def handle_write(self):
	pass
    def handle_close(self):
	pass
    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            koneksi_client, alamat_client = pair
            print 'Incoming connection from %s' % repr(alamat_client)
            ClientHandler(koneksi_client)        
	    #koneksi_client.send('haha')
	    #koneksi_client.close()
	    #s = threading.Thread(target=layani_client, args=(koneksi_client,alamat_client))
	    #s.start()

server = WebServer('localhost', 8080)
asyncore.loop()
