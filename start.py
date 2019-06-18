# -*- coding: utf-8 -*-

from flask import Flask, render_template
from lib import DadosAbertos

app = Flask(__name__)
partidos_info = []

@app.route("/")
def deputados():
   obj = DadosAbertos()
   list_dep = obj.deputados()

   return render_template('lista.html', listas=list_dep)

@app.route("/gastos/<id>")
def deputado(id):
   obj    = DadosAbertos()
   info   = obj.deputado_id(id)
   gastos = obj.deputado_despesas(id)

   valores = {}
   for gasto in gastos:
       data = str(gasto['mes']) + '/' + str(gasto['ano'])

       if data in valores:
          valores[data] += gasto['valorLiquido']    
       else:
          valores[data] = gasto['valorLiquido']   
       
   line_labels = valores.keys()
   line_values = valores.values()

   return render_template('gastos.html', title='Gráfico de Gastos', max=10000, labels=line_labels, values=line_values)

@app.route("/partidosGastos")
def partidos():
   obj    = DadosAbertos()
   partidos   = obj.partidos()
   info = {}
   for partido in partidos:
      info['sigla'] = partido['sigla']
      info['nome'] = partido['nome']
      info['deputados'] = obj.deputados_partido(partido['sigla'])
      info['gastos'] = gastos_por_partido(info['deputados'])
      partidos_info.append(info.copy())
      
  
   return render_template('listaPartidos.html', partidos=partidos_info)

def gastos_por_partido(deputados):
   obj = DadosAbertos()
   gastos = {}
   gastosPassagemAerea = 0
   detalhesPassagemAerea = []
   gastosCombustiveisLubrificantes = 0
   detalhesCombustiveisLubrificantes = []
   gastosAlimentacao = 0
   detalhesAlimentacao = []
   gastosApoioAtividade = 0
   detalhesApoioAtividade = []
   for deputado in deputados:
      despesas = obj.deputado_despesas(deputado['id'])
      info = {}
      info['deputado'] = deputado['nome']
      for despesa in despesas:
         if(despesa['tipoDespesa'] == "COMBUSTÍVEIS E LUBRIFICANTES."):
            gastosCombustiveisLubrificantes += despesa['valorLiquido']
            info['despesa'] = despesa
            detalhesCombustiveisLubrificantes.append(info.copy())
         if(despesa['tipoDespesa'] == "PASSAGENS AÉREAS"):
            gastosPassagemAerea += despesa['valorLiquido']
            info['despesa'] = despesa
            detalhesPassagemAerea.append(info.copy())
         if(despesa['tipoDespesa'] == "FORNECIMENTO DE ALIMENTAÇÃO DO PARLAMENTAR"):
            gastosAlimentacao += despesa['valorLiquido']
            info['despesa'] = despesa
            detalhesAlimentacao.append(info.copy())
         if(despesa['tipoDespesa'] == "MANUTENÇÃO DE ESCRITÓRIO DE APOIO À ATIVIDADE PARLAMENTAR"):
            gastosApoioAtividade += despesa['valorLiquido']
            info['despesa'] = despesa
            detalhesApoioAtividade.append(info.copy())
   gastos['gastosPassagemAerea'] = gastosPassagemAerea
   gastos['detalhesPassagemAerea'] = detalhesPassagemAerea
   gastos['gastosCombustiveisLubrificantes'] = gastosCombustiveisLubrificantes
   gastos['detalhesCombustiveisLubrificantes'] = detalhesCombustiveisLubrificantes
   gastos['gastosAlimentacao'] = gastosAlimentacao
   gastos['detalhesAlimentacao'] = detalhesAlimentacao
   gastos['gastosApoioAtividade'] = gastosApoioAtividade
   gastos['detalhesApoioAtividade'] = detalhesApoioAtividade
   return gastos

@app.route("/detalheGastos/<sigla>")
def detalheGastos(sigla):
   detalhes_partido = {}
   for partido in partidos_info:
      if(partido['sigla'] == sigla):
         detalhes_partido = partido
         break

   return render_template('detalheGastos.html', partido=detalhes_partido)


if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True, port=8080)
