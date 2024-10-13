from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
db_config = {
    'user': 'root',
    'password': 'password123@',
    'host': 'localhost',
    'database': 'your_database',
}

# Connect to the database
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user_id'] = user[0]  # Assuming user ID is the first column
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid credentials, please try again.')
        return redirect(url_for('home'))

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    full_name = request.form['name']
    phone_number = request.form['phone']
    address = request.form['address']
    location = request.form['location']
    email = request.form['email']
    password = request.form['password']
    looking_for_job = request.form.get('looking_for_job') is not None

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, full_name, phone_number, address, location, email, password, looking_for_job) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                       (username, full_name, phone_number, address, location, email, password, looking_for_job))
        conn.commit()
        flash('Account created successfully! Please log in.')
    except mysql.connector.Error as err:
        flash('Error: {}'.format(err))
    finally:
        conn.close()

    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    return render_template('dashboard.html')

@app.route('/coconut_tree_climber', methods=['GET', 'POST'])
def coconut_tree_climber():
    application_details = None  # Initialize application details
    climbers = []  # Initialize climbers list

    if request.method == 'POST':
        # Extract form data
        username = request.form['username']
        full_name = request.form['name']
        age = int(request.form['age'])
        phone = request.form['phone']
        location = request.form['location']
        website = request.form['website']
        daily_wages = float(request.form['daily_wages'])
        experience = int(request.form['experience'])
        trees_climbed = int(request.form['trees_climbed'])

        # Insert into coconut_climbers table
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(""" 
                INSERT INTO coconut_climbers (username, full_name, age, phone, location, website, daily_wages, experience, trees_climbed) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
            """, (username, full_name, age, phone, location, website, daily_wages, experience, trees_climbed))
            conn.commit()
            flash('Application submitted successfully!', 'success')

            # Store application details to pass to the template
            application_details = {
                'name': full_name,
                'phone': phone,
                'location': location,
                'daily_wages': daily_wages,
                'experience': experience,
                'age': age,
                'website': website,
                'trees_climbed': trees_climbed
            }
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()

    # Fetch available coconut climbers for display
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM coconut_climbers")
    climbers = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('coconut_tree_climbers.html', climbers=climbers, application_details=application_details)


    # If it's a GET request, fetch available coconut climbers for display
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM coconut_climbers")
    climbers = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('coconut_tree_climbers.html', climbers=climbers, application_details=application_details)


    # If it's a GET request, fetch available coconut climbers for display
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM coconut_climbers")
    climbers = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('coconut_tree_climbers.html', climbers=climbers, application_details=application_details)
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
