import matplotlib.pyplot as plt
import numpy as np
import pysindy as ps
from scipy.integrate import solve_ivp

# ------------------ FUNCIONES GENERALES ----------------------- #
class Model_params(object):
    def __init__(self, opt=None, initial_guess=None, feature_list=None, lib=None, 
                degree=2, deltat=0, constraint_rhs=None, constraint_lhs=None):
        self.initial_guess = initial_guess
        if opt is None:
            self.opt = ps.SR3(initial_guess=initial_guess)
        else:
             self.opt = ps.ConstrainedSR3(constraint_rhs=constraint_rhs, constraint_lhs=constraint_lhs,
                          initial_guess=initial_guess)
        self.deltat = deltat
        self.feature_list = feature_list
        if lib is not None:
            self.lib = lib
        else:
            ps.PolynomialLibrary(degree=degree)


class Model(object):
    def __init__(self, model_params=None):
        self.model_params = model_params
        self.model_sindy = None

    def crear_modelo(self, print_model=False):
        self.model_sindy = ps.SINDy(
            optimizer=self.model_params.opt, 
            feature_library=self.model_params.lib,                                           
            feature_names=self.model_params.feature_list, 
        )
        #la doc dice que en t hay que poner el time step
        
        self.model_sindy.fit(self.data_adim, t=self.model_params.deltat, 
                                multiple_trajectories=True, x_dot=self.data_adim_dot)
        if print_model:
            self.model_sindy.print(precision=4)
        
    def adimensionalizar(self, data, n_trayec, traj_val, data_dot, adim):
        #adimensionalizo buscando el maximo por caracteristica para todas las trayectorias
        data_adim = []
        data_adim_dot = []
        if adim:
            maxi = np.max(data, axis=1)
            self.maxi = np.max(maxi, axis=0)
        else:
            self.maxi = np.ones((data[0].shape[1]))

        for i in range(n_trayec):
            data_adim.append(data[i] / self.maxi)
            data_adim_dot.append(data_dot[i]) #/self.maxi

        return data_adim, traj_val/self.maxi, data_adim_dot

    def sum_ruido_x(self, x, p_n):
        x_cent = x - np.mean(x, axis=0)
        p_x = np.sum(x_cent**2, axis=0)
        n = np.random.randn(x.shape[0], x.shape[1])*np.sqrt(p_n*p_x/x.shape[0])
        return x + n

    def sum_ruido(self, n_trayec, ruido, ruido_dot):
        for i in range(n_trayec):
            self.data_adim[i] = self.sum_ruido_x(self.data_adim_cl[i], ruido)
            self.data_adim_dot[i] = self.sum_ruido_x(self.data_adim_dot_cl[i], ruido_dot)

    def error_trayec(self, t):
        self.x_sim = self.model_sindy.simulate(self.data_val_adim[0], t)    
        return (self.x_sim-self.data_val_adim)**2
    
    def error_coefs(self, coefs_real):
        return (self.model_sindy.coefficients()-coefs_real)

    def plot_trayec(self, t, plot_data_ruidosa=False, ruido=0,
                    labs=['Velocidad (m/s)', 'Ángulo de asiento de la velocidad (rad)']):
        # Plotear trayectorias
        # Con y sin ruido (si es que existe, comprobar a través de atributos/argumentos)
        # Real y simulada (asegurarse de haber llamado a fit)
        fig, axs = plt.subplots(1, self.data_val_adim.shape[1], figsize=(16, 8), squeeze=False)
        fig.suptitle("Evolución de la trayectoria", fontsize=18)
        for j in range(axs.shape[1]):
            if ruido != 0 and plot_data_ruidosa:
                val_adim_ruidosa = self.sum_ruido_x(self.data_val_adim, ruido)
                axs[0,j].plot(t, val_adim_ruidosa[:, j], 'r--', label='Trayectoria ruidosa de potencia ' + str(ruido*100) + '%')
            axs[0,j].plot(t, self.data_val_adim[:, j], 'k', label='Trayectoria real')
            axs[0,j].plot(t, self.x_sim[:, j], 'b--', label='Trayectoria simulada')
            axs[0,j].set_ylabel(labs[j], fontsize=16)
            axs[0,j].set_xlabel('Tiempo (s)', fontsize=16)
            axs[0,j].legend(fontsize=14)
            axs[0,j].tick_params(axis='both', labelsize=14)
            #axs[0,j].set_yticks(fontsize=14)

        return


    # ------------------ FUNCION PRINCIPAL ----------------------- #
    def eval(self, generate_traj, n_trayec, t, coefs_ecs, cond_inic,
            adim=True, t_val=None, ruido_dot=0, ruido=0, ders=False, mod=None, deltat_train=None,
            print_model=False):
        """
        argumentos:
        generate_traj: función que genera las trayectorias según el caso a simular
        n_traj: numero de trayectorias para generar los datos y entrenar el modelo
        t: lista que contiene los instantes de tiempo para los cuales generar datos de train
        coefs_ecs: valor de los coeficientes de la ecuación
        adim: si se desea adimensionalizar o no los valores de entrenamiento
        t_val: lista que contiene los instantes de tiempo para los que generar la trayectoria de val
        ruido_dot: potencia de ruido en las derivadas
        ruido: potencia de ruido en la trayectoria con la que alimentar a sindy
        ders: indica si pasarle o no las derivadas de la trayectoria a sindy
        mod: instancia de la clase model en la que se especifican restricciones, inital_guess, opti..  
        deltat_train: paso de tiempo que se le pasa a sindy para obtener el modelo
        print_model: si imprimir el modelo que sindy calcula
        plot_data_ruidosa: si imprimir las trayectorias 
        """
        
        # generar datos
        if t_val is None:
            t_val = t

        if ruido_dot > 0:
            ders = True
            
        data, data_dot, lib_custom, data_val = generate_traj(n_trayec, t, coefs_ecs, 
                                                t_val, cond_inic)

        self.data_adim_cl, self.data_val_adim, self.data_adim_dot_cl = self.adimensionalizar(data, 
                                                                n_trayec, data_val, data_dot,
                                                                adim)
        self.data_adim = self.data_adim_cl.copy()
        self.data_adim_dot = self.data_adim_dot_cl.copy()
        # añadir ruido
        if ruido > 0 or ruido_dot > 0:
            self.sum_ruido(n_trayec, ruido, ruido_dot)
            

        # generar modelo    
        if mod is None:
            mod = Model_params(lib=lib_custom)
        self.model_params = mod
        if deltat_train is None:
            self.model_params.deltat = t[1]-t[0]   
        else:
            self.model_params.deltat = deltat_train
            
        if not ders:
            self.data_adim_dot = None

        if t[1]-t[0] != t_val[1]-t_val[0]:
            raise ValueError("t_val array must have same step as t array")

        self.crear_modelo(print_model=print_model)

