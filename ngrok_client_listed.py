#!/usr/bin/env python3
import requests
import signal,psutil
import stat,socket
import os,sys,platform,time
import pymysql
from pyvirtualdisplay import Display

launched =0
connect =0

db=None
mydb=None

display = Display(visible=0, size=(800, 600))
display.start()

def connect_mysql():
	global db,mydb
	db = pymysql.connect(host="db4free.net",user="semara",password="semara123",db="tunnelstdc")
	mydb = db.cursor()
	connect=1

def req_ngrok():
	try:
		req = requests.get('http://localhost:4040/api/tunnels'
			,headers={"Content-Type": "text/json"}
			)
		print('[DEBUG] Requests Status [%s]'% (req.status_code))
		data = req.json()['tunnels']
		mydb.execute("TRUNCATE TABLE ip_tunnels") #clear all records
		print('[Cleaned] All Records In Remote Database Cleared')
		for i in range(len(data)):
			#temp =''
			are = str(data[i]['public_url'])
			are = are.split('://')
			#print(are)
			if ('tcp' == str(data[i]['proto'])):
				temp = are
				link_temp = str(temp[1])
				#print('Link temp tcp: ',link_temp)
				del temp
				temp = link_temp.split(':')
				#print(temp)
				#print(temp)
				print('[Tunnels Info]\n \
					Name: %s\n \
					Address: %s\n \
					Port: %s\n \
					Protokol: %s\n-------------------------------------------' \
					% (data[i]['name'], temp[0],temp[1],data[i]['proto'])
				)
				sql = "REPLACE INTO ip_tunnels(Nama,IP,Port,Protokol) VALUES (%s,%s,%s,%s)"
				mydb.execute(sql,(data[i]['name'], temp[0],temp[1],data[i]['proto']))
				db.commit()
				print("[DEBUG] Tunnels Added To The Database")
			elif (str(data[i]['proto']) == 'http' or str(data[i]['proto']) == 'https'):
				temp = are
				#print("Detected HTTP")
				del temp[0]
				temp.append("80")
				#print(temp)
				print('[Tunnels Info]\n \
					Name: %s\n \
					Address: %s\n \
					Port: %s\n \
					Protokol: %s\n---------------------' \
					% (data[i]['name'], temp[0],temp[1],data[i]['proto'])
				)
				sql = "REPLACE INTO ip_tunnels(Nama,IP,Port,Protokol) VALUES (%s,%s,%s,%s)"
				mydb.execute(sql,(data[i]['name'], temp[0],temp[1],data[i]['proto']))
				print("[DEBUG] Tunnels Added To The Database")
				#mydb.close()
				db.commit()
				#db.close()
		print("[DEBUG]-----Finished Taking The Address-----")
		print('[DEBUG] Calling The Second Ngrok Request')
		req_ngrok2()
	except (KeyboardInterrupt,Exception) as e:
		print('[DEBUG] App Terminated')
		print(e)
		mydb.close()
		db.commit()
		db.close()
		display.stop()

def req_ngrok2():
	try:
		req = requests.get('http://localhost:4041/api/tunnels'
			,headers={"Content-Type": "text/json"}
			)
		print('[DEBUG] Requests Status [%s]'% (req.status_code))
		data = req.json()['tunnels']
		#mydb.execute("TRUNCATE TABLE ip_tunnels") #clear all records --> i dont need to clear the table -,- 
		#print('[Cleaned] All Records In Remote Database Cleared')
		for i in range(len(data)):
			#temp =''
			are = str(data[i]['public_url'])
			are = are.split('://')
			#print(are)
			if ('tcp' == str(data[i]['proto'])):
				temp = are
				link_temp = str(temp[1])
				#print('Link temp tcp: ',link_temp)
				del temp
				temp = link_temp.split(':')
				#print(temp)
				#print(temp)
				print('[Tunnels Info]\n \
					Name: %s\n \
					Address: %s\n \
					Port: %s\n \
					Protokol: %s\n-------------------------------------------' \
					% (data[i]['name'], temp[0],temp[1],data[i]['proto'])
				)
				sql = "REPLACE INTO ip_tunnels(Nama,IP,Port,Protokol) VALUES (%s,%s,%s,%s)"
				mydb.execute(sql,(data[i]['name'], temp[0],temp[1],data[i]['proto']))
				db.commit()
				print("[DEBUG] Tunnels Added To The Database")
			elif (str(data[i]['proto']) == 'http' or str(data[i]['proto']) == 'https'):
				temp = are
				#print("Detected HTTP")
				del temp[0]
				temp.append("80")
				#print(temp)
				print('[Tunnels Info]\n \
					Name: %s\n \
					Address: %s\n \
					Port: %s\n \
					Protokol: %s\n---------------------' \
					% (data[i]['name'], temp[0],temp[1],data[i]['proto'])
				)
				sql = "REPLACE INTO ip_tunnels(Nama,IP,Port,Protokol) VALUES (%s,%s,%s,%s)"
				mydb.execute(sql,(data[i]['name'], temp[0],temp[1],data[i]['proto']))
				print("[DEBUG] Tunnels Added To The Database")
				#mydb.close()
				db.commit()
				#db.close()
		print("[DEBUG]-----Finished Taking The Address-----")
		print('[DEBUG] Address Saved To Remote Database')
	except (KeyboardInterrupt,Exception) as e:
		print('[DEBUG] App Terminated')
		print(e)
		mydb.close()
		db.commit()
		db.close()
		display.stop()

