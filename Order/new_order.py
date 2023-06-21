import requests
import json
import xml.dom.minidom
import xml.etree.ElementTree as ET
import cx_Oracle

print ("Running tests for cx_Oracle version", cx_Oracle.version)
# Connect as user "hr" with password "welcome" to the "orclpdb1" service running on this computer.
connection = cx_Oracle.connect(user="BO_TEST_13", password="SYS", dsn="10.0.0.137:1521/test")

########## НЕ РАБОТАЕТ:
cursor = connection.cursor()
cursor.execute("""
        SELECT b_regnum, B_STAT
        FROM ord_m
        WHERE b_regnum = :did AND B_STAT > :eid""",
        did = 7925887,
        eid = 65)
for fname, lname in cursor:
    print("Values:", fname, lname)
##########
    
with cx_Oracle.connect(user="BO_TEST_99", password="SYS", dsn="10.0.0.137:1521/test") as connection2:
    with connection2.cursor() as cursor:
        sql0 = """select sysdate from dual"""
        for r in cursor.execute(sql0):
            print(r)

id_ = 8158813

with connection as db:
    with db.cursor() as cursor:
        sql = "select b_regnum, b_stat from ord_m where b_regnum = %s" % id_
        print("DB query: ", sql)
        for r in cursor.execute(sql):
            print("DB result: ", r) # tuple object
        status = r[1]            
        print("Статус: ", status)

if status == 65:
    print("Passed")
else:
    print("Failed")


