import queue
import sqlite3
from contextlib import contextmanager


class ConnectionPool:
    def __init__(self, max_connections, database):
        self.max_connections = max_connections
        self.database = database
        self.pool = queue.Queue(maxsize=max_connections)

        for _ in range(max_connections):
            conn = self.create_connection()
            self.pool.put(conn)

    def create_connection(self):
        return sqlite3.connect(self.database)

    def get_connection(self, timeout):
        try:
            return self.pool.get(timeout=timeout)
        except queue.Empty:
            raise RuntimeError("Timeout: No available pool in the pool.")

    def release_connection(self, conn):
        self.pool.put(conn)

    @contextmanager
    def connection(self, timeout=10):
        conn = self.get_connection(timeout)
        try:
            yield conn
        finally:
            self.release_connection(conn)

def authClient(pool,data):
    with pool.connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT exists(SELECT 1 FROM clients WHERE client_username = ? and client_password = ?) AS row_exists;",data)
        data = cur.fetchone()
        return data

def authAdmin(pool,data):
    with pool.connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT exists(SELECT 1 FROM admin WHERE admin_username = ? and admin_password = ?) AS row_exists;",data)
        data = cur.fetchone()
        return data

def showEmergencyBedStatus(pool):
    with pool.connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT occupied_beds, vacant_beds FROM emergency_room;")
        data = cur.fetchone()
        return data

def showDoctorsData(pool):
    with pool.connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM doctors")
        data = cur.fetchall()
        conn.close()
        return data

