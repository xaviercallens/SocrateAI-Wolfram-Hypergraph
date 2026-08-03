import math
import scipy.special as sp

def u_n_rho(n, rho):
    total = 0.0
    for k in range(n + 1):
        # C(n+rho, k+rho) = Gamma(n+rho+1) / (Gamma(k+rho+1) Gamma(n-k+1))
        term1 = sp.gamma(n + rho + 1) / (sp.gamma(k + rho + 1) * math.gamma(n - k + 1))
        # C(n+k+rho, k) = Gamma(n+k+rho+1) / (Gamma(n+rho+1) math.gamma(k+1))
        term2 = sp.gamma(n + k + rho + 1) / (sp.gamma(n + rho + 1) * math.gamma(k + 1))
        # C(2k, k) = math.gamma(2*k+1) / (math.gamma(k+1)**2)
        term3 = math.gamma(2 * k + 1) / (math.gamma(k + 1)**2)
        
        term = (term1**2) * term2 * term3 * ((-4)**(n - k))
        total += term
    return total

def v_n(n):
    # numerical derivative
    drho = 1e-5
    return (u_n_rho(n, drho) - u_n_rho(n, -drho)) / (2 * drho)

print("v_1 =", v_n(1))
print("v_2 =", v_n(2))
