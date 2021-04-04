from flask import Flask, render_template, request, redirect, url_for, g
import pdb # this is python debugger
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/item/new", methods=["GET", "POST"])
def new_item():
    conn = get_db()
    c = conn.cursor()
    if request.method == "POST":
        # Process the form data
        c.execute("""INSERT INTO items
                    (title, description, price, image, category_id, subcategory_id)
                        VALUES (?,?,?,?,?,?)""",
                        (
                            request.form.get("title"),
                            request.form.get("description"),
                            float(request.form.get("price")),
                            "",
                            1,
                            1
                        )
        )
        conn.commit()
        print("Form data:")
        print("Title: {}, Description: {}".format(
            request.form.get("title"), request.form.get("description")
        ))
        # Redirect to some page 
        return redirect(url_for("home"))
    return render_template("new_item.html")
# opening of the connection this is flask appliictioan context
def get_db():
    db = getattr(g, '_database', None)  # see weather the database exists or not exists
    if db is None:
        db = g._databasev = sqlite3.connect("db/globomantics.db")
    return db  # here if the database is not found create else return the database

# closing of the connection use below function
@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

    
