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
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

#from Functions import *

def main(args):
    fc = '/home/willy/Documents/Novo_Conj_Dados/Mensal/08_05_2018/Folhas'
    w = '/home/willy/Documents/Novo_Conj_Dados/Mensal/08_05_2018/weka'
    img = '/home/willy/Documents/Novo_Conj_Dados/Mensal/08_05_2018/Imagens'
    cy1 = '/home/willy/PycharmProjects/YMedios_Eq.txt'
    cy3 = "/home/willy/PycharmProjects/YMedios_FIL.txt"
    nome1 = 'Eq_1_08_05_2018.arff'
    nome2 = 'Eq_2_08_05_2018.arff'
    nome3 = 'FIL_08_05_2018.arff'
    c1 = '/home/willy/Documents/Novo_Conj_Dados/Mensal/08_05_2018/Equipamentos/Eq_1_MMO_08_05_2018'
    c2 = '/home/willy/Documents/Novo_Conj_Dados/Mensal/08_05_2018/Equipamentos/Eq_2_MMO_08_05_2018'
    c3 = '/home/willy/Documents/Novo_Conj_Dados/Mensal/08_05_2018/Fil/FIL_Citrosuco_08_05_2018'

    cym = cy1
    indice = 1
    nome = nome1
    caminho = c1
    nomeimg1 = "1Sadia"
    nomeimg2 = "1Assintomatica"
    nomeimg3 = "1Sintomatica"
    


    ym = pandas.read_csv('%s' % cym, '\t', header=None)
    ymedio = numpy.array(ym)
    print(ymedio.shape)
    
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
    print(y[0].shape)
    
    folhas = fs.Identifica(fc)
    
    #Carrega identificação das folhas
    Y = [[]] * len(y)
    for i in range(len(y)):
        Y[i] = numpy.vstack((folhas[i], y[i]))

    print(Y[0].shape, Y[1].shape, Y[2].shape)
    
    
    #remove outliers
    for i in range(len(y)):
        cont = 0
        j = 0
        while j < y[i].shape[1]:
            cosseno_tetta = fs.Produto_Scalar(y[i][:, j], ymedio[:, i])
            if cosseno_tetta < 0.899:
                if cont == 0:
                    Y[i] = numpy.delete(Y[i], j, 1)
                    cont = 1
                else:
                    Y[i] = numpy.delete(Y[i], (j - cont), 1)
                    cont += 1
            j += 1

    print(Y[0].shape, Y[1].shape, Y[2].shape)
    
    #Gera arquivo.arff
    ga.Gera_Arff_Ind(x, Y, '%s/''%s' % (w, '%s' % nome))


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

    # exporter.params['width'] = 1024
    # grafico.plot(x, y[0][:, 224], name='224', pen=(2,2))
    #grafico1.setLabels(title='Fluorescência Assintomatica', left='Intensidade', bottom='Comprimento de onda')
    # grafico.setLabel('left', "Intensidade", units='arb. units')
    # grafico.setLabel('bottom', "Comprimento de Onda", units='nm')
    # A = m[0]
    # B = m[1]
    # C = m[2]
    # print(A.shape)
    # print(B.shape)
    # print(C.shape)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
