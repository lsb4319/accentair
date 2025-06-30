import json
import logging
from datetime import datetime
import requests
from enum import Enum
import singlestoredb

class singlestore:
    def __init__(self, s2_config):
        self.conn = singlestoredb.connect(host = s2_config.host,
                                     port = s2_config.port,
                                     user = s2_config.username,
                                     password = s2_config.password,
                                     database = s2_config.database)
        
    def run_sql(self, statement):
        try:    
            with self.conn.cursor() as cursor:
                cursor.execute(statement)
                self.conn.commit()
        except:
            pass
       
    def run_select(self, query):
        return_values = []
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                return_values.append(row)
        return return_values
       

    def delete_records(self, session, table_name):
        statement_text = "delete from {0};".format(table_name)
        self.run_sql(session, statement_text)
    
    def get_number_of_records(self, table_name, session):
            query_text = "select count(*) from {0};".format(table_name)
            result = self.run_select(session, query_text)
            value = result[0]["count(*)"]
            return value
        
    @staticmethod
    def get_number_of_course_records(user_id, course_code, session, s2):
        query_text = "select count(*) from enrollment where user_id = '{0}' and code = '{1}';".format(user_id, 
                                                                                                        course_code)
        result = []
        result = s2.run_select(session, query_text)
        return result


#    def record_exists(self, id_in, table_name):
#        id_in = "{0}".format(id_in)
#        query_text = "select id from {0} where id = {1}".format(table_name, id_in)
#        ids = self.run_select(query_text)
#        if len(ids) == 0:
#                return False
#        else:
#                return True

    def get_number_of_records_for_user(self, username, session, course_code):
        query_text = "select count(*) from enrollment_temp where userName = '{0}' and courseCode = '{1}';".format(username, course_code)
        result = self.run_select(session, query_text)
        return result

    def copy_table(self, src_table, dest_table):
        statement_text = "insert into {0} * {1};"
        self.run_sql(statement_text)

class s2_config:
    def __init__(self, os_in) -> None:
        if os_in == os.windows:
            config_file = open("python\config.json", "r")
        elif os_in == os.linux:
            config_file = open("./config.json", "r")
        elif os_in == os.mac:
            config_file = open("python/config.json", "r")
        config_text = config_file.read()
        config_file.close()
        config_json = json.loads(config_text)
        self.database = config_json["database"]
        self.username = config_json["username"]
        self.password = config_json["password"]
        self.host = config_json["server"]
        self.port = config_json["port"]
        
class os(Enum):
      mac = 1
      windows = 2
      linux = 3
