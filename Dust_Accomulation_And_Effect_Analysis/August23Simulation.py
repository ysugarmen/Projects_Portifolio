import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
import config as con
import AdhesionSimulation as Asim


def process_file(file, mirror):
    data = pd.read_excel(file)

    # Calculate current clean mirror value
    sample_data = data[data['Location'] == 'Sample']
    current_clean_mirror_value = (sample_data['SCI'] - sample_data['SCE']).mean()

    # Calibration coefficient
    a = current_clean_mirror_value / con.CLEAN_MIRROR_REF_VAL

    # Filter data for the specified mirror
    mirror_data = data[data['Location'].str.startswith(mirror)]
    mirror_data['Date'] = pd.to_datetime(mirror_data['Date Stamp'], format='%m.%d.%y')
    mirror_data = mirror_data[(mirror_data['Date'] >= con.AUG23_STARTING_DATE) & (mirror_data['Date'] <= con.AUG23_ENDING_DATE)]

    # Calculate reflectivity value for each row and apply calibration
    mirror_data['Reflectivity Value'] = (mirror_data['SCI'] - mirror_data['SCE']) * a

    return mirror_data[['Date', 'Reflectivity Value']]


def load_reflectivity_data(directory, mirror):
    reflectivity_files = [os.path.join(directory, file) for file in os.listdir(directory)]
    all_mirror_data = pd.concat((process_file(file, mirror) for file in reflectivity_files), ignore_index=True)

    # Calculate average reflectivity value for each date
    avg_reflectivity_data = all_mirror_data.groupby('Date').agg({'Reflectivity Value': 'mean'}).reset_index()
    avg_reflectivity_data.rename(columns={'Reflectivity Value': 'Average Reflectivity'}, inplace=True)

    return avg_reflectivity_data


def load_enviromental_data(directory):
    wind_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.startswith('AvgWindSpeed') and file.endswith('.csv')]
    humidity_data = pd.read_csv(os.path.join(directory, con.AUG23_HUMIDITY_DATA_FILE))
    temp_data = pd.read_csv(os.path.join(directory, con.AUG23_TEMP_DATA_FILE))

    wind_data = pd.concat((pd.read_csv(file) for file in wind_files), ignore_index=True)

    wind_data['Date'] = pd.to_datetime(wind_data['Date'], format='%d/%m/%Y %H:%M')
    humidity_data['Date'] = pd.to_datetime(humidity_data['Date'], format='%d/%m/%Y %H:%M')
    temp_data['Date'] = pd.to_datetime(temp_data['Date'], format='%d/%m/%Y %H:%M')

    combined_data = wind_data.merge(humidity_data, on='Date').merge(temp_data, on='Date')
    # Strip time component and group by date
    combined_data['Date'] = combined_data['Date'].dt.date
    avg_combined_data = combined_data.groupby('Date').mean().reset_index()
    avg_combined_data['Date'] = pd.to_datetime(avg_combined_data['Date'])
    return avg_combined_data


def reflectivity_reduction(stuck_particles, initial_reflectivity):
    dust_amount = stuck_particles / con.NUM_OF_PARTICLES
    soiling_attenuation_parameter = con.REDUCTION_COEFFICIENT * dust_amount
    new_reflectivity = initial_reflectivity * np.exp(-2 * soiling_attenuation_parameter / np.cos(np.radians(60)))
    return max(new_reflectivity, 0)


def run_simulation_for_dates(dates, initial_reflectivity, enviromental_data):
    reflectivity_values = [initial_reflectivity]
    for date in dates[1:]:
        day_enviromental_data = enviromental_data[enviromental_data['Date'] == pd.Timestamp(date)]
        if not day_enviromental_data.empty:
            wind_speed = day_enviromental_data['Wind Speed'].values[0]
            humidity = day_enviromental_data['Humidity'].values[0]
            stuck_particles = Asim.run_simulation(wind_speed, humidity)[60]
            new_reflectivity = reflectivity_reduction(stuck_particles, reflectivity_values[-1])
            reflectivity_values.append(new_reflectivity)
    return reflectivity_values


def plot_comparison(dates, simulated_reflectivity, actual_reflectivity):
    plt.figure(figsize=(10, 6))
    plt.plot(dates, simulated_reflectivity, marker='o', label='Simulated Reflectivity')
    plt.plot(dates, actual_reflectivity, marker='o', label='Actual Reflectivity')
    plt.xlabel('Date')
    plt.ylabel('Reflectivity')
    plt.ylim([0, 1])
    plt.title('Simulated vs. Actual Reflectivity')
    plt.legend()
    plt.grid(True)
    plt.show()


def calculate_error_metrics(simulated, actual):
    mae = mean_absolute_error(actual, simulated)
    mse = mean_squared_error(actual, simulated)
    rmse = np.sqrt(mse)
    return mae, mse, rmse




if __name__ == "__main__":

    ref_data = load_reflectivity_data(con.AUG23_REF_DIR, con.AUG23_MIRROR_NAME)
    init_ref = ref_data['Average Reflectivity'][0]/100
    enviromental_data = load_enviromental_data(con.AUG23_ENV_DIR)

    dates = ref_data['Date'].values
    actual_reflectivities = ref_data['Average Reflectivity'].values/100

    simulated_reflectivities = run_simulation_for_dates(dates, init_ref, enviromental_data)

    plot_comparison(dates, simulated_reflectivities, actual_reflectivities)