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

## SINDy

__Sparse Identification of Nonlinear Dynamics__ o SINDy, es una técnica desarrollada principalmente en la universidad de Washington, Seattle. El objetivo es obtener las ecuaciones que modelan la dinámica de un sistema a partir de mediciones de sus variables de interés, para sistemas de ecuaciones de la forma representada en la ecuación. Esta técnica aplica a diversas áreas como la ingeniería, finanzas, ecología o epidemiología. La necesidad de desarrollar esta técnica surge, por un lado de la gran cantidad de datos y técnicas para procesarlos de los que se dispone hoy en día, y por otro lado de la escasez de soluciones existentes para obtener la dinámica de un sistema a partir de estos datos medidos. Su implementación se ha realizado en el lenguaje de programación Python a través de la libería [PySINDy](https://joss.theoj.org/papers/10.21105/joss.02104).

El algoritmo que implementa la técnica de SINDy recibe dos entradas. La primera es una matriz con mediciones de las variables de estado <img src="https://render.githubusercontent.com/render/math?math=\bbX \in \reals^{m \times n}"> donde __m__ es el número de instantes temporales considerados y __n__ el número de variables de estado, i.e. la dimensión del vector de estado $\bbx \in \reals^n$. La segunda entrada es un conjunto de las $p$ funciones candidatas básicas sobre las que realizar la regresión. Por último, SINDy también recibe como entrada las derivadas del vector de estado para todos los instantes, $\dot{\bbX} \in \reals^{m \times n}$, las cuales son calculadas por la librería PySINDy en caso de que el usuario no las proporcione. A su salida, SINDy obtiene el mínimo número de funciones de entre las candidatas necesarias para describir las trayectorias que recibe a su entrada, junto con los coeficientes y variables de estado asociadas a cada función. 

Más formalmente, las entradas de SINDy se organizan en dos matrices. La primera de ellas es la matriz de trayectorias $\bbX$

\begin{equation}
\bbX = 
    \begin{bmatrix}
        x^T(t_1) \\
        x^T(t_2) \\
        \vdots \\
        x^T(t_m)
    \end{bmatrix}
    = \begin{bmatrix}
        x_1(t_1) & x_2(t_1) & \ldots & x_n(t_1) \\
        x_1(t_2) & x_2(t_2) & \ldots & x_n(t_2) \\
        \vdots & \vdots & \ddots & \vdots \\
         x_1(t_m) & x_2(t_m) & \ldots & x_n(t_m) \\
    \end{bmatrix}.
\end{equation}
 
 % theta(X) recibe una mat de tamaño mxn y devuelve una matriz de mxp
 
Por otro lado, SINDy también recibe una matriz de funciones no lineales candidatas $ \bbTheta(\bbX) \in \mathbb R^{m \times p}$, construida a partir de la función $\bbTheta: \mathbb R^{m \times n} \rightarrow \mathbb R^{m \times p}$, que aproximan los datos de entrada y donde $p$ es el número de funciones posibles a considerar. Por ejemplo, la siguiente $\bbTheta(\bbX)$ contiene términos constantes y polinómicos de hasta grado 3 (cada uno de ellos perteneciente a una librería distinta)

\begin{equation}
    \bbTheta(\bbX) = 
    \begin{bmatrix}
        \mid & \mid & \mid & \mid \\
        1 & \bbX & \bbX^{P_2} & \bbX^{P_3}\\
        \mid & \mid & \mid & \mid
    \end{bmatrix}, 
\end{equation}
%
donde $\bbX^{P_2} \in \mathbb R^{m\times p_2}$ denota la matriz
\begin{equation}
   \bbX^{P_2} = 
   \begin{bmatrix}
        x_1^2(t_1) & x_1(t_1)x_2(t_1) & \ldots & x_2^2(t_1) & \ldots & x_n^2(t_1) \\
        x_1^2(t_2) & x_1(t_2)x_2(t_2) & \ldots & x_2^2(t_2) & \ldots & x_n^2(t_2) \\
        \vdots & \vdots & \ddots & \vdots & \ddots & \vdots\\
         x_1^2(t_m) & x_1(t_m)x_2(t_m) & \ldots & x_2^2(t_m) & \ldots & x_n^2(t_m) \\
    \end{bmatrix}.
    \nonumber
\end{equation}

Como se puede ver $\bbTheta(\bbX)$ contiene en cada columna el valor de cada una de las funciones candidatas, $\bbf$, para todos los instantes temporales, y en cada fila todas las combinaciones posibles de funciones candidatas entre todas las variables de estado para un determinado instante temporal. $L$ es el número de librerías de funciones a considerar (términos constantes y polinómicas de grado 1, 2 y 3 en el ejemplo anterior, por lo que $L=4$ en este caso) y $p = \sum_{i = 0}^{L} p_i$ representa el número total de funciones a considerar. Existe un gran cantidad de soluciones posibles, por lo que SINDy utiliza regresión dispersa para determinar los coeficientes de la matriz $\bbXi \in \mathbb R^{p\times n}$ que activan aquellas funciones de la matriz $\bbTheta(\bbX)$. Se define 

\begin{align}
    \bbXi &= 
    \begin{bmatrix}
        \bbxi_1 & \bbxi_2 &  \ldots & \bbxi_n
    \end{bmatrix} 
    \nonumber \\
    \dot{\bbX} &= \bbTheta(\bbX)\bbXi,
\end{align}
%
donde $\bbxi_k \in \reals^p$ son los coeficientes asociados a la variable de estado $k$.

SINDy utiliza \textbf{regresión dispersa}, la cual consiste en asumir que solo existen unos pocos términos relevantes por los cuales aproximar la ecuación. Un ejemplo de este tipo de algoritmo sería el representado en la siguiente ecuación

\begin{equation}
    \min_{\bbXi}\| \dot{\bbX} - \bbTheta(\bbX) \bbXi\|^2_F \mbox{ sujeto a } \|\bbXi\|_0 \leq \epsilon, 
    \label{eq:reg-espar-mat}
\end{equation}

{\color{red} no debería poner $\|\bbXi\|_0$ en  el texto y no $\|\bbxi_k\|_0$???}
%
donde $\| \cdot \|_F$ representa la norma de Frobenius, $\|\bbXi\|_0$ es la norma 0 de la matriz $\bbXi$ y denota la suma de valores distintos de cero. Por otro lado, $\epsilon$ representa un escalar que limita el número de valores distintos de cero de la matriz $\bbXi$. Las funciones de la matriz $\bbTheta(\bbX) \in \mathbb R^ {m \times p}$ asociadas a la variable de estado $k$ son activadas por los coeficientes del vector $\bbxi_k \in \mathbb R^p$. La principal suposición que se realiza es que $m \gg p$. De manera que la derivada de cada elemento se denota por $\dot{\bbX} \approx \bbTheta(\bbX) \bbXi$~\cite{esparse-reg}.
