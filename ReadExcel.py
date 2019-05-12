from xlrd import open_workbook
from xlutils.copy import copy
import csv
from datetime import datetime

debug_file = r'.\log.txt'

class RFMasterList():
  """docstring for MasterList"""
	def __init__(self, rf_path):
		try:
			debug_log = open(debug_file, 'w')
			if rf_path[-3:] == "xls":
				self.rf_wb = open_workbook(rf_path, formatting_info = True, on_demand=True)
			else:
				self.rf_wb = open_workbook(rf_path, on_demand=True)
			self.rf_sheet = self.rf_wb.sheet_by_name('LTE_RF')

			#set first column as default index
			self.rf_start_row = 2
			rf_tittle_row = self.rf_start_row - 1
			#create link for tittles
			self.rf_tittle = list(self.rf_sheet.row_values(rf_tittle_row))
			#read
			self.cells = dict()
			for i in range(self.rf_start_row, self.rf_sheet.nrows):
				r_index = self.rf_sheet.cell(i, 0).value
				if r_index != None and r_index != "":
					self.cells[r_index] = dict()
					for a, b in zip(self.rf_tittle[1:], self.rf_sheet.row_values(i, 1, self.rf_sheet.ncols)):
						self.cells[r_index][a] = b
		except TypeError:
			debug_log.write('Cannot Find the Excel File Path...' + '\n')
		except IOError:
			debug_log.write('Open Excel File Failed...' + '\n')
		finally:
			debug_log.close()

class MasterList():
	"""docstring for M"""
	def __init__(self, ml_path):
		try:			
			debug_log = open(debug_file, 'w')
			ml_wb = open_workbook(ml_path, on_demand=True)
			ml_sheet = ml_wb.sheet_by_name('MASTERLIST')

			#set first column as default index
			ml_start_row = 4
			ml_tittle_row = 2
			#create link for tittles
			ml_tittle = ml_sheet.row_values(ml_tittle_row,0,20)
			ML_list = ["Cat", "LTE\nSiteID","Address","Longitude","Latitude","Cluster ID_After 24th Aug 2012"]
			ML_list2 = ["Drop","eNodeBID","SiteAddress","Longitude","Latitude","ClusterID"]
			ML_map = dict()
			#read
			self.enodebs = dict()
			for i in range(0,len(ML_list)):
				if ML_list[i] in ml_tittle:
					ML_map[ML_list2[i]] = ml_tittle.index(ML_list[i])
				else:
					debug_log.write("Cannot find %s in MasterList" % ML_list[i])
					print "Cannot find %s in MasterList" % ML_list[i]
					return False
			for i in range(ml_start_row, ml_sheet.nrows):
				enb_index = ml_sheet.cell(i,ML_map["eNodeBID"]).value
				if enb_index != None and enb_index !="" and ml_sheet.cell(i,ML_map["Drop"]).value != "Dropped":
					if str(enb_index)[:-2].isdigit():
						enb_index = str(enb_index)[:-2]
					self.enodebs[enb_index] = dict()
					self.enodebs[enb_index]["eNodeBID"] = enb_index
					for j in range(2,len(ML_list2)):
						self.enodebs[enb_index][ML_list2[j]] = ml_sheet.cell(i,ML_map[ML_list2[j]]).value
		except TypeError:
			debug_log.write('Cannot Find the MasterList File Path...' + '\n')
		except IOError:
			debug_log.write('Open MasterList File Failed...' + '\n')

		finally:
			debug_log.close()


class CMEMasterList():
	"""docstring for CMEMasterList"""
	def __init__(self, cme_path):
		#create link for tittles
		cme_tittle = ['eNodeBName','CellID','CellName','EARFCN', 'RadioBW', 'CellID',\
		'CME_Integrated','CellAdmin','OpStates','TAC','RootSequenceIndex','PCI','CellRadius',\
		'ReferenceSignalPwr']
		self.cells = dict()

		try:
			debug_log = open(debug_file, 'w')
			if cme_path[-3:] == 'csv':
				cme_file = open(cme_path, 'rb')
				cme_reader = csv.reader(cme_file, csv.excel)
				data = list(cme_reader)
				for i in range(2, len(data)):
					c_index = str(data[i][0])[:7]+str(data[i][1])
					if c_index[:4] == "1007":
						continue
					self.cells[c_index] = dict()
					for a, b in zip(cme_tittle, data[i]):
						self.cells[c_index][a] = b
			else:
				debug_log.write('The Format for CME file is not csv' & '\n')
		except TypeError:
			debug_log.write('Cannot Find the CME File Path...' + '\n')
		except IOError:
			debug_log.write('Open CME File Failed...' + '\n')
		finally:
			debug_log.close()

		
