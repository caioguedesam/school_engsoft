from flask import render_template, redirect, url_for, request, Blueprint
from skoolit import app, db
from skoolit.usuarios import models, forms
from skoolit.login.views import exigirUsuarioLogado

usuarios = Blueprint('usuarios',__name__, template_folder='templates/usuarios')

# @usuarios.route('/')
# def home():
# 	return render_template('home.html')

@usuarios.before_request
def exigirLogin():
	return exigirUsuarioLogado()

@usuarios.route('/criar', methods=['POST', 'GET'])
def criar():
	form = forms.CriarUsuarioForm()

	if form.validate_on_submit():
		novo_usuario = models.Usuario(form.email.data, form.papel.data)
		db.session.add(novo_usuario)
		db.session.commit()

		return redirect(url_for('usuarios.listar'))

	return render_template('criar.html', form=form)


@usuarios.route('/listar', methods=['POST', 'GET'])
def listar():

	usuarios = models.Usuario.query.all()

	return render_template('listar.html', usuarios=usuarios)


@usuarios.route('/atualizar/<id>', methods=['POST', 'GET'])
def atualizar(id):
	form = forms.AtualizarUsuarioForm()

	usuario = models.Usuario.query.filter_by(id=id).first_or_404()

	if form.validate_on_submit():
		usuario.email = form.email.data
		usuario.papel = form.papel.data
		db.session.commit()

		return redirect(url_for('usuarios.listar'))
	elif request.method == 'GET':
		form.email.data = usuario.email
		form.papel.data = usuario.papel

	return render_template('atualizar.html', form=form)


@usuarios.route('/excluir/<id>', methods=['GET'])
def excluir(id):

	usuario = models.Usuario.query.filter_by(id=id).first_or_404()

	db.session.delete(usuario)
	db.session.commit()

	return redirect(url_for('usuarios.listar'))