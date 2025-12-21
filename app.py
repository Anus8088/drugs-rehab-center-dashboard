import mysql.connector
from flask import Flask, render_template, request, redirect, session, url_for, flash
from decimal import Decimal
import datetime
from db_config import get_db_connection

app = Flask(__name__)
app.secret_key = "supersecretkey_rehabcare_pro_2025"

# ==================== HELPER FUNCTIONS ====================

def get_branches():
    """Fetch all branches from database"""
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT branch_id, branch_name FROM branches ORDER BY branch_name")
        branches = cursor.fetchall()
        return branches
    except mysql.connector.Error as err:
        print(f"Error fetching branches: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

def authenticate_user(username, password):
    """Authenticate user from users table"""
    conn = get_db_connection()
    if not conn: return None
    
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT user_id, username, role FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        return user
    except mysql.connector.Error as err:
        print(f"Authentication Error: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

# ==================== AUTHENTICATION ROUTES ====================

@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect("/dashboard")
    
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = authenticate_user(username, password)
        
        if user:
            session["user"] = user['username']
            session["user_id"] = user['user_id']
            session["role"] = user['role']
            return redirect("/dashboard")
        else:
            error = "Invalid Username or Password"
    
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been successfully logged out.", "success")
    return redirect("/login")

# ==================== DASHBOARD ====================

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    
    conn = get_db_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return redirect("/logout")
    
    cursor = conn.cursor(dictionary=True)
    stats = {}
    recent_patients = []
    
    try:
        # Total admitted patients
        cursor.execute("SELECT COUNT(*) as total FROM patients WHERE status IN ('Admitted', 'Discharge-Planned')")
        stats['total_patients'] = cursor.fetchone()['total']
        
        # Total users (staff)
        cursor.execute("SELECT COUNT(*) as total FROM users")
        stats['total_staff'] = cursor.fetchone()['total']
        
        # Available beds calculation
        cursor.execute("SELECT SUM(bed_count) as total_beds FROM rooms")
        total_beds = cursor.fetchone()['total_beds'] or 0
        
        cursor.execute("SELECT COUNT(*) as occupied FROM room_allocation WHERE status = 'Active'")
        occupied_beds = cursor.fetchone()['occupied'] or 0
        stats['available_beds'] = total_beds - occupied_beds
        
        # Pending bills
        cursor.execute("SELECT COUNT(*) as pending FROM billing WHERE status IN ('Pending', 'Overdue')")
        stats['pending_bills'] = cursor.fetchone()['pending']
        
        # Recent patients
        cursor.execute("""
            SELECT p.patient_id, p.patient_code, p.full_name, p.admission_date, 
                   p.status, b.branch_name
            FROM patients p
            JOIN branches b ON p.branch_id = b.branch_id
            ORDER BY p.admission_date DESC
            LIMIT 10
        """)
        recent_patients = cursor.fetchall()
        
    except mysql.connector.Error as err:
        flash(f"Error fetching dashboard data: {err}", "danger")
    finally:
        cursor.close()
        conn.close()
    
    return render_template("dashboard.html", patients=recent_patients, stats=stats)

# ==================== PATIENT MANAGEMENT ====================

@app.route("/patients")
def patients_list():
    if "user" not in session:
        return redirect("/login")
    
    conn = get_db_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return redirect("/dashboard")
    
    cursor = conn.cursor(dictionary=True)
    patients_data = []
    
    try:
        query = """
            SELECT p.patient_id as PATIENT_ID, p.patient_code as PATIENT_CODE, 
                   p.full_name as FULL_NAME, p.admission_date as ADMISSION_DATE,
                   p.status as STATUS, b.branch_name as BRANCH_NAME
            FROM patients p
            JOIN branches b ON p.branch_id = b.branch_id
            ORDER BY p.admission_date DESC
        """
        cursor.execute(query)
        patients_data = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error fetching patients: {err}", "danger")
    finally:
        cursor.close()
        conn.close()
    
    return render_template("patients_list.html", patients=patients_data)

@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    if "user" not in session:
        return redirect("/login")
    
    branches = get_branches()
    today = datetime.date.today().strftime('%Y-%m-%d')
    
    if request.method == "POST":
        conn = get_db_connection()
        if not conn:
            flash("Database connection error.", "danger")
            return redirect(request.url)
        
        cursor = conn.cursor()
        
        try:
            conn.start_transaction()
            
            # Generate patient code based on branch
            branch_id = request.form['branch_id']
            cursor.execute("SELECT branch_name FROM branches WHERE branch_id = %s", (branch_id,))
            branch = cursor.fetchone()
            
            # Create patient code: P-{BRANCH_CODE}-{NUMBER}
            branch_code = branch[0][:2].upper() if branch else "XX"
            cursor.execute("SELECT COUNT(*) FROM patients WHERE branch_id = %s", (branch_id,))
            count = cursor.fetchone()[0] + 1
            patient_code = f"P-{branch_code}-{count:03d}"
            
            # Calculate expected discharge date (3 months from admission)
            admission_date = request.form['admission_date']
            admission_dt = datetime.datetime.strptime(admission_date, '%Y-%m-%d')
            expected_discharge = admission_dt + datetime.timedelta(days=90)
            
            # Insert patient
            patient_sql = """
                INSERT INTO patients (branch_id, patient_code, full_name, dob, gender, 
                                     admission_date, expected_discharge_date, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'Admitted')
            """
            cursor.execute(patient_sql, (
                branch_id, patient_code, request.form['full_name'], request.form['dob'],
                request.form['gender'], admission_date, expected_discharge.date()
            ))
            patient_id = cursor.lastrowid
            
            # Insert medical info
            medical_sql = """
                INSERT INTO patient_medical_info (patient_id, primary_addiction, duration_of_use_months,
                                                  addiction_level, diseases, allergies, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(medical_sql, (
                patient_id, request.form['primary_addiction'], 
                request.form.get('duration_months', 0),
                request.form.get('addiction_level', 'Low'),
                request.form.get('diseases', 'None'),
                request.form.get('allergies', 'None'),
                request.form.get('notes', '')
            ))
            
            # Insert guardian
            guardian_sql = """
                INSERT INTO guardians (patient_id, name, relation, phone, address, emergency_contact)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(guardian_sql, (
                patient_id, request.form['guardian_name'], request.form['guardian_relation'],
                request.form['guardian_phone'], request.form.get('guardian_address', ''),
                1  # emergency_contact = true
            ))
            
            conn.commit()
            flash(f"Patient {patient_code} added successfully! Please allocate a room.", "success")
            return redirect(url_for('rooms_allocation', new_patient_id=patient_id))
            
        except mysql.connector.Error as err:
            conn.rollback()
            flash(f"Error adding patient: {err}", "danger")
        finally:
            cursor.close()
            conn.close()
    
    return render_template("add_patient.html", branches=branches, today=today)

@app.route("/view_patient/<int:patient_id>")
def view_patient(patient_id):
    if "user" not in session:
        return redirect("/login")
    
    conn = get_db_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return redirect("/dashboard")
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get patient details with all related info
        patient_query = """
            SELECT p.*, b.branch_name, pm.primary_addiction, pm.duration_of_use_months,
                   pm.addiction_level, pm.diseases, pm.allergies, pm.notes as medical_notes,
                   g.name as guardian_name, g.relation as guardian_relation, 
                   g.phone as guardian_phone, g.address as guardian_address,
                   r.room_number
            FROM patients p
            JOIN branches b ON p.branch_id = b.branch_id
            LEFT JOIN patient_medical_info pm ON p.patient_id = pm.patient_id
            LEFT JOIN guardians g ON p.patient_id = g.patient_id AND g.emergency_contact = 1
            LEFT JOIN room_allocation ra ON p.patient_id = ra.patient_id AND ra.status = 'Active'
            LEFT JOIN rooms r ON ra.room_id = r.room_id
            WHERE p.patient_id = %s
        """
        cursor.execute(patient_query, (patient_id,))
        patient = cursor.fetchone()
        
        if not patient:
            flash("Patient not found.", "danger")
            return redirect("/patients")
        
        # Get billing history
        cursor.execute("""
            SELECT bill_id, bill_date, amount_due, amount_paid, due_amount, status
            FROM billing WHERE patient_id = %s ORDER BY bill_date DESC
        """, (patient_id,))
        invoices = cursor.fetchall()
        
        # Get medication records
        cursor.execute("""
            SELECT mr.admin_date, mr.admin_time, mr.dosage, mr.administered_by,
                   m.name as medicine_name
            FROM medication_records mr
            JOIN medicines m ON mr.medicine_id = m.medicine_id
            WHERE mr.patient_id = %s
            ORDER BY mr.admin_date DESC, mr.admin_time DESC
            LIMIT 20
        """, (patient_id,))
        medicine_records = cursor.fetchall()
        
    except mysql.connector.Error as err:
        flash(f"Error fetching patient data: {err}", "danger")
        return redirect("/patients")
    finally:
        cursor.close()
        conn.close()
    
    return render_template("view_patient.html", patient=patient, invoices=invoices, 
                         medicine_records=medicine_records)

@app.route("/edit_patient/<int:patient_id>", methods=["GET", "POST"])
def edit_patient(patient_id):
    if "user" not in session:
        return redirect("/login")
    
    branches = get_branches()
    conn = get_db_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return redirect("/dashboard")
    
    cursor = conn.cursor(dictionary=True)
    
    if request.method == "POST":
        try:
            conn.start_transaction()
            
            # Update patient
            update_patient = """
                UPDATE patients SET full_name=%s, dob=%s, gender=%s, status=%s,
                                   expected_discharge_date=%s
                WHERE patient_id=%s
            """
            cursor.execute(update_patient, (
                request.form['full_name'], request.form['dob'], request.form['gender'],
                request.form['status'], request.form['expected_discharge'], patient_id
            ))
            
            # Update medical info
            cursor.execute("""
                UPDATE patient_medical_info 
                SET primary_addiction=%s, duration_of_use_months=%s, addiction_level=%s,
                    diseases=%s, allergies=%s, notes=%s
                WHERE patient_id=%s
            """, (
                request.form['primary_addiction'], request.form['duration_months'],
                request.form['addiction_level'], request.form.get('diseases', 'None'),
                request.form.get('allergies', 'None'), request.form.get('notes', ''),
                patient_id
            ))
            
            # Update guardian
            cursor.execute("""
                UPDATE guardians SET name=%s, relation=%s, phone=%s, address=%s
                WHERE patient_id=%s AND emergency_contact = 1
            """, (
                request.form['guardian_name'], request.form['guardian_relation'],
                request.form['guardian_phone'], request.form.get('guardian_address', ''),
                patient_id
            ))
            
            conn.commit()
            flash("Patient record updated successfully.", "success")
            return redirect(url_for('view_patient', patient_id=patient_id))
            
        except mysql.connector.Error as err:
            conn.rollback()
            flash(f"Error updating patient: {err}", "danger")
        finally:
            cursor.close()
            conn.close()
    
    # GET request - fetch patient data
    try:
        cursor.execute("""
            SELECT p.*, pm.primary_addiction, pm.duration_of_use_months, pm.addiction_level,
                   pm.diseases, pm.allergies, pm.notes, g.name as guardian_name,
                   g.relation as guardian_relation, g.phone as guardian_phone,
                   g.address as guardian_address
            FROM patients p
            LEFT JOIN patient_medical_info pm ON p.patient_id = pm.patient_id
            LEFT JOIN guardians g ON p.patient_id = g.patient_id AND g.emergency_contact = 1
            WHERE p.patient_id = %s
        """, (patient_id,))
        patient = cursor.fetchone()
    except mysql.connector.Error as err:
        flash(f"Error fetching patient: {err}", "danger")
        patient = None
    finally:
        cursor.close()
        conn.close()
    
    if not patient:
        flash("Patient not found.", "danger")
        return redirect("/patients")
    
    return render_template("edit_patient.html", patient=patient, branches=branches)

# ==================== ROOM MANAGEMENT ====================


@app.route("/rooms")
def rooms_allocation():
    if "user" not in session:
        return redirect("/login")
    
    new_patient_id = request.args.get('new_patient_id')
    today = datetime.date.today().strftime('%Y-%m-%d')
    
    conn = get_db_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return redirect("/dashboard")
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get all rooms with occupancy info
        rooms_query = """
            SELECT r.room_id, r.room_number, r.ward_type, r.bed_count as capacity,
                   r.branch_id, b.branch_name,
                   COUNT(ra.allocation_id) as occupied,
                   CASE 
                       WHEN COUNT(ra.allocation_id) >= r.bed_count THEN 'Full'
                       WHEN COUNT(ra.allocation_id) = 0 THEN 'Available'
                       ELSE 'Partial'
                   END as status
            FROM rooms r
            JOIN branches b ON r.branch_id = b.branch_id
            LEFT JOIN room_allocation ra ON r.room_id = ra.room_id AND ra.status = 'Active'
            GROUP BY r.room_id, r.room_number, r.ward_type, r.bed_count, r.branch_id, b.branch_name
            ORDER BY b.branch_name, r.room_number
        """
        cursor.execute(rooms_query)
        all_rooms = cursor.fetchall()
        
        # Get patients for allocation with their branch info
        patients_query = """
            SELECT p.patient_id, p.full_name, p.patient_code, p.branch_id,
                   b.branch_name
            FROM patients p
            JOIN branches b ON p.branch_id = b.branch_id
            LEFT JOIN room_allocation ra ON p.patient_id = ra.patient_id AND ra.status = 'Active'
            WHERE p.status = 'Admitted' AND ra.allocation_id IS NULL
            ORDER BY p.full_name
        """
        cursor.execute(patients_query)
        patients_for_allocation = cursor.fetchall()
        
        # Get occupied patients with room info
        occupied_query = """
            SELECT p.patient_id, p.full_name, p.patient_code, r.room_number,
                   DATE_FORMAT(ra.allocation_date, '%Y-%m-%d') as allocation_date
            FROM room_allocation ra
            JOIN patients p ON ra.patient_id = p.patient_id
            JOIN rooms r ON ra.room_id = r.room_id
            WHERE ra.status = 'Active'
            ORDER BY ra.allocation_date DESC
        """
        cursor.execute(occupied_query)
        occupied_patients = cursor.fetchall()
        
    except mysql.connector.Error as err:
        flash(f"Error fetching room data: {err}", "danger")
        all_rooms = []
        patients_for_allocation = []
        occupied_patients = []
    finally:
        cursor.close()
        conn.close()
    
    return render_template("rooms_allocation.html", all_rooms=all_rooms,
                         patients_for_allocation=patients_for_allocation,
                         occupied_patients=occupied_patients,
                         new_patient_id=new_patient_id, today=today)

@app.route("/allocate_room", methods=["POST"])
def allocate_room():
    if "user" not in session:
        return redirect("/login")
    
    patient_id = request.form.get('patient_id')
    room_id = request.form.get('room_id')
    allocation_date = request.form.get('allocation_date')
    
    conn = get_db_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return redirect("/rooms")
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        conn.start_transaction()
        
        # Check if room has available bed
        cursor.execute("""
            SELECT r.bed_count, COUNT(ra.allocation_id) as occupied
            FROM rooms r
            LEFT JOIN room_allocation ra ON r.room_id = ra.room_id AND ra.status = 'Active'
            WHERE r.room_id = %s
            GROUP BY r.room_id, r.bed_count
        """, (room_id,))
        room_info = cursor.fetchone()
        
        if room_info and room_info['occupied'] >= room_info['bed_count']:
            flash("Room is full. Please select another room.", "danger")
            return redirect("/rooms")
        
        # Deactivate any existing allocation for this patient
        cursor.execute("""
            UPDATE room_allocation SET status = 'Released', release_date = CURDATE()
            WHERE patient_id = %s AND status = 'Active'
        """, (patient_id,))
        
        # Get next bed number
        cursor.execute("""
            SELECT COALESCE(MAX(bed_number), 0) + 1 as next_bed
            FROM room_allocation
            WHERE room_id = %s AND status = 'Active'
        """, (room_id,))
        next_bed = cursor.fetchone()['next_bed']
        
        # Allocate new room
        cursor.execute("""
            INSERT INTO room_allocation (room_id, patient_id, bed_number, 
                                        allocation_date, status)
            VALUES (%s, %s, %s, %s, 'Active')
        """, (room_id, patient_id, next_bed, allocation_date))
        
        conn.commit()
        flash("Room allocated successfully!", "success")
        
    except mysql.connector.Error as err:
        conn.rollback()
        flash(f"Error allocating room: {err}", "danger")
    finally:
        cursor.close()
        conn.close()
    
    return redirect("/rooms")

@app.route("/deallocate_room/<int:patient_id>")
def deallocate_room(patient_id):
    if "user" not in session:
        return redirect("/login")
    
    conn = get_db_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return redirect("/rooms")
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE room_allocation 
            SET status = 'Released', release_date = CURDATE()
            WHERE patient_id = %s AND status = 'Active'
        """, (patient_id,))
        conn.commit()
        flash("Room deallocated successfully.", "success")
    except mysql.connector.Error as err:
        flash(f"Error deallocating room: {err}", "danger")
    finally:
        cursor.close()
        conn.close()
    
    return redirect("/rooms")

# ==================== BILLING MANAGEMENT ====================

@app.route("/billing")
def billing_management():
    if "user" not in session:
        return redirect("/login")
    
    conn = get_db_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return redirect("/dashboard")
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get all billing records with proper formatting
        cursor.execute("""
            SELECT b.bill_id, DATE_FORMAT(b.bill_date, '%Y-%m-%d') as bill_date, 
                   b.amount_due, b.amount_paid, b.due_amount,
                   b.status, p.full_name, p.patient_id, b.branch_id
            FROM billing b
            JOIN patients p ON b.patient_id = p.patient_id
            ORDER BY b.bill_date DESC
        """)
        patients = cursor.fetchall()
        
        # Get recent payments (last 30 days)
        cursor.execute("""
            SELECT DATE_FORMAT(py.payment_date, '%Y-%m-%d') as date, 
                   p.full_name as patient, 
                   py.amount, py.payment_method as type
            FROM payments py
            JOIN billing b ON py.bill_id = b.bill_id
            JOIN patients p ON b.patient_id = p.patient_id
            WHERE py.payment_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            ORDER BY py.payment_date DESC
            LIMIT 20
        """)
        payments = cursor.fetchall()
        
    except mysql.connector.Error as err:
        flash(f"Error fetching billing data: {err}", "danger")
        patients = []
        payments = []
    finally:
        cursor.close()
        conn.close()
    
    return render_template("billing_management.html", patients=patients, payments=payments)

@app.route("/generate_invoice", methods=["GET", "POST"])
def generate_invoice():
    if "user" not in session:
        return redirect("/login")

    patient_id = request.args.get('patient_id')
    today = datetime.date.today().strftime('%Y-%m-%d')

    conn = get_db_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return redirect("/billing")

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT patient_id AS PATIENT_ID, full_name AS FULL_NAME
            FROM patients
            WHERE status IN ('Admitted', 'Discharge-Planned')
            ORDER BY full_name
        """)
        patients = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error fetching patients: {err}", "danger")
        patients = []

    if request.method == "POST":
        try:
            # YAHAN FIELD NAMES MATCH KARO HTML SE
            patient_id_form = request.form.get('patient_id')
            bill_date = request.form.get('bill_date')
            amount_due = request.form.get('amount_due')  # ← HTML mein name="amount_due"
            
            if not all([patient_id_form, bill_date, amount_due]):
                flash("Please fill all required fields.", "danger")
                return redirect(request.url)
            
            amount_due_float = float(amount_due)

            # Get patient's branch
            cursor.execute(
                "SELECT branch_id FROM patients WHERE patient_id = %s",
                (patient_id_form,)
            )
            branch_result = cursor.fetchone()

            if not branch_result:
                flash("Patient not found.", "danger")
                return redirect("/billing")

            branch_id = branch_result['branch_id']

            # Insert billing record
            cursor.execute("""
                INSERT INTO billing (
                    patient_id, branch_id, bill_date,
                    amount_due, amount_paid, due_amount, status
                )
                VALUES (%s, %s, %s, %s, 0, %s, 'Pending')
            """, (
                patient_id_form,
                branch_id,
                bill_date,
                amount_due_float,
                amount_due_float
            ))

            bill_id = cursor.lastrowid
            conn.commit()

            flash("Invoice generated successfully!", "success")
            return redirect(url_for('view_bill', bill_id=bill_id))

        except ValueError:
            flash("Invalid amount. Please enter a valid number.", "danger")
        except mysql.connector.Error as err:
            conn.rollback()
            flash(f"Error generating invoice: {err}", "danger")
        finally:
            cursor.close()
            conn.close()

    cursor.close()
    conn.close()
    return render_template(
        "generate_invoice.html",
        patients=patients,
        patient_id=patient_id,
        today=today
    )
    
@app.route("/record_payment/<int:bill_id>", methods=["GET", "POST"])
def record_payment(bill_id):
    if "user" not in session:
        return redirect("/login")
    
    today = datetime.date.today().strftime('%Y-%m-%d')
    
    conn = get_db_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return redirect("/billing")
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT b.bill_id, b.amount_due as bill_amount, 
                   b.due_amount as pending_amount, p.full_name
            FROM billing b
            JOIN patients p ON b.patient_id = p.patient_id
            WHERE b.bill_id = %s
        """, (bill_id,))
        invoice = cursor.fetchone()
        
        if not invoice:
            flash("Invoice not found.", "danger")
            return redirect("/billing")
        
        invoice['invoice_number'] = f"INV-{bill_id:06d}"
        
    except mysql.connector.Error as err:
        flash(f"Error fetching invoice: {err}", "danger")
        return redirect("/billing")
    
    if request.method == "POST":
        try:
            amount_paid = Decimal(request.form['amount_paid'])
            
            if amount_paid <= 0 or amount_paid > invoice['pending_amount']:
                flash("Invalid payment amount.", "danger")
                return redirect(request.url)
            
            cursor.execute("""
                INSERT INTO payments (bill_id, payment_date, amount,
                                      payment_method, recorded_by)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                bill_id,
                request.form['payment_date'],
                amount_paid,
                request.form['payment_method'],
                session['user_id']
            ))
            
            new_due = invoice['pending_amount'] - amount_paid
            new_status = 'Paid' if new_due <= 0 else 'Pending'
            
            cursor.execute("""
                UPDATE billing 
                SET amount_paid = amount_paid + %s,
                    due_amount = %s,
                    status = %s
                WHERE bill_id = %s
            """, (amount_paid, new_due, new_status, bill_id))
            
            conn.commit()
            flash(f"Payment of PKR {amount_paid} recorded successfully!", "success")
            return redirect(url_for('view_bill', bill_id=bill_id))
            
        except mysql.connector.Error as err:
            conn.rollback()
            flash(f"Error recording payment: {err}", "danger")
        finally:
            cursor.close()
            conn.close()
    
    cursor.close()
    conn.close()
    return render_template(
        "record_payment.html",
        invoice=invoice,
        today=today
    )
