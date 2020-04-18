# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
import pandas as pd
import numpy as np
import csv
import StringIO 
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

globalEmissions = [0,0,'']
@app.route('/export', methods=['GET'])
def export():
	if request.method == 'GET':
		csvlist = globalEmissions
		si = StringIO.StringIO()
		cw = csv.writer(si)
		cw.writerow(["Electricite", "Gaz", "Batiment"])
		cw.writerows(csvlist)
		output = make_response(si.getvalue())
		output.headers["Content-Disposition"] = "attachment; filename=emissions.csv"
		output.headers["Content-type"] = "text/csv"
		return output

@app.route('/helper', methods=['GET','POST'])
def form_example():
    if request.method == 'POST': #this block is only entered when the form is submitted
        service = request.form['services']
        region = request.form['regions']
        emissionsTotal = CalculateEmissions(service, 2019.0, region)
        electricite = emissionsTotal[0]
        gaz = emissionsTotal[1]
        #value = u'Les emissions du service %s dans la region %s est gaz: %s electricite: %s' % (service, region, gaz, electricite)
        return ReturnAsHtml(emissionsTotal, serviceToCode[service][0], region)

data = pd.read_csv("Export_Deepki_Ready_dae.csv",sep=',')
def ReturnAsHtml(total,nom,region):
	global globalEmissions 
	globalEmissions = total
	#html = '<head><title>Bilan d\'emissions: '+ nom + '(' + region + ')' + '</title></head>'
	html = '<head><title>Bilan d\'emission</title><header><h1>Bilan d\'emission</h1></header></head>'
	html += '<body><table><tr><th>Batiment</th><th>Emissions electricite (kgCO2)</th><th>Emissions gaz (kgCO2)</th></tr>'
	for row in total:
		if row[2] == 'Total':
			html += '<tr><td>' + ' ' + '</td></tr>'
			html += '<tr><td>' + ' ' + '</td></tr>'
			html += '<tr><td>' + ' ' + '</td></tr>'
			html += '<tr><td>' + ' ' + '</td></tr>'
			html += "<tr style=\"font-weight:bold\"><td>"+row[2]+ "</td><td>"+str(row[0])+"</td><td>"+str(row[1])+"</td></tr>"
		else:
			html += "<tr><td>"+row[2]+ "</td><td>"+str(row[0])+"</td><td>"+str(row[1])+"</td></tr>"
	html += '</table>'
	html += '<form action="export" method="GET"><input type="submit" value="Export"></body>'
	return html

def GetDataPerBatiment(service, year, region):
    if service not in serviceToCode:
        return "Le service indiqué n'a pas ete trouve pour ce region."
    code = str(serviceToCode[service][1])
    return data[(data['Code bien'].str.contains(code)) & (data['Année'] == year) & (data['Région'] == region)]

def CalculateEmissions(service, year, region):
    electriciteEmission = 0.0571 #kgCO2e/kWh
    gazEmission = 0.227 #kgCO2e/kWh
    data = GetDataPerBatiment(service, year, region)
    #print data
    if data is None:
        return "Les données n'étaient pas trouvé pour ce service dans ce région."
    totalDonnee = data[['Consommation d\'électricité (kWh)','Consommation de gaz (kWh)','Nom du bien']]
    calculParBatiment = [ [0,0,'']  
             for x in range( len(data) ) ] 
    totalDonnee.reset_index(inplace=True, drop=True) 
    for idx, row in totalDonnee.iterrows():
        if row[0] > 0:
            calculParBatiment[idx][0] = row[0]*electriciteEmission
        if row[1] > 0:
            calculParBatiment[idx][1] = row[1]*gazEmission
        calculParBatiment[idx][2] = row[2]
    transpose = zip(*calculParBatiment)
    total = np.array([sum(transpose[0]), sum(transpose[1]), 'Total'])
    calculParBatiment.append(total)
    return calculParBatiment

serviceToCode = {'1':['Routes',1000007090],
                '2':['Ports maritimes et littoral',1000006785],
                '3':['Phares et balises',1000005715],
                '4':['Prevention des pollutions',1000005896],
                '5':['Protection de la nature et des paysages',1000006833],
                '6':['Direction de l\'eau',1000007063],
                '7':['MEEDDAT \(services centraux\)',1000006798],
                '8':['MEEDDAT \(services sociaux\)',1000006018],
                '9':[u'MEEDDM \(services déconcentrés\)',1000006970],
                '10':[u'Affaires maritimes \(services déconcentrés\)',1000006765],
                '11':[u'Éducation routière \(services déconcentrés\)',1000006002],
                '12':[u'DIR - Direct. Interdépart. des Routes',1000055091],
                '13':[u'DIRM- Direction interrégionale de la mer -DIRM',1000005889],
                '14':['DREAL',1000026692],
                '15':['DEAL',1000061412],
                '16':['DRIEA IDF',1000055136],
                '17':[u'SNOI - Service national des oléoducs interallié',1000005891],
                '18':['TRAPIL',1000050607],
                '19':['Culture marine',1000050192],
                '20':[u'Domaine remis aux collectivités territ.- Lois de décentralisation',1000005889],
                '21':[u'AVIATION CIVILE - Domaine régalien',1000005888],
                '22':[u'AVIATION CIVILE - Contrôle et Exploitation Aériens',1000005907],
                '23':['Chemins de fer',1000006831],
                '24':[u'Foncier d\'origine routière en Île de France',1000007093],
                '25':[u'Aménagement foncier',1000007060],
                '26':['MINISTERE ECOLOGIE, DEVELOPPEMENT DURABLE, TRANSPORT ET LOGEMENT',1000025380]}

