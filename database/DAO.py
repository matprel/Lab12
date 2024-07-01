from database.DB_connect import DBConnect
from model.arco import Arco
from model.rivenditore import Rivenditore


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def getNazioni():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query ="""  select distinct(gr.Country) 
                    from go_retailers gr 
                    order by gr.Country 
        """

        cursor.execute(query)
        for row in cursor:
            result.append(row["Country"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select distinct(year(g.`Date`)) as anno
                    from go_daily_sales g 
            """

        cursor.execute(query)
        for row in cursor:
            result.append(row["anno"])
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getRivenditori(c):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select *
                    from go_retailers gr 
                    where gr.Country = %s
                """

        cursor.execute(query, (c,))
        for row in cursor:
            result.append(Rivenditore(**row))
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getCollegamenti(a,idMap):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT g1.Retailer_code as r1, g2.Retailer_code as r2, COUNT(distinct g1.Product_number) AS peso
                    FROM go_daily_sales g1
                    JOIN go_daily_sales g2
                    ON g1.Product_number = g2.Product_number
                    AND g1.Retailer_code != g2.Retailer_code
                    AND YEAR(g1.`Date`) = YEAR(g2.`Date`)
                    WHERE YEAR(g1.`Date`) = %s
                    GROUP BY g1.Retailer_code, g2.Retailer_code"""

        cursor.execute(query, (a,))
        for row in cursor:
            if row["r1"] in idMap and row["r2"] in idMap:
                result.append(Arco(idMap[row["r1"]], idMap[row["r2"]], row["peso"]))
        cursor.close()
        conn.close()
        return result


