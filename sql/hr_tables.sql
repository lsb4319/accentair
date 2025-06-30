CREATE TABLE IF NOT EXISTS hr.employee_backup (
  employee_id INT NOT NULL,
  first_name VARCHAR(45) NOT NULL,
  middle_name VARCHAR(45) NULL DEFAULT NULL,
  last_name VARCHAR(45) NOT NULL,
  email VARCHAR(100) NOT NULL,
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

