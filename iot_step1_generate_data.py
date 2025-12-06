import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime

fake = Faker()


# ---------------------------------------------------------
# 1. Generate 1000 user records
# ---------------------------------------------------------
def generate_user_data(num_users=1000):
    users = []

    for user_id in range(num_users):
        profile = fake.simple_profile()

        users.append({
            "user_id": user_id,
            "first_name": profile["name"].split()[0],
            "last_name": profile["name"].split()[-1],
            "age": random.randint(18, 80),
            "gender": profile["sex"],
            "username": profile["username"],
            "address": fake.address().replace("\n", ", "),
            "email": profile["mail"]
        })

    return pd.DataFrame(users)



# ---------------------------------------------------------
# 2. Generate 1000 sensor samples per user
# ---------------------------------------------------------
def generate_sensor_data(users_df, samples_per_user=1000):
    all_records = []

    start_date = datetime(2015, 1, 1)

    for _, user in users_df.iterrows():
        # time sampled every 6 hours
        timestamps = pd.date_range(
            start=start_date,
            periods=samples_per_user,
            freq="6H"
        )

        for ts in timestamps:
            outside_temp = random.uniform(70, 95)
            room_temp = outside_temp - random.uniform(0, 10)

            outside_humidity = random.uniform(50, 95)
            room_humidity = outside_humidity - random.uniform(0, 10)

            all_records.append({
                "user_id": user["user_id"],
                "datetime": ts,
                "outside_temp": outside_temp,
                "outside_humidity": outside_humidity,
                "room_temp": room_temp,
                "room_humidity": room_humidity
            })

    return pd.DataFrame(all_records)



# ---------------------------------------------------------
# 3. Merge users with their sensor data
# ---------------------------------------------------------
def combine_data(users_df, sensors_df):
    return sensors_df.merge(users_df, on="user_id", how="left")



# ---------------------------------------------------------
# 4. REQUIRED BY YOUR GUI — Generate & return full dataset
# ---------------------------------------------------------
def generate_users_and_sensors():
    print("Generating users...")
    users_df = generate_user_data()
    print("Users generated:", len(users_df))

    print("Generating sensor data (this may take a moment)...")
    sensors_df = generate_sensor_data(users_df)
    print("Sensor records generated:", len(sensors_df))

    print("Combining data...")
    full_df = combine_data(users_df, sensors_df)

    print("Data generation complete.")
    return full_df



# ---------------------------------------------------------
# 5. Allow running file standalone (optional)
# ---------------------------------------------------------
if __name__ == "__main__":
    df = generate_users_and_sensors()
    print(df.head())
    df.head(1000).to_csv("iot_sample_preview.csv", index=False)
    print("Sample saved as iot_sample_preview.csv")
