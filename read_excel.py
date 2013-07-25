from xlrd import open_workbook
import sys
import simplekml
sys.path.append('C:\\Python27\\project\\')
import kml_creater
rf_path = 'D:\\RNP&RNO\\ENGINEER\\Parameters\\RF Parameter\\20130703\\RF_MasterList20130703.xls'


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
pci_rf_col=7
tr_rf_col=8
rs_rf_col=9
int_rf_col=10
op_rf_col=11
clu_rf_col=12
tac_rf_col=13
tal_rf_col=14
mme_rf_col=15
enbname_rf_col=16
addr_rf_col=17
long_rf_col=18
lat_rf_col=19
az_rf_col=20
cr_rf_col= 24
sp_rf_col=25
#open rf masterlist
rf_wb=open_workbook(rf_path,on_demand=True)
rf_sheet=rf_wb.sheet_by_name('LTE_RF')
rf_start_row=2

enb = []
eNodeBs = []
Cells = []

for i in range(rf_start_row,rf_sheet.nrows):
  if rf_sheet.cell(i,index_rf_col).value != '':
		try:
			index = str(rf_sheet.cell(i,index_rf_col).value)
			enbid = int(rf_sheet.cell(i,enbid_rf_col).value)
			lat = float(rf_sheet.cell(i,lat_rf_col).value)
			longi = float(rf_sheet.cell(i,long_rf_col).value)
			enbname = rf_sheet.cell(i,enbname_rf_col).value
			#if str(rf_sheet.cell(i,27).value).index("."):
			#	bw = int(rf_sheet.cell(i,27).value)
			#else:
			#	bw = 0
			if enb.count(enbid) == 0:
				#add eNodeB here, need eNodeB ID, address, lat/long
				enb.append(enbid)
				eNodeBs.append([enbid,enbname,(longi,lat)])
			integrated = bool(rf_sheet.cell(i,int_rf_col).value)
			#if bw == 250000:
			#	integrated = True
			#else:
			#	integrated = False
			celltype = str(rf_sheet.cell(i,type_rf_col).value)
			pci = None
			earfcn = None
			azimuth = None
			if integrated:
				pci = int(rf_sheet.cell(i,pci_rf_col).value)
				earfcn = int(rf_sheet.cell(i,earfcn_rf_col).value)
			if celltype == 'Outdoor':
				azimuth = int(rf_sheet.cell(i,az_rf_col).value)
			
			info = ''
			for j in range(0,30):
				info = info + str(rf_sheet.cell(1,j).value) + ": " + str(rf_sheet.cell(i,j).value) + '\t\n'
			#add cell here, need index, azimuth, lat/long, pci, freq, description
			Cells.append([index,celltype,integrated,azimuth,[longi,lat],pci,earfcn,info])
			
		except:
			print 'Failed to create cell for '+ index



kml = simplekml.Kml()

fol_site = kml.newfolder(name = 'Site')
fol_cell = kml.newfolder(name = 'Cell')

fol_site.style = simplekml.Style(iconstyle = simplekml.IconStyle(scale = 0.4))
fol_site.style.iconstyle.icon.href = u'http://maps.google.com/mapfiles/kml/shapes/campground.png'

for enb in eNodeBs:
	kml_creater.newsite(fol_site,str(enb[0]),enb[1],enb[2])

for cell in Cells:
	kml_creater.newcell(fol_cell,cell[0],cell[1],cell[2],cell[3],cell[4],cell[5],cell[6],cell[7])

#kml_creater.newsite(fol_site, '130332', 'Clifford_Centre', (103.1, 1.3))
#kmlc.newcell(fol_cell, '130330_1',120, [103.1,1.3],211,1850,'information')

kml.save('D:\\123.kml')
kml.savekmz('D:\\123.kmz')
