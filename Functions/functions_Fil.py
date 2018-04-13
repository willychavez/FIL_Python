import os
import pandas
import numpy



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


def Corte(x, y, x1, x2):
	ind = numpy.nonzero((x > x1) & (x < x2))
	X = x[ind]
	Y = y[ind]
	return X, Y


def Offset(y, valor_y=0):
	Y = numpy.zeros_like(y)
	if valor_y > 0:
		Y = y - valor_y
		return Y
	else:
		m = y.min()
		Y = y - m
		return Y


def Produto_Scalar(y, yref):
	norm_ym = numpy.linalg.norm(yref)
	norm_y = numpy.linalg.norm(y)
	print(y.shape, yref.shape)
	if y.shape[0] == yref.shape[0]:
		costheta = y.dot(yref.transpose()) / (norm_y * norm_ym)
		return costheta
	else:
		costheta = y.dot(yref) / (norm_y * norm_ym)
		return costheta


