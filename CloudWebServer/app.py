from flask import Flask, render_template, request
import mysql.connector
import json

app = Flask(__name__)


mysql_host = 'localhost'
mysql_user = 'ubuntu'
mysql_password = ''
mysql_database = 'assignment03'

# Flask 1: Meeting Room Dashboard

@app.route('/dashboard')
def meeting_room_dashboard():
    # Connect to MySQL database
    connection = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
        )
    cursor = connection.cursor()

    # Retrieve data from the admin_table
    cursor.execute('SELECT * FROM admin_table')
    rows = cursor.fetchall()

    # Close the database connection
    cursor.close()

    # Prepare the data for rendering in the HTML template
    rooms_data = []
    for row in rows:
        rooms = {
            'name': row[0],
            'status': row[1],
            'peopleCount': row[2],
            'noiseLevel': row[3],
            'temperature': row[4]
        }
        rooms_data.append(rooms)
    
    rooms_data_json = json.dumps(rooms_data)

    # Render the template with the data
    return render_template('dashboard.html', rooms_data_json=rooms_data_json)

# Flask 2: Booking Form

@app.route('/booking', methods=['GET', 'POST'])
def booking_form():
    if request.method == 'POST':
        capacity = request.form.get('capacity')
        start_time = request.form.get('start_time')
        student_ids = []

        if (capacity == "sana_4" or capacity == "andy_4"):
            for i in range(1, 5):
                student_id = request.form.get('student' + str(i))
                if student_id:
                    student_ids.append(student_id)
        elif (capacity == "kahlid_6"):
            for i in range(1, 7):
                student_id = request.form.get('student' + str(i))
                if student_id:
                    student_ids.append(student_id)
        elif (capacity == "mehrab_8"):
            for i in range(1, 9):
                student_id = request.form.get('student' + str(i))
                if student_id:
                    student_ids.append(student_id)
                
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database
        )
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM booking_v1 WHERE capacity = %s AND start_time = %s", (capacity, start_time))
        result = cursor.fetchone()
        
        if result is None:
            for i in range(0, len(student_ids)):
                insert_query = "INSERT INTO booking_v1 (rfid, capacity, start_time) VALUES (%s, %s, %s)"
                booking_data = (student_ids[i], capacity, start_time)
                cursor.execute(insert_query, booking_data)
                connection.commit()

            # Returning a simple message indicating successful submission
            return 'Form submitted successfully.'
        else:
            return 'The room is booked, try another time or room.'

    # Render the HTML template if it's a GET request
    return render_template('booking_index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)