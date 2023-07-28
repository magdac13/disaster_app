import os

import pandas as pd
from disaster.disaster_app.models import Asteroid
import csv


class AsteroidScrypt():
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'asteroid_data.csv')
        self.data = self.clean_data_from_file(self.data_path)
    def clean_data_from_file(self, data):

        df = pd.read_csv(data,
                         sep=',',
                         header=0,
                         encoding='utf-8',
                         )
        df = df.drop(columns=['Absolute Magnitude', 'Est Dia in KM(min)', 'Est Dia in M(min)',
                              'Est Dia in M(max)', 'Est Dia in Miles(min)', 'Est Dia in Miles(max)',
                              'Est Dia in Feet(min)', 'Est Dia in Feet(max)', 'Epoch Date Close Approach',
                              'Relative Velocity km per sec', 'Miles per hour', 'Miss Dist.(Astronomical)',
                              'Miss Dist.(lunar)', 'Miss Dist.(miles)', "Orbit ID'Miss Dist.(miles)",
                              'Orbit Uncertainity', 'Minimum Orbit Intersection', 'Jupiter Tisserand Invariant',
                              'Epoch Osculation', 'Eccentricity', 'Semi Major Axis', 'Semi Major Axis',
                              'Asc Node Longitude', 'Orbital Period', 'Perihelion Distance', 'Perihelion Arg',
                              'Aphelion Dist', 'Perihelion Time', 'Mean Anomaly', 'Mean Motion', 'Equinox'
                              ])

        df = df.rename(columns={
            'Name': 'name',
            'Est Dia in KM(max)': 'diameter',
            'Close Approach Date': 'close_approach_date',
            'Relative Velocity km per hr': 'velocity',
            'Miss Dist.(kilometers)': 'miss_distance',
            'Orbiting Body': 'orbiting_body',
            'Hazardous': 'is_hazardous'
                                })



        return df

    data = 'data_files/nasa.csv'
    df = clean_data_from_file(data)
    df.to_csv('data_files/nasa_clean.csv', index=False, sep=';')

    def save_data_from_file_to_db(self, data):
        df = pd.read_csv(data,
                         sep=',',
                         header=0,
                         encoding='utf-8')