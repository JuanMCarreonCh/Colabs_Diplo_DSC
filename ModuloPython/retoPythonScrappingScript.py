#Reto1.-Hacer un scrapping de una pagina que tu decidas
#Vamos a Scrappear la pagina de https://www.dineroeneltiempo.com/divisas/usd-mxn/historico
# para obtener su tabla de precios del dolar por año desde 1990
## Debemos tener instalado el modulo de beautiful soup


import os
import subprocess
import sys

if __name__=='__main__':
  # Comando para instalar BeautifulSoup4
  subprocess.check_call([sys.executable, "-m", "pip", "install", "bs4"])

  # Comando para instalar pandas
  subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])

  # Comando para instalar requests
  subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

  try:
    from bs4 import BeautifulSoup as bs4
    import requests
    import pandas as pd
  except Exception as error:
    print(error)
    print('No se cuenta con las librerias necesarias, Pandas, requests y BeautifulSoup (bs4)')
    sys.exit(-1)

  #Comienza logica del programa
  url = r'https://www.dineroeneltiempo.com/divisas/usd-mxn/historico'
  page_html = requests.request(url=url,method='get')
  print(f'Estatus de la peticion {page_html.status_code}')
  if page_html.status_code == 200:
    # Parseamos el contenido de la pagina con bs
    page_soup = bs4(page_html.content,'html.parser')
    # buscamos las tablas
    tables = page_soup.findAll('table')
    headers = [i.get_text() for i in tables[0].findAll('th')]
    print(headers)
    content_table = [[j.get_text() for j in i.findAll('td')] for i in tables[0].findAll('tr')[1:]]
    #print(content_table)
    # Guardamos el contenido en un dataframe
    df = pd.DataFrame(data=content_table, columns=headers)
    # definimos los tipos de datos
    column_types = {'Año': int, 'Precio Cierre': float, 'Cambio %':str, 'Promedio':float,'Mínimo':float,'Máximo':float}
    df = df.astype(column_types)
    # Listo tenemos un dataframe con informacion historica anual del precio del dolar en Mexico
    print(df)
    print(df.dtypes)
    print(df.describe())
    if os.path.exists('DatosDescargadosReto1.csv'):
      os.remove('DatosDescargadosReto1.csv')
    # Se guarda sin indices y se pasa una codificacion ISO-8859-1 por que si se seleccioan utf los datos se 
    # meuestran de la siguiente manera
    # MÃ¡ximo en lugar de Máximo
    df.to_csv('DatosDescargadosReto1.csv',encoding='ISO-8859-1',index=False)
  else:
    print(f'No se pudo obtener la informacion de la pagina {url}')
