import datetime
import random
import string
from flask import Flask, session, render_template, request, url_for, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Azerty@localhost:5432/hotel"
app.config['SECRET_KEY'] = 'Azerty'
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'

# Configuration du GMail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'nourad23seid@gmail.com'
app.config['MAIL_PASSWORD'] = 'jyil fwly ftvi pmaa'
app.config['MAIL_DEFAULT_SENDER'] = 'nourad23seid@gmail.com'

mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class UserRegister(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(150), nullable=False)
    prenom = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    tel = db.Column(db.String(20))
    password = db.Column(db.String(255), nullable=False)
    verification_code = db.Column(db.String(6), nullable=True)
    verified = db.Column(db.Boolean, default=False)
    mes_reservations = db.relationship('Chambre', backref='user_register', lazy=True)


class Chambre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    est_reservee = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_register.id'), nullable=True)
    date_debut = db.Column(db.Date, nullable=True)
    date_fin = db.Column(db.Date, nullable=True)
    image = db.Column(db.String(255), nullable=True)




@app.route('/')
def index():
    chambres = Chambre.query.all()
    return render_template('accueil.html', chambres=chambres)


def generate_verification_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = UserRegister.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
            flash(f'Connecté avec succès {user.email}', 'success')


        else:
            flash("Erreur lors de la connexion. Veuillez vérifier vos identifiants.", 'danger')

    return render_template('login.html')


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        tel = request.form['tel']
        password = request.form['password']
        verification_code = generate_verification_code()

        if not nom or not prenom or not email or not tel or not password:
            flash("Veuillez saisir tous les champs.", 'danger')
            return redirect(url_for('inscription'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        try:
            msg = Message('Vérification de votre compte', sender='nourad23seid@gmail.com', recipients=[email])
            msg.body = f'Votre code de vérification est : {verification_code}'
            mail.send(msg)
        except Exception as e:
            flash(f"Erreur lors de l'envoi de l'email : {str(e)}", 'danger')
            return redirect(url_for('inscription'))

        user = UserRegister(nom=nom, prenom=prenom, email=email, tel=tel, password=hashed_password,
                            verification_code=verification_code)
        db.session.add(user)
        db.session.commit()

        flash('Inscription réussie. Veuillez vérifier votre email pour le code de vérification.', 'success')
        return redirect(url_for('verification_code'))

    return render_template('inscription.html')


@app.route('/verification_code', methods=['GET', 'POST'])
def verification_code():
    if request.method == 'POST':
        email = request.form.get('email')
        code = request.form.get('verification_code')

        print(f"Email: {email}, Code: {code}")  # Pour déboguer

        user = UserRegister.query.filter_by(email=email).first()
        if user:
            print(f"User found: {user.email}, Verification code: {user.verification_code}")
        else:
            print("User not found")

        if user and user.verification_code == code:
            flash('Votre compte a été vérifié avec succès. Vous pouvez maintenant vous connecter.', 'success')
            user.verified = True
            db.session.commit()

            return redirect(url_for('login'))
        else:
            flash('Code de vérification incorrect. Veuillez réessayer.', 'danger')

    # Toujours retourner le template pour GET et en cas d'erreur
    return render_template('verifrication_code.html')


@app.route('/dashboard')
def dashboard():

    if 'user_id' in session:
        user = UserRegister.query.get(session['user_id'])
        chambres = Chambre.query.all()
        reservations = user.mes_reservations

    images = {
        1: 'chambre1.jpg',
        2: 'chambre2.jpg',
        3: 'chambre3.jpg',
        4: 'chambre4.jpg',
        5: 'chambre5.jpg',
        6: 'chambre6.jpg',
        7: 'chambre7.jpg',
    }

    for chambre_id, image_name in images.items():
        chambre = Chambre.query.get(chambre_id)
        if chambre:
            chambre.image = f'{image_name}'

    db.session.commit()
    print("Mise à jour des images terminée.")

    chambres = Chambre.query.all()
    return render_template('dashboard.html', user=user, chambres=chambres, reservations=reservations)

@app.route('/details/<int:chambre_id>')
def details(chambre_id):
    chambre = Chambre.query.get_or_404(chambre_id)
    return render_template('details.html', chambre=chambre)


@app.route('/chambres')
def chambres():
    classe = request.args.get('classe')

    if classe:
        chambres = Chambre.query.filter_by(classe=classe).all()
    else:
        chambres = Chambre.query.all()

    return render_template('chambres.html', chambres=chambres)

@app.route('/reservation/<int:chambre_id>', methods=['GET', 'POST'])
def reservation(chambre_id):
    if 'user_id' not in session:
        flash("Vous devez être connecté pour réserver une chambre.", 'warning')
        return redirect(url_for('login'))

    chambre = Chambre.query.get_or_404(chambre_id)
    if chambre.est_reservee:
        flash("Cette chambre est déjà réservée.", 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        date_debut = request.form['date_debut']
        date_fin = request.form['date_fin']

        # Convertir les dates en objets datetime
        date_debut = datetime.datetime.strptime(date_debut, '%Y-%m-%d')
        date_fin = datetime.datetime.strptime(date_fin, '%Y-%m-%d')

        if date_debut >= date_fin:
            flash("La date de fin doit être après la date de début.", 'danger')
            return redirect(url_for('reservation', chambre_id=chambre_id))

        chambre.est_reservee = True
        chambre.date_debut = date_debut
        chambre.date_fin = date_fin
        chambre.user_id = session['user_id']

        # Calculer le prix total
        nombre_de_jours = (date_fin - date_debut).days
        prix_total = chambre.prix * nombre_de_jours

        db.session.commit()

        # Envoyer la facture par email
        user = UserRegister.query.get(session['user_id'])
        try:
            msg = Message('Facture de réservation', sender='nourad23seid@gmail.com', recipients=[user.email])
            msg.body = f'''
            Merci pour votre réservation.

            Détails de la réservation :
            Numero Chambre : {chambre.numero}
            Description : {chambre.description}
            Date de début : {date_debut.strftime('%Y-%m-%d')}
            Date de fin : {date_fin.strftime('%Y-%m-%d')}
            Prix total : {prix_total} CFFA

            Merci de votre confiance.
            '''
            mail.send(msg)
        except Exception as e:
            flash(f"Erreur lors de l'envoi de l'email : {str(e)}", 'danger')

        flash("Chambre réservée avec succès. Une facture vous a été envoyée par email.", 'success')
        return redirect(url_for('dashboard'))

    return render_template('reservation.html', chambre=chambre)


@app.route('/mes_reservations/<int:user_id>')
def mes_reservations(user_id):
    user = UserRegister.query.get_or_404(user_id)

    reservations = user.mes_reservations

    return render_template('historique.html', user=user, reservations=reservations)

@app.route('/annuler_reservation/<int:reservation_id>', methods=['POST'])
def annuler_reservation(reservation_id):
    reservation = Chambre.query.get_or_404(reservation_id)

    if reservation.user_id != session.get('user_id'):
        flash("Vous n'êtes pas autorisé à annuler cette réservation.", 'danger')
        return redirect(url_for('mes_reservations', user_id=session.get('user_id')))

    # Libérer la chambre
    reservation.est_reservee = False
    reservation.date_debut = None
    reservation.date_fin = None
    reservation.user_id = None
    flash("Réservation annulée avec succès. La chambre est maintenant libre.", 'success')


    db.session.commit()

    return redirect(url_for('mes_reservations', user_id=session.get('user_id')))


@app.route('/rechercher_chambres')
def rechercher_chambres():
    classe = request.args.get('classe', '')

    if classe:
        chambres = Chambre.query.filter(Chambre.type.ilike(f'%{classe}%')).all()
    else:
        chambres = Chambre.query.all()

    chambres_data = [{
        'id': chambre.id,
        'type': chambre.type,
        'description': chambre.description,
        'prix': chambre.prix,
        'est_reservee': chambre.est_reservee,
        'image_filename': chambre.image_filename
    } for chambre in chambres]

    return jsonify({'chambres': chambres_data})




@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Vous avez été déconnecté.', 'success')
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
