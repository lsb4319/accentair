import random
import time
import singlestore
import platform
import json
from singlestore import os
import math


class accendair_db:
    def __init__(self):
        self.executive_target = 5
        self.rnd_target = 131
        self.sales_target = 1501
        self.support_target = 327
        self.marketing_target = 507
        self.hr_target = 327
        self.engineering_target = 2532
        self.training_target = 98
        self.accounting_target = 409
        self.pm_target = 414
        self.services_target = 147
        self.it_target = 98
        self.legal_target = 82
        
    def get_os(self):
        current_os = platform.system()
        if current_os=="Darwin":
                my_os = os.mac
        elif current_os=="Windows":
                my_os = os.windows
        elif current_os=="Linux":
                my_os = os.linux
        return_value = my_os
        return return_value

    def populate_emp_dep(self):
        executive = 0
        rnd = 0
        sales = 0
        support = 0
        marketing = 0
        hr = 0
        engineering = 0
        training = 0
        accounting = 0
        pm = 0
        services = 0
        it = 0
        legal = 0
        os = self.get_os()
        s2_config = singlestore.s2_config(os)
        s2 = singlestore.singlestore(s2_config)
        statement = "SELECT employee_id FROM employee WHERE end_date is null order by employee_id;"
        records = s2.run_select(statement)
        rows = []
        retries = 0
        while self.executive_target > executive or \
            self.rnd_target > rnd or \
            self.sales_target > sales or \
            self.support_target > support or \
            self.marketing_target > marketing or \
            self.hr_target > hr or \
            self.engineering_target > engineering or \
            self.training_target > training or \
            self.accounting_target > accounting or \
            self.pm_target > pm or \
            self.services_target > services or \
            self.it_target > it or \
            self.legal_target > legal:
            for id in records:
                record_ok = False
                while not record_ok:
                    dept_id = self.get_dept()
                    time.sleep(.1)
                    if self.executive_target == executive and \
                        self.rnd_target == rnd and \
                        self.sales_target == sales and \
                        self.support_target == support and \
                        self.marketing_target == marketing and \
                        self.hr_target == hr and \
                        self.training_target == training and \
                        self.accounting_target == accounting and \
                        self.pm_target == pm and \
                        self.services_target == services and \
                        self.it_target == it and \
                        self.legal_target == legal:
                        dept_id = 7
                    elif self.executive_target == executive and \
                        self.rnd_target == rnd and \
                        self.engineering_target == engineering and \
                        self.support_target == support and \
                        self.marketing_target == marketing and \
                        self.hr_target == hr and \
                        self.training_target == training and \
                        self.accounting_target == accounting and \
                        self.pm_target == pm and \
                        self.services_target == services and \
                        self.it_target == it and \
                        self.legal_target == legal:
                        dept_id = 3
                    record = (id, dept_id, '2023-01-01')
                    if dept_id == 1:
                        if executive < self.executive_target:
                            rows.append(record)
                            executive += 1
                            record_ok = True
                        else:
                            record_ok = False
                            retries += 1
                    elif dept_id == 2:
                        if rnd < self.rnd_target:
                            rows.append(record)
                            rnd += 1
                            record_ok = True
                        else:
                            record_ok = False
                            retries += 1
                    elif dept_id == 3:
                        if sales < self.sales_target:
                            rows.append(record)
                            sales += 1
                            record_ok = True
                        else:
                            record_ok = False
                            retries += 1
                    elif dept_id == 4:
                        if support < self.support_target:
                            rows.append(record)
                            support += 1
                            record_ok = True
                        else:
                            record_ok = False
                            retries += 1
                    elif dept_id == 5:
                        if marketing < self.marketing_target:
                            rows.append(record)
                            marketing += 1
                            record_ok = True
                        else:
                            record_ok = False
                            retries += 1
                    elif dept_id == 6:
                        if hr < self.hr_target:
                            rows.append(record)
                            hr += 1
                            record_ok = True
                        else:
                            record_ok = False
                            retries += 1
                    elif dept_id == 7:
                        if engineering < self.engineering_target:
                            rows.append(record)
                            engineering += 1
                            record_ok = True
                        else:
                            record_ok = False
                            retries += 1
                    elif dept_id == 8:
                        if training < self.training_target:
                            rows.append(record)
                            training += 1
                            record_ok = True
                        else:
                            record_ok = False
                            retries += 1
                    elif dept_id == 9:
                        if accounting < self.accounting_target:
                            rows.append(record)
                            accounting += 1
                            record_ok = True
                        else:
                            record_ok = False
                            retries += 1
                    elif dept_id == 10:
                        if pm < self.pm_target:
                            rows.append(record)
                            pm += 1
                            record_ok = True
                        else:
                            record_ok = False
                            retries += 1
                    elif dept_id == 11:
                        if services < self.services_target:
                            rows.append(record)
                            services += 1
                            record_ok = True
                        else:
                            record_ok = False
                            retries += 1
                    elif dept_id == 12:
                        if it < self.it_target:
                            rows.append(record)
                            it += 1
                            record_ok = True
                            retries += 1
                        else:
                            record_ok = False
                    elif dept_id == 13:
                        if legal < self.legal_target:
                            rows.append(record)
                            legal += 1
                            record_ok = True
                        else:
                            record_ok = False
                            retries += 1
                    else:
                        record_ok = False
                        retries += 1
        insert_text = "insert into employee_department(employee_id, department_id, start_date) values"
        i = 0
        os = self.get_os()
        s2_config = singlestore.s2_config(os)
        s2 = singlestore.singlestore(s2_config)
        s2.run_sql(insert_text)
    
    def populate_emp_pos(self):
        os = self.get_os()
        s2_config = singlestore.s2_config(os)
        s2 = singlestore.singlestore(s2_config)
        query = "select distinct(department_id) from department order by department_id"
        departments = s2.run_select(query)
        for department in departments:
            position_file = open("python/position.json","r")
            position_text = position_file.read()
            position_file.close()
            position_json = json.loads(position_text)
            ic1_target = position_json[str(department)]["ic1"]
            ic2_target = position_json[str(department)]["ic2"]
            ic3_target = position_json[str(department)]["ic3"]
            m1_target = position_json[str(department)]["m1"]
            m2_target = position_json[str(department)]["m2"]
            m3_target = position_json[str(department)]["m3"]
            m4_target = position_json[str(department)]["m4"]
            m5_target = position_json[str(department)]["m5"]
            ic1 = 0
            ic2 = 0
            ic3 = 0
            m1 = 0
            m2 = 0
            m3 = 0
            m4 = 0
            m5 = 0
            os = self.get_os()
            s2_config = singlestore.s2_config(os)
            s2 = singlestore.singlestore(s2_config)
            min_query = "select min(position_id) from position where department_id = {0}".format(department)
            max_query = "select max(position_id) from position where department_id = {0}".format(department)
            min_pos = s2.run_select(min_query)[0]
            max_pos = s2.run_select(max_query)[0]
            employee_query = "select employee_id from employee_department where department_id = {0} \
                                and end_date is null;".format(department)
            employees = s2.run_select(employee_query)
            insert_text = "insert into employee_position (employee_id, position_id, start_date) values"
            for employee in employees:
                done = False
                while not done:
                    position_id = random.randint(int(min_pos),int(max_pos))
                    level_query = "select level from position where position_id = {0}".format(position_id)
                    level = s2.run_select(level_query)[0].rstrip("\r")
                    level = level.lower()
                    if level == "ic1" and ic1 < ic1_target:
                        insert_text = "{0}({1},{2},'{3}'),".format(insert_text, employee, position_id, '2023-01-01')
                        ic1 += 1
                        done = True
                    elif level == "ic2" and ic2 < ic2_target:
                        insert_text = "{0}({1},{2},'{3}'),".format(insert_text, employee, position_id, '2023-01-01')
                        ic2 += 1
                        done = True    
                    elif level == "ic3" and ic3 < ic3_target:
                        insert_text = "{0}({1},{2},'{3}'),".format(insert_text, employee, position_id, '2023-01-01')
                        ic3 += 1
                        done = True  
                    elif level == "m1" and m1 < m1_target:
                        insert_text = "{0}({1},{2},'{3}'),".format(insert_text, employee, position_id, '2023-01-01')
                        m1 += 1
                        done = True  
                    elif level == "m2" and m2 < m2_target:
                        insert_text = "{0}({1},{2},'{3}'),".format(insert_text, employee, position_id, '2023-01-01')
                        m2 += 1
                        done = True  
                    elif level == "m3" and m3 < m3_target:
                        insert_text = "{0}({1},{2},'{3}'),".format(insert_text, employee, position_id, '2023-01-01')
                        m3 += 1
                        done = True  
                    elif level == "m4" and m4 < m4_target:
                        insert_text = "{0}({1},{2},'{3}'),".format(insert_text, employee, position_id, '2023-01-01')
                        m4 += 1
                        done = True  
                    elif level == "m5" and m5 < m5_target:
                        insert_text = "{0}({1},{2},'{3}'),".format(insert_text, employee, position_id, '2023-01-01')
                        m5 += 1
                        done = True  
            insert_text = insert_text.rstrip(",")
            insert_text = insert_text + ";"
            os = self.get_os()
            s2_config = singlestore.s2_config(os)
            s2 = singlestore.singlestore(s2_config)
            s2.run_sql(insert_text)
    
    def populate_ic_m1_man(self):
        os = self.get_os()
        s2_config = singlestore.s2_config(os)
        s2 = singlestore.singlestore(s2_config)
        #depts_query = "select distinct(department_id) from department where department_id <> 1 order by department_id"
        #departments = s2.run_select(depts_query)
        #for department in departments:
        m3_query = "select employee_id from(\
            select ep.employee_id as employee_id, p.level as level\
                from employee_position ep\
                join position p\
                on ep.position_id = p.position_id\
                where p.department_id = {0})\
                where level like '%M3%'".format(7)
        m3s = s2.run_select(m3_query)
        m4_query = "select employee_id from(\
            select ep.employee_id as employee_id, p.level as level\
                from employee_position ep\
                join position p\
                on ep.position_id = p.position_id\
                where p.department_id = {0})\
                where level like '%M2%'".format(7)
        m4s = s2.run_select(m4_query)
        m4_count = len(m4s)
        m3_count = len(m3s)
        m4_curr = 0
        for m3 in m3s:
            insert_text = "insert into employee_manager(employee_id, manager_id, start_date) values({0},{1},'{2}')".format(m3,m4s[m4_curr],'2003-01-01')
            s2.run_sql(insert_text)
            if m4_curr +1 < m4_count:
                m4_curr+=1
            elif m4_curr + 1 == m4_count:
                m4_curr = 0
                         
        
    def populate_salary(self):
        os = self.get_os()
        s2_config = singlestore.s2_config(os)
        s2 = singlestore.singlestore(s2_config)
        query_text = "select e.employee_id, p.level\
                        from employee e\
                        join employee_position ep\
                            on e.employee_id = ep.employee_id\
                        join position p\
                            on ep.position_id = p.position_id;"
        emp_level = s2.run_select(query_text)
        salary_bands = s2.run_select("select * from salary_band order by position_level;")
        ic1_low = salary_bands[0][1]
        ic1_high = salary_bands[0][2]
        ic2_low = salary_bands[1][1]
        ic2_high = salary_bands[1][2]
        ic3_low = salary_bands[2][1]
        ic3_high = salary_bands[2][2]
        m1_low = salary_bands[3][1]
        m1_high = salary_bands[3][2]
        m2_low = salary_bands[4][1]
        m2_high = salary_bands[4][2]
        m3_low = salary_bands[5][1]
        m3_high = salary_bands[5][2]
        m4_low = salary_bands[6][1]
        m4_high = salary_bands[6][2]
        m5_low = salary_bands[7][1]
        m5_high = salary_bands[7][2]
        m6_low = salary_bands[8][1]
        m6_high = salary_bands[8][2]
        insert_text = ""
        for emp in emp_level:
            if emp[1]=="IC1":
                salary = random.randint(ic1_low,ic1_high)
                insert_text = "insert into employee_salary (employee_id, salary, start_date)values({0},{1},'2023-01-01');"\
                    .format(emp[0],salary)
            elif emp[1]=="IC2":
                salary = random.randint(ic2_low,ic2_high)
                insert_text = "insert into employee_salary (employee_id, salary, start_date)values({0},{1},'2023-01-01');"\
                    .format(emp[0],salary)
            elif emp[1]=="IC3":
                salary = random.randint(ic3_low,ic3_high)
                insert_text = "insert into employee_salary (employee_id, salary, start_date)values({0},{1},'2023-01-01');"\
                    .format(emp[0],salary)
            elif emp[1]=="M1":
                salary = random.randint(m1_low,m1_high)
                insert_text = "insert into employee_salary (employee_id, salary, start_date)values({0},{1},'2023-01-01');"\
                    .format(emp[0],salary)
            elif emp[1]=="M2":
                salary = random.randint(m2_low,m2_high)
                insert_text = "insert into employee_salary (employee_id, salary, start_date)values({0},{1},'2023-01-01');"\
                    .format(emp[0],salary)
            elif emp[1]=="M3":
                salary = random.randint(m3_low,m3_high)
                insert_text = "insert into employee_salary (employee_id, salary, start_date)values({0},{1},'2023-01-01');"\
                    .format(emp[0],salary)
            elif emp[1]=="M4":
                salary = random.randint(m4_low,m4_high)
                insert_text = "insert into employee_salary (employee_id, salary, start_date)values({0},{1},'2023-01-01');"\
                    .format(emp[0],salary)
            elif emp[1]=="M5":
                salary = random.randint(m5_low,m5_high)
                insert_text = "insert into employee_salary (employee_id, salary, start_date)values({0},{1},'2023-01-01');"\
                    .format(emp[0],salary)
            elif emp[1]=="M6":
                salary = random.randint(m6_low,m6_high)
                insert_text = "insert into employee_salary (employee_id, salary, start_date)values({0},{1},'2023-01-01');"\
                    .format(emp[0],salary)
            s2.run_sql(insert_text)
                            
    def get_dept(self):
        dept = random.randint(1,13)
        return dept
    
    def get_salary(self, level):
        query_text = "select "
        pass
    
def main():
    adb = accendair_db()
    #adb.populate_emp_dep()
    #adb.populate_emp_pos()
    #adb.populate_ic_m1_man()
    adb.populate_salary()
    
if __name__ == '__main__':
    main()