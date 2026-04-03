# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Replace None with your code
df_boston = pd.read_sql("""
                        SELECT firstName,lastName
                        FROM employees
                        JOIN offices 
                             USING (officeCode)
                             WHERE city = 'Boston'
                          """,conn)


# STEP 2
# Replace None with your code
df_zero_emp = pd.read_sql("""
                        SELECT *
                        FROM offices
                        JOIN employees
                             USING (officeCode)
                        WHERE  reportsTo = "NULL"
                                """,conn)


# STEP 3
# Replace None with your code
df_employee = pd.read_sql("""
                          SELECT firstName,lastName,city,state
                          FROM employees
                          LEFT JOIN offices
                              USING (officeCode)
                            ORDER BY  firstName ,lastName;
                          """,conn)

# STEP 4
# Replace None with your code
df_contacts = pd.read_sql("""
                          SELECT contactFirstName,contactLastName,phone,salesRepEmployeeNumber
                          FROM customers
                          LEFT JOIN orders
                              USING (customerNumber)
                              WHERE orders.customerNumber IS NUll
                            ORDER BY  contactLastName ;
                          """,conn)


# STEP 5
# Replace None with your code
df_payment = pd.read_sql("""
                          SELECT contactFirstName,contactLastName,amount,paymentDate
                          FROM customers
                          JOIN payments
                              USING (customerNumber)
                          ORDER BY CAST (amount AS FLOAT) DESC;  
                          """,conn)

# STEP 6
# Replace None with your code
df_credit = pd.read_sql("""
                          SELECT e.employeeNumber,e.firstName,e.lastName,
                            COUNT(c.customerNUmber) AS numCustomers 
                          FROM employees e
                          JOIN customers c  ON  e.employeeNumber=c.salesRepEmployeeNumber
                          GROUP BY e.employeeNumber ,e.firstName,e.lastName
                          HAVING AVG (CAST (c.creditLimit AS FLOAT)) > 90000
                          ORDER BY numCustomers DESC;  
                          """,conn)


# STEP 7
# Replace None with your code
df_product_sold = pd.read_sql("""
                          SELECT p.productName,COUNT(o.orderNumber) AS numorders,SUM(o.quantityOrdered) AS totalunits
                          FROM products p
                          JOIN orderdetails o
                               USING (productCode)
                               GROUP BY (p.productName)
                          ORDER BY totalUnits DESC;  
                           """,conn)

# STEP 8
# Replace None with your code
df_total_customers = pd.read_sql("""
                          SELECT p.productName,p.productCode,COUNT (DISTINCT o.customerNumber) AS numpurchasers
                          FROM products p
                          JOIN orderdetails od ON p.productCode =od.productCode 
                          JOIN orders o ON od.orderNumber = o.orderNumber
                          GROUP BY p.productName,p.productCode
                          ORDER BY  numpurchasers DESC;  
                           """,conn)

# STEP 9
# Replace None with your code
df_customers = pd.read_sql("""
                      SELECT o.officeCode, o.city,
                      COUNT(c.customerNumber) AS n_customers
                         FROM offices o
                      JOIN employees e USING (officeCode)
                      JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
                     GROUP BY o.officeCode, o.city;
                          """,conn)


# STEP 10
# Replace None with your code
df_under_20 = pd.read_sql("""
                          SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName,o.city, o.officeCode
                          FROM employees e
                          JOIN offices o USING (officeCode)
                          JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
                          JOIN orders ord USING (customerNumber)
                          JOIN orderdetails od USING (orderNumber)
                          WHERE od.productCode IN (
                              SELECT productCode
                              FROM orderdetails
                              JOIN orders USING (orderNumber)
                              GROUP BY productCode
                              HAVING COUNT(DISTINCT customerNumber) < 20
                              )
                          ORDER BY e.lastName;
                          """,conn)

conn.close()