# ------------------ CASO A ----------------------- #
def ecs_casoA(t, cond_inic):
    #caalculo el valor de cada variable y almaceno en un array
    n = t.shape[0]
    deltat = t[1]-t[0]
    gamma0, x0, h0, v0 = cond_inic

    v = v0*np.ones(n)
    gamma = -np.pi*gamma0/180*np.ones(n) #esto es gamma no gammae 

    x = np.zeros(n)
    h = np.zeros(n)
    h[0] = h0
    x[0] = x0
    for i in range(1, n):
        x[i] = x[i-1] + v[i]*np.cos(gamma[i])*deltat
        h[i] = h[i-1] + v[i]*np.sin(gamma[i])*deltat
    
    #calculo el valor de las derivadas:
    x_dot = v*np.cos(gamma)
    h_dot = v*np.sin(gamma)
    v_dot = np.zeros(n)
    gamma_dot = np.zeros(n)
    
    return np.stack((gamma, x, h, v)), np.stack((gamma_dot, x_dot, h_dot, v_dot))

def custom_ecs_A():
    library_functions = [
        lambda theta, d : d*np.sin(theta),
        lambda theta, d : d*np.cos(theta),
        #lambda d: 0,
    ]
    library_function_names = [
        lambda theta, d : '+' + d + '*' + 'sen(' + theta + ')',
        lambda theta, d : d + '*' + 'cos(' + theta + ')', 
        #lambda d: d
    ]
    library = ps.CustomLibrary(library_functions=library_functions, function_names=library_function_names,
                              interaction_only=True)
    return library

def casoA(n_trayec, t, coefs_ecs, t_val, cond_inic):
    data = []
    data_dot = []
    for i in range(n_trayec):
        gamma0 = np.random.uniform(low=1, high=90)
        x0 =  np.random.uniform(low=0, high=100)
        h0 =  np.random.uniform(low=100, high=1000)
        v0 =  np.random.uniform(low=1, high=10)
        p, h = ecs_casoA(t, [gamma0, x0, h0, v0])
        data.append(p.T)
        data_dot.append(h.T)

    data_val, _ = ecs_casoA(t_val, cond_inic)

    return data, data_dot, custom_ecs_A(), data_val.T
# ------------------ CASO B ----------------------- #
def ecs_casoB(t, vx0, coefs):
    T0, A, B = coefs
    n = t.shape[0]
    deltat = t[1]-t[0]
    vx = np.zeros((n, 1))
    vx[0] = vx0
    vx_dot = np.zeros((n, 1))
    vx_dot[0] = -A*vx0**2 + T0
    T = T0 * np.ones(n) #en realidad esto es T/m no el empuje

    for i in range(1, n):
        vx[i] = vx[i - 1] + deltat * (T[i-1]-A*vx[i-1]**2-B/vx[i-1]**2*0)
        vx_dot[i] = -A*vx[i]**2 + T0
    return vx, vx_dot

