import simplekml
import math

DEGREE = 5
RADIUS = 0.0016875
BEAMWIDTH = 30

def calc_latlong(_shape = 'Outdoor', _direction = 0, _latlong = None):
    if _shape == 'Outdoor':
        tmp = []
        tmp.append(_latlong)
        for ang_step in range(0,BEAMWIDTH+DEGREE,DEGREE):
            tmp.append(calc_sec((ang_step+_direction-BEAMWIDTH/2)%360,RADIUS,_latlong))
        tmp.append(_latlong)
        return tmp
    elif _shape == 'Indoor':
        tmp = []
        for ang_step in range(0, 360, DEGREE):
            tmp.append(calc_sec(ang_step,RADIUS/5,_latlong))
        return tmp
    else:
        return False


def calc_sec(_direction = 0.0, _radius = RADIUS, _latlong = None):
    result = [0,0]
    try:
        result[0] = _latlong[0] + _radius * math.sin(_direction/180.0*math.pi)
        result[1] = _latlong[1] + _radius * math.cos(_direction/180.0*math.pi)
    except:
        print 'Calc Lat/long Error'
    finally:
        return result

def newsite(fol_site, siteid, sitename, latlong):
    pnt = fol_site.newpoint(name = siteid, coords = [latlong])
    pnt.snippet.content = sitename
    #pnt.snippet.maxlines = 1
    pnt.style = fol_site.style

def newcell(fol_cell, index,celltype, integrated, azimuth, latlong, pci, freq,info):
    if integrated == True:
        cell = fol_cell.newpolygon(name = index, outerboundaryis = calc_latlong(_shape =celltype ,_direction = azimuth, _latlong = latlong),description =info)
        cell.style = cellstyle((pci)%3,freq,True)
    else:
        cell = fol_cell.newpolygon(name = index, outerboundaryis = calc_latlong(_shape =celltype ,_direction = azimuth, _latlong = latlong),description =info)
        cell.style = cellstyle(None,freq,False)


def cellstyle(pci, freq, integrated):
    if not integrated:
        color1 = simplekml.Color.darkgray
        color2 = '6'+simplekml.Color.darkgray[1:]
    else:
        if pci == 0:
            color1 = simplekml.Color.darkseagreen
        elif pci == 1:
            color1 = simplekml.Color.purple
        elif pci == 2:
            color1 = simplekml.Color.yellow
        else:
            color1 = simplekml.Color.darkgray
            print 'PCI mod error'
        if freq == 1850:
            color2 = '6'+simplekml.Color.blue[1:]
        elif freq == 2970:
            color2 = '6'+simplekml.Color.red[1:]
        else:
            color2 = '6'+simplekml.Color.darkgray[1:]
            print 'Freq is not 1.8GHz or 2.6GHz'
    cell_style = simplekml.Style(linestyle = simplekml.LineStyle(width =2, color = color1),\
            polystyle = simplekml.PolyStyle(color = color2))
    return cell_style

def createnewmap():
    kml = simplekml.Kml()

    fol_site = kml.newfolder(name = 'Site')
    fol_cell = kml.newfolder(name = 'Cell')

    fol_site.style = simplekml.Style(iconstyle = simplekml.IconStyle(scale = 0.4))
    fol_site.style.iconstyle.icon.href = u'http://maps.google.com/mapfiles/kml/shapes/campground.png'

    #fol_cell.style = cellstyle(1,1850)

    newsite(fol_site, '130330', 'Clifford_Centre', (103.1,1.3))
    newcell(fol_cell, '130330_1',120, [103.1,1.3],211,1850,'information')
    newcell(fol_cell, '130330_2',240, [103.1,1.3],212,2970,'information')
    newcell(fol_cell, '130330_3',0, [103.1,1.3], 213, 1850, 'information')

def savemap(Kml = None, filepath = 'D:\\123.kml'):
    try:
        kml.save(filepath)
        kml.savekmz(filepath[:-3]+'kmz')
    except:
        print 'Save File failed...'
    finally:
        kml = None