@app.route("/view_bill/<int:bill_id>")
def view_bill(bill_id):
    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return redirect("/billing")

    cursor = conn.cursor(dictionary=True)

    try:
        # Get bill details
        cursor.execute("""
            SELECT b.bill_id as BILL_ID,
                   DATE_FORMAT(b.bill_date,'%Y-%m-%d') as ISSUE_DATE,
                   DATE_FORMAT(DATE_ADD(b.bill_date, INTERVAL 30 DAY),'%Y-%m-%d') as DUE_DATE,
                   b.amount_due as BILL_AMOUNT,
                   b.amount_paid as AMOUNT_PAID,
                   b.due_amount as PENDING_AMOUNT,
                   b.status as STATUS,
                   p.full_name as FULL_NAME,
                   br.branch_name as BRANCH_NAME
            FROM billing b
            JOIN patients p ON b.patient_id = p.patient_id
            JOIN branches br ON b.branch_id = br.branch_id
            WHERE b.bill_id = %s
        """, (bill_id,))

        bill = cursor.fetchone()

        if not bill:
            flash("Invoice not found.", "danger")
            return redirect("/billing")

        bill['INVOICE_NUMBER'] = f"INV-{bill['BILL_ID']:06d}"
        bill['DESCRIPTION'] = "Rehabilitation Services"

        # ✅ FIX: Get payment history with UPPERCASE column names
        cursor.execute("""
            SELECT DATE_FORMAT(py.payment_date, '%Y-%m-%d') as PAYMENT_DATE,
                   py.amount as AMOUNT_PAID,
                   py.payment_method as PAYMENT_METHOD,
                   u.username as RECORDED_BY
            FROM payments py
            JOIN users u ON py.recorded_by = u.user_id
            WHERE py.bill_id = %s
            ORDER BY py.payment_date DESC
        """, (bill_id,))
        payments = cursor.fetchall()
        
        # ✅ DEBUG: Check if payments are being fetched
        print(f"=== PAYMENTS FOR BILL {bill_id} ===")
        print(f"Found {len(payments)} payments")
        for p in payments:
            print(p)
        print("===================================")

    except mysql.connector.Error as err:
        flash(f"Error loading invoice: {err}", "danger")
        return redirect("/billing")
    finally:
        cursor.close()
        conn.close()

    return render_template("view_bill.html", bill=bill, payments=payments)


