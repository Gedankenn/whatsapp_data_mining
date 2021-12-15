# -*- coding : utf-8 -*-
# author: Fabio S. Stella

import pandas as pd
import numpy as np
import sys
import datetime
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages as pdf

amostras = 6


class contato:
	""" A classe :class:`contato` implementa a strutura de dados contendo
	todas as informações necessarias para cada contato
	"""
	nome = ''

	def __init__(self):
		self.total_mes = [0]*13
		self.total = 0
		self.palavras_faladas = []
		self.total_horas_mes = [0]*24
		self.palavras_faladas_mes = []
		self.palavras_total = []
		self.horas_ano = []

	def pal(self, palavra):
		palavra = palavra.lower()
		if len(palavra) > 4 and 'kkkk' not in palavra and 'ahah' not in palavra:
			tam = len(self.palavras_faladas)
			cont = 0
			while cont < tam and self.palavras_faladas[cont][0] != palavra:
				cont = cont+1
			if cont < tam:
				if self.palavras_faladas[cont][0] == palavra:
					self.palavras_faladas[cont][1] = str(1+int(self.palavras_faladas[cont][1]))
			else:
				self.palavras_faladas.extend([[palavra,'1']])
		if len(palavra) > 4 and 'kkkk' not in palavra and 'ahah' not in palavra and len(palavra) < 8:
			cont = 0
			tam = len(self.palavras_total)
			while cont < tam and self.palavras_total[cont][0] != palavra:
				cont = cont+1
			if cont < tam:
				if self.palavras_total[cont][0] == palavra:
					self.palavras_total[cont][1] = 1+self.palavras_total[cont][1]
			else:
				self.palavras_total.extend([[palavra,1]])
	def msg(self,hora,mes):
		self.total_mes[mes]=self.total_mes[mes]+1
		self.total_horas_mes[hora]=self.total_horas_mes[hora]+1

	def maisfalada(self, mes, ano):
		self.palavras_faladas.sort(key = lambda x: x[1], reverse=True)
		tam = len(self.palavras_faladas)
		cont = 0
		falada=''
		while cont < tam and cont < amostras+4:
			#print(self.palavras_faladas[cont])
			falada=falada+str(self.palavras_faladas[cont])+'\n'
			self.palavras_faladas_mes.extend([[falada,mes,ano]])
			cont=cont+1
		self.palavras_faladas=[]
		return falada

	def trocames(self, mes):
		self.total=self.total+self.total_mes[int(mes)]
		self.horas_ano.append([self.total_horas_mes,mes])
		self.total_horas_mes = [0]*24

	def maisfaladas_total(self):
		self.palavras_total.sort(key = lambda x: x[1], reverse=True)
		tam = len(self.palavras_total)
		cont = 0
		total=''
		while cont < tam and cont < amostras:
			total = total+str(self.palavras_total[cont])+'\n'
			cont=cont+1
		return total
	
	def trocaano(self):
		self.total_mes = [0]*13
		self.palavras_faladas_mes=[]
		self.horas_ano=[]


ps = []
relatorio='---------====== relatorio gerado as: ' + str(datetime.datetime.now()) +' ======---------\n'
historico = sys.argv[1]
arquivo = open(historico,'r',encoding = "utf-8")
data = arquivo.readlines()
historico.strip('.txt')
historico=historico+'_graficos.pdf'
pp=pdf(historico)

dia = 0
mes = 0
mes_anterior = 0
ano_anterior = 0
ano = 0
horas = 0
minutos = 0
x_axis = np.arange(24)
mes_x_axis = np.arange(13)

