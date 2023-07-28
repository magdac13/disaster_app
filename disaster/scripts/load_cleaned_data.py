import os
import pandas as pd
from disaster_app.models import Asteroid
import csv


class AsteroidScrypt:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_files','archive', 'nasa.csv')
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

    def save_data_to_csv(self):
        self.data.to_csv('data_files/archive/nasa_clean.csv', index=False, sep=';')

    def save_data_from_file_to_db(self):

        for _, row in self.data.iterrows():
            asteroid = Asteroid(
                name=row['name'],
                diameter=row['diameter'],
                close_approach_date=row['close_approach_date'],
                velocity=row['velocity'],
                miss_distance=row['miss_distance'],
                orbiting_body=row['orbiting_body'],
                is_hazardous=row['is_hazardous']
            )
            asteroid.save()


asteroid_scrypt = AsteroidScrypt()
asteroid_scrypt.save_data_to_csv()
asteroid_scrypt.save_data_from_file_to_db()
