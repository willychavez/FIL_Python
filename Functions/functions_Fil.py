#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#  Copyright 2018 Willy Chavez <wchavezmareco@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
import sys; sys.dont_write_bytecode = True # não gera arquivos pyc

import os
import pandas
import numpy
from sklearn.cross_decomposition import PLSRegression

# Carrega arquivos de acordo com uma configuração de pastas retornando uma matrix onde as colunas são as intensidades dos espectros
def Carrega_Arquivos(caminho, inicio_linea):
	pastas = os.listdir('%s' % caminho)
	pastas.sort()
	matrix = []
	for i in pastas:
		amostras = os.listdir('%s/%s' % (caminho, i))
		amostras.sort()
		chave = 0
		for j in amostras:
			Dados = pandas.read_csv('%s/%s/%s' % (caminho, i, j), sep='\t', skiprows=int(inicio_linea), header=None)
			if pandas.isnull(Dados[Dados.columns[-2]]).sum() > 0:
				Espectros = Dados[Dados.columns[:-2]]
			elif pandas.isnull(Dados[Dados.columns[-1]]).sum() > 0:
				Espectros = Dados[Dados.columns[:-1]]
			else:
				Espectros = Dados
			if chave == 0:
				x = numpy.array(Espectros)[:, 0]
				matrix_y = numpy.array(Espectros)[:, 1:]
				chave = 1
			else:
				matrix_y = numpy.column_stack((matrix_y, numpy.array(Espectros)[:, 1:]))
		matrix.append(matrix_y)
	return x, matrix

