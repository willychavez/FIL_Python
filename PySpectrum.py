#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
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

import os
import numpy
import pandas
import pyqtgraph as pg
import pyqtgraph.exporters
from Functions import functions_Fil as fs
from Functions import gera_arff as ga
import matplotlib.pyplot as plt
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

#from Functions import *

def main(args):
	# fc = '/home/willy/Documents/Novo_Conj_Dados/Mensal/29_03_2018/Folhas'
	fc = '/home/willy/Documents/Novo_Conj_Dados/Agrupados/folhas_p'
	w = '/home/willy/Documents/Novo_Conj_Dados/Agrupados/TesteOutliers/weka'
	img = '/home/willy/Documents/Novo_Conj_Dados/Agrupados/TesteOutliers/Imagens'
	cy1 = '/home/willy/PycharmProjects/YMedios_Eq.txt'
	cy3 = "/home/willy/PycharmProjects/YMedios_FIL.txt"
	nome1 = 'EQ1'
	nome2 = 'EQ2'
	nome3 = 'FIL'
	# sheet1 = 'Teste_EQ1'
	# sheet2 = 'Teste_EQ2'
	# sheet3 = 'Teste_FIL'
	sheet1 = 'Beta_EQ1'
	sheet2 = 'Beta_EQ2'
	sheet3 = 'Beta_FIL'
	# c1 = '/home/willy/Documents/Novo_Conj_Dados/Mensal/29_03_2018/Equipamentos/Eq_1_MMO_29_03_2018'
	# c2 = '/home/willy/Documents/Novo_Conj_Dados/Mensal/29_03_2018/Equipamentos/Eq_2_MMO_29_03_2018'
	# c3 = '/home/willy/Documents/Novo_Conj_Dados/Mensal/29_03_2018/Fil/FIL_Citrosuco_29_03_2018'


	c1 = '/home/willy/Documents/Novo_Conj_Dados/Agrupados/EQ1_p'
	c2 = '/home/willy/Documents/Novo_Conj_Dados/Agrupados/EQ2_p'
	c3 = '/home/willy/Documents/Novo_Conj_Dados/Agrupados/FIL_p'


	# cym = cy1
	indice = 3
	
	Sheet = sheet3
	nome = nome3
	caminho = c3
	nomeimg1 = "fSadia"
	nomeimg2 = "fAssintomatica"
	nomeimg3 = "fSintomatica"
	
	
	# Indice para teste
	ind_beta = 2


	# ym = pandas.read_csv('%s' % cym, '\t', header=None)
	# ymedio = numpy.array(ym)
	# # print(ymedio, ym)

	x, m = fs.Carrega_Arquivos(caminho, 1)

	#Corte Equipamento1
	x1 = 494.3046
	x2 = 758.7687

	#Cortes FIL
	x3 = 444.2869
	x4 = 819.9622

	if indice == 1:
		ind = fs.Corte(x, x1, x2)
	else:
		ind = fs.Corte(x, x3, x4)

	x = x[ind]
	y = []
	for j in range(len(m)):
		for i in range(m[j].shape[1]):
			if i == 0:
				y_temp = m[j][:, i]
				yy = fs.Normaliza(fs.Offset(fs.Boxcar(y_temp, 10)[ind]), x)
			else:
				y_temp = m[j][:, i]
				yy = numpy.column_stack((yy, fs.Normaliza(fs.Offset(fs.Boxcar(y_temp, 10)[ind]), x)))
		y.append(yy)
	# print(y[0].shape)

	folhas = fs.Identifica_Agrup(fc)
	# print(folhas[0].shape, folhas[1].shape, folhas[2].shape)

	#Carrega identificação das folhas
	Y = [[]] * len(y)
	for i in range(len(y)):
		Y[i] = numpy.vstack((folhas[i], y[i]))

	print(Y[0].shape, Y[1].shape, Y[2].shape)
	
	# matrix = [[]]*3
	# #matriz de produto scalar
	# for k in range(len(Y)):
	# 	m_temp = []
	# 	for i in range(Y[k].shape[1]):
	# 		for j in range(Y[k].shape[1]):
	# 			if j == 0:
	# 				m_temp = numpy.array(fs.Produto_Scalar(Y[k][2:, i], Y[k][2:, j]))
	# 				# print(m_temp)
	# 			else:
	# 				m_temp = numpy.column_stack((m_temp, fs.Produto_Scalar(Y[k][2:, i], Y[k][2:, j])))
	# 				# print(m_temp)
	# 		if i == 0:
	# 			tp = m_temp
	# 		else:
	# 			tp = numpy.vstack((tp, m_temp))
	# 	# print(tp.shape)
	# 	matrix[k] = tp
	#
	# print(len(matrix))
	
	# h = [[]]*len(matrix)
	# for i in range(len(matrix)):
	# 	h[i] = (sum(matrix[i])-1)/(matrix[i].shape[0] - 1)
	#
	# print(h[0].shape)
	# print(h[0].shape, h[1].shape, h[2].shape)
	
	# plt.hist(matrix[0], bins='auto')
	# plt.show()
	# plt.hist(matrix[1], bins='auto')
	# plt.show()
	# plt.hist(matrix[2], bins='auto')
	# plt.show()
	
	# for i in range(len(h)):
	# 	if i == 0:
	# 		h[i] = fs.remove_outliers(h[i], 0.989)
	# 		Y[i] = numpy.delete(Y[i], h[i], 1)
	# 	elif i == 1:
	# 		h[i] = fs.remove_outliers(h[i], 0.997)
	# 		Y[i] = numpy.delete(Y[i], h[i], 1)
	# 	elif i == 2:
	# 		h[i] = fs.remove_outliers(h[i], 0.981)
	# 		Y[i] = numpy.delete(Y[i], h[i], 1)
	#
	# print(Y[0].shape, Y[1].shape, Y[2].shape)
	
	
	
	# a = numpy.array([[1], [2], [3], [4]])
	# c = numpy.array([[1], [2], [3], [4]])
	# b = a.T
	# f = a.T
	# print(a.shape, b.shape)
	# print(a, b)
	# print(f, b)
	# d = fs.Produto_Scalar(b, a)
	# print(d.shape)
	#
	
	
	
	# #remove outliers
	# for i in range(len(y)):
	# 	cont = 0
	# 	j = 0
	# 	while j < y[i].shape[1]:
	# 		cosseno_tetta = fs.Produto_Scalar(y[i][:, j], ymedio[:, i])
	# 		if cosseno_tetta < 0.899:
	# 			if cont == 0:
	# 				Y[i] = numpy.delete(Y[i], j, 1)
	# 				cont = 1
	# 			else:
	# 				Y[i] = numpy.delete(Y[i], (j - cont), 1)
	# 				cont += 1
	# 		j += 1
	#
	folhas_beta = fs.importa_excel(Sheet)
	# print(folhas_beta[0].shape, folhas_beta[2].shape, folhas_beta[2].shape)

	#seleciona espectros que vão compor o beta
	n = []
	for k in range(len(folhas)):
		for j in range(folhas_beta[k].shape[1]):
			for i in range(folhas[k].shape[1]):
				if folhas[k][0, i] == folhas_beta[k][0, j] and folhas[k][1, i] == folhas_beta[k][1, j]:
					n.append(i)
		Y[k] = Y[k][:, numpy.array(n)]
		n = []
	print(Y[0].shape, Y[1].shape, Y[2].shape)

	# dados = numpy.vstack((Y[0][2:, :].T, Y[1][2:, :].T, Y[2][2:, :].T))
	# numpy.savetxt('%s/''%s' % (img, '%s.txt' % nome), dados, delimiter='\t')

	#Gera arquivo.arff
	ga.Gera_Arff_Ind(x, Y, '%s/''%s' % (w, '%s.arff' % nome))


	grafico = pg.plot()
	#grafico.addLegend()
	for i in range(Y[1].shape[1]):
		grafico.plot(x, Y[1][2:, i], pen=(i, Y[1].shape[1]))
	grafico.setTitle('Sadia')
	grafico.setLabels(left='Intensidade (u.a.)', bottom='Comprimento de Onda (nm)')

	grafico1 = pg.plot()
	#grafico1.addLegend()
	for i in range(Y[0].shape[1]):
		grafico1.plot(x, Y[0][2:, i], pen=(i, Y[0].shape[1]))
	grafico1.setTitle('Assintomatica')
	grafico1.setLabels(left='Intensidade (u.a.)', bottom='Comprimento de Onda (nm)')

	grafico2 = pg.plot()
	#grafico2.addLegend()
	for i in range(Y[2].shape[1]):
		grafico2.plot(x, Y[2][2:, i], pen=(i, Y[2].shape[1]))
	grafico2.setTitle('Sintomatica')
	grafico2.setLabels(left='Intensidade (u.a.)', bottom='Comprimento de Onda (nm)')

	pg.QtGui.QApplication.exec_()
	exporter = pg.exporters.ImageExporter(grafico.plotItem)
	exporter.params.param('width').setValue(1024, blockSignal=exporter.widthChanged)
	exporter.params.param('height').setValue(768, blockSignal=exporter.heightChanged)
	exporter.export('%s/''%s' % (img, '%s.png' % nomeimg1))
	exporter = pg.exporters.ImageExporter(grafico1.plotItem)
	exporter.params.param('width').setValue(1024, blockSignal=exporter.widthChanged)
	exporter.params.param('height').setValue(768, blockSignal=exporter.heightChanged)
	exporter.export('%s/''%s' % (img, '%s.png' % nomeimg2))
	exporter = pg.exporters.ImageExporter(grafico2.plotItem)
	exporter.params.param('width').setValue(1024, blockSignal=exporter.widthChanged)
	exporter.params.param('height').setValue(768, blockSignal=exporter.heightChanged)
	exporter.export('%s/''%s' % (img, '%s.png' % nomeimg3))

	
	

	# beta = fs.importa_dados('/home/willy/Desktop/Betas2/EQ2')
	# print(beta[0].shape, beta[1].shape, beta[2].shape)
	# # print(beta[0], beta[1], beta[2])
	#
	# teste, resultado = fs.Prediction(beta, Y)
	# # print(teste[0], teste[1], teste[2])
	# print(resultado[1], resultado[0], resultado[2])
	# print(Y[1].shape[0], Y[0].shape[0], Y[2].shape[0])
	# print(((resultado[1]/Y[1].shape[0])*100).round(2), ((resultado[0]/Y[0].shape[0])*100).round(2), ((resultado[2]/Y[2].shape[0])*100).round(2))


	# amostras = fs.importa_dados('/home/willy/Desktop/Modelo_Scale/5plantas')
	# N = amostras[ind_beta].shape[0]//3
	# # print(amostras[ind_beta].shape[0]//3)
	# refencia = [[]]*3
	# refencia[0] = numpy.hstack(([1]*N, [0]*N, [0]*N))
	# refencia[1] = numpy.hstack(([0]*N, [1]*N, [0]*N))
	# refencia[2] = numpy.hstack(([0]*N, [0]*N, [1]*N))
	# # print(refencia[0].shape, amostras[ind_beta].shape)
	#
	#
	# #cria os betas
	# beta = []
	# for i in range(len(refencia)):
	# 	Beta_temp = fs.beta(amostras[ind_beta], refencia[i], 8)
	# 	beta.append(Beta_temp)
	# # print(beta2[0].shape, beta2[1].shape, beta2[2].shape)
	#
	# teste, resultado = fs.Prediction(beta, Y)
	# # print(teste[0], teste[1], teste[2])
	# print(resultado[1], resultado[0], resultado[2])
	# # print(Y[1].shape[0], Y[0].shape[0], Y[2].shape[0])
	# print(((resultado[1]/Y[1].shape[0])*100).round(2), ((resultado[0]/Y[0].shape[0])*100).round(2), ((resultado[2]/Y[2].shape[0])*100).round(2))
	#
	#
	#
	# for i in range(len(Y)):
	# 	Y[i] = Y[i][:, 1:]
	#
	#
	# # print(Y[0].shape, Y[1].shape, Y[2].shape)
	# print('---------------')
	#
	# beta2 = []
	#
	# for i in range(len(Y)):
	# 	for j in range(len(refencia)):
	# 		if j == 0:
	# 			pred = fs.Predicao_python(Y[i], amostras[ind_beta], refencia[j], 8)
	# 		else:
	# 			pred = numpy.column_stack((pred, fs.Predicao_python(Y[i], amostras[ind_beta], refencia[j], 8)))
	# 	beta2.append(pred)
	#
	# resultado2 = fs.matrix_conf(beta2)
	# print(resultado2[1], resultado2[0], resultado2[2])
	# print(((resultado2[1] / Y[1].shape[0]) * 100).round(2), ((resultado2[0] / Y[0].shape[0]) * 100).round(2), ((resultado2[2] / Y[2].shape[0]) * 100).round(2))
	# # print(beta[0][0].shape, beta[1][1].shape, beta[2][2].shape)
	# # # print(beta[0], beta[1], beta[2])
	# # print(len(beta))
	# # print(beta)
	#
	#
	
	# beta = Y[1][2:, :].T #numpy.vstack((Y[0][2:, :].T, Y[1][2:, :].T, Y[2][2:, :].T))
	# numpy.savetxt('%s/''%s' % (img, '%s.txt' % nome), beta, delimiter='\t')
	# numpy.savetxt('x_fil.txt', x)
	# exporter.params['width'] = 1024
	# grafico.plot(x, y[0][:, 224], name='224', pen=(2,2))
	#grafico1.setLabels(title='Fluorescência Assintomatica', left='Intensidade', bottom='Comprimento de onda')
	# grafico.setLabel('left', "Intensidade", units='arb. units')
	# grafico.setLabel('bottom', "Comprimento de Onda", units='nm')
	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
