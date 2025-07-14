import tkinter as tk
from tkinter import messagebox
import csv
import matplotlib.pyplot as plt

def calculate_bmi(weight, height_in_feet):
    # Convert height from feet to meters
    height_in_meters = height_in_feet * 0.3048
    return weight / (height_in_meters ** 2)

def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

def save_data(weight, height_in_feet, age, bmi, category):
    with open("bmi_data.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([weight, height_in_feet, age, bmi, category])

def plot_bmi_trends():
    weights, heights, ages, bmis = [], [], [], []
    
    try:
        with open("bmi_data.csv", mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                weights.append(float(row[0]))
                heights.append(float(row[1]))
                ages.append(int(row[2]))
                bmis.append(float(row[3]))
        
        plt.plot(range(len(bmis)), bmis, label="BMI Trend")
        plt.xlabel("Entries")
        plt.ylabel("BMI")
        plt.title("BMI Trend Over Time")
        plt.legend()
        plt.show()
    except FileNotFoundError:
        messagebox.showerror("Error", "No BMI data found to display.")

def on_calculate():
    try:
        weight = float(weight_entry.get())
        height_in_feet = float(height_entry.get())
        age = int(age_entry.get())
        
        if weight <= 0 or height_in_feet <= 0 or age <= 0:
            messagebox.showerror("Invalid Input", "Weight, height, and age must be positive numbers.")
            return
        
        bmi = calculate_bmi(weight, height_in_feet)
        category = categorize_bmi(bmi)
        
        result_label.config(text=f"Your BMI is: {bmi:.2f}\nCategory: {category}\nAge: {age} years")
        
        # Save data to file
        save_data(weight, height_in_feet, age, bmi, category)
        
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numerical values.")

# Set up GUI
root = tk.Tk()
root.title("BMI Calculator")

# Set background color to Lavender
root.configure(bg="#E6E6FA")  # Lavender color hex code

# Maximize the window
root.state('zoomed')  # This maximizes the window upon startup

# Set a fixed large font size for a maximized screen
font_size = 16 
font = ("Helvetica", font_size, "bold")

# Frame to center everything
frame = tk.Frame(root, bg="#E6E6FA")
frame.pack(expand=True)

# Title Label for BMI Calculator
title_label = tk.Label(frame, text="BMI Calculator", bg="#E6E6FA", font=("Helvetica", 24, "bold"))
title_label.pack(pady=20)  # Add some space below the title

# Input fields (centered)
weight_label = tk.Label(frame, text="Weight (kg):", bg="#E6E6FA", font=font)
weight_label.pack(pady=10)

weight_entry = tk.Entry(frame, font=font)
weight_entry.pack(pady=5)

height_label = tk.Label(frame, text="Height (ft):", bg="#E6E6FA", font=font)
height_label.pack(pady=10)

height_entry = tk.Entry(frame, font=font)
height_entry.pack(pady=5)

age_label = tk.Label(frame, text="Age (years):", bg="#E6E6FA", font=font)
age_label.pack(pady=10)

age_entry = tk.Entry(frame, font=font)
age_entry.pack(pady=5)

# Calculate button
calculate_button = tk.Button(frame, text="Calculate BMI", command=on_calculate, font=font)
calculate_button.pack(pady=20)

# Result label
result_label = tk.Label(frame, text="", bg="#E6E6FA", font=font)
result_label.pack(pady=10)

# Trend button
trend_button = tk.Button(frame, text="Show BMI Trend", command=plot_bmi_trends, font=font)
trend_button.pack(pady=20)

# Start the GUI
root.mainloop()
