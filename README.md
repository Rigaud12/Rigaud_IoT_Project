# IoT Data Generator – wxPython Application

This project is a wxPython-based desktop application that generates artificial IoT sensor data for 1000 users, each with 1000 time-sampled sensor readings.  
The application supports data generation, exporting to JSON/CSV, descriptive statistics, and plotting visualizations using Matplotlib.

---

## 🔧 Features

### ✅ **1. Generate Artificial IoT Data**
Uses the `faker` library to create:
- First name, last name  
- Age  
- Gender  
- Username  
- Address  
- Email  

For each user, 1000 IoT sensor readings are generated:
- Date & time (sampled every 6 hours from Jan 1st, 2015 to present)
- Outside temperature (70–95°F)
- Room temperature (outside temp minus 0–10°F)
- Outside humidity (50–95%)
- Room humidity (outside humidity minus 0–10%)

---

### ✅ **2. Save Files**
The application allows exporting the generated dataset as:
- **CSV file**
- **JSON file**

---

### ✅ **3. Statistics**
A descriptive summary of the numeric columns is shown in a popup window.

---

### ✅ **4. Plots**
The app includes three visualizations:

#### 📊 **Plot A – Histogram of Outside Temperature**
Shows frequency distribution of all outside temperatures in the dataset.

#### 📈 **Plot B – Line Graph: Outside vs Room Temperature**
Displays a 500-sample comparison line plot of outside vs room temperature.

#### 📊 **Plot C – Combined Histogram**
Overlaid histograms of:
- Outside temperature  
- Room temperature  
- Outside humidity  
- Room humidity  

---

## 📦 Requirements

Before running the program, install the required libraries:

```bash
pip install wxPython pandas matplotlib faker
pip install wxPython pandas matplotlib faker numpy
pip install pyobjc-framework-Cocoa
Python 3.9+
