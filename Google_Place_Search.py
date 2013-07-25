import Queue
import threading
import time
from googleplaces import GooglePlaces, types, lang


import sys
sys.path.append('C:\\Python27\\project\\')
from re_excel import RFMasterList

#unicodecs.unicodeData.encode('ascii', 'ignore')

queue = Queue.Queue()
cells = list()
threadlock = threading.Lock()

class ThreadUrl(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            Site_Address = self.queue.get()
            #print Site_Address
            API_KEY = 'xxx'
            google_places = GooglePlaces(API_KEY)

            quey_result = google_places.nearby_search(location='Singapore',keyword=Site_Address,radius = 30000)
            for place in quey_result.places:
                place.get_details()
                out_put = Site_Address+';'+place.name+';'+str(place.geo_location['lat'])+';'+str(place.geo_location['lng'])+';'+place.formatted_address
                threadlock.acquire()
                print out_put
                threadlock.release()
            self.queue.task_done()
            
def main(cells):
    for i in range(10):
        t = ThreadUrl(queue)
        t.setDaemon(True)
        t.start()

    for cell in cells:
        queue.put(cell)
        
    queue.join()
    

if __name__ == '__main__':
    rf = RFMasterList(rf_path = 'D:\\RF_MasterList20130228.xlsx')
    for cell in rf.cells.keys():
        address = rf.cells[cell].quey_info('Site Address')
        if cells.count(address) == 0:
            cells.append(address)
    start_time =  time.time()
    main(cells[:10])
    print time.time()-start_time
