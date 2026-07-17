from singlestore import s2_config, singlestore
from populate_hr import ascentair_db
import re
import secrets

class user_management:
    USERNAME_RE = re.compile(r'^[A-Za-z0-9_]+$')

    def __init__(self):
        pass

    def add_users(self):
        aca = ascentair_db()
        s2cnf = s2_config(aca.get_os())
        query_text = "select username from hr.employee;"
        s2 = singlestore(s2cnf)
        results = s2.run_select(query_text)
        credentials = []
        for result in results:
            username = (result[0])
            username = self.clean_username(username)
            password = secrets.token_urlsafe(12)
            sql_text = "create user {0} identified by %s;".format(username)
            s2.run_sql(sql_text, (password,))
            credentials.append((username, password))
        for username, password in credentials:
            print("{0}: {1}".format(username, password))


    def delete_users(self):
        aca = ascentair_db()
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
        results = self.run_statement("select username FROM hr.employee;", "select")
        for result in results:
            username = (result[0])
            username = self.clean_username(username)
            sql_text = "GRANT GROUP 'all' to {0};".format(username)
            self.run_statement(sql_text, "other")
            
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
            query_text = "select username from employee where employee_id = %s;"
            u_name = self.run_statement(query_text, "select", (id,))
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
                
    def assign_manager_access_roles(self):
        query_text = "select em.employee_id, em.manager_id, p.position_name, p.level, e.username \
                    from employee e, employee_manager em, employee_position ep, position p \
                    where em.manager_id = e.employee_id \
                    and e.employee_id = ep.employee_id \
                    and ep.position_id = p.position_id \
                    and p.level = 'm5';"
        results = self.run_statement(query_text, "select")
        direct_list = [result[0] for result in results]
        role = "{0}_role".format(results[0][4])
        self._grant_access_role_to_reports(role, direct_list)
        self._cascade_access_roles(direct_list)

    def _cascade_access_roles(self, direct_list):
        for direct in direct_list:
            query_text = "select em.employee_id, em.manager_id, e.username \
                    from employee e, employee_manager em, employee_position ep \
                    where em.manager_id = e.employee_id \
                    and e.employee_id = ep.employee_id \
                    and manager_id = %s;"
            results = self.run_statement(query_text, "select", (direct,))
            if len(results) != 0:
                role = "{0}_role".format(results[0][2])
                new_directs = [result[0] for result in results]
                self._grant_access_role_to_reports(role, new_directs)
                self._cascade_access_roles(new_directs)

    def _grant_access_role_to_reports(self, role, employee_ids):
        placeholders = ",".join(["%s"] * len(employee_ids))
        update_text = "update employee_salary set access_roles = concat(access_roles, %s, ',') " \
                       "where employee_id in ({0});".format(placeholders)
        params = [role] + employee_ids
        self.run_statement(update_text, "other", params)

    def run_statement(self, statement, type, params=None):
        aca = ascentair_db()
        s2cnf = s2_config(aca.get_os())
        s2 = singlestore(s2cnf)
        if type == 'select':
            results = s2.run_select(statement, params)
            return results
        elif type == 'other':
            s2.run_sql(statement, params)

    def clean_username(self, username_in):
        username = username_in.strip()
        username = username.replace(" ","")
        username = username.replace("'","")
        username = username.replace("-","")
        username = username.replace(".","")
        username = username.replace("`","")
        if not self.USERNAME_RE.match(username):
            raise ValueError("Unsafe username after cleaning: {0!r}".format(username_in))
        return username
    
            
            
def main():
    um = user_management()
    #um.delete_users()
    #um.add_users()
    #um.add_employees_to_all()
    #um.create_manager_roles()
    #um.add_managers_to_roles()
    #um.assign_manager_access_roles()

if __name__ == '__main__':
    main()