# Filtro passa baixa (elimina altas frequencias)
def Boxcar(y, n=1):
	if n == 1:
		return y
	elif n > 1:
		Y = numpy.zeros_like(y)
		for i in range(n // 2, len(y) - n // 2):
			Y[i] = numpy.mean(y[(i - n // 2): (i + n // 2)])
		return Y
	else:
		raise ValueError('não é possível boxcar de zero e numero negativo')

# Delimita a região do espectro onde se quer trabalhar
def Corte(x, x1, x2):
	ind = numpy.nonzero((x > x1) & (x < x2))
	return ind

# Função encarregada de remover offset pegando um valor minimo do espectro automaticamente ou fornecendo um valor minimo
def Offset(y, valor_y=0):
	Y = numpy.zeros_like(y)
	if valor_y > 0:
		Y = y - valor_y
		return Y
	else:
		m = y.min()
		Y = y - m
		return Y

# função que realiza o produto scalar entre dois vetores retornando o cosseno theta
def Produto_Scalar(y, yref):
	norm_ym = numpy.linalg.norm(yref)
	norm_y = numpy.linalg.norm(y)
	if y.shape[0] > y.shape[1]:
		y = y.T
	if yref.shape[0] < yref.shape[1]:
		yref = yref.T
	costheta = y.dot(yref) / (norm_y * norm_ym)
	return costheta

# função que normaliza utlizandando a area embaixo da curva
def Normaliza(y, x=None):
	Y = numpy.zeros_like(y)
	Y = y/numpy.trapz(y, x)
	return Y

# Identifica as folhas
def Identifica(caminho):
	amostras=os.listdir('%s' % caminho)
	amostras.sort()
	matrix = []
	folhas = []
	nf = []
	chave = 0
	for i in amostras:
		Dados = pandas.read_csv('%s/%s' % (caminho, i), sep='\t',  header=None)
		if chave == 0:
			matrix = numpy.array(Dados)
			chave = 1
		else:
			matrix = numpy.column_stack((matrix, numpy.array(Dados)))
	for i in range(len(matrix[1])):
		for j in range(len(matrix[:, i])):
			temp = numpy.vstack(([j + 1]*matrix[j, i], numpy.arange(1, (matrix[j, i] + 1))))
			if j == 0:
				nf = temp
			else:
				nf = numpy.column_stack((nf, temp))
		folhas.append(nf)
	return folhas

def Identifica_Agrup(caminho):
	pastas = os.listdir('%s' % caminho)
	pastas.sort()
	matrix = []
	folhas = []
	nf = []
	for i in pastas:
		amostras = os.listdir('%s/%s' % (caminho, i))
		amostras.sort()
		chave = 0
		for j in amostras:
			Dados = pandas.read_csv('%s/%s/%s' % (caminho, i, j), sep='\t',  header=None)
			if chave == 0:
				matrix_y = numpy.array(Dados)
				chave = 1
			else:
				matrix_y = numpy.vstack((matrix_y, numpy.array(Dados)))
		matrix.append(matrix_y)
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			temp = numpy.vstack(([j + 1]*matrix[i][j, 0], numpy.arange(1, (matrix[i][j, 0] + 1))))
			if j == 0:
				nf = temp
			else:
				nf = numpy.column_stack((nf, temp))
		folhas.append(nf)
	return folhas

def importa_dados(caminho):
	amostras = os.listdir(caminho)
	amostras.sort()
	matrix = []
	for i in amostras:
		Dados = pandas.read_csv('%s/%s' % (caminho, i), sep='\t', header=None)
		matrix.append(numpy.array(Dados))
	return matrix

#preciso melhorar esta função
def importa_excel(sheet):
	xl = pandas.ExcelFile('/home/willy/Documents/Novo_Conj_Dados/Agrupados/teste.xls', skiprows=1, header=None)
	df = xl.parse('%s' % sheet)
	matrix = [[]]*3
	matrix[1] = numpy.array(df)[:, 6:8].T
	matrix[0] = numpy.array(df)[:, 15:17].T
	matrix[2] = numpy.array(df)[:, 24:].T
	return matrix

def Predicao_python(conj_test, modelo, referencia, n_component):
	pls = PLSRegression(n_component).fit(modelo, referencia)
	pls.coef_
	pred = pls.predict(conj_test)
	return pred


#Constroi o beta apartir de um conjunto de teinamento para depois jogar na função pedriction
def beta(modelo, referencia, n_component):
	pls = PLSRegression(n_component, scale=False).fit(modelo, referencia)
	pls.coef_
	fit_intercept = pls.y_mean_ - numpy.dot(pls.x_mean_, pls.coef_)
	fit_coef = pls.coef_
	beta = numpy.row_stack((fit_intercept, fit_coef))
	return beta

#baseado ao beta gerado tanto no matlab quanto no proprio PySpectrum retorna a matrix confução do conjunto de teste
def Prediction(beta, amostras):
	matrix = []
	temp = []
	for k in range(len(amostras)):
		amostras[k] = amostras[k][2:, :]
		amostras[k] = numpy.vstack(([1]*amostras[k].shape[1], amostras[k]))
		amostras[k] = amostras[k].T
		for i in range(len(beta)):
			for j in range(amostras[k].shape[0]):
				if j == 0:
					pred = numpy.dot(amostras[k][j, :], beta[i])
				else:
					pred = numpy.row_stack((pred, numpy.dot(amostras[k][j, :], beta[i])))
			if i == 0:
				temp = numpy.array(pred)
			else:
				temp = numpy.column_stack((temp, numpy.array(pred)))
		matrix.append(temp)
	Assintomatica = 0
	Sadia = 0
	Sintomatica = 0
	resultado = [[]]*len(matrix)
	for i in range(len(matrix)):
		for j in range(matrix[i].shape[0]):
			if matrix[i][j, 0] > matrix[i][j, 1] and matrix[i][j, 0] > matrix[i][j, 2]:
				Assintomatica += 1
			elif matrix[i][j, 1] > matrix[i][j, 0] and matrix[i][j, 1] > matrix[i][j, 2]:
				Sadia += 1
			elif matrix[i][j, 2] > matrix[i][j, 0] and matrix[i][j, 2] > matrix[i][j, 1]:
				Sintomatica += 1
		resultado[i] = numpy.column_stack((Sadia, Assintomatica, Sintomatica))
		Assintomatica = 0
		Sadia = 0
		Sintomatica = 0
	return matrix, resultado

def matrix_conf(matrix):
	Assintomatica = 0
	Sadia = 0
	Sintomatica = 0
	resultado = [[]] * len(matrix)
	for i in range(len(matrix)):
		for j in range(matrix[i].shape[0]):
			if matrix[i][j, 0] > matrix[i][j, 1] and matrix[i][j, 0] > matrix[i][j, 2]:
				Assintomatica += 1
			elif matrix[i][j, 1] > matrix[i][j, 0] and matrix[i][j, 1] > matrix[i][j, 2]:
				Sadia += 1
			elif matrix[i][j, 2] > matrix[i][j, 0] and matrix[i][j, 2] > matrix[i][j, 1]:
				Sintomatica += 1
		resultado[i] = numpy.column_stack((Sadia, Assintomatica, Sintomatica))
		Assintomatica = 0
		Sadia = 0
		Sintomatica = 0
	return resultado