# -*- coding: utf-8 -*-
import connectorBehavior
import displayGroupOdbToolset as dgo
import xyPlot
import visualization
import sketch
import job
import optimization
import mesh
import load
import interaction
import step
import assembly
import material
import part
import displayGroupMdbToolset as dgm
import regionToolset
import section
from abaqus import *
from abaqusConstants import *
import __main__

# Para ler as áreas
import csv

# MUDAR ISSO ANTES DE RODAR!
basedir = 'C:/Users/FOUSP/Documents/01_Ensino/02_PosGraduacao/PMR5251/Larissa/Aula02/AbaqusPython'


# Para gravar em um csv único
from datetime import datetime
now = datetime.now().strftime("%Y-%m-%d_%H-%M")
result_csv = '{0}/dados_trelica_{1}.csv'.format(basedir, now)

# Imports do ABAQUS

# Grava os cabeçalhos da saída
with open(result_csv, 'w') as f:
    f.write('iteration,{},'.format(
        ','.join(['area{}'.format(x) for x in range(1, 11)])))
    f.write('{},'.format(','.join(['d{}'.format(x) for x in range(1, 9)])))
    f.write('{},'.format(','.join(['s11_{}'.format(x) for x in range(1, 11)])))
    f.write('{}\n'.format(
        ','.join(['mises_{}'.format(x) for x in range(1, 11)])))

# Lê as áreas geradas
with open('{0}/areas.csv'.format(basedir), 'rb') as f:
    reader = csv.reader(f)
    todas_as_areas = []
    for row in reader:
        todas_as_areas.append([float(x) for x in row])

len_areas = len(todas_as_areas)

# Importa o arquivo de entrada gerado
mdb.ModelFromInputFile(
    name='newinput', inputFileName='{0}/BasicInput.inp'.format(basedir))

session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
a = mdb.models['newinput'].rootAssembly

# Garante a funcionalidade do código anterior, mantendo o nome do modelo
del mdb.models['Model-1']

mdb.models.changeKey(fromName='newinput', toName='Model-1')


# Altera as áreas das seções transversais para um vetor ordenado "areas"
def muda_secoes(areas):
    mdb.models['Model-1'].sections['Section-1-SET-9'].setValues(
        material='PAPER-ALUMINUM-6061', area=areas[0])
    mdb.models['Model-1'].sections['Section-2-SET-12'].setValues(
        material='PAPER-ALUMINUM-6061', area=areas[1])
    mdb.models['Model-1'].sections['Section-3-SET-13'].setValues(
        material='PAPER-ALUMINUM-6061', area=areas[2])
    mdb.models['Model-1'].sections['Section-4-SET-14'].setValues(
        material='PAPER-ALUMINUM-6061', area=areas[3])
    mdb.models['Model-1'].sections['Section-5-SET-8'].setValues(
        material='PAPER-ALUMINUM-6061', area=areas[4])
    mdb.models['Model-1'].sections['Section-6-SET-11'].setValues(
        material='PAPER-ALUMINUM-6061', area=areas[5])
    mdb.models['Model-1'].sections['Section-7-SET-10'].setValues(
        material='PAPER-ALUMINUM-6061', area=areas[6])
    mdb.models['Model-1'].sections['Section-8-SET-6'].setValues(
        material='PAPER-ALUMINUM-6061', area=areas[7])
    mdb.models['Model-1'].sections['Section-9-SET-7'].setValues(
        material='PAPER-ALUMINUM-6061', area=areas[8])
    mdb.models['Model-1'].sections['Section-10-SET-15'].setValues(
        material='PAPER-ALUMINUM-6061', area=areas[9])


for i, areas in enumerate(todas_as_areas):
    # Define a área da seção transversal
    muda_secoes(areas)

    # Cria o trabalho e o executa
    mdb.Job(name='Bar10_Job', model='Model-1',
            description='10 bar Structure', type=ANALYSIS, atTime=None,
            waitMinutes=0, waitHours=0, queue=None, memory=90,
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
            scratch='', resultsFormat=ODB)
    mdb.jobs['Bar10_Job'].submit(consistencyChecking=OFF)
    mdb.jobs['Bar10_Job'].waitForCompletion()
    session.mdbData.summary()
    o3 = session.openOdb(name='C:/temp/Bar10_Job.odb')
    session.viewports['Viewport: 1'].setValues(displayedObject=o3)
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
        DEFORMED, ))

    # Para retirar os dados
    odb = session.odbs['C:/temp/Bar10_Job.odb']
    # Retirando os deslocamentos
    session.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=(('U',
                                                                          NODAL), ), nodeLabels=(('TRELICA-1', (1, 2, 3, 4)), ))
    print('{} of {}'.format(i+1, len_areas))
    dx = [
        session.xyDataObjects['U:U1 PI: TRELICA-1 N: {}'.format(x)][1][1] for x in range(1, 5)]
    dy = [
        session.xyDataObjects['U:U2 PI: TRELICA-1 N: {}'.format(x)][1][1] for x in range(1, 5)]
    # Os nós no Abaqus são diferentes da figura do paper.
    # O código abaixo respeita a ordem da figura
    deslocamentos = [dx[3], dy[3], dx[0], dy[0], dx[2], dy[2], dx[1], dy[1]]

    # Tensões
    session.xyDataListFromField(odb=odb, outputPosition=INTEGRATION_POINT,
                                variable=(('S', INTEGRATION_POINT,
                                           ((COMPONENT, 'S11'), )), ),
                                elementSets=(" ALL ELEMENTS", ))

    session.xyDataListFromField(odb=odb, outputPosition=INTEGRATION_POINT,
                                variable=(('S', INTEGRATION_POINT,
                                           ((INVARIANT, 'Mises'), )), ),
                                elementSets=("TRELICA-1.SET-1", ))

    # A ordem das tensões com certeza está diferente da figura, mas não é muito relevante
    mises = [
        session.xyDataObjects['S:Mises PI: TRELICA-1 E: {} IP: 1'.format(x)][1][1] for x in range(1, 11)]
    s11 = [
        session.xyDataObjects['S:S11 PI: TRELICA-1 E: {} IP: 1'.format(x)][1][1] for x in range(1, 11)]

    # Adiciona ao arquivo de saída os deslocamentos obtidos nessa iteração
    with open(result_csv, 'a') as f:
        f.write('{},{},'.format(i, ','.join((str(x) for x in areas))))
        f.write('{},'.format(','.join((str(x) for x in deslocamentos))))
        f.write('{},'.format(','.join((str(x) for x in s11))))
        f.write('{}\n'.format(','.join((str(x) for x in mises))))

    # session.writeXYReport(fileName='C:/temp/trelica_dados_{}.rpt'.format(now), xyData=(x0, x1, x2,
    #                                                                                   x3, x4, x5))

    xyKeys = session.xyDataObjects.keys()
    for key in xyKeys:
        del session.xyDataObjects[key]


print("END!!!! ;)")
