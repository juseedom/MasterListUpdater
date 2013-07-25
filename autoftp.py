import ftplib
import time, os
from zipfile import ZipFile

mytime = time.localtime(time.time())
today_date = "%4d-%02d-%02d" %(mytime.tm_year,mytime.tm_mon,mytime.tm_mday)

def getfilefromftp(ftpaddr, ftppath, lcdpath, ftpusr = "ftpuser",ftppwd = "ftpuser",  mode = 'datepath'):
  try:
		filepath = ftppath
		ftp = ftplib.FTP(host = ftpaddr, timeout = 5)
		ftp.login(user="ftpuser",passwd="ftpuser")
		ftp.cwd(filepath)
		filelists = ftp.nlst()
		for file in filelists:
			if file.find(today_date) != -1:
				filepath = filepath + file
				ftp.cwd(filepath)
				filelists = ftp.nlst()
				for file in filelists:
					ftp.retrbinary("RETR " + file ,open(lcdpath+file, 'wb').write)
				return True
		print "Cannot find the Date path."
		return False
	except ftplib.error_perm, e:
		print e.messsage
		return False
	except ftplib.all_errors, e:
		print e.messsage
		return False


def zipfile(lcdpath, tcdpath):
	if not os.path.isfile(lcdpath+'ConfigurationReport_LTE_Status.zip'):
		print 'Cannot find ConfigurationReport_LTE_Status.zip file'
	else:
		if not os.path.isdir(tcdpath):
			os.system('mkdir "'+ tcdpath +'"')
		with ZipFile(lcdpath+'ConfigurationReport_LTE_Status.zip', 'r') as tmpzip:
			tmpzip.extractall(path = tcdpath)
		

if __name__ == '__main__':
	getfilefromftp(ftpaddr = '172.18.95.2', ftppath = '/export/home/sysm/ftproot/TimerTask/12878/output/', \
		lcdpath = 'D:\\RNP&RNO\\ENGINEER\\Parameters\\CME Data\\')
	zipfile(lcdpath = 'D:\\RNP&RNO\\ENGINEER\\Parameters\\CME Data\\', tcdpath = 'D:\\RNP&RNO\\ENGINEER\\Parameters\\CME Data\\12')
	
