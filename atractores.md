# Atractores

Un atractor es un conjunto de estados hacia los cuales tiende un sistema dinámico, es decir, en ciertos sistemas dinámicos, una vez eliminado el transitorio inicial, el sistema tiende a unos valores típicos o atractores. Otra forma de verlo es que el sistema converge a un estado del que no puede salir. El concepto de atractor está muy asociado a sistemas disipativos, que pierden energía, ya que estos también convergen a un estado final único.

Existen dos tipos de atractores, clásicos y extraños. En los **atractores clásicos** todos los estados del sistema tienden a un único punto o estado estacionario. Se caracterizan porque cuando desparece la fuerza externa aplicada y/o existen fuerzas de fricción, las condiciones iniciales para los cuales han sido generados se mimetizan con el estado estacionario del sistema

Por otro lado, para hablar de los atractores extraños es necesario introducir la Teoría del Caos. En los atractores clásicos una misma condición inicial produce que el sistema evolucione de la misma manera. Los sistemas caóticos son sistemas dinámicos deterministas no lineales en los cuales una pequeña variación en las condiciones iniciales provoca que el sistema evolucione de diferente manera, aunque el cambio en las condiciones iniciales sea mínimo. Debido a ello, la Teoría del Caos también es conocida como efecto mariposa.

Un sistema dinámico que presente un **atractor extraño** es denominado sistema caótico y exhibirá un comportamiento no predecible. Esta definición puede parecer contradictoria con el concepto introducido anteriormente de atractor. En un sistema caótico que presente atractores extraños se sabe que su comportamiento general será siempre el mismo y tendrá la misma forma en todos los casos (representada por las mismas ecuaciones) (esto no estoy seguro, ponlo solo si es verdad y te convence), pero no se puede conocer el estado exacto del sistema en un instante determinado, es impredecible. A pesar de que estos sistemas son deterministas, un pequeño error de medición en las condiciones iniciales provoca resultados muy diferentes, complicando su predicción a largo plazo.

El atractor extraño más famoso es el **atractor de Lorenz**. Este atractor aparece en el sistema dinámico caótico que postuló Edward N. Lorenz en 1963 para modelar, de forma simplificada, el comportamiento de grandes masas de aire en la atmósfera. Asimismo existen otros atractores extraños usados en este proyecto, todos ellos representados a continuación junto con las ecuaciones que los caracterizan:
- El **atractor de Rössler** que aparece en los sistemas de reacciones químicas oscilantes~\cite{atractor-ros}.
- El **atractor de Thomas** presenta una forma simétrica en las variables $x$, $y$, y $z$~\cite{atractor-tho}.
- El **atractor del sistema caótico unificado de tres lóbulos o en inglés __Three-Scroll Unified Chaotic System__** el cual se obtiene de una particularización en los parámetros del atractor de Lü. 

![](/assets/images/atractores.png)

En el algoritmo SINDy se han implementado estos atractores obteniéndose los siguientes errores en los coeficientes de sus ecuaciones

![](/assets/images/errores_atractores.png)

Se aprecia que el atractor Three-Scroll es el que más error obtiene seguido del atractor de Rössler. En ambos casos es debido a que algunos de los coeficientes obtenidos por el algoritmo difieren de su valor real. A continuación, el atractor de Thomas es el que mayor error obtiene, puede ser debido a que los coeficientes obtenidos en la ecuación varían en algunos de sus decimales con el valor real de los mismos. Por último, el que mejor resultado obtiene es el atractor de Lorenz, con una predicción prácticamente perfecta de sus coeficientes cuyo error puede ser debido a la precisión decimal de la máquina.

En todos los casos, vemos que el error no supera el valor de <img src="https://render.githubusercontent.com/render/math?math=10^{-4}"> que, teniendo en cuenta que estamos ante valores de <img src="https://render.githubusercontent.com/render/math?math=p"> (número de funciones a considerar en la matriz <img src="https://render.githubusercontent.com/render/math?math=\textbf{\Xi} \in \mathbb R^{p\times n}">) de 35, 10, 70 y 10 para los atractores de Lorenz, Rössler, Thomas y Three-Scroll, respectivamente, se trata de un error muy bajo y el algoritmo SINDy es capaz de obtener las ecuaciones de forma fiable. Con ello concluimos que utilizar dicho algoritmo en trayectorias caóticas puede ser una línea de investigación muy prometedora.

[volver](./)