def custom_ecs_B():
    library_functions = [
        lambda v : v**2,
        lambda v: 1/v**2,
        lambda t: 1
    ]
    library_function_names = [
        lambda v : v + "^2",
        lambda v: '1/' + v + "^2", 
        lambda t: "1"
    ]
    library = ps.CustomLibrary(library_functions=library_functions, 
                                function_names=library_function_names,
                              interaction_only=True)
    return library

def casoB(n_trayec, t, coefs_ecs, t_val, cond_inic):
    # condiciones iniciales:
    vx0 = np.ones(n_trayec)
    for i in range(n_trayec):
        vx0[i] = np.random.uniform(low=10, high=100)
    vx0[0] = 100

    # obtengo la trayectoria:
    data = []
    data_dot = []
    for i in range(n_trayec):
        v, v_dot = ecs_casoB(t, vx0[i], coefs_ecs)
        data.append(v)
        data_dot.append(v_dot)
        
    
    data_val, _ = ecs_casoB(t_val, cond_inic, coefs_ecs)

    return data, data_dot, custom_ecs_B(), data_val

# ------------------ CASO C.1 ----------------------- #
def ecs_dot_casoC1(t, y, T0, A, B):
    vx = y
    return T0 - A*vx**2 - B/vx**2

def ecs_casoC1(t, v_sol, coefs):
    T0, A, B = coefs
    n = t.shape[0]
    deltat = t[1]-t[0]
   
    vx_dot = np.zeros((n, 1))
    
    for i in range(0, n):
        vx_dot[i] = T0 - A*v_sol[i]**2 - B/v_sol[i]**2
    return vx_dot

def casoC1(n_trayec, t, coefs, t_val, cond_inic):
    data = []
    data_dot = []
    # condiciones iniciales:
    for i in range(n_trayec):
        v0 = np.random.uniform(low=5, high=5.5)
        v_sol = solve_ivp(ecs_dot_casoC1, (t[0], t[-1]), [v0], args=(coefs), t_eval=t)
        data.append(v_sol.y.T)
        data_dot.append(ecs_casoC1(t, v_sol.y.T, coefs))

    # obtengo la trayectoria:
    v0 = cond_inic
    data_val = solve_ivp(ecs_dot_casoC1, (t_val[0], t_val[-1]), [v0], args=(coefs), t_eval=t_val)

    return data, data_dot, custom_ecs_B(), data_val.y.T


# ------------------ CASO C.2 ----------------------- #

def casoC2(n_trayec, t, coefs, t_val, cond_inic):
    data = []
    data_dot = []
    # condiciones iniciales:
    for i in range(n_trayec):
        v0 = np.random.uniform(low=5, high=15)
        v_sol = solve_ivp(ecs_dot_casoC1, (t[0], t[-1]), [v0], args=(coefs), t_eval=t)
        data.append(v_sol.y.T)
        data_dot.append(ecs_casoC1(t, v_sol.y.T, coefs))

    # obtengo la trayectoria:
    v0 = cond_inic
    data_val = solve_ivp(ecs_dot_casoC1, (t_val[0], t_val[-1]), [v0], args=(coefs), t_eval=t_val)

    return data, data_dot, ps.PolynomialLibrary(degree=3), data_val.y.T


# ------------------ CASO D.1 ----------------------- #
def ecs_casoD1(t, cond_inic, coefs):
    A3, A4, cd0, k = coefs
    v0, gamma0 = cond_inic
    n = t.shape[0]
    deltat = t[1]-t[0]

    v = np.zeros(n)
    v[0] = v0
    
    #gamma0 está en grados asi que hay que pasarlo a rad
    gamma = np.zeros(n)
    gamma[0] = gamma0 * np.pi /180
    
    v_dot = np.zeros(n)
    gamma_dot = np.zeros(n)

    v_dot[0] = (A3 - (cd0 + k*A4**2)*v0**2 - 2*k*A4*np.cos(gamma0) 
                    - np.sin(gamma0) - k*np.cos(gamma0)**2/v0**2)
    gamma_dot[0] = v0*A4

    for i in range(1, n):
        v[i] = v[i - 1] + deltat * (A3 - (cd0 + k*A4**2)*v[i - 1]**2 - 2*k*A4*np.cos(gamma[i-1]) 
                    - np.sin(gamma[i - 1]) - k*np.cos(gamma[i-1])**2/v[i - 1]**2)
        gamma[i] = gamma[i-1] + A4 * v[i - 1]* deltat
        
        
        v_dot[i] = (A3 - (cd0 + k*A4**2)*v[i]**2 - 2*k*A4*np.cos(gamma[i]) 
                    - np.sin(gamma[i]) + + k*np.cos(gamma[i])**2/v[i]**2)
        gamma_dot[i] = v[i]*A4
    
    return np.stack((v, gamma)), np.stack((v_dot, gamma_dot))

