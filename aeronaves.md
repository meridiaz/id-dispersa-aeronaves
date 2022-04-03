# Obtención de las ecuaciones del movimiento de una aeronave

En este apartado se exponen los pasos a seguir y los principales resultados alcanzados. Para más detalle se dirige al lector al capítulo 5 de la memoria. 

## Arquitectura general
En el desarrollo de cada uno de los seis experimentos planteados se ha seguido una estructura similar:
1.    **Obtención de las ecuaciones de la mecánica de vuelo y adimensionalización/normalización de las mismas** [en ejes viento](https://meridiaz.github.io/id-dispersa-aeronaves/teoria.html#sistema-de-referencia-y-ecuaciones-de-una-aeronave). Tal y como se detallará más adelante, eliminar las dimensiones o normalizar los valores entre 0 y 1 permite que el algoritmo calcule de manera más precisa los términos que intervienen en la ecuación.
2.    **Generación de las trayectorias sintéticas:** en este paso se generan mediante software trayectorias sintéticas a partir de datos físicos de la aeronave o valores ya conocidos, como es la superficie alar o la densidad del aire. Para ello, se implementan las ecuaciones de la aeronave para unas condiciones iniciales aleatorias, con densidad de probabilidad uniforme en un rango que se especificará en cada caso. A continuación, se normalizan/adimensionalizan, según el caso, vía software (dividiendo entre la velocidad máxima) y se añade ruido. También se obtiene una trayectoria de validación que será utilizada para medir el error obtenido.
3.    **Creación y entrenamiento del modelo de SINDy**: una vez generadas las trayectorias, se elige la librería de funciones a utilizar, el optimizador y, si es necesario, las restricciones y suposición inicial. Por último se entrena el modelo de SINDy para obtener las ecuaciones que mejor se adaptan a los datos proporcionados.
4.    **Evaluación de resultados:** una vez obtenido el modelo que SINDy considera más adecuado se evalúan cualitativamente las ecuaciones obtenidas verificando que tienen los términos adecuados, se prueban las trayectorias obtenidas por dicho modelo obteniendo el error entre la trayectoria proporcionada por el algoritmo y la sintética y, en algunos casos, se calcula el error cuadrático entre los coeficientes del modelo que obtiene SINDy y los valores esperados.
5.    **Variación de las entradas y parámetros que el algoritmo permite configurar**, detalladas en el [este enlace](https://meridiaz.github.io/id-dispersa-aeronaves/teoria.html#par%C3%A1metros-configurables). El objetivo es comprobar cómo afecta la variación de estas entradas en el desempeño del modelo calculado. 

El siguiente pseudocódigo implementa los pasos anteriores.
```
# PASO 2
t = generar_vector_tiempos(n_puntos, paso_tiempo)
coefs = coeficientes_caso()
# condiciones iniciales para las trayectorias de train aleatorias
cond_inic = condiciones_iniciales_aleatorias(n_var, n_trayec, rangos)
# condiciones iniciales para la trayectoria de validacion no aleatorias
cond_inic_val = [cond1, cond2, ...]
# generar los datos segun el caso
data_train, data_dot_train = generar_trayectoria(t, coefs, cond_inic, n_trayec)
data_val, data_dot_val = generar_trayectoria(t, coefs, cond_inic_val, 1)
# normalizar los datos si es necesario
if normalizar:
    data_train, data_dot_train = normalizar(data_train, data_dot_train)
    data_val, _ = normalizar(data_val, data_dot_val)
# anadir ruido AWGN
if ruido:
    data_train, data_dot_train = sumar_ruido(data_train, data_dot_train, pn, pn_dot)
```
El código indicado más arriba se encarga de implementar el paso 2 de la lista anterior. En primer lugar, se genera el vector de tiempos y coeficientes para el desarrollo del caso. En segundo lugar, se generan condiciones iniciales aleatorias con densidad de probabilidad uniforme, según el número de incógnitas y trayectorias elegidas, para los datos de entrenamiento, y no aleatorias (deterministas) para los datos de validación, utilizados para medir el error en la trayectoria. En tercer lugar y utilizando estas condiciones iniciales, los coeficientes de la ecuación, el vector de tiempos generado y especificando el número de trayectorias, se genera la matriz de datos, <img src="https://render.githubusercontent.com/render/math?math=\mathbf{\dot{X}}"> así como la de derivadas, <img src="https://render.githubusercontent.com/render/math?math=\mathbf{{X}}">. Los siguientes pasos consisten en normalizar la trayectoria (dividiendo entre la velocidad máxima de la misma) y sumarle ruido, según el caso.

Para la generación del ruido se ha considerado ruido aditivo, blanco y gaussiano (AWGN en inglés) que es utilizado para contaminar la matriz <img src="https://render.githubusercontent.com/render/math?math=\mathbf{X}"> y <img src="https://render.githubusercontent.com/render/math?math=\mathbf{\dot{X}}">. Para generarlo se ha normalizado dicho ruido con respecto a la potencia de la señal, de manera que la potencia del ruido representa <img src="https://render.githubusercontent.com/render/math?math=pn"> veces la potencia de la señal original.

En el código mostrado a continuación se implementan los pasos 3 y 4 de la estructura anterior, los cuales se encargan de crear el modelo, entrenarlo y evaluar los resultados obtenidos. El primer lugar, se crea la librería de funciones a utilizar por el algoritmo para la obtención de las ecuaciones. Conocidas las funciones que componen la librería es posible obtener la matriz de coeficientes <img src="https://render.githubusercontent.com/render/math?math=\mathbf{\Xi}"> que debería obtener SINDy. En segundo lugar, se obtienen las restricciones y suposición inicial, si se requiere. En tercer lugar, se crea el modelo de SINDy mediante la sentencia `ps.SINDy`, donde `ps` es un alias para la librería PySINDy, especificando el optimizador, suposición inicial, restricciones, librería de funciones y nombre de las variables. En cuarto lugar, se alimenta al modelo con los datos generados en el código anterior. A continuación, se calcula la trayectoria que simula el algoritmo para las ecuaciones que ha devuelto dada la condición inicial de la trayectoria de validación. Por último, se calcula el error cuadrático medio de los coeficientes de la ecuación y el error entre las trayectorias de validación real y simulada. 
```
# PASOS 3 Y 4
lib = crear_libreria_funciones()
matriz_real_coefs = crear_mat_coefs(data_train, coefs, lib)
# generar initial guess y restricciones en caso necesario
initial_guess, restric_lhs, restric_rhs = generar_prereq(data_train, lib, n_restris, rhs)
# crear el modelo de SINDy
model_sindy = ps.SINDy(
            optimizer=ps.sindy_opt(initial_guess=initial_guess, 
                    lhs=restric_lhs, rhs=restric_rhs), 
            feature_library=lib,                                           
            feature_names=['var1', 'var2'...])   
# entrenar el modelo de SINDy       
model_sindy.fit(data_train, t=paso_tiempo, 
                multiple_trajectories=True, x_dot=data_dot_train)
# obtener una trayectoria para las ecuaciones calculadas
x_sim = model_sindy.simulate(cond_inic_val, t)
# calcular error en trayectoria y coeficientes 
error_trayec = mean((x_sim-data_val)**2)
error_coefs = mean((model_sindy.coefficients()-matriz_real_coefs)**2)
```

## Casos desarrollados de aeronaves

En la tabla que se muestra a continuación se agrupan los diversos casos realizados sobre trayectorias de aeronaves
![índice de casos desarrollados sobre aeronaves](/assets/images/tabla_casos_aeronaves2.png)

### Caso A
Este primer caso es el más sencillo que se ha desarrollado y el objetivo es familiarizarse con la implementación de las ecuaciones de la mecánica de vuelo vía software y entender el funcionamiento del algoritmo. En este caso no se adimensionalizan o normalizan las ecuaciones debido a su simplicidad. 

Se pretende implementar el vuelo de un planeador (sin empuje) con un ángulo de asiento de la velocidad <img src="https://render.githubusercontent.com/render/math?math=\gamma"> y velocidad aerodinámica uniformes. Este es el único caso en el que se obtienen las [ecuaciones cinemáticas](https://meridiaz.github.io/id-dispersa-aeronaves/teoria.html#sistema-de-referencia-y-ecuaciones-de-una-aeronave). Se ha decidido llevar a cabo este enfoque por ilustrar un ejemplo de implementación de estas ecuaciones y no de las dinámicas.

En la imagen que se muestra a continuación se puede ver la trayectoria sintética de la aeronave, la predicha por el algoritmo y las ecuaciones obtenidas por el mismo.

![trayectoria caso A](/assets/images/casoA.png)
### Caso B
En este caso se modela un vuelo con empuje orientado según el sentido que indica el eje <img src="https://render.githubusercontent.com/render/math?math=\x_w"> y describiendo un vuelo rectilíneo, uniforme y simétrico, por lo que el ángulo de asiento de la velocidad, <img src="https://render.githubusercontent.com/render/math?math=\gamma">, es nulo. 

Se sustituye el valor de <img src="https://render.githubusercontent.com/render/math?math=L"> por su expresión <img src="https://render.githubusercontent.com/render/math?math=L = \frac{1}{2} \rho_{aire} V^{2} S c_L"> se despeja de la [ecuación dinámica](https://meridiaz.github.io/id-dispersa-aeronaves/teoria.html#sistema-de-referencia-y-ecuaciones-de-una-aeronave) del eje <img src="https://render.githubusercontent.com/render/math?math=z_w"> el coeficiente de sustentación, <img src="https://render.githubusercontent.com/render/math?math=c_L">. A continuación, se incluye la resistencia aerodinámica por la expresión <img src="https://render.githubusercontent.com/render/math?math=D = \frac{1}{2} \rho_{aire} V^{2} S (c_{D0} + kc_L^2)"> en la ecuación del eje <img src="https://render.githubusercontent.com/render/math?math=x_w"> y se sustituye el <img src="https://render.githubusercontent.com/render/math?math=c_L"> en el término de resistencia aerodinámica inducida. Agrupando los términos constantes, asumiendo velocidades grandes y normalizando la ecuación de la velocidad por la relación <img src="https://render.githubusercontent.com/render/math?math=\hat{V} = V/{U_c}"> se obtiene la siguiente ecuación que modela el comportamiento de la aeronave

<img src="https://render.githubusercontent.com/render/math?math=\hat{\dot{V}} = -a{\hat{V}}^2 + c">,

donde <img src="https://render.githubusercontent.com/render/math?math=a = \frac{1}{2} \rho_{aire} \frac{S}{m} c_{D0}U_c"> y <img src="https://render.githubusercontent.com/render/math?math=c = \frac{T}{mU_c}">

Al alimentar al algoritmo SINDy con trayectorias sintéticas que siguen la cuación anterior se obtiene la siguiente trayectoria simulada junto al sistema de ecuaciones predicho:

![trayectoria caso B](/assets/images/casoB.png)

### Caso C-1
En este caso y a diferencia del anterior, se cosideran velocidades pequeñas, por lo que el término de la resistencia dependiente de <img src="https://render.githubusercontent.com/render/math?math=1{\hat{V}^2}"> ya no se puede despreciar de la ecuación. La ecuación que modela este movimiento es la siguiente.

<img src="https://render.githubusercontent.com/render/math?math=\hat{\dot{V}} = -a\hat{V}^2 + c - \frac{b}{\hat{V}^2}">,

donde <img src="https://render.githubusercontent.com/render/math?math=b = k \frac{g^2}{\frac{1}{2} \rho_{aire}U_c^3}"> y <img src="https://render.githubusercontent.com/render/math?math=a"> y <img src="https://render.githubusercontent.com/render/math?math=c"> siguen las expresiones detalladas en el caso anterior C-1.

Al alimentar al algoritmo SINDy con trayectorias sintéticas que siguen la cuación anterior se obtiene la siguiente trayectoria simulada junto al sistema de ecuaciones predicho:

![trayectoria caso C-1](/assets/images/casoC1.png)

### Caso C-2
En este caso se pretende obtener la ecuación desarrollada en el caso anterior para velocidades pequeñas pero aproximando el término <img src="https://render.githubusercontent.com/render/math?math=1{\hat{V}^2}"> por una aproximación en serie de Taylor de orden 2 y 3. Por tanto, la ecuación aproximada para orden 2 sería la siguiente

<img src="https://render.githubusercontent.com/render/math?math=\hat{\dot{V}} = -(a +3b)\hat{V}^2 + 8b\hat{V} + (-6b + c)">
y para orden 3

<img src="https://render.githubusercontent.com/render/math?math=\hat{\dot{V}} = 4b\hat{V}^3 -(a + 15b)\hat{V}^2 + 20b\hat{V} + (-10b + c)">.

Al alimentar al algoritmo SINDy con trayectorias sintéticas que siguen la cuación anterior se obtiene la siguiente trayectoria simulada junto al sistema de ecuaciones predicho:

![trayectoria caso C-2](/assets/images/casoC2.png)

### Caso D-1

En este casos las variables dependientes del tiempo son la velocidad y el ángulo de asiento de la velocidad, <img src="https://render.githubusercontent.com/render/math?math=\gamma">. Primeramente, se ha tratado de alimentar al algoritmo con trayectorias normalizadas. Sin embargo, los resultados obtenidos no han sido satisfactorios y es necesario realizar otras transformaciones a las ecuaciones. Para ello, se adimensionaliza la ecuación de la velocidad por un tiempo característico <img src="https://render.githubusercontent.com/render/math?math=t_c"> y una velocidad característica <img src="https://render.githubusercontent.com/render/math?math=U_c">. 

Se mantiene la definición <img src="https://render.githubusercontent.com/render/math?math=\hat{V} = V/{U_c}"> y se incorporan las siguientes

<img src="https://render.githubusercontent.com/render/math?math=\hat{\dot{V}} = \frac{\dot{V}t_c}{U_c}">
    
<img src="https://render.githubusercontent.com/render/math?math=\hat{\dot{\gamma}} = \dot{\gamma}t_c">.

Sustituyendo las expresiones anteriores en las [ecuaciones dinámicas](https://meridiaz.github.io/id-dispersa-aeronaves/teoria.html#sistema-de-referencia-y-ecuaciones-de-una-aeronave) y <img src="https://render.githubusercontent.com/render/math?math=\dot{\gamma} = \frac{V}{R}"> y eligiendo cuidadosamente la velocidad característica se obtiene el siguiente sistema de ecuaciones

<img src="https://render.githubusercontent.com/render/math?math=\hat{\dot{V}} = A_3 - A_5\hat{V}^2 - A_6\cos{\gamma} - A_7\sin{\gamma} - \frac{A_8(\cos{\gamma})^2}{\hat{V}^2}">

<img src="https://render.githubusercontent.com/render/math?math=\hat{\dot{\gamma}} = A_4 \hat{V}">,

donde los coeficientes son constantes y vienen representados por las siguientes expresiones

<img src="https://render.githubusercontent.com/render/math?math=A_3 = \frac{T}{mg}">

<img src="https://render.githubusercontent.com/render/math?math=A_4 = \frac{2m}{\rho_{aire} S R}">

<img src="https://render.githubusercontent.com/render/math?math=A_5 = c_{D0} + kA_4^2">

<img src="https://render.githubusercontent.com/render/math?math=A_6 = 2kA_4">

<img src="https://render.githubusercontent.com/render/math?math=A_5 = c_{D0} + kA_4^2">

<img src="https://render.githubusercontent.com/render/math?math=A_7 = 1">

<img src="https://render.githubusercontent.com/render/math?math=A_8 = k">.

Al alimentar al algoritmo SINDy con trayectorias sintéticas que siguen la cuación anterior se obtiene la siguiente trayectoria simulada junto al sistema de ecuaciones predicho:
![trayectoria caso D-1](/assets/images/casoD1.png)

### Caso D-2
En este caso las incógnitas dependientes del tiempo son <img src="https://render.githubusercontent.com/render/math?math=T">, <img src="https://render.githubusercontent.com/render/math?math=c_L"> y <img src="https://render.githubusercontent.com/render/math?math=\gamma"> que quedan descritas por 3 ecuaciones, dos [ecuaciones dinámicas](https://meridiaz.github.io/id-dispersa-aeronaves/teoria.html#sistema-de-referencia-y-ecuaciones-de-una-aeronave) y una ecuación angular <img src="https://render.githubusercontent.com/render/math?math=\dot{\gamma} = \frac{V}{R}">. Nótese que la velocidad es constante en este caso. Desarrollando dichas ecuaciones y agrupando términos se obtiene el siguiente sistema formado por dos ecuaciones 

<img src="https://render.githubusercontent.com/render/math?math=\dot{T} = -A_8sin(2\gamma) - A_9sin(\gamma) + A_{10}cos(\gamma)">
 
<img src="https://render.githubusercontent.com/render/math?math=\dot{\gamma} = A_6">, 

donde

<img src="https://render.githubusercontent.com/render/math?math=A_4 = \frac{2kW^2}{\rho_{aire} S V_0^2}">

<img src="https://render.githubusercontent.com/render/math?math=A_5 = \frac{4kWm}{\rho_{aire} S R}">

<img src="https://render.githubusercontent.com/render/math?math=A_8 = A_4\frac{V_0}{R}">

<img src="https://render.githubusercontent.com/render/math?math=A_9 = A_5\frac{V_0}{R}">

<img src="https://render.githubusercontent.com/render/math?math=A_{10} = W\frac{V_0}{R}">.


Al alimentar al algoritmo SINDy con trayectorias sintéticas que siguen la cuación anterior se obtiene la siguiente trayectoria simulada junto al sistema de ecuaciones predicho:
![trayectoria caso D-2](/assets/images/casoD2.png)

## Resultados 

Para concluir este capítulo se representa en la siguiente tabla una comparativa entre las ecuaciones teóricas y las ecuaciones obtenidas por el algoritmo y el error cuadrático medio en los coeficientes. Esta tabla, al igual que el gráfico de barras localizado al final de este apartado se han generado utilizando 20 trayectorias para los datos de entrenamiento. De nuevo, para aumentar la robustez de los resultados se ha repetido todo el proceso de generación de datos, creación del modelo, entrenamiento del mismo y validación de resultados en diez ocasiones y se muestra la mediana del error de estas diez ejecuciones.

![tabla ecuaciones](/assets/images/resumen_casos.png)

En dicha tabla se puede observar que de manera general el algoritmo es capaz de recuperar correctamente las ecuaciones, mostrando un error en los coeficientes de las mismas bajo. Sin embargo, en el caso C-2, tanto para la aproximación de orden 2 como de orden 3, se puede ver que el error asociado es mayor. Esto puede ser debido a que el algoritmo es alimentado con trayectorias que siguen la ecuación del caso C-1 en la tabla pero se utiliza una librería polinómica de grado 2 y 3 en la que no aparece el término <img src="https://render.githubusercontent.com/render/math?math=1/v^2">. El algoritmo, en lugar de obtener los coeficientes asociados al desarrollo en serie de Taylor entorno al punto 1, trata de aproximar la trayectoria en todos los puntos, la cual no ha sido generada utilizando esta aproximación. Esto se confirma si vemos el error asociado a los coeficientes en la tabla y el error asociado a la trayectoria, ver gráfica de la trayectoria del caso C-2, estos difieren considerablemente.

Por otro lado, vemos que para el caso D-1 el error asociado a los coeficientes es mayor que el caso homólogo D-2, esto es debido a que el coeficiente asociado al término <img src="https://render.githubusercontent.com/render/math?math=(\cos{\gamma})^2/v^2"> no es detectado correctamente por el algoritmo. 

En el gráfico de barras se representa el error cuadrático medio de los coeficientes de las ecuaciones teóricas y predichas representadas en la tabla anterior. No se ha incluido el caso A debido a que la estimación de los coeficientes era perfecta, y el error que mostraba era debido a la resolución del ordenador, obstaculizando la correcta visualización de los órdenes de magnitud del resto de casos.

![error en los coeficientes](/assets/images/error_coefs.png)

[volver](./)
