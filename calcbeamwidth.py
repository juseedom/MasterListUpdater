from xlrd import open_workbook
import sys
import math
import simplekml
sys.path.append('C:\\Python27\\project\\')
rf_path = 'D:\\RNP&RNO\\ENGINEER\\Parameters\\RF Parameter\\20121231\\RF_MasterList20121231.xlsx'

def rad(d):
    return d * math.pi / 180.0

def GetDistance(lat1, lng1, lat2, lng2):
    EARTH_RADIUS = 6378.137
    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    a = radLat1 - radLat2
    b = rad(lng1) - rad(lng2)
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2),2) + \
    math.cos(radLat1)*math.cos(radLat2)*math.pow(math.sin(b/2),2)))
    s = s * EARTH_RADIUS
    return s


if (rf_path==None):
    print 'Need History RF master list path...'

#read col id in rf master list
index_rf_col=0
enb_rf_col=1
enbid_rf_col=1
clname_rf_col=2
clid_rf_col=3
type_rf_col=4
earfcn_rf_col=5
pci_rf_col=6
tr_rf_col=7
rs_rf_col=8
int_rf_col=9
op_rf_col=10
clu_rf_col=11
tac_rf_col=12
tal_rf_col=13
mme_rf_col=14
enbname_rf_col=15
addr_rf_col=16
long_rf_col=17
lat_rf_col=18
az_rf_col=19
cr_rf_col=23
sp_rf_col=24
#open rf masterlist
rf_wb=open_workbook(rf_path,on_demand=True)
rf_sheet=rf_wb.sheet_by_name('LTE_RF')
rf_start_row=2

enb = []
eNodeBs = {}
Cells = []

for i in range(rf_start_row,rf_sheet.nrows):
  #if rf_sheet.cell(i,index_rf_col).value != '':
		#try:
	#index = str(rf_sheet.cell(i,index_rf_col).value)
	enbid = str(rf_sheet.cell(i,enbid_rf_col).value)
	lat = float(rf_sheet.cell(i,lat_rf_col).value)
	longi = float(rf_sheet.cell(i,long_rf_col).value)
	#enbname = rf_sheet.cell(i,enbname_rf_col).value
	if enb.count(enbid) == 0:
		#add eNodeB here, need eNodeB ID, address, lat/long
		enb.append(enbid)
		eNodeBs[enbid] = (longi, lat)

		#except:
			#print 'Failed to create cell for '+ index

dist = {}
for enbid1, loc1 in eNodeBs.items():
	distance = 100000
	for enbid2, loc2 in eNodeBs.items():
		if enbid1 != enbid2:
			distance = min(distance, 1000.0*GetDistance(loc1[0],loc1[1],loc2[0],loc2[1]))
	dist[enbid1] = distance
	print enbid1, distance
