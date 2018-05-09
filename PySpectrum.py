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
    nome = 'FIL_08_05_2018.arff'
    w = '/home/willy/Documents/Av_temporal/08_05_2018/Equipamentos/weka'
    wf = '/home/willy/Documents/Av_temporal/08_05_2018/Fil/weka'
    
    c = '/home/willy/Documents/Av_temporal/08_05_2018/Equipamentos/Eq_1_MMO_08_05_2018'
    d = '/home/willy/Documents/Av_temporal/08_05_2018/Fil/FIL_Citrosuco_08_05_2018'
    
    ie = '/home/willy/Documents/Av_temporal/08_05_2018/Equipamentos/Imagens'
    If = '/home/willy/Documents/Av_temporal/08_05_2018/Fil/Imagens'
    
    ym = pandas.read_csv('/home/willy/PycharmProjects/YMedios_Eq.txt', '\t', header=None)
    ymedio = numpy.array(ym)[:, 1]
    x, m = fs.Carrega_Arquivos(d, 1)
    
    #Corte Equipamento1
    x1 = 494.3046
    x2 = 758.7687
    
    #Corte Equipamento2
    x3 = 492.1631
    x4 = 758.7687
    
    #Cortes FIL
    x5 = 444.2869
    x6 = 819.9622
    
    ind = fs.Corte(x, x5, x6)
    
    x = x[ind]
    y = []
    for j in range(len(m)):
        for i in range(m[j].shape[1]):
            if i == 0:
                y_temp = m[j][:, i]
                yy = fs.Normaliza(fs.Offset(fs.Boxcar(y_temp, 20)[ind]), x)
            else:
                y_temp = m[j][:, i]
                yy = numpy.column_stack((yy, fs.Normaliza(fs.Offset(fs.Boxcar(y_temp, 20)[ind]), x)))
        y.append(yy)
    print(y[0].shape)

    
    ga.Gera_Arff(x,y,'%s/''%s' % (wf, nome))
    
    # s, f = Corte(x, z, 494.3046, 758.7687
    # off = Offset(f)
    # t = Produto_Scalar(f, ymedio)
    # print(t)
    # print(s.shape, f.shape)
    grafico = pg.plot()
    #grafico.addLegend()
    for i in range(y[1].shape[1]):
        grafico.plot(x, y[1][:, i], pen=(i, y[1].shape[1]))
    grafico.setTitle('Sadia')
    grafico.setLabels(left='Intensidade (u.a.)', bottom='Comprimento de Onda (nm)')
    # grafico.setLabel('left', "Intensidade", units='u.a')
    # grafico.setLabel('bottom', "Comprimento de Onda", units='nm')
    # pg.QtGui.QApplication.exec_()
    # exporter = pg.exporters.ImageExporter(grafico.plotItem)
    # exporter.params.param('width').setValue(1024, blockSignal=exporter.widthChanged)
    # exporter.params.param('height').setValue(768, blockSignal=exporter.heightChanged)
    # exporter.export('%s/''%s' % (ie, 'Sadia2.png'))
    
    grafico1 = pg.plot()
    #grafico1.addLegend()
    for i in range(y[0].shape[1]):
        grafico1.plot(x, y[0][:, i], pen=(i, y[0].shape[1]))
    grafico1.setTitle('Assintomatica')
    grafico1.setLabels(left='Intensidade (u.a.)', bottom='Comprimento de Onda (nm)')
    # grafico1.setLabel('left', "Intensidade", units='arb. units')
    # grafico1.setLabel('bottom', "Comprimento de Onda", units='nm')
    # pg.QtGui.QApplication.exec_()
    # exporter = pg.exporters.ImageExporter(grafico1.plotItem)
    # exporter.params.param('width').setValue(1024, blockSignal=exporter.widthChanged)
    # exporter.params.param('height').setValue(768, blockSignal=exporter.heightChanged)
    # exporter.export('%s/''%s' % (ie, 'Assintomatica2.png'))

    grafico2 = pg.plot()
    #grafico2.addLegend()
    for i in range(y[2].shape[1]):
        grafico2.plot(x, y[2][:, i],pen=(i, y[2].shape[1]))
    grafico2.setTitle('Sintomatica')
    grafico2.setLabels(left='Intensidade (u.a.)', bottom='Comprimento de Onda (nm)')
    # grafico2.setLabel('left', "Intensidade", units='u.a')
    # grafico2.setLabel('bottom', "Comprimento de Onda", units='nm')
    # pg.QtGui.QApplication.exec_()
    # exporter = pg.exporters.ImageExporter(grafico2.plotItem)
    # exporter.params.param('width').setValue(1024, blockSignal=exporter.widthChanged)
    # exporter.params.param('height').setValue(768, blockSignal=exporter.heightChanged)
    # exporter.export('%s/''%s' % (ie, 'Sintomatica2.png'))

    pg.QtGui.QApplication.exec_()
    exporter = pg.exporters.ImageExporter(grafico.plotItem)
    exporter.params.param('width').setValue(1024, blockSignal=exporter.widthChanged)
    exporter.params.param('height').setValue(768, blockSignal=exporter.heightChanged)
    exporter.export('%s/''%s' % (If, 'Sadia.png'))
    exporter = pg.exporters.ImageExporter(grafico1.plotItem)
    exporter.params.param('width').setValue(1024, blockSignal=exporter.widthChanged)
    exporter.params.param('height').setValue(768, blockSignal=exporter.heightChanged)
    exporter.export('%s/''%s' % (If, 'Assintomatica.png'))
    exporter = pg.exporters.ImageExporter(grafico2.plotItem)
    exporter.params.param('width').setValue(1024, blockSignal=exporter.widthChanged)
    exporter.params.param('height').setValue(768, blockSignal=exporter.heightChanged)
    exporter.export('%s/''%s' % (If, 'Sintomatica.png'))

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