def addApptsData(pool, data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlInsertQuery = "INSERT INTO appointments (appnt_id, doc_name, patient_name, patient_phone, date, time) VALUES (?, ?, ?, ?, ?, ?)"
        cur.execute(sqlInsertQuery, data)
        conn.commit()

def delApptsData(pool,data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlInsertQuery = "delete from appointments where appnt_id=?"
        cur.execute(sqlInsertQuery, (data,))
        sqlUpdateQuery = "UPDATE appointments SET appnt_id = appnt_id - 1 WHERE appnt_id > ?;"
        cur.execute(sqlUpdateQuery,(data,))
        conn.commit()

def showApptsData(pool):
    with pool.connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM appointments")
        data = cur.fetchall()
        return data

def checkHealthInsurance(pool, name, phone):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlQuery = f'''SELECT health_insurance_number FROM patient WHERE patient_name=? AND phone=?'''
        cur.execute(sqlQuery, (name, phone))
        data = cur.fetchone()
        return data[0] if data else None

def showTestsData(pool):
    with pool.connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM tests")
        data = cur.fetchall()
        return data
    
def showMedsData(pool):
    with pool.connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM medicine")
        data = cur.fetchall()
        return data

def showEmergencyBedsData(pool):
    with pool.connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM emergency_room_beds")
        data = cur.fetchall()
        return data
    
def updateAllotmentBedData(pool,data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlUpdateDataQuery = "UPDATE emergency_room_beds SET patient_name = ?,reason= ?,date=?,time=?,gender=?,age=?,address=?,phone=? WHERE bed_no = ?;"
        cur.execute(sqlUpdateDataQuery,data)
        conn.commit()

def updateBedStatus(pool):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlReleaseDataQuery = "SELECT COUNT(*) FROM emergency_room_beds WHERE patient_name = 'NA';"
        cur.execute(sqlReleaseDataQuery)
        data = cur.fetchall()
        empty_beds=data[0][0]
        sqlGetTotalBedsQuery = "SELECT total_beds FROM emergency_room;"
        cur.execute(sqlGetTotalBedsQuery)
        data = cur.fetchall()
        tot_beds = data[0][0]
        occupied_beds = tot_beds-empty_beds
        update_data = (occupied_beds,empty_beds)
        sqlUpdateBedStatusQuery = "update emergency_room set occupied_beds=?,vacant_beds=?;"
        cur.execute(sqlUpdateBedStatusQuery,update_data)
        conn.commit()

def showDeptsData(pool):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlReleaseDataQuery = "SELECT * FROM departments;"
        cur.execute(sqlReleaseDataQuery)
        data = cur.fetchall()
        return data

def addDocData(pool,data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlAddDocDataQuery = "INSERT INTO doctors (license_number,doctor_name,status,age_in_yr,gender,exp_in_yr,speciality,department,fee,appt_days,time_slot) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
        cur.execute(sqlAddDocDataQuery,data)
        conn.commit()

def getLicenseNos(pool):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlQuery = "select license_number from doctors;"
        cur.execute(sqlQuery)
        data = cur.fetchall()
        return data

def updteDocData(pool,data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlAddDocDataQuery = "update doctors set license_number=?,doctor_name=?,status=?,age_in_yr=?,gender=?,exp_in_yr=?,speciality=?,department=?,fee=?,appt_days=?,time_slot=? where license_number=?"
        cur.execute(sqlAddDocDataQuery,data)
        conn.commit()

def deleteDocData(pool,key):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlDeleteQuery = "delete from doctors where license_number=?"
        cur.execute(sqlDeleteQuery,(key,))
        conn.commit()

def addDeptData(pool,data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlQuery = "insert into departments (dept_id,dept_name,doc_count,nurse_count,staff_count,estd_date,status) values (?,?,?,?,?,?,?);"
        cur.execute(sqlQuery,data)
        conn.commit()

def updtDeptData(pool,data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlQuery = "update departments set dept_id=?,dept_name=?,doc_count=?,nurse_count=?,staff_count=?,estd_date=?,status=? where dept_id=?;"
        cur.execute(sqlQuery,data)
        conn.commit()

def deleteDeptData(pool,key):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlDeleteQuery = "delete from departments where dept_id=?"
        cur.execute(sqlDeleteQuery,(key,))
        conn.commit()

def showPatientsData(pool):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlQuery = "select * from patient"
        cur.execute(sqlQuery)
        data = cur.fetchall()
        return data
    
def updtPatientData(pool,data,flag):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlQuery = ""
        if flag==1:
            sqlQuery = "update patient set patient_id=?,patient_name=?,age_in_yr=?,gender=?,address=?,phone=? where patient_id=?;"
        elif flag==2:
            sqlQuery = "update patient set patient_id=?,patient_name=?,age_in_yr=?,gender=?,address=?,phone=?,email=? where patient_id=?;"
        elif flag==3:
            sqlQuery = "update patient set patient_id=?,patient_name=?,age_in_yr=?,gender=?,address=?,phone=?,health_insurance_number=? where patient_id=?;"
        elif flag==4:
            sqlQuery = "update patient set patient_id=?,patient_name=?,age_in_yr=?,gender=?,address=?,phone=?,email=?,health_insurance_number=? where patient_id=?;"
        cur.execute(sqlQuery,data)
        conn.commit()

def addPatientData(pool,data,flag):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlQuery = ""
        if flag==1:
            sqlQuery = "insert into patient (patient_id,patient_name,age_in_yr,gender,address,phone) values (?,?,?,?,?,?);"
        elif flag==2:
            sqlQuery = "insert into patient (patient_id,patient_name,age_in_yr,gender,address,phone,email) values (?,?,?,?,?,?,?);"
        elif flag==3:
            sqlQuery = "insert into patient (patient_id,patient_name,age_in_yr,gender,address,phone,health_insurance_number) values (?,?,?,?,?,?,?);"
        elif flag==4:
            sqlQuery = "insert into patient (patient_id,patient_name,age_in_yr,gender,address,phone,email,health_insurance_number) values (?,?,?,?,?,?,?,?);"
        cur.execute(sqlQuery,data)
        conn.commit()

def deletePatData(pool,key):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlDeleteQuery = "delete from patient where patient_id=?"
        cur.execute(sqlDeleteQuery,(key,))
        conn.commit()

def showEmergencyBedAllData(pool):
    with pool.connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM emergency_room;")
        data = cur.fetchall()
        return data

def updateEmergencyBedsData(pool,data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlQuery = "update emergency_room set total_beds=?,occupied_beds=?,vacant_beds=?;"
        cur.execute(sqlQuery,data)
        sqlClearRowsQuery="delete from emergency_room_beds;"
        cur.execute(sqlClearRowsQuery)
        for i in range(1,int(data[0])+1):
            sqlAddRowsQuery="insert into emergency_room_beds (bed_no,patient_name,reason,date,time,gender,age,address,phone) values (?,'NA','NA','NA','NA','NA','NA','NA','NA');"
            cur.execute(sqlAddRowsQuery,(str(i),))
        conn.commit()

def showAllMeds(pool):
    with pool.connection() as conn:
        cur = conn.cursor()
        cur.execute("select * from medicine;")
        data = cur.fetchall()
        return data
    
def addMedData(pool,data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlQuery = "insert into medicine (med_id,med_name,status,qty_avail,cost) values (?,?,?,?,?);"
        cur.execute(sqlQuery,data)
        conn.commit()

def updtMedData(pool,data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlQuery = "update medicine set med_id=?,med_name=?,status=?,qty_avail=?,cost=? where med_id=?;"
        cur.execute(sqlQuery,data)
        conn.commit()

def deleteMedData(pool,key):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlDeleteQuery = "delete from medicine where med_id=?;"
        cur.execute(sqlDeleteQuery,(key,))
        conn.commit()

def updtApptsData(pool, data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlInsertQuery = "update appointments set appnt_id=?, doc_name=?, patient_name=?, patient_phone=?, date=?, time=? where appnt_id=?;"
        cur.execute(sqlInsertQuery, data)
        conn.commit()

def addTestsData(pool,data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlQuery = "insert into tests (test_id,test_name,test_type,status,test_days,test_time,cost) values (?,?,?,?,?,?,?);"
        cur.execute(sqlQuery,data)
        conn.commit()

def updtTestsData(pool, data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlInsertQuery = "update tests set test_id=?,test_name=?,test_type=?,status=?,test_days=?,test_time=?,cost=? where test_id=?;"
        cur.execute(sqlInsertQuery, data)
        conn.commit()

def deleteTestsData(pool,key):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlDeleteQuery = "delete from tests where test_id=?;"
        cur.execute(sqlDeleteQuery,(key,))
        conn.commit()

def showAllNurses(pool):
    with pool.connection() as conn:
        cur = conn.cursor()
        cur.execute("select * from nurses;")
        data = cur.fetchall()
        return data
    
def addNursesData(pool,data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlQuery = "insert into nurses (lic_no,name,status,age,gender,exp,speciality,dept,fee,appnt_days,time_slot) values (?,?,?,?,?,?,?,?,?,?,?);"
        cur.execute(sqlQuery,data)
        conn.commit()

def updtNursesData(pool, data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlInsertQuery = "update nurses set lic_no=?,name=?,status=?,age=?,gender=?,exp=?,speciality=?,dept=?,fee=?,appnt_days=?,time_slot=? where lic_no=?;"
        cur.execute(sqlInsertQuery, data)
        conn.commit()

def deleteNursesData(pool,key):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlDeleteQuery = "delete from nurses where lic_no=?;"
        cur.execute(sqlDeleteQuery,(key,))
        conn.commit()

def showAllStaff(pool):
    with pool.connection() as conn:
        cur = conn.cursor()
        cur.execute("select * from staff;")
        data = cur.fetchall()
        return data

def addStaffData(pool,data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlQuery = "insert into staff (id,name,status,age,gender,occupation,fee,dept,time_slot,appnt_days) values (?,?,?,?,?,?,?,?,?,?);"
        cur.execute(sqlQuery,data)
        conn.commit()

def updtStaffData(pool, data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlInsertQuery = "update staff set id=?,name=?,status=?,age=?,gender=?,occupation=?,fee=?,dept=?,time_slot=?,appnt_days=? where id=?;"
        cur.execute(sqlInsertQuery, data)
        conn.commit()

def deleteStaffData(pool,key):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlDeleteQuery = "delete from staff where id=?;"
        cur.execute(sqlDeleteQuery,(key,))
        conn.commit()

def showAllPharmacists(pool):
    with pool.connection() as conn:
        cur = conn.cursor()
        cur.execute("select * from pharmacists;")
        data = cur.fetchall()
        return data
    
def addPharmacistsData(pool,data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlQuery = "insert into pharmacists (lic_no,name,status,age,gender,exp,speciality,dept,fee,appnt_days,time_slot) values (?,?,?,?,?,?,?,?,?,?,?);"
        cur.execute(sqlQuery,data)
        conn.commit()

def updtPharmacistsData(pool, data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlInsertQuery = "update pharmacists set lic_no=?,name=?,status=?,age=?,gender=?,exp=?,speciality=?,dept=?,fee=?,appnt_days=?,time_slot=? where lic_no=?;"
        cur.execute(sqlInsertQuery, data)
        conn.commit()

def deletePharmacistsData(pool,key):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlDeleteQuery = "delete from pharmacists where lic_no=?;"
        cur.execute(sqlDeleteQuery,(key,))
        conn.commit()

def showAllAccountants(pool):
    with pool.connection() as conn:
        cur = conn.cursor()
        cur.execute("select * from accountants;")
        data = cur.fetchall()
        return data
    
def addAccountantsData(pool,data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlQuery = "insert into accountants (accnt_id,accnt_name,status,age,gender,exp,fee,dept,time_slot,appnt_days) values (?,?,?,?,?,?,?,?,?,?);"
        cur.execute(sqlQuery,data)
        conn.commit()

def updtAccountantsData(pool, data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlInsertQuery = "update accountants set accnt_id=?,accnt_name=?,status=?,age=?,gender=?,exp=?,fee=?,dept=?,time_slot=?,appnt_days=? where accnt_id=?;"
        cur.execute(sqlInsertQuery, data)
        conn.commit()

def deleteAccountantsData(pool,key):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlDeleteQuery = "delete from accountants where accnt_id=?;"
        cur.execute(sqlDeleteQuery,(key,))
        conn.commit()

def showAllPayments(pool):
    with pool.connection() as conn:
        cur = conn.cursor()
        cur.execute("select * from payments;")
        data = cur.fetchall()
        return data
    
def updtPaymentsData(pool, data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlInsertQuery = "update payments set payment_id=?,invoice_id=?,no_of_items=?,total=?,date_of_issue=?,time_of_issue=? where payment_id=?;"
        cur.execute(sqlInsertQuery, data)
        conn.commit()

def deletePaymentsData(pool,key):
    with pool.connection() as conn:
        cur = conn.cursor()
        sqlDeleteQuery = "delete from payments where payment_id=?;"
        cur.execute(sqlDeleteQuery,(key,))
        conn.commit()

def addPaymentsOrder(pool,data):
    with pool.connection() as conn:
        cur = conn.cursor()
        sql_getPayId_Query = "SELECT MAX(payment_id) AS max_pay_id FROM payments;"
        cur.execute(sql_getPayId_Query)
        pay_id = cur.fetchone()[0]
        sql_getInvId_Query = "SELECT MAX(invoice_id) AS max_inv_id FROM payments;"
        cur.execute(sql_getInvId_Query)
        inv_id = cur.fetchone()[0]
        sqlAddQuery = "insert into payments (payment_id,invoice_id,no_of_items,total,date_of_issue,time_of_issue) values (?,?,?,?,?,?);"
        insertion_data = (str(pay_id+1),str(inv_id+1),data[0],data[1],data[2],data[3])
        cur.execute(sqlAddQuery,insertion_data)
        conn.commit()
