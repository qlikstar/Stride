import geopy
import geopy.distance

pt1 = geopy.Point(37.76,-122.39)
pt2 = geopy.Point(37.78,-122.43)

print pt1
print pt2
dist = geopy.distance.distance(pt1, pt2).miles

print dist