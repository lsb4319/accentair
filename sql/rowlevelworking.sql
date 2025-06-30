CREATE TABLE IF NOT EXISTS hr.employee_backup (
  employee_id INT NOT NULL,
  first_name VARCHAR(45) NOT NULL,
  middle_name VARCHAR(45) NULL DEFAULT NULL,
  last_name VARCHAR(45) NOT NULL,
  email VARCHAR(100) NOT NULL,
  username AS substring_index(email,'@',1) PERSISTED VARCHAR(50),
  phone VARCHAR(20) NOT NULL,
  street_address VARCHAR(45) NOT NULL,
  address_line_2 VARCHAR(45) NULL DEFAULT NULL,
  city VARCHAR(45) NOT NULL,
  state_province VARCHAR(3) NOT NULL,
  country_code VARCHAR(3) NOT NULL,
  postal_code VARCHAR(45) NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NULL DEFAULT NULL,
  PRIMARY KEY (employee_id)
);
alter table hr.employee drop column username;
alter table hr.employee add column username as substring_index(email,'@',1) PERSISTED VARCHAR(50);
split('lorrin@smith-bates.com','@');
CREATE TABLE IF NOT EXISTS hr.department (
  department_id INT NOT NULL,
  department_name VARCHAR(45) NOT NULL,
  PRIMARY KEY (department_id)
);

CREATE TABLE IF NOT EXISTS hr.position (
  position_id INT NOT NULL,
  position_name VARCHAR(45) NOT NULL,
  department_id INT, NOT NULL,
  level VARCHAR(10),
  PRIMARY KEY (position_id)
);

