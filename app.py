from flask import Flask, render_template, request, redirect, session
import pymysql

app = Flask(__name__)
app.secret_key = 'secret_key'

# Fungsi koneksi database
def connect_db():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='password', #kosongkan punya kalian kalau ga ada password di phpmyadmin
        database='' #nama database yang kalian buat 
    )
    return conn

# Fungsi untuk memeriksa keberhasilan login
def check_login(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    # Query untuk memeriksa username dan password
    query = "SELECT * FROM Register WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    conn.close()

    return result

# Fungsi untuk menambahkan pengguna baru
def add_user(username, password, email):
    conn = connect_db()
    cursor = conn.cursor()

    # Query untuk menambahkan pengguna baru
    query = "INSERT INTO Register (username, password,email) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, password,email))
    conn.commit()

    conn.close()

#fungsi untuk menampilkan semua data pada tabel register
def get_all_register():
    conn = connect_db()
    cursor = conn.cursor()

    # query untuk menampilkan
    query = "SELECT * FROM Register"
    cursor.execute(query,)
    result = cursor.fetchall()

    conn.close()

    return result
# Fungsi dashboard (hanya dapat diakses setelah login)
@app.route('/')
def dashboard():
    # Periksa apakah pengguna telah login
    if 'username' in session:
        username = session['username']
        data = get_all_register()
        return render_template('index.html', username=username,data=data)
    else:
        return redirect('/login')

# Fungsi login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        result = check_login(username, password)

        # Memeriksa keberhasilan login
        if result:
            session['username'] = username
            return redirect('/')
        else:
            error = 'Username atau password salah'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Fungsi register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Memeriksa apakah username sudah digunakan
        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT * FROM Register WHERE username=%s"
        cursor.execute(query, username)
        result = cursor.fetchone()

        if result:
            error = 'Username sudah digunakan'
            return render_template('register.html', error=error)

        # Menambahkan pengguna baru
        add_user(username, password,email)
        session['username'] = username
        return redirect('/login')

    return render_template('register.html')

# Fungsi logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


if __name__ == '__main__':
    app.run()
