import numpy as np
import EffectiveForces as EF
import config as con


def main(particle_size, wind_speed, humidity, theta, velocity_particle, delta):
    F_n = EF.total_forces_normal(particle_size, wind_speed, humidity, theta, velocity_particle, delta)
    F_t_1, F_t_2 = EF.total_forces_tangential(particle_size, wind_speed, theta, velocity_particle, delta)
    F_f_1 = EF.friction_force(F_t_1)
    F_f_2 = EF.friction_force(F_t_2)
    con1 = condition_1(F_n)
    con2 = condition_2(F_t_1, F_f_1, theta)
    con3 = condition_3(F_t_2, F_f_2, theta)
    return con1 & con2 & con3


def condition_1(force):
    return force >= 0


def condition_2(force, f_f, theta):
    return force <= f_f*(np.sin(np.radians(theta)))*(np.sin(np.radians(con.PHI)) + 0.1)


def condition_3(force, f_f, theta):
    return force <= f_f*(np.sin(np.radians(theta)))*(np.cos(np.radians(con.PHI)) + 0.1)