CREATE TABLE IF NOT EXISTS hr.employee_manager (
  employee_id INT NOT NULL,
  manager_id INT NOT NULL,
  start_date DATETIME NOT NULL,
  end_date DATETIME NULL DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS hr.employee_salary (
  employee_id INT NOT NULL,
  salary DECIMAL(7,2) NOT NULL,
  start_date DATETIME NOT NULL,
  end_date DATETIME NULL DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS hr.employee_department (
  employee_id INT NOT NULL,
  department_id INT NOT NULL,
  start_date DATETIME NOT NULL,
  end_date DATETIME NULL DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS hr.employee_position (
  employee_id INT NOT NULL,
  position_id VARCHAR(45) NOT NULL,
  start_date DATETIME NOT NULL,
  end_date DATETIME NULL DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS hr.time_off (
  employee_id INT NOT NULL,
  start_date DATETIME NOT NULL,
  end_date DATETIME NOT NULL,
  reason VARCHAR(20) NOT NULL
);

create table IF NOT EXISTS position(
  position_id INT primary key,
  position_name VARCHAR(255),
  department_id INT,
  level varchar(5)
);

create table IF NOT EXISTS employee_salary(
  employee_id INT,
  salary double,
  start_date Date,
  end_date DATE
);

create table IF NOT EXISTS hr.salary_band(
  position_level varchar(10),
  low_end DECIMAL,
  high_end DECIMAL
);
show users;
CREATE ROLE 'r_hrusers';
show roles;
grant select on hr.employee to role 'r_hrusers';
create group 'g_hrusers';
grant role 'r_hrusers' to 'g_hrusers';
grant usage on *.* to 'obisb' identified by 'goSinglestore1';
grant group 'g_hrusers' to 'obisb';

CREATE ROLE 'employee_editors_role';
grant SELECT, INSERT, UPDATE, DELETE ON hr.employee to ROLE employee_editors_role;
CREATE GROUP 'employee_editors_group';
GRANT ROLE 'employee_editors_role' TO 'employee_editors_group';
GRANT USAGE ON *.* TO jorbell IDENTIFIED BY 'goSinglestore1';
GRANT USAGE ON *.* TO zfuzzey IDENTIFIED BY 'goSinglestore1'; 
GRANT USAGE ON *.* TO mnice IDENTIFIED BY 'goSinglestore1';
GRANT GROUP 'employee_editors_group' to jorbell;
GRANT GROUP 'employee_editors_group' to zfuzzey;
GRANT GROUP 'employee_editors_group' to mnice;



show grants for 'employee_editors_role';
show roles for group 'employee_editors_group';
show users for group 'employee_editors_group';
SET PASSWORD FOR 'jorbell'@'%' = PASSWORD('goSinglestore1');
drop user jorbell, zfuzzey, mnice;
drop role 'employee_editors_role';

select * from employee limit 10;

create view employee_view AS
  select e.first_name, e.last_name, e.email, e.state_province, e.country_code, p.position_name as title
    from employee e
    join employee_position ep
    on e.employee_id = ep.employee_id
    join position p
    on ep.position_id = p.position_id; 

select count(*) from employee_view;

create role all_role;
grant select on hr.employee_view to all_role;
create group 'all';
grant role all_role to 'all';
grant group 'all' to mnice;
show users for group 'all';
show grants for all_role;

grant select on hr.employee_view to 'all_role';
grant select on hr.employee_view to 'all';
show grants for all_role;
show roles for group 'all';
show users for group 'all';
grant select on hr.employee_view to 'mnice'@'%';
show views;


select count(*) from enrollment;
select count(*) from user;

CREATE MILESTONE "ed_data_test" for hr;

show milestones;

drop table position;
show tables;

detach database hr;

attach database hr at milestone "ed_data_test";

drop table position;

detach database hr;
attach database hr at milestone 'ed_data_test';

show roles for group 'organization';
show groups;
show users;
show grants for role 'owner';
show roles;

show teams;
select current_security_groups();
grant role 'employee_editors_role' to 'owners';
show grants for 'organization owners'@'%';
show users;
use hr;
select now();
attach database hr at milestone '2023-07-10 23_53_13.399963';
backup database hr to s3 "singlestore-education/backup/hr/"+ now();
CONFIG '{"region":"us-east-1"}'
CREDENTIALS '{}';
drop user *;
select now() + 0;
backup database hr to s3 'singlestore-education/backup.hr/20230717172537'
CONFIG '{"region":"us-east-1"}'
CREDENTIALS '{}';

`concat('singlestore-education/backup.hr/',now()+0) :> VARCHAR(255)`;

singlestore-education/backup.hr/20230712230438


select concat('singlestore-education/backup.hr/',now()+0) :> VARCHAR(255);

select concat('singlestore-education/backup.hr/',now()+0) :> VARCHAR(255);

select USER from information_schema.users where type = 'NATIVE';
delete from information_schema.users where type = 'NATIVE';

select substring_index(email, '@', 1) from employee;
select e1.email, e2.email from employee e1 join employee e2 on e1.email != e2.email limit 10000;

select distinct(email) from employee limit 10000;

SELECT email, COUNT(*) AS count
FROM employee
GROUP BY email
HAVING count > 1;

select * from employee where email not like '%@accentair.com';

select * from employee where email = 'gumarquand@accentair.com';
DROP TABLE employee_1;
update employee set email = 'pdyhouse@accentair.com' where employee_id = 3485;
CREATE TABLE IF NOT EXISTS hr.employee_1 (
  employee_id INT NOT NULL,
  first_name VARCHAR(45) NOT NULL,
  middle_name VARCHAR(45) NULL DEFAULT NULL,
  last_name VARCHAR(45) NOT NULL,
  email VARCHAR(255) NOT NULL,
  username as substring_index(email, '@', 1) PERSISTED VARCHAR(30),
  street_address VARCHAR(45) NOT NULL,
  address_line_2 VARCHAR(45) NULL DEFAULT NULL,
  city VARCHAR(255) NOT NULL,
  state_province VARCHAR(2) NOT NULL,
  country_code VARCHAR(3) NOT NULL,
  postal_code VARCHAR(45) NOT NULL,
  start_date DATETIME NOT NULL,
  end_date DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (employee_id)
);

SELECT * FROM salary_band;
show users;

select count(*) from information_schema.users;

alter table employee add column username as substring_index(email,'@',1) PERSISTED VARCHAR(30);
select count(distinct username) from employee; 

show users;

create user 'mde guise' identified by 'goSinglestore1';


DROP USER 'mde guise'@'%';

DROP USER mdeguise;
show users;


select * from employee_view;
grant select on hr.employee_view to all_role;
create group 'all';
grant role 'all_role' to 'all';

DELIMITER //
CREATE PROCEDURE AddUsersToGroup() AS
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE Username VARCHAR(50);
    DECLARE userCursor CURSOR FOR SELECT username FROM hr.employee;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    OPEN userCursor;
    
    read_loop: LOOP
        FETCH userCursor INTO Username;
        GRANT GROUP 'all' TO Username;
        IF done = 1 THEN
            LEAVE read_loop;
        END IF;
    END LOOP;
    CLOSE userCursor;
END //
DELIMITER ;

DELIMITER //

CREATE PROCEDURE AddUsersToGroup() AS
BEGIN
    -- Declare variables
    DECLARE done INT DEFAULT FALSE;
    DECLARE username VARCHAR(50);

    -- Declare cursor for selecting usernames
    DECLARE userCursor CURSOR FOR
        SELECT Username FROM YourTableName; -- Replace with the name of your table

    -- Declare handler for cursor operations
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Declare temporary table for holding group information
    CREATE TEMPORARY TABLE TempGroup (
        Username VARCHAR(50),
        GroupName VARCHAR(50)
    );

    -- Open cursor
    OPEN userCursor;

    -- Fetch usernames and insert into temporary table
    read_loop: LOOP
        -- Fetch the next username
        FETCH userCursor INTO username;

        -- Exit loop if no more usernames found
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Insert username and group information into temporary table
        INSERT INTO TempGroup (Username, GroupName)
        VALUES (username, 'YourGroupName'); -- Replace with the name of the group
    END LOOP;

    -- Close cursor
    CLOSE userCursor;

    -- Update group-related column in the target table
    UPDATE YourTableName -- Replace with the name of your table
    SET GroupName = (
        SELECT GroupName
        FROM TempGroup
        WHERE TempGroup.Username = YourTableName.Username
    );

    -- Drop temporary table
    DROP TABLE TempGroup;
END //

DELIMITER ;

DELIMITER //

CREATE OR REPLACE PROCEDURE select_and_group() RETURNS VARCHAR(30) AS
DECLARE
    query QUERY(username VARCHAR(30)) = SELECT username FROM employee;
    echo select query;
    usernames ARRAY(RECORD(username varchar(30));
    count INT default 0;
    _username VARCHAR(30);
BEGIN
    SET count = 0;
    usernames = COLLECT(query);
    FOR x in usernames LOOP
      _username = x.username;
      GRANT GROUP 'all' TO _username;
      SET count = count+1;
    END LOOP;
    RETURN count;
END //

DELIMITER ;

CALL select_and_group();

select username from employee;

CREATE TABLE source(a int, b int);
CREATE TABLE target(a int, b int);
INSERT INTO source VALUES(1, 2), (2, 2), (3, 2), (4, 3), (5, 3);

DELIMITER //

CREATE OR REPLACE PROCEDURE p() AS
DECLARE
    q QUERY(a int, b int) = SELECT a, b FROM source;
BEGIN
    ECHO SELECT a, b from q;
END //

DELIMITER ;

CALL p();
SELECT * FROM target;
delete from target;


DELIMITER //

CREATE OR REPLACE PROCEDURE iterate_over_results() AS
DECLARE
  user VARCHAR(255);
  cur CURSOR FOR (SELECT username FROM employee);
BEGIN
  OPEN cur;
  
END //

DELIMITER ;

CALL iterate_over_results();

FETCH NEXT FROM cur INTO user;
  WHILE cur FOUND LOOP
    ECHO SELECT user;
    FETCH NEXT FROM cur INTO user;
  END LOOP;

  DELIMITER //

CREATE OR REPLACE PROCEDURE select_and_group() RETURNS VARCHAR(30) AS
DECLARE
    query QUERY(username VARCHAR(30)) = SELECT username FROM employee;
    echo select query;
    usernames ARRAY(RECORD(username varchar(30));
    count INT default 0;
    _username VARCHAR(30);
BEGIN
    SET count = 0;
    usernames = COLLECT(query);
    FOR x in usernames LOOP
      _username = x.username;
      GRANT GROUP 'all' TO _username;
      SET count = count+1;
    END LOOP;
    RETURN count;
END //

DELIMITER ;

DELIMITER //

CREATE OR REPLACE PROCEDURE select_and_group() AS
DECLARE
    query QUERY(username VARCHAR(30)) = SELECT username FROM employee;
BEGIN 
    echo select query.username;
END //

DELIMITER ;

call select_and_group();
show groups for role 'all_role';
show users for group 'all';
select COUNT(*) from information_schema.USERS_GROUPS WHERE `GROUP` = 'all';
show grants for 'all';
grant USAGE ON hr.* to 'all_role';
grant role all_role to 'all';
show roles for group 'all';
show roles for user 'aartz'@'%';

show grants for group 'all';
show grants for role 'all_role';
show grants for 'aartz'@'%';

grant select on hr.employee_view to role 'all_role';
revoke select on hr.employee from role 'all_role';


ALTER TABLE employee_salary add column access_roles varbinary(255) DEFAULT ",";

select e.employee_id, 
  from employee e
  join employee_position ep
  join position p
  join department d
  where e.employee_id = ep.employee_id
  and ep.position_id = p.position_id
  and p.department_id = d.department_id
  order by d.department_name, p.level;

select e.username, e.employee_id as manager_id, p.level
  from employee e
  join employee_position ep
  join position p
  join employee_manager em
  where e.employee_id = ep.employee_id
  and ep.position_id = p.position_id
  and e.employee_id = em.manager_id
  and p.level in ('m1', 'm2', 'm3', 'm4', 'm5')
  group by e.username
  order by em.manager_id;

select * from hr.employee_salary;
  
  drop role tscrivens_role

;

select count(*) from information_schema.role_privileges;
show roles;
backup_database hr to s3 singlestore-education/backup/hr/1689355632.681667;


select distinct(manager_id)
  from employee_manager
  order by manager_id
  limit 1000;

select username
  from employee
  where employee_id = 7;

select employee_id
  from employee_manager
  where manager_id = 7;

update employee_salary
  set access_roles  = concat(access_roles,"tscrivens_role,") where employee_id = 1375;

create view reports_view AS
  select e.employee_id, e.first_name, e.last_name, p.position_name, p.department_id, p.level, es.salary
    from employee e, position p, employee_salary es, employee_position ep
    where e.employee_id = es.employee_id
    and e.employee_id = ep.employee_id
    and p.position_id = ep.position_id
    and SECURITY_LISTS_INTERSECT(CURRENT_SECURITY_ROLES(), access_roles);

select * from employee_salary where employee_id = 1375;

select * from reports_view;

select manager_id from employee_manager;
create group 'rjustin_group';
create role 'rjustun_role';
grant group 'rjustin_group' to rjustun;
grant role rjustun_role to 'rjustin_group';
drop role rjustun_role;
drop group 'rjustun_group';
drop group 'rjustin_group';
show groups;
drop group 'rdeery_group';
select distinct(`group`) from information_schema.users_groups where `group` like '%_group';
grant select on hr.reports_view to role 'all_role';
show roles;

select * from hr.reports_view;
show users;

select manager_id from employee_manager order by manager_id;

select es.* 
  from employee_salary es, employee e, employee_manager em
  where es.employee_id =  e.employee_id
  and em.employee_id = e.employee_id
  and em.manager_id = 7;

revoke select on hr.employee_salary from role 'all_role';
update hr.employee_salary set access_roles = ',';
select * from employee_salary;
select
(select count(*) from hr.employee_salary where access_roles != ',') as done,
(select count(*) from hr.employee_salary where access_roles = ',') as remaining,
(select count(*) from hr.employee_salary) as total;

show users;

show variables like '%password%';
revoke select on hr.employee_salary from teka@smith-bates.com;
show grants for 'lsmithbates@singlestore.com';
select * from hr.employee_salary where access_roles != ',' limit 10000 ;


select em.manager_id, em.employee_id, e.username as manager_username 
  from employee_manager em, employee_position ep, position p, employee e
  where em.employee_id = ep.employee_id
  and ep.employee_id = e.employee_id
  and ep.position_id = p.position_id
  and p.level = 'm4'
  and e.employee_id = em.manager_id
  order by em.manager_id;

select distinct e.username, e.employee_id
  from hr.employee_position ep, hr.position p, hr.employee e
  where ep.position_id = p.position_id
  and e.employee_id = ep.employee_id
  and p.level = 'm1';

select * from employee where employee_id = 63;

select e.username, p.position_name, p.level
  from employee e, position p, employee_position ep
  where e.employee_id = ep.employee_id
  and p.position_id = ep.position_id
  and e.employee_id = 63;

update employee_salary
  set access_roles = 'ykerbler_role,';

select * from employee_salary order by employee_id limit 10000;

with recursive employee_hierarchy as (
  select e.employee_id, e.username, em.manager_id, p.level
  from employees e, employee_manager em, position p, employee_position ep
  where e.employee_id = em.employee_id
  and e.employee_id = ep.employee_id
  and ep.position_id = p.position_id);

select manager_id, count(employee_id) 
from employee_manager where employee_id in
(select manager_id from
employee_manager where employee_id in
(select manager_id 
  from employee_manager
  group by manager_id)
  group by manager_id)
  group by manager_id;


select em.employee_id, em.manager_id, p.position_name, p.level, e.username 
  from employee e, employee_manager em, employee_position ep, position p 
  where em.manager_id = e.employee_id
  and e.employee_id = ep.employee_id 
  and ep.position_id = p.position_id 
  and p.level = 'm5';

select em.employee_id, em.manager_id, p.position_name, p.level 
  from employee e, employee_manager em, employee_position ep, position p 
  where em.manager_id = e.employee_id
  and e.employee_id = ep.employee_id 
  and ep.position_id = p.position_id
  and manager_id = 574;

select em.employee_id, em.manager_id, p.position_name, p.level, e.username                     from employee e, employee_manager em, employee_position ep, position p                     where em.manager_id = e.employee_id                     and e.employee_id = ep.employee_id                     and ep.position_id = p.position_id                     and p.level = 'm5';,574,3246,945,588,2356"