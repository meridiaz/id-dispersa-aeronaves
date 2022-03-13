# Conceptos teóricos
Los conceptos teóricos asociados a este proyecto pueden dividirse en dos partes: 
- La primera comprende los conceptos asociados al modelado matemático de sistemas y las ecuaciones generales de la mecánica de vuelo
- La segunda tiene que ver con el funcionamiento del algoritmo SINDY

## Modelado de sistemas

### Sistemas dinámicos

El modelado matemático de sistemas es una tarea que puede resultar muy compleja a la par que necesaria para entender el mundo que nos rodea. Nos permite describir las variables de las que depende un sistema así como las relaciones existentes existentes entre ellas. Gracias a ello somos capaces de entender su funcionamiento y conocer cualquier estado de dicho sistema

De manera general un sistema consiste en un conjunto de componentes interconectados, construidos con un propósito determinado. En la naturaleza es posible encontrar sistemas estáticos, cuya salida depende únicamente del valor de la entrada, y modelos dinámicos, cuya salida depende
del valor pasado y presente de la variable de entrada.

Un sistema dinámico es la representación matemática abstracta que modela un fenómeno creado por el hombre, biológico o físico que cambia con el
tiempo. En concreto, define los elementos que intervienen en él y las relaciones entre ellos. Estos sistemas se pueden representar mediante un conjunto de ecuaciones diferenciales ordinarias y ecuaciones en derivadas parciales 
(ambos en el caso de sistemas continuos) o por transformaciones discretas, típicamente ecuaciones en diferencias como la que se muestra a continuación


<img src="https://render.githubusercontent.com/render/math?math=\frac{dx}{dt} = f(x(t)).">


A través de estas ecuaciones diferenciales somos capaces de describir fenómenos como la expansión de una enfermedad, [atractores](./atractores.html) o modelar el comportamiento de una aeronave en vuelo

### Sistema de referencia y ecuaciones de una aeronave

Un sistema de referencia es un conjunto de coordenadas medidas en el espacio y tiempo necesarias para determinar la posición de un punto en el espacio. Es decir, es el conjunto de convenciones que un observador necesita para medir magnitudes físicas en un sistema mecánico. Los sistema de referencia son necesarios para entender el contexto y dimensiones sobre las que se desarrolla el movimiento de un cuerpo. En la mecánica de vuelo existen diversos sistemas de referencia: sistema de referencia inercial, sistema de referencia geocéntrico giratorio, sistema de ejes tierra, sistema de ejes de horizonte local, sistema de ejes cuerpo y sistema de ejes viento. Excepto los dos últimos, todos ellos son sistemas de referencia inerciales. Esto es que no es necesario considerar fuerzas ficticias ni la aceleración de Coriolis en el lado derecho de la ecuación.

Los sistemas ejes cuerpo y viento son sistemas no inerciales, es decir, su posición no es fija respecto un punto y no se puede utilizar la expresión 

<img src="https://render.githubusercontent.com/render/math?math=F = m\frac{d^2x}{dt^2}">. 

En concreto, el sistema utilizado en este proyecto será el sistema de **ejes viento** denotado como <img src="https://render.githubusercontent.com/render/math?math=F_w(O_w, x_w, y_w, z_w)">, donde <img src="https://render.githubusercontent.com/render/math?math=O_w"> es el centro u origen del sistema y <img src="https://render.githubusercontent.com/render/math?math=x_w, y_w, z_w"> son los tres ejes perpendiculares entre sí que forman un triedro a derechas. Este sistema de referencia se encuentra ligado a la dirección del vector velocidad aerodinámica. En concreto, su centro es cualquier punto del avión dentro del plano de simetría, aunque se suele seleccionar el centro de masas. El eje <img src="https://render.githubusercontent.com/render/math?math=x_w"> se orienta según la dirección y sentido de la velocidad aerodinámica, <img src="https://render.githubusercontent.com/render/math?math=z_w"> se orienta en el plano de simetría hacia abajo, perpendicular a <img src="https://render.githubusercontent.com/render/math?math=x_w">. Por último, <img src="https://render.githubusercontent.com/render/math?math=y_w"> se dirige formando un triedro a derechas con los otros dos ejes. 

Se han seleccionado el sistema de ejes viento porque junto con el sistema ejes cuerpo es el más utilizado y permite proyectar fácilmente los vectores de las fuerzas aerodinámicas.

En este proyecto los movimientos simulados son simétricos, con las alas a nivel y con el empuje orientado según la dirección <img src="https://render.githubusercontent.com/render/math?math=x_w"> por lo que las ecuaciones dinámicas de la aeronave son las siguientes

![](/assets/images/ec_din.png)

Por otro lado, para la obtención de las ecuaciones del planeador se utilizan las ecuaciones cinemáticas

![](/assets/images/ec_cin.png)

## SINDy

