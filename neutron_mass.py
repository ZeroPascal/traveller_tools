import numpy as np
from scipy.integrate import solve_ivp

# Define constants
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
c = 3.0e8         # Speed of light (m/s)

# Equation of state: Relates pressure P to energy density epsilon (simple polytropic example)
def equation_of_state(energy_density):
    K = 1e-9  # Polytropic constant (adjust for realistic models)
    gamma = 2.0  # Polytropic index
    return K * energy_density**gamma

def tov_equations(r, y):
    """
    TOV equations to integrate.

    Parameters:
    r : float
        Radius (m).
    y : array
        Array containing [m(r), P(r)] where:
        - m(r): Enclosed mass (kg).
        - P(r): Pressure (Pa).

    Returns:
    dydr : array
        Derivatives [dm/dr, dP/dr].
    """
    m, P = y

    # If pressure is effectively zero, stop integration
    if P <= 0:
        return [0, 0]

    # Calculate energy density from pressure (inverse of equation of state)
    epsilon = (P / 1e-9)**(1 / 2.0)  # Adjust based on equation_of_state

    # TOV equations
    dm_dr = 4 * np.pi * r**2 * epsilon
    dP_dr = (
        -G * (epsilon + P / c**2) * (m + 4 * np.pi * r**3 * P / c**2)
        / (r**2 * (1 - 2 * G * m / (r * c**2)))
    )

    return [dm_dr, dP_dr]

def find_star_radius_and_mass(mass_guess, central_pressure):
    """
    Solves the TOV equations to find the radius and total mass of a neutron star.

    Parameters:
    mass_guess : float
        Initial mass guess (kg).
    central_pressure : float
        Central pressure (Pa).

    Returns:
    radius : float
        Radius of the star (m).
    total_mass : float
        Total mass of the star (kg).
    """
    # Initial conditions
    r_initial = 1e-3  # Start at a small radius to avoid singularity (m)
    m_initial = 0     # No mass enclosed at the center (kg)
    P_initial = central_pressure

    # Integration range (stop when pressure reaches zero)
    r_max = 1e6  # Initial guess for maximum radius (m)

    # Solve TOV equations
    sol = solve_ivp(
        tov_equations,
        [r_initial, r_max],
        [m_initial, P_initial],
        method="RK45",
        dense_output=True,
        events=lambda r, y: y[1],  # Stop when pressure (y[1]) reaches zero
    )

    # Extract results
    print(sol)
    radius = sol.t_events[0][0]  # Radius where pressure becomes zero
    total_mass = sol.y[0][-1]    # Total mass enclosed

    return radius, total_mass

# Example usage
if __name__ == "__main__":
    central_pressure = 1e35  # Example central pressure (Pa)
    mass_guess = 1.4 * 1.989e30  # Example mass guess (~1.4 solar masses in kg)

    radius, total_mass = find_star_radius_and_mass(mass_guess, central_pressure)
    print(f"Radius: {radius / 1e3:.2f} km")
    print(f"Total Mass: {total_mass / 1.989e30:.2f} solar masses")
