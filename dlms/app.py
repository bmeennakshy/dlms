from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
db_config = {
    'user': 'root',
    'password': 'your password',
    'host': 'your localhost',
    'database': ' databasename',
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
                'username': username,
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
@app.route('/gardener', methods=['GET', 'POST'])
def gardener():
    application_details = None  # Initialize application details

    if request.method == 'POST':
        # Extract form data
        username = request.form['username']
        full_name = request.form['name']
        age = int(request.form['age'])
        phone = request.form['phone']
        location = request.form['location']
        website = request.form['website']
        daily_wages = float(request.form['daily_wages'])
        experience = int(request.form['experience']) # Specific to gardener

        # Insert into gardeners table
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(""" 
                INSERT INTO gardeners (username, full_name, age, phone, location, website, daily_wages, experience) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
            """, (username, full_name, age, phone, location, website, daily_wages, experience))
            conn.commit()
            flash('Gardener application submitted successfully!', 'success')

            # Store application details to pass to the template
            application_details = {
                'username': username,
                'name': full_name,
                'phone': phone,
                'location': location,
                'daily_wages': daily_wages,
                'experience': experience,
                'age': age,
                'website': website,
                
            }
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()

    # Fetch available gardeners for display
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gardeners")
    gardeners = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('gardener.html', gardeners=gardeners, application_details=application_details)

@app.route('/house_maid', methods=['GET', 'POST'])
def house_maid():
    application_details = None  # Initialize application details

    if request.method == 'POST':
        # Extract form data
        username = request.form['username']
        full_name = request.form['name']
        age = int(request.form['age'])
        phone = request.form['phone']
        location = request.form['location']
        website = request.form['website']
        
        # Get selected services
        services = request.form.getlist('services')
        num_services = len(services)  # Count selected services
        
        # Extract daily wages (base on number of services)
        base_wage = float(request.form['daily_wages'])
        daily_wages = base_wage * num_services  # Multiply base wage by number of services selected

        # Insert into house_maids table
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(""" 
                INSERT INTO house_maids (username, full_name, age, phone, location, website, services, daily_wages) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
            """, (username, full_name, age, phone, location, website, ','.join(services), daily_wages))
            conn.commit()
            flash('House Maid application submitted successfully!', 'success')

            # Store application details to pass to the template
            application_details = {
                'username': username,
                'name': full_name,
                'phone': phone,
                'location': location,
                'daily_wages': daily_wages,
                'age': age,
                'website': website,
                'services': services,
            }
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()

    # Fetch available house maids for display
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM house_maids")
    house_maids = cursor.fetchall()
    cursor.close()
    conn.close()
    # Handle search query for GET requests
    search_query = request.args.get('search')  # Get the search term from the URL
    conn = get_db_connection()
    cursor = conn.cursor()

    if search_query:
        # If a search query is provided, filter house maids by location
        cursor.execute("SELECT * FROM house_maids WHERE location LIKE %s", ('%' + search_query + '%',))
    else:
        # If no search query is provided, fetch all house maids
        cursor.execute("SELECT * FROM house_maids")

    house_maids = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('house_maid.html', house_maids=house_maids, application_details=application_details)

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if request.method == 'POST':
        # Get the current user's ID from the session
        user_id = session.get('user_id')  # Assuming you store the user ID in session

        # Get form data
        full_name = request.form['full_name']
        phone_number = request.form['phone_number']
        address = request.form['address']
        location = request.form['location']
        email = request.form['email']

        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Update the user's profile in the database
        update_query = """
            UPDATE users
            SET full_name = %s, phone_number = %s, address = %s, location = %s, email = %s
            WHERE id = %s  -- Use user ID for the update
        """
        cursor.execute(update_query, (full_name, phone_number, address, location, email, user_id))
        conn.commit()

        cursor.close()
        conn.close()

        flash('Profile updated successfully!', 'success')  # Flash success message
        return redirect(url_for('dashboard'))  # Redirect to the dashboard after updating

    # For GET request, fetch the current user's data to pre-fill the form
    user_id = session.get('user_id')
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("SELECT full_name, phone_number, address, location, email FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('update_profile.html', user_data=user_data)
@app.route('/delete_profile', methods=['POST'])
def delete_profile():
    user_id = session.get('user_id')  # Get the user ID from session
    if user_id:
        # Connect to the database and delete the user
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        connection.commit()
        cursor.close()
        connection.close()

        # Clear the session and redirect to the login page
        session.clear()
        return redirect(url_for('home'))
    else:
        flash('You are not logged in.')
        return redirect(url_for('home'))

    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  # Remove user from session
    return redirect(url_for('home'))  # Redirect to login page


if __name__ == '__main__':
    app.run(debug=True)
