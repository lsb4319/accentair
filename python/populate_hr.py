import random
import singlestore
import platform
import json
from singlestore import os


class ascentair_db:
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
        os = self.get_os()
        s2_config = singlestore.s2_config(os)
        s2 = singlestore.singlestore(s2_config)
        statement = "SELECT employee_id FROM employee WHERE end_date is null order by employee_id;"
        records = s2.run_select(statement)
        employee_ids = [record[0] for record in records]

        # department_id -> target headcount
        targets = {
            1: self.executive_target,
            2: self.rnd_target,
            3: self.sales_target,
            4: self.support_target,
            5: self.marketing_target,
            6: self.hr_target,
            7: self.engineering_target,
            8: self.training_target,
            9: self.accounting_target,
            10: self.pm_target,
            11: self.services_target,
            12: self.it_target,
            13: self.legal_target,
        }
        total_target = sum(targets.values())
        if total_target != len(employee_ids):
            raise ValueError(
                "department targets ({0}) do not match employee count ({1})".format(
                    total_target, len(employee_ids)))

        dept_ids = []
        for dept_id, target in targets.items():
            dept_ids.extend([dept_id] * target)
        random.shuffle(dept_ids)

        rows = [(employee_id, dept_id, '2023-01-01')
                for employee_id, dept_id in zip(employee_ids, dept_ids)]

        insert_text = "insert into employee_department(employee_id, department_id, start_date) values (%s, %s, %s)"
        s2.run_many(insert_text, rows)

    def populate_emp_pos(self):
        os = self.get_os()
        s2_config = singlestore.s2_config(os)
        s2 = singlestore.singlestore(s2_config)
        query = "select distinct(department_id) from department order by department_id"
        departments = s2.run_select(query)
        position_file = open("python/position.json","r")
        position_json = json.loads(position_file.read())
        position_file.close()
        for department in departments:
            department = department[0]
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
            min_pos = s2.run_select(
                "select min(position_id) from position where department_id = %s", (department,))[0][0]
            max_pos = s2.run_select(
                "select max(position_id) from position where department_id = %s", (department,))[0][0]
            employees = s2.run_select(
                "select employee_id from employee_department where department_id = %s \
                                and end_date is null;", (department,))
            rows = []
            for employee in employees:
                employee = employee[0]
                done = False
                while not done:
                    position_id = random.randint(int(min_pos),int(max_pos))
                    level = s2.run_select(
                        "select level from position where position_id = %s", (position_id,))[0][0]
                    level = level.rstrip("\r").lower()
                    if level == "ic1" and ic1 < ic1_target:
                        rows.append((employee, position_id, '2023-01-01'))
                        ic1 += 1
                        done = True
                    elif level == "ic2" and ic2 < ic2_target:
                        rows.append((employee, position_id, '2023-01-01'))
                        ic2 += 1
                        done = True
                    elif level == "ic3" and ic3 < ic3_target:
                        rows.append((employee, position_id, '2023-01-01'))
                        ic3 += 1
                        done = True
                    elif level == "m1" and m1 < m1_target:
                        rows.append((employee, position_id, '2023-01-01'))
                        m1 += 1
                        done = True
                    elif level == "m2" and m2 < m2_target:
                        rows.append((employee, position_id, '2023-01-01'))
                        m2 += 1
                        done = True
                    elif level == "m3" and m3 < m3_target:
                        rows.append((employee, position_id, '2023-01-01'))
                        m3 += 1
                        done = True
                    elif level == "m4" and m4 < m4_target:
                        rows.append((employee, position_id, '2023-01-01'))
                        m4 += 1
                        done = True
                    elif level == "m5" and m5 < m5_target:
                        rows.append((employee, position_id, '2023-01-01'))
                        m5 += 1
                        done = True
            insert_text = "insert into employee_position (employee_id, position_id, start_date) values (%s, %s, %s)"
            s2.run_many(insert_text, rows)

    def populate_ic_m1_man(self):
        os = self.get_os()
        s2_config = singlestore.s2_config(os)
        s2 = singlestore.singlestore(s2_config)
        #depts_query = "select distinct(department_id) from department where department_id <> 1 order by department_id"
        #departments = s2.run_select(depts_query)
        #for department in departments:
        department = 7
        m3_query = "select employee_id from(\
            select ep.employee_id as employee_id, p.level as level\
                from employee_position ep\
                join position p\
                on ep.position_id = p.position_id\
                where p.department_id = %s)\
                where level like '%%M3%%'"
        m3s = s2.run_select(m3_query, (department,))
        m4_query = "select employee_id from(\
            select ep.employee_id as employee_id, p.level as level\
                from employee_position ep\
                join position p\
                on ep.position_id = p.position_id\
                where p.department_id = %s)\
                where level like '%%M2%%'"
        m4s = s2.run_select(m4_query, (department,))
        m4_count = len(m4s)
        m4_curr = 0
        rows = []
        for m3 in m3s:
            rows.append((m3[0], m4s[m4_curr][0], '2003-01-01'))
            if m4_curr +1 < m4_count:
                m4_curr+=1
            elif m4_curr + 1 == m4_count:
                m4_curr = 0
        insert_text = "insert into employee_manager(employee_id, manager_id, start_date) values (%s, %s, %s)"
        s2.run_many(insert_text, rows)

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
        bands = {
            "IC1": (salary_bands[0][1], salary_bands[0][2]),
            "IC2": (salary_bands[1][1], salary_bands[1][2]),
            "IC3": (salary_bands[2][1], salary_bands[2][2]),
            "M1": (salary_bands[3][1], salary_bands[3][2]),
            "M2": (salary_bands[4][1], salary_bands[4][2]),
            "M3": (salary_bands[5][1], salary_bands[5][2]),
            "M4": (salary_bands[6][1], salary_bands[6][2]),
            "M5": (salary_bands[7][1], salary_bands[7][2]),
            "M6": (salary_bands[8][1], salary_bands[8][2]),
        }
        rows = []
        for emp in emp_level:
            band = bands.get(emp[1])
            if band is None:
                continue
            salary = random.randint(band[0], band[1])
            rows.append((emp[0], salary, '2023-01-01'))
        insert_text = "insert into employee_salary (employee_id, salary, start_date) values (%s, %s, %s)"
        s2.run_many(insert_text, rows)

    def get_dept(self):
        dept = random.randint(1,13)
        return dept

    def get_salary(self, level):
        query_text = "select "
        pass

def main():
    adb = ascentair_db()
    #adb.populate_emp_dep()
    #adb.populate_emp_pos()
    #adb.populate_ic_m1_man()
    adb.populate_salary()

if __name__ == '__main__':
    main()
