from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, FloatField, IntegerField, FormField, FieldList
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField

class LoginForm(FlaskForm):
    email= StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    phone_num = StringField("Phone Number", validators=[DataRequired()])
    submit = SubmitField("Sign up")

class AddProduct(FlaskForm):
    category = SelectField(label="Select Category", validators=[DataRequired()],
                           choices= [(1,"Men"), (2, "Women"), (3,"Kids"), (4,"Accessories"), (5,"Other")])
    product_name = StringField("Your Product", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    desc = CKEditorField("Description", validators=[DataRequired()])
    XL_size = IntegerField("Quantity 0f XL size",)
    L_size = IntegerField("Quantity 0f L size", )
    M_size = IntegerField("Quantity 0f M size", )
    S_size = IntegerField("Quantity 0f S size", )
    one_size = IntegerField("Quantity 0f one size", )
    front_image = StringField("Front face", validators=[DataRequired(), URL()])
    back_image = StringField("Back face", validators=[DataRequired(), URL()])
    seller_name = StringField("Seller Name", validators=[DataRequired()])
    seller_email = StringField("Seller Email Address", validators=[DataRequired(), Email()])
    submit = SubmitField("Add Product")

class ImageForm(FlaskForm):
    img_url = StringField("Image URL",validators=[DataRequired()])