class ReadnCompare():
	"""docstring for ReadnCompare"""
	def __init__(self, rf, ml, cme, output_path):
		self.rf = rf
		self.old_rf = rf
		self.ml = ml
		self.cme = cme
		self.updated_cells = list()
		log_file = output_path[:output_path.rfind('\\')] + u'\\log.txt'
		log_writer = open(log_file, 'w')
		
		#missing cme cells in rf list
		self.add_cells =  [a for a in self.cme.cells.keys() if not self.rf.cells.has_key(a)]
		for cell in self.add_cells:
			self.rf.cells[cell] = dict()
			for info in [b for b in self.cme.cells[cell].keys() if self.rf.cells["133900_1"].has_key(b)]:			   
				self.rf.cells[cell][info] = str(self.cme.cells[cell][info])
				log_writer.write("Add Cell Parameter %s: %s for cell %s" %(info, str(self.cme.cells[cell][info]),cell) + '\n')
			self.UpdateCellInfo(cell, "All")			


			if self.ml.enodebs.has_key(cell[:6]):
				for info in [b for b in self.ml.enodebs[cell[:6]].keys() if self.rf.cells["133900_1"].has_key(b)]:
					self.rf.cells[cell][info] = str(self.ml.enodebs[cell[:6]][info])
					log_writer.write("Add eNodeB Parameter %s: %s for cell %s" %(info, str(self.ml.enodebs[cell[:6]][info]),cell) + '\n')


		#Existed in both cme and rf list
		existed_cells = [a for a in self.rf.cells.keys() if self.cme.cells.has_key(a)]
		for cell in existed_cells:
			for info in [b for b in self.cme.cells[cell].keys() if self.rf.cells[cell].has_key(b)]:
				if str(self.rf.cells[cell][info]) != str(self.cme.cells[cell][info]):
					self.updated_cells.append(cell)
					log_writer.write("Update Cell Parameter %s from %s to %s for cell %s" %(info, str(self.rf.cells[cell][info]), str(self.cme.cells[cell][info]),cell) + '\n')
					self.rf.cells[cell][info] = self.cme.cells[cell][info]

		#Compare rf list with enodeb in mastlist
		existed_enbs = [a for a in self.rf.cells.keys() if self.ml.enodebs.has_key(a[:6])]
		for cell in existed_enbs:
			for info in [b for b in self.ml.enodebs[cell[:6]].keys() if self.rf.cells[cell].has_key(b)]:
				if str(self.rf.cells[cell][info]) != str(self.ml.enodebs[cell[:6]][info]):
					self.updated_cells.append(cell)
					log_writer.write("Update eNodeB Parameter %s from %s to %s for cell %s" %(info, str(self.rf.cells[cell][info]), str(self.ml.enodebs[cell[:6]][info]),cell) + '\n')
					self.rf.cells[cell][info] = self.ml.enodebs[cell[:6]][info]
		log_writer.close()

	def UpdateCellInfo(self, cell, info):
		mmekeys = {311:'ROC',312:'ROC',411:'ROC',421:'ROC',\
			313:'MOC',314:'MOC',431:'MOC',441:'MOC',412:'ROC',None:'NULL'}
		if info == "All" or info == "CellName":
			if self.rf.cells[cell]["CellName"].find('2T2R') != -1:
				self.rf.cells[cell]["TxRxMode"] = '2T2R'
			else:
				self.rf.cells[cell]["TxRxMode"] = '1T1R'
			if self.rf.cells[cell]["CellName"].find('M') != -1:
				self.rf.cells[cell]["Type"] = 'Outdoor'
			else:
				self.rf.cells[cell]["Type"] = 'Indoor'
			self.rf.cells[cell]["eNodeBID"] = self.rf.cells[cell]["CellName"][1:7]
		if info == "All" or info == "TAC":
			self.rf.cells[cell]["TAL"] = int(self.rf.cells[cell]["TAC"][:3])
			self.rf.cells[cell]["MME"] = mmekeys[self.rf.cells[cell]["TAL"]]
	
	def Update2Excel(self, output_path):
		#create new file
		self.output_wb = copy(self.old_rf.rf_wb)
		self.output_sheet = self.output_wb.get_sheet(0)
		#Update the information into new RF Masterlist file
		for i in range(self.old_rf.rf_start_row, self.old_rf.rf_sheet.nrows):
			r_index = self.old_rf.rf_sheet.cell(i, 0).value
			if r_index in self.updated_cells:
				for info in self.rf.cells[r_index].keys():
					self.output_sheet.write(i,self.old_rf.rf_tittle.index(info),self.rf.cells[r_index][info])
		for i in range(0, len(self.add_cells)):
			cell = self.add_cells[i]
			for info in self.rf.cells[cell].keys():
				self.output_sheet.write(self.old_rf.rf_sheet.nrows + i,0,cell)
				self.output_sheet.write(self.old_rf.rf_sheet.nrows + i,self.old_rf.rf_tittle.index(info),self.rf.cells[cell][info])
		self.output_wb.save(output_path)

if __name__ == '__main__':
	#print datetime.now()
	rf = RFMasterList(rf_path = ".\\RF_MasterList20130604.xls")
	print rf.cells["133900_1"]
	ml = MasterList(ml_path = ".\\LTE MASTERLIST_23 May 2013.xlsx")
	print ml.enodebs["133900"]
	cme = CMEMasterList(cme_path = ".\\LTE_Status.csv")
	print cme.cells["133900_1"]
	result = ReadnCompare(rf,ml,cme,".\\reslut.xls")
	result.Update2Excel(".\\reslut.xls")
