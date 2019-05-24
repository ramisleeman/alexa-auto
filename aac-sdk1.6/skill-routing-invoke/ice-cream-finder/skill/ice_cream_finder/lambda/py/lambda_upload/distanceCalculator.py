import math

def distanceInKmBetweenCoordinates(lat1, lon1, lat2, lon2):
  earthRadiusKm = 6371

  dLat = (lat2-lat1) * math.pi/180.
  dLon = (lon2-lon1) * math.pi/180.

  lat1 = lat1 * math.pi/180.
  lat2 = lat2 * math.pi/180.

  a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2); 
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)); 
  return earthRadiusKm * c