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

import numpy
import pandas
import pyqtgraph as pg
from Functions import functions_Fil as fs

def main(args):
    c = '/home/willy/PycharmProjects/Eq_1_MMO_29_03_2018'
    d = '/home/willy/PycharmProjects/FIL_Citrosuco_22_03_2018_7_5s_C'
    ym = pandas.read_csv('/home/willy/PycharmProjects/YMedios_Eq.txt', '\t', header=None)
    ymedio = numpy.array(ym)[:, 1]
    x, m = fs.Carrega_Arquivos(c, 1)
    z = fs.Boxcar(m[0][:, 0], 10)
    s, f = fs.Corte(x, z, 494.3046, 758.7687)
    off = fs.Offset(f)
    t = fs.Produto_Scalar(f, ymedio)
    print(t)
    print(s.shape, f.shape)
    pg.plot(s, off)
    pg.QtGui.QApplication.exec_()
    A = m[0]
    B = m[1]
    C = m[2]
    print(A.shape)
    print(B.shape)
    print(C.shape)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))