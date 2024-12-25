import config as con
import AdhesionSimulation as Asim
import numpy as np
import matplotlib.pyplot as plt


def reflectivity_reduction(stuck_particles_per_angle, initial_reflectivities):
    reflectivity_reduction_per_angle = {}
    for angle, count in stuck_particles_per_angle.items():
        dust_amount = count / con.NUM_OF_PARTICLES
        initial_reflectivity = initial_reflectivities[angle]
        soiling_attenuation_parameter = con.REDUCTION_COEFFICIENT * dust_amount
        new_reflectivity = initial_reflectivity * np.exp(-2 * soiling_attenuation_parameter / np.cos(np.radians(angle)))
        reflectivity = max(new_reflectivity, 0)
        reflectivity_reduction_per_angle[angle] = reflectivity

    return reflectivity_reduction_per_angle


def reflectivity_reduction_output(day, reflectivity_reduction_per_angle):
    for angle, reflectivity in reflectivity_reduction_per_angle.items():
        initial_reflectivity = con.INITIAL_REFLECTIVITIES[angle]
        print(
            f'Day {day} - Tilt angle {angle}°: Reflectivity before: {initial_reflectivity:.2f}, Reflectivity after: {reflectivity:.2f}')


def calculate_average_ddr(reflectivity_reduction_per_angle, initial_reflectivities):
    total_ddr = 0
    count = 0
    for angle, new_reflectivity in reflectivity_reduction_per_angle.items():
        initial_reflectivity = initial_reflectivities[angle]
        ddr = 1 - new_reflectivity / initial_reflectivity
        total_ddr += ddr
        count += 1

    average_ddr = total_ddr / count if count != 0 else 0
    print(f'Average DDR: {average_ddr * 100:.2f}%')

    return average_ddr


def plot_reflectivity(days, reflectivity_data):
    for angle, reflectivities in reflectivity_data.items():
        plt.figure(figsize=(10, 6))
        plt.plot(days, reflectivities, marker='o', label=f'Tilt Angle {angle}°')
        plt.xlabel('Day')
        plt.ylabel('Reflectivity')
        plt.ylim([0, 1])
        plt.title(f'Reflectivity vs. Day for Tilt Angle {angle}°')
        plt.legend()
        plt.grid(True)
        plt.show()


def plot_all_reflectivities(reflectivity_data, days):
    plt.figure(figsize=(10, 6))
    for day, reflectivities in reflectivity_data.items():
        plt.plot(list(reflectivities.keys()), list(reflectivities.values()), marker='o', label=f'Day {day}')
    plt.xlabel('Tilt Angle (degrees)')
    plt.ylabel('Reflectivity')
    plt.ylim([0, 1])
    plt.title('Reflectivity vs. Tilt Angle for All Days')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_average_ddr(days, average_ddr_values):
    plt.figure(figsize=(10, 6))
    plt.plot(days, average_ddr_values, marker='o', label='Average DDR')
    plt.xlabel('Day')
    plt.ylabel('Average Daily Degradation Rate (DDR)')
    plt.title('Average DDR vs. Day')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    days = range(1, 8)
    initial_reflectivities = con.INITIAL_REFLECTIVITIES.copy()
    reflectivity_data = {angle: [] for angle in initial_reflectivities.keys()}
    average_ddr_values = []
    all_reflectivities = {}

    for day in days:
        wind_speed = np.random.choice(con.WIND_SPEEDS)
        humidity = np.random.choice(con.HUMIDITIES)
        stuck_particles_per_angle = Asim.run_simulation(wind_speed, humidity)
        reflectivity_reduction_per_angle = reflectivity_reduction(stuck_particles_per_angle, initial_reflectivities)
        reflectivity_reduction_output(day, reflectivity_reduction_per_angle)

        for angle in reflectivity_reduction_per_angle.keys():
            reflectivity_data[angle].append(reflectivity_reduction_per_angle[angle])

        average_ddr = calculate_average_ddr(reflectivity_reduction_per_angle, initial_reflectivities)
        average_ddr_values.append(average_ddr)

        initial_reflectivities = reflectivity_reduction_per_angle.copy()
        all_reflectivities[day] = reflectivity_reduction_per_angle

    plot_reflectivity(days, reflectivity_data)
    plot_average_ddr(days, average_ddr_values)
    plot_all_reflectivities(all_reflectivities, days)
