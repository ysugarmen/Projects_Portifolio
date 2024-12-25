import numpy as np
import matplotlib.pyplot as plt
import config as con
import ParticleAdhesion as PA


def run_simulation(wind_speed, humidity):
    stuck_particles_per_angle = {angle: 0 for angle in con.TILT_ANGLES}

    for _ in range(con.NUM_OF_PARTICLES):
        particle_size = np.random.choice(con.PARTICLE_SIZES)
        for delta in con.TILT_ANGLES:
            theta = np.random.uniform(0, 5)
            if PA.main(particle_size, wind_speed, humidity, theta, wind_speed, delta):
               stuck_particles_per_angle[delta] += 1

    return stuck_particles_per_angle

def simulation_output(stuck_particles_per_angle):
    # Print results
    for angle, count in stuck_particles_per_angle.items():
        print(f'Tilt angle {90-angle}°: {count} particles stuck')
    print(f'Total particles: {con.NUM_OF_PARTICLES * len(con.TILT_ANGLES)}')
    print(f'Total stuck particles: {sum(stuck_particles_per_angle.values())}')
    print(
        f'Percentage stuck: {sum(stuck_particles_per_angle.values()) / (con.NUM_OF_PARTICLES * len(con.TILT_ANGLES)) * 100:.2f}%')
    # Generate bar chart
    generate_bar_chart(stuck_particles_per_angle)


def generate_bar_chart(stuck_particles_per_angle):
    tilt_angles = [90 - angle for angle in stuck_particles_per_angle.keys()]
    percentages_stuck = [(count / con.NUM_OF_PARTICLES) * 100 for count in stuck_particles_per_angle.values()]

    # Creating the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(tilt_angles, percentages_stuck, color='darkblue', width=2.5)
    plt.xlabel('Tilt Angle (degrees)')
    plt.ylabel('Percentage of Particles Stuck (%)')
    plt.title('Percentage of Particles Stuck vs. Tilt Angle')
    plt.grid(axis='y')

    # Displaying the plot
    plt.show()

if __name__ == "__main__":
    # Choose wind speed and humidity randomly once for the entire simulation
    wind_speed = np.random.choice(con.WIND_SPEEDS)
    humidity = np.random.choice(con.HUMIDITIES)
    stuck_particles_per_angle = run_simulation(wind_speed, humidity)
    simulation_output(stuck_particles_per_angle)