# ==================== MEDICINE MANAGEMENT ====================

@app.route("/medicine_history")
def medicine_history():
    if "user" not in session:
        return redirect("/login")
    
    conn = get_db_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return redirect("/dashboard")
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get inventory with uppercase aliases for template
        cursor.execute("""
            SELECT medicine_id as MEDICINE_ID, 
                   name as MEDICINE_NAME, 
                   dosage_form as UNIT, 
                   stock_quantity as CURRENT_STOCK
            FROM medicines
            ORDER BY name
        """)
        inventory = cursor.fetchall()
        
        # Get recent medication records with uppercase aliases
        cursor.execute("""
            SELECT mr.record_id as RECORD_ID, 
                   DATE_FORMAT(mr.admin_date, '%Y-%m-%d') as ADMIN_DATE, 
                   DATE_FORMAT(mr.admin_time, '%H:%i') as ADMIN_TIME, 
                   mr.dosage as DOSAGE,
                   mr.administered_by as ADMINISTERED_BY, 
                   m.name as MEDICINE_NAME,
                   p.patient_id as PATIENT_ID, 
                   p.full_name as FULL_NAME
            FROM medication_records mr
            JOIN medicines m ON mr.medicine_id = m.medicine_id
            JOIN patients p ON mr.patient_id = p.patient_id
            ORDER BY mr.admin_date DESC, mr.admin_time DESC
            LIMIT 50
        """)
        records = cursor.fetchall()
        
    except mysql.connector.Error as err:
        flash(f"Error fetching medicine data: {err}", "danger")
        inventory = []
        records = []
    finally:
        cursor.close()
        conn.close()
    
    return render_template("medicine_history.html", inventory=inventory, records=records)

