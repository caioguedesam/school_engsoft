from flask import render_template, redirect, url_for, request, Blueprint
from skoolit import app, db
from skoolit.turmas import models, forms

turmas = Blueprint('turmas',__name__, template_folder='templates/turmas')

@turmas.route('/')
def home():
	return render_template('home.html')

@turmas.route('/criar', methods=['POST', 'GET'])
def criar():
	form = forms.CriarTurmaForm()

	if form.validate_on_submit():
		nova_turma = models.Turma(titulo=form.titulo.data,
									materia=form.materia.data,
									  professor=form.professor.data)
		db.session.add(nova_turma)
		db.session.commit()

		return redirect(url_for('turmas.listar'))

	return render_template('turmas/criar_turma.html', form=form)


@turmas.route('/listar', methods=['POST', 'GET'])
def listar():

	turmas = models.Turma.query.all()

	return render_template('turmas/listar_turmas.html', turmas=turmas)


@turmas.route('/atualizar/<id>', methods=['POST', 'GET'])
def atualizar(id):
	turma = models.Turma.query.filter_by(id=id).first_or_404()

	form = forms.AtualizarTurmaForm()

	if form.validate_on_submit():
		turma.titulo = form.titulo.data
		turma.materia = form.materia.data
		turma.professor = form.professor.data
		db.session.commit()

		return redirect(url_for('turmas.listar'))
	elif request.method == 'GET':
		form.titulo.data = turma.titulo
		form.materia.data = turma.materia
		form.professor.data = turma.professor

	return render_template('turmas/atualizar_turma.html', form=form)


@turmas.route('/excluir/<id>', methods=['GET'])
def excluir(id):

	turma = models.Turma.query.filter_by(id=id).first_or_404()

	db.session.delete(turma)
	db.session.commit()

	return redirect(url_for('turmas.listar'))


@turmas.route('/criar-materia', methods=['POST', 'GET'])
def criar_materia():
	form = forms.CriarMateriaForm()

	if form.validate_on_submit():
		nova_materia = models.Materia(form.nome.data)
		db.session.add(nova_materia)
		db.session.commit()

		return redirect(url_for('turmas.listar_materias'))

	return render_template('turmas/criar_materia.html', form=form)


@turmas.route('/listar-materias', methods=['POST', 'GET'])
def listar_materias():

	materias = models.Materia.query.all()

	return render_template('turmas/listar_materias.html', materias=materias)

@turmas.route('/listar-materia/<id>', methods=['POST', 'GET'])
def listar_materia(id):

	materia = models.Materia.query.filter_by(id=id).first_or_404();

	return render_template('turmas/detalhes_materia.html', materia=materia)


@turmas.route('/atualizar-materia/<id>', methods=['POST', 'GET'])
def atualizar_materia(id):
	form = forms.AtualizarMateriaForm()

	materia = models.Materia.query.filter_by(id=id).first_or_404()

	if form.validate_on_submit():
		materia.nome = form.nome.data
		db.session.commit()

		return redirect(url_for('turmas.listar_materias'))
	elif request.method == 'GET':
		form.nome.data = materia.nome

	return render_template('turmas/atualizar_materia.html', form=form)


@turmas.route('/excluir-materia/<id>', methods=['GET'])
def excluir_materia(id):

	materia = models.Materia.query.filter_by(id=id).first_or_404()

	db.session.delete(materia)
	db.session.commit()

	return redirect(url_for('turmas.listar_materias'))