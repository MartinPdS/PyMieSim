import numpy as np
from scipy import special
from numpy import cos, sin
from scipy.special import spherical_yn as yn, spherical_jn as jn, hankel1 as h
from scipy.special import legendre as Pn, factorial as fac



def hn(n, z, derivative=False):
    return jn(n,z,derivative) + 1j*yn(n,z,derivative)


def Pnm(n, m, theta):
    """Eq:II.77 """
    if m < 0: return (-1)**m * fac(n-m)/fac(n+m) * Pnm(n,-m,theta)
    else:     return (-1)**m * sin(theta)**m * Pn(n).deriv(m)(cos(theta))


def Pin(n, x):
    lpn = Pn(n)
    lpn_p = lpn.deriv()

    return -1*lpn_p(cos(x))


def Taun(n, x):
    lpn = Pn(n)
    lpn_p = lpn.deriv()
    lpn_p2 = lpn_p.deriv()

    return -1*cos(x)*lpn_p(cos(x)) + sin(x)**2*lpn_p2(cos(x))


def Taunk(n, k, theta):
    """Eq: III.51 """
    return Pn(n).deriv(k)(cos(theta))


def Pink(n, k, theta):
    """Eq: III.52 """
    return Pn(n)(cos(theta)) / sin(theta)

def M1o1n(n, k, r, theta, phi):
    theta_comp =      cos(phi) * Pin(n, theta)  * jn(n, k * r)
    phi_comp   = -1 * sin(phi) * Taun(n, theta) * jn(n, k * r)
    r_comp     = np.zeros(shape = theta.shape, dtype=np.complex)

    return np.array([r_comp, theta_comp, phi_comp])


def M1e1n(n, k, r, theta, phi):
    theta_comp = -1*sin(phi) * Pin(n, theta)  * jn(n, k * r)
    phi_comp =   -1*cos(phi) * Taun(n, theta) * jn(n, k * r)
    r_comp = np.zeros(shape = theta.shape, dtype=np.complex)

    return np.array([r_comp, theta_comp, phi_comp])


def N1o1n(n, k, r, theta, phi):
    p = k * r
    theta_comp = sin(phi) * Taun(n, theta) * (jn(n, p) + p * jn(n, p, derivative=True) ) / p
    phi_comp   = cos(phi) * Pin(n, theta)  * (jn(n, p) + p * jn(n, p, derivative=True) ) / p
    r_comp     = sin(phi) * n * (n + 1) * sin(theta) * Pin(n, theta) * jn(n, p) / p

    return np.array([r_comp, theta_comp, phi_comp])



def N1e1n(n, k, r, theta, phi):
    p = k*r
    theta_comp =    cos(phi) * Taun(n, theta) * ( jn(n, p) + p * jn(n, p, derivative=True) ) / p
    phi_comp   = -1*sin(phi) * Pin(n, theta)  * ( jn(n, p) + p * jn(n, p, derivative=True) ) / p
    r_comp     =    cos(phi) * n * (n+1)      * sin(theta) * Pin(n, theta) * jn(n, p) / p

    return np.array([r_comp, theta_comp, phi_comp])




def M3o1n(n, k, r, theta, phi):
    theta_comp =      cos(phi) * Pin(n, theta)  * hn(n, k * r)
    phi_comp   = -1 * sin(phi) * Taun(n, theta) * hn(n, k * r)
    r_comp     = np.zeros(shape = theta.shape, dtype=np.complex)

    return np.array([r_comp, theta_comp, phi_comp])


def M3e1n(n, k, r, theta, phi):
    theta_comp = -1*sin(phi) * Pin(n, theta)  * hn(n, k * r)
    phi_comp =   -1*cos(phi) * Taun(n, theta) * hn(n, k * r)
    r_comp = np.zeros(shape = theta.shape, dtype=np.complex)

    return np.array([r_comp, theta_comp, phi_comp])


def N3o1n(n, k, r, theta, phi):
    p = k * r
    theta_comp = sin(phi) * Taun(n, theta) * (hn(n, p) + p * hn(n, p, derivative=True) ) / p
    phi_comp   = cos(phi) * Pin(n, theta)  * (hn(n, p) + p * hn(n, p, derivative=True) ) / p
    r_comp     = sin(phi) * n * (n + 1) * sin(theta) * Pin(n, theta) * hn(n, p) / p

    return np.array([r_comp, theta_comp, phi_comp])



def N3e1n(n, k, r, theta, phi):
    p = k*r
    theta_comp =    cos(phi) * Taun(n, theta) * ( hn(n, p) + p * hn(n, p, derivative=True) ) / p
    phi_comp   = -1*sin(phi) * Pin(n, theta)  * ( hn(n, p) + p * hn(n, p, derivative=True) ) / p
    r_comp     =    cos(phi) * n * (n+1)      * sin(theta) * Pin(n, theta) * hn(n, p) / p

    return np.array([r_comp, theta_comp, phi_comp])

def _Psi(type, n, x):
    """Eq:II.83-86 """
    if type == 0: return x*jn(n, x)
    if type == 1: return jn(n, x)
    if type == 2: return yn(n, x)
    if type == 3: return _Psi(1, n, x) + 1j * _Psi(2, n, x)
    if type == 4: return _Psi(1, n, x) - 1j * _Psi(2, n, x)


def Psi(n, x):
    return x * _Psi(1, n, x)

def Psi_p(n, x):
    return x * _Psi_p(1, n, x) + _Psi(1, n, x)


def _Psi_p(type, n, x):
    """Eq:II.83-86 """
    if type == 0: return x*jn(n, x, derivative=True) + jn(n, x, derivative=False)
    if type == 1: return jn(n, x, derivative=True)
    if type == 2: return yn(n, x, derivative=True)
    if type == 3: return jn(n,x,derivative=True) + 1j*yn(n,x,derivative=True)
    if type == 4: return jn(n,x,derivative=True) - 1j*yn(n,x,derivative=True)


def Xi(n, x):
    """Eq:II.87 """
    return x * _Psi(4, n, x)

def Xi_p(n, x):
    return x * _Psi_p(4, n, x) + _Psi(4, n, x)









#-