@app.route("/add_medicine", methods=["GET", "POST"])
def add_medicine():
    if "user" not in session:
        return redirect("/login")
    
    med_id = request.args.get('med_id')
    
    conn = get_db_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return redirect("/medicine_history")
    
    cursor = conn.cursor(dictionary=True)
    medicine = None
    
    try:
        if med_id:
            cursor.execute("""
                SELECT medicine_id as MEDICINE_ID, 
                       name as MEDICINE_NAME, 
                       dosage_form as UNIT,
                       stock_quantity as CURRENT_STOCK
                FROM medicines WHERE medicine_id = %s
            """, (med_id,))
            medicine = cursor.fetchone()
    except mysql.connector.Error as err:
        flash(f"Error fetching medicine: {err}", "danger")
    
    if request.method == "POST":
        try:
            stock_qty = int(request.form['stock_quantity'])
            
            if request.form.get('med_id'):  # Restock existing medicine
                cursor.execute("""
                    UPDATE medicines 
                    SET stock_quantity = stock_quantity + %s,
                        supplier_batch = %s
                    WHERE medicine_id = %s
                """, (stock_qty, request.form.get('supplier', ''), request.form['med_id']))
                flash("Medicine restocked successfully!", "success")
            else:  # Add new medicine
                cursor.execute("""
                    INSERT INTO medicines (name, dosage_form, stock_quantity, supplier_batch)
                    VALUES (%s, %s, %s, %s)
                """, (
                    request.form['medicine_name'], request.form['unit'],
                    stock_qty, request.form.get('supplier', '')
                ))
                flash("New medicine added successfully!", "success")
            
            conn.commit()
            return redirect("/medicine_history")
            
        except mysql.connector.Error as err:
            flash(f"Error saving medicine: {err}", "danger")
        finally:
            cursor.close()
            conn.close()
    
    cursor.close()
    conn.close()
    return render_template("add_medicine.html", medicine=medicine)

