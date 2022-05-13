# Viabilidad del uso de la técnica de regresión dispersa sobre trayectorias de aeronaves
Este proyecto trata de evaluar la viabilidad del uso de la técnica de regresión dispersa (*sparse* en inglés) para recuperar las ecuaciones que modelan el movimiento de una aeronave en vuelo a partir de datos de sus trayectorias. Para ello se utiliza el paquete de Python PySINDy que se basa en la técnica [Sparse Identification of Nonlinear Dynamics (SINDy)](https://www.pnas.org/doi/pdf/10.1073/pnas.1517384113). Se han desarrollado varios casos de uso de esta herramienta, el primero son casos de juguete sobre atractores extraños y el segundo sobre trayectorias de aeronaves que se resumen en la siguiente imagen 

![tabla de casos de aeroanves](/../gh-pages/assets/images/tabla_casos_aeronaves2.png)

Para más información se dirige a [la página web del proyecto](https://meridiaz.github.io/id-dispersa-aeronaves/) en la cual es posible leer un resumen de los resultados del mismo y donde descargar la memoria completa en formato PDF.

## Organización del respositorio
La organización del repositorio es la siguiente:
- `atractores_extraños/` en esta carpeta encuentran los siguientes jupyter notebook:
  - `3_original_paper.ipynb` contiene ejemplos sencillos de aplicación de SINDy, como por ejemplo ecuaciones lineales de segundo y tercer orden y en ecuaciones diferenciales en derivadas parciales, entre otros. Este notebook ha sido desarrollado por los propios creadores de PySINDy y puede ser encontrado en su [repositorio](https://github.com/dynamicslab/pysindy) junto a otros ejemplos.
  - `atractores_extraños.ipynb` contiene casos de aplicación de SINDy para los atractores extraños de Lorenz, Rössler, Thomas y Three-Scroll Unified System.
- `casos_aeronave/` se encuentran los siguientes jupyter notebook:
  - `caso-X.ipynb` contiene el análisis sobre la variación de los parámetros del algoritmo para mejorar las ecuaciones obtenidas por el algoritmo SINDy. 
  - `ablation_study.ipynb` contiene un análisis sobre los 6 casos desarrollados. En concreto se analiza el tiempo de ejecución y se obtiene en un gráfico de barras el error en los coeficientes entre la ecuación teórica y predicha de cada caso.
  - `planeador_test.ipynb` contiene el caso de uso de SINDy sobre la trayectoria de un planeador sin empuje en descenso.
  - `turborreactor_test.ipynb` contiene un resumen de los archivos `caso-B.ipynb`, `caso-C-1.ipynb`, `caso-C-2.ipynb`, `caso-D-1.ipynb`y `caso-D-2.ipynb`. En este único fichero se obtienen trayectorias sintéticas de cada caso y se alimenta al algoritmo con ellas.
  - `utils.py` es el fichero que contiene las clases y métodos necesarios para llevar a cabo la variación de los parámetros de los ficheros `caso-X.ipynb`.
  
## Versiones necesarias  
Para ejecutar estos archivos es necesaria la **versión 3.8.10 de Python** y la **versión 1.6.3 de PySINDy**. Para instalar este último tan solo es necesario ejecutar el comando `pip install pysindy`.
