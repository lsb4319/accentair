from singlestore import s2_config, singlestore
from populate_hr import accendair_db
import singlestoredb
from datetime import datetime
import concurrent.futures
import os

class user_management:
    def __init__(self):
        pass
    
    def add_users(self):
        aca = accendair_db()
        s2cnf = s2_config(aca.get_os())
        query_text = "select username from hr.employee;"
        s2 = singlestore(s2cnf)
        results = s2.run_select(query_text)
        for result in results:
            username = (result[0])
            username = self.clean_username(username)
            sql_text = "create user {0} identified by 'goSinglestore1';".format(username)
            s2.run_sql(sql_text)

            
    def delete_users(self):
        aca = accendair_db()
        s2cnf = s2_config(aca.get_os())
        query_text = "select USER FROM information_schema.USERS WHERE TYPE = 'NATIVE'"
        s2 = singlestore(s2cnf)
        results = s2.run_select(query_text)
        for result in results:
            username = (result[0])
            username = self.clean_username(username)
            if username != 'admin' and username != 'root' and username != 'all':
                sql_text = "DROP USER {0};".format(username)
                s2.run_sql(sql_text)
                
    def add_employees_to_all(self):
        results = self.run_statement("select username FROM hr.employee;")
        for result in results:
            username = (result[0])
            username = self.clean_username(username)
            sql_text = "GRANT GROUP 'all' to {0};".format(username)
            self.run_statement(sql_text)
            
    def create_manager_roles(self):
        query_text = "select e.username, e.employee_id as manager_id, p.level\
                    from employee e\
                    join employee_position ep\
                    join position p\
                    join employee_manager em\
                    where e.employee_id = ep.employee_id\
                    and ep.position_id = p.position_id\
                    and e.employee_id = em.manager_id\
                    and p.level in ('m1', 'm2', 'm3', 'm4', 'm5')\
                    group by e.username\
                    order by em.manager_id;"
        results = self.run_statement(query_text, "select")
        for result in results:
            username = result[0]
            username = self.clean_username(username)
            sql_text = "create role {0}_role;".format(username)
            self.run_statement(sql_text, "other")
        
    def add_managers_to_roles(self):
        query_text = "select manager_id from employee_manager;"
        u_ids = self.run_statement(query_text, "select")
        for u_id in u_ids:
            id = u_id[0]
            query_text = "select username from employee where employee_id = {0};".format(id)
            u_name = self.run_statement(query_text, "select")
            username = u_name[0][0]
            try:
                username = self.clean_username(username)
                sql_text = "drop group if exists '{0}_group';".format(username)
                self.run_statement(sql_text, "other")
                sql_text = "create group '{0}_group';".format(username)
                self.run_statement(sql_text, "other")
                sql_text = "grant group '{0}_group' to '{0}'".format(username)
                self.run_statement(sql_text, "other")
                sql_text = "grant role {0}_role to '{0}_group';".format(username)
                self.run_statement(sql_text, "other")
            except:
                print("exception")
                
    def test(self):
        query_text = "select em.employee_id, em.manager_id, p.position_name, p.level, e.username \
                    from employee e, employee_manager em, employee_position ep, position p \
                    where em.manager_id = e.employee_id \
                    and e.employee_id = ep.employee_id \
                    and ep.position_id = p.position_id \
                    and p.level = 'm5';"
        results = self.run_statement(query_text, "select")
        direct_list = []
        for result in results:
            direct_list.append(result[0])
        role = "{0}_role".format(results[0][4])
        update_text = "update employee_salary \
                    set access_roles = concat(access_roles, '{0}', ',' ) \
                    where employee_id in (".format(role)
        for direct in direct_list:
            update_text = "{0}{1},".format(update_text, direct)
        update_text = update_text[:-1]
        update_text = "{0});".format(update_text)
        update_text = " ".join(update_text.split())
        self.run_statement(update_text, "other")
        self.test2(direct_list)
        
    def test2(self, direct_list):
        for direct in direct_list:
            query_text = "select em.employee_id, em.manager_id, e.username \
                    from employee e, employee_manager em, employee_position ep \
                    where em.manager_id = e.employee_id \
                    and e.employee_id = ep.employee_id \
                    and manager_id = {0};".format(direct)
            new_directs = []
            results = self.run_statement(query_text, "select")
            if len(results) != 0:
                role = "{0}_role".format(results[0][2])
                update_text = "update employee_salary \
                    set access_roles = concat(access_roles, '{0}', ',' ) \
                    where employee_id in (".format(role)
                for result in results:
                    update_text = "{0}{1},".format(update_text, result[0])
                    new_directs.append(result[0])
                update_text = update_text[:-1]
                update_text = "{0});".format(update_text)
                update_text = " ".join(update_text.split())  
                self.run_statement(update_text,"other")          
                self.test2(new_directs)
                
    def test3(self, direct_list):
        for direct in direct_list:
            query_text = "select employee_id from employee_manager where manager_id = {0}".format(direct)
            results = self.run_statement(query_text,"select")
            new_direct_list = []
            for result in results:
                new_direct_list.append(result[0])
            self.test3(new_direct_list)
            
    
    
    def run_statement(self, statement, type):
        aca = accendair_db()
        aca = accendair_db()
        s2cnf = s2_config(aca.get_os())
        s2 = singlestore(s2cnf)
        if type == 'select':
            results = s2.run_select(statement)
            return results
        elif type == 'other':
            s2.run_sql(statement)
            
                
    def clean_username(self, username_in):
        username = username_in.strip()
        username = username.replace(" ","")
        username = username.replace("'","")
        username = username.replace("-","")
        username = username.replace(".","")
        username = username.replace("`","")
        return username
    
            
            
def main():
    um = user_management()
    #um.delete_users()
    #um.add_users()
    #um.add_employees_to_all()
    #um.create_manager_roles()
    #um.add_managers_to_roles()
    direct_list = []
    direct_list.append(63)
    um.test3(direct_list);        
if __name__ == '__main__':
    main()
