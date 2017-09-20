from collections import namedtuple
from pprint import pprint as pp
import sys
 
Pt = namedtuple('Pt', 'x, y')               
Edge = namedtuple('Edge', 'a, b')           
Poly = namedtuple('Poly', 'edges')    
 
eps = 0.00001
_max = sys.float_info.max
_min = sys.float_info.min
 
def linea_interseccion_x(p, edge):    
    a,b = edge

    if (p.y == a.y and p.x == a.x) or(
        p.y == b.y and p.x == b.x): 
        return True


    if a.y >= b.y:
        a,b = b,a
    if p.y == a.y or p.y == b.y:
        p = Pt(p.x, p.y + eps)
 
    intersect = False
 
    if (p.y >= b.y or p.y <= a.y) or (
        p.x >= max(a.x, b.x)):
        return False
 
    if p.x <= min(a.x, b.x):
        intersect = True
    else:
        if abs(a.x - b.x) >= _min:
            m_red = (b.y - a.y) / float(b.x - a.x)
        else:
            m_red = _max
        if abs(a.x - p.x) >= _min:
            m_blue = (p.y - a.y) / float(p.x - a.x)
        else:
            m_blue = _max
        intersect = m_blue >= m_red
    return intersect
 
def valid(x):
    return x%2 == 1
 
def point_inside(p, poly):
    ln = len(poly)
    return valid(sum(linea_interseccion_x(p, edge)
                    for edge in poly.edges ))
 
if __name__ == '__main__':
    file = open('/Users/PieroTerreros/PeqConsultores/test/example.txt', 'r')
    polys = []
    edge = []  
    for row in file:
        array_pt_jail = []
        array_pt_person = []
        jail_coordinates, person_coordinates = row.split('|')
        back_coordinate = None
        
        for coordinate in jail_coordinates.split(','):
            x,y = coordinate.strip().split(' ')
            array_pt_jail.append(Pt(x=int(x), y=int(y)))

        for coordinate in person_coordinates.split(','):
            x,y = coordinate.strip().split(' ')
            array_pt_person.append(Pt(x=int(x), y=int(y)))    
        
        for x in xrange(1,len(array_pt_jail)):
            edge.append(Edge(a=array_pt_jail[x-1], b=array_pt_jail[x]))

        polys = [Poly(edges=tuple(edge)),]

        points = tuple(array_pt_person)
        
        for poly in polys:
            for p in points[:1]:
                result = point_inside(p, poly)
            if result:
                print('Prisoner')
            else:
                print('Citizen')