for line in data:
	#print(line)
	if line[0] != '\n' and len(line) > 18 and ' - ' in line and ': ' in line and '/' in line and '<Arquivo' not in line and line[2] == '/' :
		palavra = line.split(' - ',1)
		mes_anterior=mes
		ano_anterior=ano
		#aquisicao da data
		#print(line)
		data = palavra[0].split()
		data1 = data[0].split("/")
		dia = data1[0]
		mes = data1[1]
		ano = data1[2]

		#aquisição da hora
		tempo = data[1].split(":")
		horas = tempo[0]
		minutos = tempo[1]

		#gera os graficos do mes anterior
		if mes_anterior!=mes and mes_anterior!= 0:
			legenda =[]
			relatorio = relatorio+'\n\nrelatorio de: '+str(mes_anterior)+'/'+str(ano_anterior)+ '\n'
			for p in ps:
				relatorio=relatorio+'palavras mais faladas por: '+p.nome+'\n'+p.maisfalada(mes_anterior,ano_anterior)+'-----------------\n'
				plt.plot(x_axis,p.total_horas_mes)
				legenda.append(p.nome)
				p.trocames(mes_anterior)
			relatorio=relatorio+'\n\n'
			title='horas do mes: '+mes_anterior+' '+ano_anterior
			plt.title(title)
			plt.xlabel("horas")
			plt.ylabel("total mensagens")
			plt.xticks(np.arange(0,23,2))
			plt.xlim(0,23)
			plt.legend(legenda)
			plt.grid(True)
			#plt.show() #mostra o grafico
			pp.savefig() #salva o grafico em pdf na figura
			plt.clf() #limpa grafico anterior.


		#Gera os graficos para o ano todo
		if ano != ano_anterior and ano_anterior!= 0:
			legenda = []
			for p in ps:
				plt.plot(mes_x_axis,p.total_mes)
				legenda.append(p.nome)
				#p.trocaano()
			title='Total de mensagens no ano: '+ano_anterior
			plt.title(title)
			plt.xlabel("meses")
			plt.xticks(np.arange(1,12,1))
			plt.xlim(1,12)	
			plt.legend(legenda)
			plt.grid(True)
			pp.savefig()
			plt.clf()

			#Grafico compilando as horas de todos os meses em 1 unico grafico
			for p in ps:
				legenda=[]
				for hora in p.horas_ano:
					plt.plot(x_axis,hora[0])
					texto='mes: '+hora[1]
					legenda.append(texto)
					texto=''
				texto='Compilado horas de: '+p.nome
				plt.title(texto)
				plt.xticks(np.arange(0,23,2))
				plt.xlim(0,23)
				plt.legend(legenda)
				plt.xlabel('horas')
				plt.grid(True)
				pp.savefig()
				plt.clf()
				p.trocaano()

		#aquisição do nome
		data2 = palavra[1].split(': ',1)
		nome = data2[0]
		
		#achando posicao do vetor
		cont_p = 0
		tam = len(ps)
		
		while cont_p < tam and ps[cont_p].nome != nome:
			cont_p=cont_p+1
		if cont_p == tam:
			p1 = contato()
			p1.nome = nome
			ps.append(p1)

		ps[cont_p].msg(int(horas),int(mes)) #envia para contador de msgs

		#print(data2)
		palavra = data2[1].split()
		cont=0
		tam = len(palavra)
		word = ''
		while cont<tam:
			word = palavra[cont]
			ps[cont_p].pal(word)
			cont=cont+1

print('------ Teste saida  -----------------')
print(relatorio)

print("------ Mais Faladas Total -----------")
for p in ps:
	print(p.nome)
	print(p.maisfaladas_total())
	p.palavras_total.sort(key = lambda x: x[1], reverse=True)
	cont = 0
	while cont < amostras and cont < len(p.palavras_total):
		x=p.palavras_total[cont][0]
		y=p.palavras_total[cont][1]
		plt.bar(x,y)
		cont=cont+1
	titulo='Numero de palavras mais faladas de: '+p.nome
	plt.title(titulo)
	plt.grid(True)
	pp.savefig() #salva o grafico em pdf na figura
	plt.clf() #limpa grafico anterior.
	p.trocames(mes_anterior)
for p in ps:
	legenda=[]
	for hora in p.horas_ano:
		plt.plot(x_axis,hora[0])
		texto='mes: '+hora[1]
		legenda.append(texto)
		texto=''
	texto='Compilado horas de: '+p.nome
	plt.title(texto)
	plt.xticks(np.arange(0,23,2))
	plt.xlim(0,23)
	plt.legend(legenda)
	plt.xlabel('horas')
	plt.grid(True)
	pp.savefig()
	plt.clf()

pp.close()
arquivo.close()