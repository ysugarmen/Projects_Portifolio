from scipy.constants import g
import numpy as np
import config as con


def water_film_thickness(humidity):
    return (con.em * con.Cb * humidity) / ((1 - humidity)*(1 + (con.Cb - 1)*humidity))


def capillary_force(particle_size, humidity):
    h = water_film_thickness(humidity)*1e-9
    return -8 * np.pi * (particle_size / 2) * (h * con.Rg * con.TEMP * np.log(humidity/100)) / con.V0


def waals_force(particle_size, humidity):
    # van der Waals force in newtons
    h = water_film_thickness(humidity) * 1e-9  # Convert to meters
    r = particle_size / 2
    return (con.H2 * r) / (6 * con.a**2) + ((con.H1 - con.H2) * r) / (6 * (2 * h + con.a)**2)


def adhesion_force(particle_size, humidity):
    F_c = capillary_force(particle_size, humidity)
    F_w = waals_force(particle_size, humidity)
    return F_c + F_w


def gravity_force(particle_size):
    return np.pi * ((2*particle_size)**3) * con.PARTICLE_DENSITY * g / 6 + np.random.uniform(-0.01, 0.01)  # Adding some randomness to the condition


def buoyancy_force(particle_size):
    return np.pi * ((2*particle_size)**3) * con.AIR_DENSITY * g / 6


def fluid_drag_force(particle_size, wind_speed, velocity_particle):
    m = (4 / 3) * np.pi * (particle_size / 2) ** 3 * con.PARTICLE_DENSITY
    m_prime = 1 / ((1 / m) + (1 / con.M))
    Rer = (con.AIR_DENSITY * wind_speed * particle_size) / con.VISCOSITY_AIR
    Cd = (24 * (1 + 0.15 * Rer**0.687)) / Rer
    tau_p = (2 * con.PARTICLE_DENSITY * (particle_size**2)) / (9 * con.VISCOSITY_AIR * Cd * Rer)
    return m_prime * (wind_speed - velocity_particle) / tau_p


def collision_force(particle_size, velocity_particle):
    # Elastic deformation coefficients
    a1 = (1 - con.v1**2) / (np.pi * con.E1)
    a2 = (1 - con.v2 ** 2) / (np.pi * con.E2)
    # Collision coefficient
    n = 4 / (3 * np.pi * (a1 + a2))
    # Equivalent mass'
    m = (4 / 3) * np.pi * (particle_size / 2) ** 3 * con.PARTICLE_DENSITY
    m_prime = 1 / ((1 / m) + (1 / con.M))
    # Maximum compression displacement
    Smax = ((5 * m_prime / (4 * n)) * velocity_particle**2)**0.4
    # Compression displacement
    S = (1 / n) * np.trapz([Smax * np.sin(x) for x in np.linspace(0, np.pi, 100)])
    return n * S**1.5

def electrostatic_force(particle_size):
    particle_radios = particle_size/2
    q = con.XI*((4*(10**3))*np.pi*con.PARTICLE_DENSITY*(particle_radios)**3)/3
    F_e = (q**2)/(4*con.EPSILON_0*(2*particle_radios + con.a)**2)
    return F_e


def friction_force(force):
    return con.mu * force


def total_forces_normal(particle_size, wind_speed, humidity, theta, velocity_particle, delta):
    F_c = capillary_force(particle_size, humidity)
    F_w = waals_force(particle_size, humidity)
    F_g = gravity_force(particle_size) * np.cos(np.radians(delta))
    F_p = collision_force(particle_size, velocity_particle)
    F_b = buoyancy_force(particle_size) * np.cos(np.radians(delta)) * con.BUOYANCY_AF
    F_d = fluid_drag_force(particle_size, wind_speed, velocity_particle) * np.cos(np.radians(theta)) * con.DRAG_AF
    particle_mass = con.PARTICLE_MASSES_DICT[particle_size]*1.5
    E_p = (1/2) * particle_mass * (velocity_particle**2)
    F_e = electrostatic_force(particle_size)
    return F_c + F_w + F_g + F_e + E_p*np.cos(np.radians(theta))**2 - F_p - F_b - F_d


def total_forces_tangential(particle_size, wind_speed, theta, velocity_particle, delta):
    F_g = gravity_force(particle_size) * np.sin(np.radians(delta))
    F_d = fluid_drag_force(particle_size, wind_speed, velocity_particle) * con.DRAG_AF
    F_b = buoyancy_force(particle_size) * np.sin(np.radians(delta)) * con.BUOYANCY_AF
    particle_mass = con.PARTICLE_MASSES_DICT[particle_size]*1.5
    E_p = (1/2) * particle_mass * (velocity_particle**2)
    F_t_1 = F_g + F_d * np.sin(np.radians(theta)) * np.sin(np.radians(con.PHI)) - F_b + E_p*(np.sin(np.radians(theta))**2)*(np.sin(np.radians(con.PHI))**2)
    F_t_2 = F_d * np.sin(np.radians(theta)) * np.cos(np.radians(con.PHI)) + E_p*(np.sin(np.radians(theta))**2)*(np.cos(np.radians(con.PHI))**2)
    return F_t_1, F_t_2

