# Sobre este proyecto

Este proyecto trata un área de gran interés poco explorada con anterioridad. Se trata de obtener las ecuaciones que modelan el movimiento de una aeronave a partir de datos de sus trayectorias. Para ello, se utilizará la técnica de regresión dispersa o [SINDy](https://www.pnas.org/doi/10.1073/pnas.1517384113).
Se analizará si esta técnica resulta viable para esta aplicación y se darán indicaciones sobre aquellos parámetros y transformaciones que es necesario llevar a cabo para la obtención de resultados precisos.


## Índice
Esta página web se organiza de la siguiente manera:
- Se explicarán los [conceptos teóricos](./teoria.html) asociados al modelado de sistemas, ecuaciones de una aeronave y aquellos conceptos necesarios para entender la técnica propuesta en SINDy.
- Se detallarán los casos prácticos implementados:
  - [Atractores extraños](./atractores.html), se trata de los atractores de Lorenz, Rössler, Thomas y Three-Scroll Unified Chaotic System
  - [Trayectorias de aeronaves](./aeronaves.html) para el caso de un planeador, un turborreactor en vuelo rectilíneo horizontal y lazo ideal en el plano vertical

## Conclusiones
A lo largo de este proyecto se ha tratado analizar si es posible utilizar la técnica SINDy, basada en regresión dispersa, en el campo de la ingeniería aeroespacial para la predicción de las ecuaciones que modelan el comportamiento de una aeronave en vuelo a partir de datos de sus trayectorias. El resultado es positivo, es decir, es posible utilizar SINDy en este ámbito, sin embargo, puede ser necesario llevar a cabo una serie de transformaciones a las datos. Tal y como se ha visto en el capítulo anterior normalizar y, sobretodo, adimensionalizar ecuaciones complejas facilita que el algoritmo obtenga las ecuaciones correctamente.

Gracias al uso de SINDy en este campo sería posible obtener modelos más precisos simplemente a partir de los datos medidos por los sensores ya instalados. También nos permitiría obtener modelos más simples, que aunque no contengan todos los elementos de la ecuación teórica también describan de manera precisa el movimiento de la aeronave. Por otro lado, es especialmente interesante alimentar al algoritmo con utilizando datos de trayectorias breves temporalmente, ya que el algoritmo es capaz de obtener trayectorias mucho más largas en el tiempo con bastante precisión.

También se ha llegado a diversas conclusiones en cuanto a los parámetros opcionales que ofrece este algoritmo, concretamente: se ha visto en varios experimentos que utilizar múltiples trayectorias cuya condición inicial sea distinta resulta muy beneficioso; aplicar restricciones para forzar que uno de los términos aparezca en la salida del algoritmo puede empeorar el error al cambiar el punto óptimo; aportar las derivadas de las variables cuando se dispone de ellas, para evitar que el algoritmo tenga que calcularlas numéricamente, ayuda a mejorar el error; usar una suposición inicial, la cual puede mejorar el error si se utiliza un menor número de trayectorias, pero en ningún caso lo empeora; y cambiar el paso de tiempo permite al algoritmo detectar aquellos coeficientes cuyo orden de magnitud en la ecuación es pequeño.

Por último, es especialmente interesante la robustez que ofrece este algoritmo en determinados tipos de ecuaciones ante ruido. En la mayoría de casos el error ante ruidos elevados es pequeño, por lo que usar esta técnica en un entorno real (donde las trayectorias son ruidosas) puede ser muy interesante. 


## Agradecimientos
<table>
  <tr>
<td align="center"><img src="assets/images/persona_generica.png?raw=true" height="120" width="110px;" alt=""/><br /><sub><b>Pablo Solano López</b></sub><br /><a title="Code">💻</a> <a title="Documentation">📖</a></td>
  
<td align="center"><a href="https://github.com/vmtenorio"><img src="https://github.com/vmtenorio/vmtenorio.github.io/blob/master/images/vmtg.jpg?raw=true" height="120" width="100px;" alt=""/><br /><sub><b>Víctor Manuel Tenorio Gómez</b></sub></a><br /><a title="Code">💻</a> <a title="Answering Questions">💬</a> <a title="Documentation">📖</a> <a title="Reviewed Pull Requests" >👀</a></td>

<td align="center"><img src="https://raw.githubusercontent.com/meridiaz/MLOps-Evaluation/gh-pages/assets/images/mother.jpg" height="120" width="100px;" alt=""/><br /><sub><b>My mother</b></sub><br /><a title="Code">💻<a title="Reviewed Pull Requests" >👀</a> <strong> ❤️ </strong></a></td>
</tr>  
</table>