@app.route("/record_dose", methods=["GET", "POST"])
def record_dose():
    if "user" not in session:
        return redirect("/login")
    
    patient_id = request.args.get('patient_id')
    
    conn = get_db_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return redirect("/medicine_history")
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT patient_id as PATIENT_ID, 
                   full_name as FULL_NAME, 
                   patient_code as PATIENT_CODE
            FROM patients 
            WHERE status = 'Admitted'
            ORDER BY full_name
        """)
        patients = cursor.fetchall()
        
        cursor.execute("""
            SELECT medicine_id as MEDICINE_ID, 
                   name as MEDICINE_NAME, 
                   stock_quantity as CURRENT_STOCK
            FROM medicines 
            WHERE stock_quantity > 0
            ORDER BY name
        """)
        medicine = cursor.fetchall()
        
    except mysql.connector.Error as err:
        flash(f"Error fetching data: {err}", "danger")
        patients = []
        medicine = []
    
    if request.method == "POST":
        try:
            
            cursor.execute("""
                SELECT stock_quantity 
                FROM medicines 
                WHERE medicine_id = %s
            """, (request.form['medicine_id'],))
            stock = cursor.fetchone()
            
            if not stock or stock['stock_quantity'] < 1:
                flash("Insufficient stock! Please restock this medicine.", "danger")
                return redirect(request.url)
            
            cursor.execute("""
                INSERT INTO medication_records 
                (patient_id, medicine_id, dosage, administered_by, admin_date, admin_time)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                request.form['patient_id'],
                request.form['medicine_id'],
                request.form['dosage'],
                request.form['administered_by'],
                request.form['admin_date'],
                request.form['admin_time']
            ))
            
            cursor.execute("""
                UPDATE medicines 
                SET stock_quantity = stock_quantity - 1
                WHERE medicine_id = %s
            """, (request.form['medicine_id'],))
            
            conn.commit()
            flash("Medication dose recorded successfully!", "success")
            return redirect(url_for('view_patient', patient_id=request.form['patient_id']))
            
        except mysql.connector.Error as err:
            conn.rollback()
            flash(f"Error recording dose: {err}", "danger")
        finally:
            cursor.close()
            conn.close()
    
    cursor.close()
    conn.close()
    return render_template(
        "record_dose.html",
        patients=patients,
        medicine=medicine,
        patient_id=patient_id
    )

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(e):
    return "<h1>404 - Page Not Found</h1><p>The page you're looking for doesn't exist.</p>", 404

@app.errorhandler(500)
def server_error(e):
    return "<h1>500 - Server Error</h1><p>Something went wrong on our end.</p>", 500

# ==================== RUN APPLICATION ====================

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