__Sparse Identification of Nonlinear Dynamics__ o SINDy, es una técnica desarrollada principalmente en la universidad de Washington, Seattle. El objetivo es obtener las ecuaciones que modelan la dinámica de un sistema a partir de mediciones de sus variables de interés, para sistemas de ecuaciones de la forma representada en la ecuación. Esta técnica aplica a diversas áreas como la ingeniería, finanzas, ecología o epidemiología. La necesidad de desarrollar esta técnica surge, por un lado de la gran cantidad de datos y técnicas para procesarlos de los que se dispone hoy en día, y por otro lado de la escasez de soluciones existentes para obtener la dinámica de un sistema a partir de estos datos medidos. Su implementación se ha realizado en el lenguaje de programación Python a través de la libería [PySINDy](https://joss.theoj.org/papers/10.21105/joss.02104).

El algoritmo que implementa la técnica de SINDy recibe dos entradas. La primera es una matriz con mediciones de las variables de estado <img src="https://render.githubusercontent.com/render/math?math=\textbf{X} \in \mathbb R^{m \times n}"> donde<img src="https://render.githubusercontent.com/render/math?math=m"> es el número de instantes temporales considerados y <img src="https://render.githubusercontent.com/render/math?math=n"> el número de variables de estado, i.e. la dimensión del vector de estado <img src="https://render.githubusercontent.com/render/math?math=\textbf{x} \in \mathbb R^n">. La segunda entrada es un conjunto de las <img src="https://render.githubusercontent.com/render/math?math=p"> funciones candidatas básicas sobre las que realizar la regresión. Por último, SINDy también recibe como entrada las derivadas del vector de estado para todos los instantes, <img src="https://render.githubusercontent.com/render/math?math=\dot{\textbf{X}} \in \mathbb R^{m \times n}">, las cuales son calculadas por la librería PySINDy en caso de que el usuario no las proporcione. A su salida, SINDy obtiene el mínimo número de funciones de entre las candidatas necesarias para describir las trayectorias que recibe a su entrada, junto con los coeficientes y variables de estado asociadas a cada función. 

Más formalmente, las entradas de SINDy se organizan en dos matrices. La primera de ellas es la matriz de trayectorias <img src="https://render.githubusercontent.com/render/math?math=\textbf{X}">

![](/assets/images/matriz_x.png)
 
Por otro lado, SINDy también recibe una matriz de funciones no lineales candidatas <img src="https://render.githubusercontent.com/render/math?math=\textbf{\Theta}(\textbf{X}) \in \mathbb R^{m \times p}">, construida a partir de la función <img src="https://render.githubusercontent.com/render/math?math=\textbf{\Theta}: \mathbb R^{m \times n} \rightarrow \mathbb R^{m \times p}">, que aproximan los datos de entrada y donde <img src="https://render.githubusercontent.com/render/math?math=p"> es el número de funciones posibles a considerar. Por ejemplo, la siguiente <img src="https://render.githubusercontent.com/render/math?math=\textbf{\Theta}(\textbf{X})"> contiene términos constantes y polinómicos de hasta grado 3 (cada uno de ellos perteneciente a una librería distinta)

![](/assets/images/matriz_theta.png)

donde <img src="https://render.githubusercontent.com/render/math?math=\textbf{X}^{P_2} \in \mathbb R^{m\times p_2}">  denota la matriz

![](/assets/images/matriz_xp2.png)

Como se puede ver <img src="https://render.githubusercontent.com/render/math?math=\textbf{\Theta}(\textbf{X})"> contiene en cada columna el valor de cada una de las funciones candidatas, <img src="https://render.githubusercontent.com/render/math?math=\textbf{f}">, para todos los instantes temporales, y en cada fila todas las combinaciones posibles de funciones candidatas entre todas las variables de estado para un determinado instante temporal. <img src="https://render.githubusercontent.com/render/math?math=L"> es el número de librerías de funciones a considerar (términos constantes y polinómicas de grado 1, 2 y 3 en el ejemplo anterior, por lo que <img src="https://render.githubusercontent.com/render/math?math=L=4"> en este caso) y <img src="https://render.githubusercontent.com/render/math?math=p = \sum_{i = 0}^{L} p_i"> representa el número total de funciones a considerar. Existe un gran cantidad de soluciones posibles, por lo que SINDy utiliza regresión dispersa para determinar los coeficientes de la matriz <img src="https://render.githubusercontent.com/render/math?math=\textbf{\Xi} \in \mathbb R^{p\times n}"> que activan aquellas funciones de la matriz <img src="https://render.githubusercontent.com/render/math?math=\textbf{\Theta}(\textbf{X})">. Se define 

![](/assets/images/matriz_xi.png)


donde <img src="https://render.githubusercontent.com/render/math?math=\textbf{\xi_k} \in \mathbb R^p"> son los coeficientes asociados a la variable de estado <img src="https://render.githubusercontent.com/render/math?math=k">.

SINDy utiliza **regresión dispersa**, la cual consiste en asumir que solo existen unos pocos términos relevantes por los cuales aproximar la ecuación. Un ejemplo de este tipo de algoritmo sería el representado en la siguiente ecuación

![](/assets/images/prob_opt.png)

donde <img src="https://render.githubusercontent.com/render/math?math=\| \cdot \|_F"> representa la norma de Frobenius, <img src="https://render.githubusercontent.com/render/math?math=\|\textbf{\Xi}\|_0"> es la norma 0 de la matriz <img src="https://render.githubusercontent.com/render/math?math=\textbf{\Xi}"> y denota la suma de valores distintos de cero. Por otro lado, <img src="https://render.githubusercontent.com/render/math?math=\epsilon"> representa un escalar que limita el número de valores distintos de cero de la matriz  <img src="https://render.githubusercontent.com/render/math?math=\textbf{\Xi}">. Las funciones de la matriz <img src="https://render.githubusercontent.com/render/math?math=\textbf{\Theta}(\textbf{X}) \in \mathbb R^ {m \times p}"> asociadas a la variable de estado <img src="https://render.githubusercontent.com/render/math?math=k"> son activadas por los coeficientes del vector <img src="https://render.githubusercontent.com/render/math?math=\textbf{\xi_k} \in \mathbb R^p">. La principal suposición que se realiza es que <img src="https://render.githubusercontent.com/render/math?math=m \gg p">. De manera que la derivada de cada elemento se denota por <img src="https://render.githubusercontent.com/render/math?math=\dot{\textbf{X}} \approx \textbf{\Theta}(\textbf{X}) \textbf{\Xi}">.

La implementación del algoritmo SINDy en la librería PySINDy permite configurar diversas entradas a su algoritmo. Las más relevantes son:
- **Matriz de datos,** <img src="https://render.githubusercontent.com/render/math?math=\textbf{X}">: tal y como se indica anteriormente debe contener en sus filas los distintos instantes temporales y en sus columnas las variables de estado.
- **Matriz de derivadas,** <img src="https://render.githubusercontent.com/render/math?math=\dot{\textbf{X}}"> (opcional): similar al caso anterior pero ahora debe contener el valor de las derivadas del vector de estado en cada instante temporal.
- **Paso de tiempo** (opcional, por defecto 1): PySINDy permite indicar el lapso de tiempo que transcurre entre las muestras del vector de tiempos <img src="https://render.githubusercontent.com/render/math?math=\textbf{t}">.
- **Librería de funciones candidatas**: PySINDy debe recibir las funciones candidatas para las cuales aproximar <img src="https://render.githubusercontent.com/render/math?math=\dot{\textbf{X}}">. Existen diversas librerías ya creadas como la polinómica o de Fourier (incluye términos trigonométricos).
- **Optimizador** (opcional, por defecto __Sequentially thresholded least squares algorithm__, STLSQ): PySINDy permite indicar qué optimizador usará en el proceso de regresión dispersa para la obtención de los pesos o coeficientes. 
    - **STLSQ**: el funcionamiento general de este optimizador consiste en a cada iteración se calculan los valores de los pesos y se da un valor de 0 a aquellos coeficientes inferiores a un umbral (por defecto 0.1), con la intención de conseguir una solución dispersa.
        
    - **Regresión regularizada relajada dispersa** (__Sparse relaxed regularized regression__, SR3): esta propuesta es más robusta a errores y falsos positivos. 
    - **SR3 restringido** (__Sparse relaxed regularized regression with linear equality constraints__): este optimizador es similar al anterior, pero permite al usuario indicar una serie de restricciones lineales del tipo menor o igual a aplicar sobre los pesos.

   En este proyecto se ha utilizado el optimizador SR3 para todos los casos, excepto en aquellos en los que se introducen restricciones sobre un coeficiente determinado, en estos casos se utilizará el optimizador SR3 restringido.
- **Diferenciador** (opcional, por defecto diferencia de derivadas finitas o __finite difference derivatives__): SINDy permite, como ya hemos indicado, recibir como argumento opcional la matriz de derivadas. Si no se le pasa dicha matriz, el algoritmo necesita calcularla, y utilizará para ello el diferenciador que le indiquemos en este argumento. Existen diferentes diferenciadores según la naturaleza de los datos (ruidosos o que presentan un paso de tiempo no uniforme). En el caso del método por defecto calcula las derivadas usando la aproximación de Taylor de primer orden. Otros métodos son __savitzky golay__ y __spline__.
- **Suposición inicial o __initial guess__** (opcional): matriz <img src="https://render.githubusercontent.com/render/math?math=\in \mathbb R^{n\times p}"> que indica la suposición inicial a partir de la cual el optimizador debe empezar a buscar el valor de los pesos o matriz <img src="https://render.githubusercontent.com/render/math?math=\textbf{\Xi}^T">.
- **Múltiples trayectorias** (opcional, por defecto falso): indica si existen varias trayectorias para los datos presentes en la matriz <img src="https://render.githubusercontent.com/render/math?math=\textbf{X}">. Estas trayectorias pueden variar sus condiciones iniciales o contener datos para distintos instantes temporales.


[volver](./)
