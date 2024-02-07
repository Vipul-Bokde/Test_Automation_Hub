import pymysql
import configparser

def connection_to_ini(db_name):
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    connection = {"host": config[db_name]['db_host'],
                  "port": int(config[db_name]['db_port']),
                  "user": config[db_name]['db_user'],
                  "password": config[db_name]['db_passwd']}
    return connection


def _connection_env(db_name):
    environment = connection_to_ini(db_name)
    connection = pymysql.connect(host=environment["host"],
                                 port=environment["port"],
                                 user=environment["user"],
                                 password=environment["password"])
    return connection


def database_select_to_test(db_name, query_select):
    connection = _connection_env(db_name)
    with connection.cursor() as cursor:
        cursor.execute(query_select)
        result_select = cursor.fetchall()
    connection.close()
    list_new = []
    for data in result_select:
        new_data = list(data)
        for position in range(len(data)):
            if data[position] is None:
                new_data[position] = ''
        list_new.append(new_data)
    return list_new


def database_update_to_test(env, query_update):
    connection = _connection_env(env)
    with connection.cursor() as cursor:
        cursor.execute(query_update)
        connection.commit()
    connection.close()


def concatenate_information_for_where_in_db(data_filter):
    data_for_database = ""
    for data in data_filter:
        data_for_database += str("'" + data.lower() + "', ")
    delete_space = len(data_for_database) - 2
    data_for_where = data_for_database[0:delete_space]
    return data_for_where
