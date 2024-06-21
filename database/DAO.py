from database.DB_connect import DBConnect
from model.location import Location


class DAO:
    @staticmethod
    def get_providers():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT  provider
FROM nyc_wifi_hotspot_locations nwhl 
ORDER BY Provider ASC"""
            cursor.execute(query)
            for row in cursor:
                result.append(row['provider'])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_locations(provider):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT  Location , AVG(Latitude) as Latitude, AVG(Longitude) as Longitude
FROM nyc_wifi_hotspot_locations nwhl 
WHERE Provider = %s
GROUP BY Location 
"""
            cursor.execute(query, (provider,))
            for row in cursor:
                result.append(Location(**row))
            cursor.close()
            cnx.close()
        return result
