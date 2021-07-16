from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegisterForm, AddProduct, ImageForm
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_gravatar import Gravatar
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = "hfiudhriusrhysiud"

bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///shop.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
ckeditor = CKEditor(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    phone_num = db.Column(db.String(250), nullable=False)

    added_products = relationship("Product", secondary="cart")


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)

    cat_product = relationship('Product', back_populates="cat_name")


class Seller(db.Model):
    __tablename__ = "seller"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = email = db.Column(db.String(250), unique=True, nullable=False)

    seller_product = relationship("Product", back_populates="seller_name")


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),unique=True ,nullable=False)
    price = db.Column(db.Float, nullable=False)
    desc = db.Column(db.Text ,nullable=False,)
    XL_size = db.Column(db.Integer, nullable=True)
    L_size = db.Column(db.Integer, nullable=True)
    M_size = db.Column(db.Integer,nullable=True)
    S_size = db.Column(db.Integer, nullable=True)
    one_size = db.Column(db.Integer, nullable=True)
    front_img = db.Column(db.String(250),nullable=False )
    back_img = db.Column(db.String(250), nullable=False)


    #one-to-many relationship
    # between seller and products
    #assuming only one seller will provide a particular product
    #product.seller_name = seller of that product
    seller_id = db.Column(db.Integer, db.ForeignKey("seller.id"))
    seller_name = relationship("Seller", back_populates="seller_product")


    #
    cat_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    cat_name = relationship("Category", back_populates="cat_product")

    users = relationship("User", secondary="cart")

class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    user = relationship('User', backref="orders")
    product = relationship('Product', backref="orders")


db.create_all()




@app.route('/')
def home():
    return render_template('index.html', current_user=current_user)


@app.route('/contact')
def contact():
    return render_template('contact.html', current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = User.query.filter_by(email=form.email.data).first()
    if form.validate_on_submit():
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
            flash("Incorrect password, try again.")
            return redirect(url_for('login'))
        flash("Email does not exist, try again.")
        return redirect(url_for('login'))
    return render_template('login.html', loginform=form, current_user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email = form.email.data).first():
            flash("You've already signed up with this email, try logging in instead.")
            return redirect(url_for('login'))
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=generate_password_hash(
                password=form.password.data,
                method="pbkdf2:sha256",
                salt_length=8,
            ),
            phone_num = form.phone_num.data,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))

    return render_template('register.html', registerform=form, current_user=current_user)

@app.route('/payment')
def payment():
    return render_template('payment.html', current_user=current_user)

@app.route('/about')
def about():
    return render_template('about.html',current_user=current_user)


@app.route('/faq')
def faq():
    return render_template('faq.html', current_user=current_user)

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    form  = AddProduct()
    if form.validate_on_submit():
        print("validate")
        new_product = Product(
            name = form.product_name.data,
            price = form.price.data,
            desc = form.desc.data,
            XL_size = form.XL_size.data,
            L_size= form.L_size.data,
            M_size = form.M_size.data,
            S_size = form.S_size.data,
            one_size = form.one_size.data,
            front_img = form.front_image.data,
            back_img = form.back_image.data,
            cat_id = form.category.data
        )
        seller = Seller.query.filter_by(email=form.seller_email.data).first()
        if not seller:
            print("new seller")
            new_seller = Seller(
                name=form.seller_name.data,
                email=form.seller_email.data
            )
            db.session.add(new_seller)
            db.session.commit()
        seller = Seller.query.filter_by(email=form.seller_email.data).first()
        new_product.seller_id = seller.id
        db.session.add(new_product)
        db.session.commit()
    return render_template('add-product.html', form= form)    


@app.route('/cat-products/<int:cat_id>',methods = ['GET', 'POST'])
def cat_products(cat_id):
    category = Category.query.get(cat_id)
    return render_template("store.html", cat=category)

@app.route('/single-product/<int:product_id>')
def product(product_id):
    product = Product.query.get(product_id)
    return render_template('single_product.html', product=product)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/cart/<int:product_id>', methods=['GET', 'POST'])
def cart(product_id):
    user = current_user
    cart = Cart(
        user_id = user.id,
        product_id = product_id,
    )
    db.session.add(car)
    db.session.commit()

    return render("cart.html", user = user)

if __name__ == '__main__':
    app.run(debug=True)
