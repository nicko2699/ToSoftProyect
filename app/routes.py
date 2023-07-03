from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_wtf import form
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, SignUpForm, EditUserForm, orderServForm, orderWorkForm
from app.models import User, OrderServ, OrderWork
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
@app.route("/index")
def index():

    if current_user.is_authenticated:
        return redirect(url_for('menuclient'))

    return render_template("base.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario ya ingreso mandalo al index
    if current_user.is_authenticated:
        if current_user.username == "admin":
            return redirect(url_for('menutosoft'))
        else:
            return redirect(url_for('menuclient'))    
    form = LoginForm()
    # Si hace un submit
    if form.validate_on_submit():
        # Haz una consulta de usuarios con el mismo nombre
        user = User.query.filter_by(username=form.username.data).first()
        # Si no se encontro el usuario o la contraseña es incorrecta
        if user is None or not user.check_password(form.password.data):
            # Muestra el error
            flash('No se encontró el usuario o la contraseña es incorrecta')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('Iniciaste sesión correctamente, Hola {}'.format(form.username.data))
        return redirect('menuclient')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
        # Si el usuario ya ingreso mandalo al index
        if current_user.is_authenticated:
                if current_user.username == "admin":
                    return redirect(url_for('menutosoft'))
                else:
                    return redirect(url_for('menuclient'))    
        # Si hace un submit
        form = SignUpForm()
        if form.validate_on_submit():
                # Haz una consulta de usuarios con el mismo nombre
                check_username = User.query.filter_by(username=form.username.data).first()
                if check_username:
                        # Muestra el error
                        flash('Nombre de usuario ya existente.')
                        return redirect(url_for('signup'))
                        # Validar correo
                check_username = User.query.filter_by(email=form.email.data).first()
                if check_username:
                        # Muestra el error
                        flash('Correo ya existente.')
                        return redirect(url_for('signup'))
                user = User()
                user.name = form.name.data
                user.last_names = form.last_names.data
                user.username = form.username.data
                user.set_password(form.password.data)
                user.email = form.email.data
                user.address = form.address.data
                user.phone = form.phone.data
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
        return render_template('signup.html', title='Registro', form=form)

@app.route("/menuclient")
def menuclient():

    if current_user.username == "admin":
        return redirect(url_for('menutosoft'))

    return render_template("menuClient.html")

@app.route("/menutosoft")
def menutosoft():

    return render_template("menuToSoft.html")

@app.route('/menuclient/edit_User', methods=['GET', 'POST'])
@login_required
def edit_User():
    form = EditUserForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.last_names = form.last_names.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Se han guardado los cambios')
        return redirect(url_for('edit_User'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.last_names.data = current_user.last_names
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.phone.data = current_user.phone
    return render_template('edit_User.html', title="Datos de usuario", form=form)

@app.route('/menuclient/addOrder', methods=['GET', 'POST'])
@login_required
def addorder():
    form = orderServForm()
    if form.validate_on_submit():
        new_order = OrderServ()
        # La orden es lo que se recibe del form
        new_order.typeService = form.typeService.data
        # El id es el id del objeto usuario actual
        new_order.user_id = current_user.id
        # Añadir y enviar a la bd
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for('menuclient'))
    # Si es POST agregar la orden
    return render_template('orderServ.html', title='Generar nueva orden de servicio', form=form)


@app.route("/menuclient/showOrdersServ", methods=['GET','POST'])
@login_required
def showOrdersServ():

    #if(current_user.id == OrderServ.user_id):
    servOrders = OrderServ.query.all()

    return render_template("userOrdersServ.html", title="Ordenes registradas", servOrders = servOrders)


@app.route("/menutosoft/addworkOrder", methods=['GET', 'POST'])
@login_required
def addorderwork():
    form = orderWorkForm()
    if form.validate_on_submit():
        new_workOrder = OrderWork()
        
        new_workOrder.typeWork = form.typeWork.data
        new_workOrder.budget = form.budget.data
        new_workOrder.workDuration = form.workDuration.data
        new_workOrder.technician = form.technician.data
        db.session.add(new_workOrder)
        db.session.commit()
        return redirect(url_for('menutosoft'))
    return render_template("orderWork.html", title="Generar nueva orden de trabajo", form=form)

@app.route("/menutosoft/showOrdersWork", methods=['GET', 'POST'])
@login_required
def showOrdersWork():

    workorders = OrderWork.query.all()

    return render_template("tosoftOrdersWork.html", title="Ordenes de trabajo", workorders = workorders )


