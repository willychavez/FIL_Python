#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#  Copyright 2018 Willy Chavez <wchavezmareco@gmail.com>
#
#  This program is free software you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
import sys; sys.dont_write_bytecode = True # não gera arquivos pyc

def Gera_Arff(x,y,nome_aquivo):
	arq = open('%s' % nome_aquivo, 'w')
	arq.write('@RELATION Diagnostico \n')
	arq.write('\n')
	# o primeiro atributo sera o nome da folha
	for i in range(len(x)):
		arq.write('@ATTRIBUTE %s  NUMERIC \n' % x[i])
	
	arq.write('@ATTRIBUTE class {Sadia,Assintomatica,Sintomatica} \n')
	arq.write('\n')
	arq.write('@DATA \n')
	
	for l in range(y[1].shape[1]):
		for j in range(y[1].shape[0]):
			arq.write('%.5f,' % y[1][j, l])
		arq.write('Sadia\n')
		
	for l in range(y[0].shape[1]):
		for j in range(y[0].shape[0]):
			arq.write('%.5f,' % y[0][j, l])
		arq.write('Assintomatica\n')

	for l in range(y[2].shape[1]):
		for j in range(y[2].shape[0]):
			arq.write('%.5f,' % y[2][j, l])
		arq.write('Sintomatica\n')
	
	arq.close()