def isNgrokRun():
	if str(platform.system()).lower() =='windows':
		for proc in psutil.process_iter():
	# check whether the process to kill name matches
			if proc.name() == 'ngrok.exe':
				return 1
				break
			else:
				cek = 0
		return int(cek)
	else:
		for proc in psutil.process_iter():
	# check whether the process to kill name matches
			if proc.name() == 'ngrok':
				return 1
				break
			else:
				cek = 0
		return int(cek)

def killit():
	if str(platform.system()).lower() =='windows':
		for proc in psutil.process_iter():
	# check whether the process to kill name matches
			if proc.name() == 'ngrok.exe':
				proc.kill()
	else:
		for proc in psutil.process_iter():
	# check whether the process to kill name matches
			if proc.name() == 'ngrok':
				proc.kill()

def panggil():
	try:
		os_system = str(platform.system())
		director = os.path.dirname(os.path.abspath( __file__ ))
		print('[INFO] Retrieved OS Info: ',os_system)
		if os_system.lower() == 'windows':
			print("[SYSTEM] Windows Detected")
			command = "ngrok start --all --config=ngrok.yml"
			#ngrok = open("ngrok_cmd_fixed.bat","w")
			#ngrok.write(str(command))
			#ngrok.close()
			os.spawnv(os.P_NOWAIT, "ngrok.exe",["ngrok.exe","start"," --config=ngrok.yml"," --all"]) #i have two account :p
			os.spawnv(os.P_NOWAIT, "ngrok.exe",["ngrok.exe","start"," --config=ngrok2.yml"," --all"])
			print("[INFO] App Launched")
		else:
			#command = "ngrok start --all --config=ngrok.yml"
			#ngrok = open("ngrok_cmd_fixed","w")
			#ngrok.write(str(command))
			#ngrok.close()
			#st = os.stat('ngrok_cmd')
			#print(st)
			#os.chmod('ngrok_cmd_fixed', st.st_mode | stat.S_IEXEC)
			os.spawnv(os.P_NOWAIT, "ngrok",["ngrok","start","--all","--config","ngroklin.yml"]) #i have two account :p
			os.spawnv(os.P_NOWAIT, "ngrok",["ngrok","start","--all","--config","ngrok2lin.yml"])
			print("[INFO] App Launched")
	except (KeyboardInterrupt,Exception) as k:
		print("[INFO] App Stopped,Closing Mysql Connection")
		mydb.close()
		db.commit()
		db.close()
		display.stop()
		sys.exit()

def inet_check():
	try:
		try:
			socket.setdefaulttimeout(5)
			socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
			return 1 #connected
		except (KeyboardInterrupt,Exception) as e:
			return 0 #disconnected
	except KeyboardInterrupt as f:
		print("[DEBUG] Terminate The App, Closing Mysql Connection")
		killit()
		mydb.close()
		db.commit()
		db.close()
		display.stop()
		sys.exit()

def inet_verif():
	while True:
		if inet_check():
			break
while True:
	if connect == 0:
		connect_mysql()
		connect = 1
	try:
		if inet_check() == 1 and launched == 0 and isNgrokRun() == 0 :
			print("[DEBUG] Launching Ngrok With Current Setting")
			panggil()
			launched=1
			print("[DEBUG] Ngrok Is Running On The Background Please Don't Close The App")
			print("[DEBUG] Getting Tunnels Information")
			time.sleep(6)
			req_ngrok()
		elif inet_check() == 0:
			print("[ERROR] No Internet Connection, Terminate The Ngrok, Auto Start Ngrok When Connection Is Available")
			#terminate it
			killit()
			time.sleep(1)
			launched=0
			inet_verif()	
	except (KeyboardInterrupt,Exception) as e:
		print("[DEBUG] App Terminated, Closing Mysql Connection")
		killit()
		mydb.close()
		db.commit()
		db.close()
		display.stop()
		sys.exit()