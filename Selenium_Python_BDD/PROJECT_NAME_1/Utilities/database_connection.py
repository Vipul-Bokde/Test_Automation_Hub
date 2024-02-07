from asyncio.log import logger
from cmath import log
import pandas as pd
import psycopg2
import psycopg2.extras

class SqlConnection:
    def connection(query):
        hostname = 'qa-icyte-sparc-db.integrichain.net'
        database = 'claims'
        username = 'icyteapp2'
        pwd = 'vPF4mUbegtjXCcN4'
        port_no = '5432'
        conn = ''

        try:
            conn = psycopg2.connect(
            host = hostname,
            database = database,
            user = username,
            password = pwd,
            port = port_no
            )
            logger.info("connection established!")
            cur = conn.cursor()
            cur.execute(query)
            output = cur.fetchall()
            logger.info(output)
            return output
        
        except Exception as error:
            print(error)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
  