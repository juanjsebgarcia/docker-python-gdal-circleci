"""
A series of simple calculations to test Python GDAL is installed correctly
"""
import sys

try:
    from osgeo import ogr, osr, gdal
except:
    raise NotImplementedError('cannot find GDAL/OGR modules')

version_num = int(gdal.VersionInfo('VERSION_NUM'))
if version_num < 1100000:
    raise NotImplementedError('Python bindings of GDAL 1.10 or later required')

print(f'GDAL VERSION: {version_num}')


def calculate_geometry_line():
    wkt = 'LINESTRING (1181866.263593049 615654.4222507705, 1205917.1207499576 623979.7189589312, 1227192.8790041457 643405.4112779726, 1224880.2965852122 665143.6860159477)'
    geom = ogr.CreateGeometryFromWkt(wkt)
    return True


def force_polygon_to_multipolygon():
    poly_wkt= 'POLYGON ((1179091.164690328761935 712782.883845978067257,1161053.021822647424415 667456.268434881232679,1214704.933941904921085 641092.828859039116651,1228580.428455505985767 682719.312399842427112,1218405.065812198445201 721108.180554138729349,1179091.164690328761935 712782.883845978067257))'
    geom_poly = ogr.CreateGeometryFromWkt(poly_wkt)
    if geom_poly.GetGeometryType() == ogr.wkbPolygon:
        geom_poly = ogr.ForceToMultiPolygon(geom_poly)
        wkt = geom_poly.ExportToWkt()
        return True


if not (
    calculate_geometry_line()
    and force_polygon_to_multipolygon()
):
    raise NotImplementedError('GDAL installation broken')