def custom_ecs_D1():
    library_functions = [
        lambda v : v,
        lambda v : v**2,
        lambda theta: np.sin(theta),
        lambda theta: np.cos(theta),
        lambda v, theta: np.cos(theta)**2/v**2,
        #lambda v: 1/v**2,
        #lambda v: 1/v**3,
        lambda cte: 1
    ]
    library_function_names = [
        lambda v : v,
        lambda v : v + "^2",
        lambda theta: 'sin(' + theta + ")", 
        lambda theta: 'cos(' + theta + ")",
        lambda v, theta: 'cos(' + theta + ")^2" + '/' + v + "^2",
        #lambda v: '1/' + v + "^2",
        #lambda v: '1/' + v + "^3",
        lambda cte: "1"+cte
    ]
    library = ps.CustomLibrary(library_functions=library_functions, function_names=library_function_names,
                              interaction_only=True)
    return library

def casoD1(n_trayec, t, coefs_ecs, t_val, cond_inic):
    # condiciones iniciales:
    v0 = np.ones(n_trayec)
    gamma0 = np.ones(n_trayec)
    for i in range(n_trayec):
        v0[i] = np.random.uniform(low=30, high=100)
        gamma0[i] = np.random.uniform(low=10, high=360)

    # obtengo la trayectoria:
    data = []
    data_dot = []
    
    for i in range(n_trayec):
        vars, vars_dot = ecs_casoD1(t, [v0[i], gamma0[i]], coefs_ecs)
        vars = vars.T
        vars_dot = vars_dot.T

        data.append(vars)
        data_dot.append(vars_dot)

    data_val, _ = ecs_casoD1(t_val, cond_inic, coefs_ecs)
    return data, data_dot, custom_ecs_D1(), data_val.T

# ------------------ CASO D.2 ----------------------- #
def ecs_casoD2(t, cond_inic, coefs):
    A6, A8, A9, A10 = coefs
    T0, gamma0 = cond_inic

    n = t.shape[0]
    deltat = t[1]-t[0]

    T = np.zeros(n)

    #gamma0 está en grados asi que hay que pasarlo a rad
    gamma = np.zeros(n)
    gamma[0] = gamma0 * np.pi /180
    
    T_dot = np.zeros(n)
    T_dot[0] = A10
    gamma_dot = np.ones(n)*A6


    for i in range(1, n):
        gamma[i] = gamma[i-1] + A6 * deltat
        #T[i] = A7 + + A4*np.cos(gamma[i])**2 + A5*np.cos(gamma[i]) + W*np.sin(gamma[i])

        T[i] = T[i-1] + deltat*(A10*np.cos(gamma[i-1]) - A9*np.sin(gamma[i-1]) - A8*np.sin(2*gamma[i-1])) 
        T_dot[i] = A10*np.cos(gamma[i]) - A9*np.sin(gamma[i]) - A8*np.sin(2*gamma[i]) 

    
    return np.stack((T, gamma)), np.stack((T_dot, gamma_dot))

def custom_ecs_D2():
    library_functions = [
        lambda theta: np.sin(2*theta),
        lambda theta: np.sin(theta),
        lambda theta: np.cos(theta),
        lambda cte: 1
    ]
    library_function_names = [
        
        lambda theta: 'sin(2*' + theta + ")", 
        lambda theta: 'sin(' + theta + ")", 
        lambda theta: 'cos(' + theta + ")",
        lambda cte: "1"+cte
    ]
    library = ps.CustomLibrary(library_functions=library_functions, function_names=library_function_names,
                              interaction_only=True)
    return library

def casoD2(n_trayec, t, coefs_ecs, t_val, cond_inic):
    # condiciones iniciales:
    T0 = np.ones(n_trayec)
    gamma0 = np.ones(n_trayec)


    for i in range(n_trayec):
        T0[i] = np.random.uniform(low=20, high=50)
        gamma0[i] = np.random.uniform(low=10, high=360)


    # obtengo la trayectoria:
    data = []
    data_dot = []
    
    for i in range(n_trayec):
        vars, vars_dot = ecs_casoD2(t, [T0[i], gamma0[i]], coefs_ecs)
        vars = vars.T
        vars_dot = vars_dot.T

        data.append(vars)
        data_dot.append(vars_dot)


    data_val, _ = ecs_casoD2(t_val, cond_inic, coefs_ecs)
    return data, data_dot, custom_ecs_D2(), data_val.T






        

