# sez_to_ecef.py
#
# Usage: python3 sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km
#  Converts SEZ (South, East, Zenith) to ECEF (Earth-Centered Earth-Fixed) coordinates
#  using the observer's location (lat, lon, and height above ellipsoid).
#  Based on standard transformations from SEZ to ECEF.
# Parameters:
#  o_lat_deg: Observer's Latitude in degrees
#  o_lon_deg: Observer's Longitude in degrees
#  o_hae_km: Observer's Height Above Ellipsoid in km
#  s_km: South component of SEZ vector in km
#  e_km: East component of SEZ vector in km
#  z_km: Zenith component of SEZ vector in km
# Output:
#  Prints the ECEF x, y, and z coordinates in km
#
# Written by Nick Davis
# Other contributors: None
#
# This work is licensed under CC BY-SA 4.0

# import Python modules
import math  # math module
import sys   # argv

# "constants"
R_E_KM = 6378.137  # Equatorial radius in kilometers
E_E    = 0.081819221456  # Earth's eccentricity

# helper functions
def calc_denom(ecc, lat_rad):
    """Calculate the denominator in the ECEF conversion equation."""
    return math.sqrt(1.0-(ecc**2)*(math.sin(lat_rad)**2))

def llh_to_ecef(o_lat_rad, o_lon_rad, o_hae_km):
    """Convert observer's latitude, longitude, and height to ECEF coordinates."""
    denom = calc_denom(E_E, o_lat_rad)
    N = R_E_KM/denom  # Radius of curvature in the prime vertical
    x = (N+o_hae_km)*math.cos(o_lat_rad)*math.cos(o_lon_rad)
    y = (N+o_hae_km)*math.cos(o_lat_rad)*math.sin(o_lon_rad)
    z = (N*(1-E_E**2)+o_hae_km)*math.sin(o_lat_rad)
    return x, y, z

def sez_to_ecef(o_lat_rad, o_lon_rad, s_km, e_km, z_km):
    """Converts SEZ to ECEF coordinates given observer latitude, longitude, and SEZ vector."""
    # Transformation matrix from SEZ to ECEF
    cos_lat = math.cos(o_lat_rad)
    sin_lat = math.sin(o_lat_rad)
    cos_lon = math.cos(o_lon_rad)
    sin_lon = math.sin(o_lon_rad)

    # SEZ to ECEF conversion formulas
    ecef_x = (s_km*sin_lat*cos_lon)+(e_km*(-sin_lon))+(z_km*cos_lat*cos_lon)
    ecef_y = (s_km*sin_lat*sin_lon)+(e_km*cos_lon)+(z_km*cos_lat*sin_lon)
    ecef_z = (s_km*-cos_lat)+(z_km*sin_lat)

    return ecef_x, ecef_y, ecef_z

# initialize script arguments
o_lat_deg = float('nan')  # Observer's Latitude in degrees
o_lon_deg = float('nan')  # Observer's Longitude in degrees
o_hae_km  = float('nan')  # Observer's Height Above Ellipsoid in km
s_km      = float('nan')  # South component of SEZ vector in km
e_km      = float('nan')  # East component of SEZ vector in km
z_km      = float('nan')  # Zenith component of SEZ vector in km

# parse script arguments
if len(sys.argv) == 7:
    o_lat_deg = float(sys.argv[1])
    o_lon_deg = float(sys.argv[2])
    o_hae_km  = float(sys.argv[3])
    s_km      = float(sys.argv[4])
    e_km      = float(sys.argv[5])
    z_km      = float(sys.argv[6])
else:
    print('Usage: python3 sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km')
    exit()

# convert observer's latitude and longitude to radians
o_lat_rad = math.radians(o_lat_deg)
o_lon_rad = math.radians(o_lon_deg)

# convert observer's location (LLH) to ECEF coordinates
obs_ecef_x_km, obs_ecef_y_km, obs_ecef_z_km = llh_to_ecef(o_lat_rad, o_lon_rad, o_hae_km)

# convert SEZ coordinates to ECEF coordinates (relative to observer)
sez_x_km, sez_y_km, sez_z_km = sez_to_ecef(o_lat_rad, o_lon_rad, s_km, e_km, z_km)

# add observer's ECEF position to the SEZ-transformed ECEF coordinates
ecef_x_km = obs_ecef_x_km+sez_x_km
ecef_y_km = obs_ecef_y_km+sez_y_km
ecef_z_km = obs_ecef_z_km+sez_z_km

# print ECEF x, y, and z coordinates in km
print(ecef_x_km)
print(ecef_y_km)
print(ecef_z_km)