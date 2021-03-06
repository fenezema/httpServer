import socket
import sys
import threading
import os
import subprocess as sub

#inisialisasi
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#proses binding
address="10.151.254.67"
server_address = (address, 10001)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

#listening
sock.listen(1)


def response_files():
	filepath="resources"
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

def response_redirect():
	hasil = "HTTP/1.1 301 Moved Permanently\r\n" \
		"Location: {}\r\n" \
		"\r\n"  . format('http://www.its.ac.id')
	return hasil




#fungsi melayani client
def layani_client(koneksi_client,alamat_client):
	try:
		print >>sys.stderr, 'ada koneksi dari ', alamat_client
		request_message = ''
		while True:
			data = koneksi_client.recv(1024)
			print "sebelum decode"
			print data
			request_message = request_message+data
			if request_message[-4:]=="\r\n\r\n" or request_message[-4:]=="--\r\n":
				break
		baris = request_message.split("\r\n")
		baris_request = baris[0]
		for i in range(0,len(baris)):
			print str(i)+' '+baris[i]
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
		elif method=="POST":
			if url=="/uploadfile":
				length=len(baris)
				for i in range(0,len(baris)):
					if 'filename=' in baris[i]:
						index_nama=i
					else:
						continue
				name_file=baris[index_nama]
				name_file=name_file.split(';')
				for i in range(0,len(name_file)):
					if 'filename=' in name_file[i]:
						indexnya=i
					else:
						continue
				name_file=name_file[indexnya]
				name_file=name_file.split('=')
				name_file=name_file[1]
				name_file=name_file.replace('"','')
				with open('resources/'+name_file,'w+') as the_file:
					the_file.write(baris[length-3])
				respon = response_upfile()

		koneksi_client.send(respon)
		print "End"
	finally:
        # Clean up the connection
		koneksi_client.close()


while True:
    # Wait for a connection
	print "waiting for a connection"
	koneksi_client, alamat_client = sock.accept()
	s = threading.Thread(target=layani_client, args=(koneksi_client,alamat_client))
	s.start()                                                                                                                                                     
