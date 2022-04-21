from flask_app import app
from flask import render_template,flash,redirect,request,session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

#  ====================================
#  Login and registration stuff
#  ====================================
@app.route('/register', methods=['POST'])
def register():
    is_valid = User.validate_user(request.form)
    if not is_valid:
        return redirect("/")
    new_user = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
    }
    id = User.add_user(new_user)
    if not id:
        flash("Email already taken.","register")
        return redirect('/')
    session['user_id'] = id
    return redirect("/dashboard")

@app.route('/login', methods=['POST'])
def login():
    user=User.get_by_email({"email": request.form["email"]})
    
    if not user:
        flash("*Invalid Credentials", "login")
        return redirect('/')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("*Invalid Credentials", "login")
        return redirect('/')

    session['user_id']=user.id
    return redirect ("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    flash("logged out!", "login")
    return redirect("/")

# ==========================================
#  Main page 
#  =========================================

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:    
        flash("Must be registered or logged in!", "register")
        return redirect("/")
    else:
        data = {
            "user_id": session["user_id"]
        }
        users = User.get_one(data)
        recipes = Recipe.get_recipes(data)
        return render_template("dashboard.html", users=users, recipes=recipes)

# ==========================================
#  Recipes page 
#  =========================================

@app.route("/recipe/new")
def new_form():
    if "user_id" not in session:   
        flash("Must be registered or logged in!", "register")
        return redirect("/")

    return render_template("add_recipe.html")

@app.route('/addrecipe', methods=["POST"])
def add_recipe():
    if Recipe.validate_recipe(request.form):
        data = {
            "name":request.form["name"],
            "under_30":request.form['under_30'],
            "description":request.form["description"],
            "instructions":request.form["instructions"],
            "created_at":request.form["created_at"],
            "user_id": session ['user_id']
            }
        Recipe.save_recipe(data)
        return redirect("/dashboard")
    else:
        return redirect("/recipe/new")

# ==========================================
#  Delete recipe
#  =========================================

@app.route("/delete/<int:id>")
def delete_recipe(id):
    data = {
        "id":id
    }
    Recipe.delete(data)
    return redirect("/dashboard")

# ==========================================
#  Edit recipe
#  =========================================

@app.route("/edit/<int:id>")
def edit_recipe(id):
    if "user_id" not in session:     
        flash("Must be registered or logged in!", "register")
        return redirect("/")
    data = {
        "id":id
    }
    recipe = Recipe.get_recipe(data)
    return render_template("edit_recipe.html",recipe=recipe)

@app.route("/update/<int:id>",methods=["POST"])
def update(id):
    if Recipe.validate_recipe(request.form):
        data = {
            "name":request.form["name"],
            "under_30": request.form['under_30'],
            "description":request.form["description"],
            "instructions":request.form["instructions"],
            "created_at":request.form["created_at"],
            "id":id
            }
        Recipe.update(data)
        return redirect("/dashboard")
    else:
        return redirect(f"/edit/{id}")

# ==========================================
#  View one recipe
# =========================================

@app.route("/show_recipe/<int:id>")
def show_recipe(id):
    if "user_id" not in session:   
        flash("Must be registered or logged in!", "register")
        return redirect("/")
    data = {
        "id":id,
        "user_id":session["user_id"]
    }
    user = User.get_one(data)
    recipe = Recipe.get_recipe(data)
    return render_template("recipe_info.html", user=user, recipe=recipe)