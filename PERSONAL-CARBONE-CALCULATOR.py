
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Personal Carbon Footprint Calculator
# HCL Career Shaper - Python Mini Project
# Student: Aryan Dev Pal
# Branch: BCA First Year
# Domain: Data Analytics
# College: ABES Engineering College, Ghaziabad


EMISSION_FACTORS = {
    "Electricity (kWh)": 0.675,
    "Petrol vehicle travel (km)": 0.190,
    "Diesel vehicle travel (km)": 0.170,
    "Public bus / metro travel (km)": 0.050,
    "LPG used (kg)": 2.980,
    "Household waste (kg)": 0.500
}


def get_non_negative_value(activity):
    """Get and validate monthly activity input."""
    while True:
        try:
            value = float(input(f"Enter monthly {activity}: "))

            if value < 0:
                print("Please enter a non-negative value.")
            else:
                return value

        except ValueError:
            print("Invalid input! Please enter a number.")


def calculate_footprint(usage):
    """Calculate monthly and annual carbon emissions."""

    activities = list(EMISSION_FACTORS.keys())

    usage_array = np.array(usage)
    factor_array = np.array(
        list(EMISSION_FACTORS.values())
    )

    monthly_emissions = usage_array * factor_array
    annual_emissions = monthly_emissions * 12

    total_monthly = np.sum(monthly_emissions)

    if total_monthly > 0:
        percentage = (
            monthly_emissions / total_monthly
        ) * 100
    else:
        percentage = np.zeros(len(activities))

    data = {
        "Activity": activities,
        "Monthly Usage": usage_array,
        "Emission Factor": factor_array,
        "Monthly CO2 (kg)": monthly_emissions,
        "Annual CO2 (kg)": annual_emissions,
        "Share (%)": percentage
    }

    df = pd.DataFrame(data)

    return df, total_monthly


def show_charts(df):
    """Display bar and pie charts."""

    active_data = df[df["Monthly CO2 (kg)"] > 0]

    if active_data.empty:
        print("No emissions data available for charts.")
        return

    # Bar Chart
    plt.figure(figsize=(10, 5))

    plt.bar(
        active_data["Activity"],
        active_data["Monthly CO2 (kg)"]
    )

    plt.title("Monthly Carbon Emissions by Activity")
    plt.xlabel("Activity")
    plt.ylabel("CO2 Emissions (kg)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    plt.show()

    # Pie Chart
    plt.figure(figsize=(8, 6))

    plt.pie(
        active_data["Monthly CO2 (kg)"],
        labels=active_data["Activity"],
        autopct="%1.1f%%"
    )

    plt.title("Carbon Emission Percentage Share")
    plt.tight_layout()

    plt.show()


def run_calculator():
    print("=" * 50)
    print("PERSONAL CARBON FOOTPRINT CALCULATOR")
    print("ABES Engineering College, Ghaziabad")
    print("HCL Career Shaper | Data Analytics")
    print("=" * 50)

    usage = []

    print("\nEnter your monthly activity details:\n")

    for activity in EMISSION_FACTORS:
        value = get_non_negative_value(activity)
        usage.append(value)

    df, total_monthly = calculate_footprint(usage)

    total_annual = total_monthly * 12

    print("\n========== CARBON FOOTPRINT REPORT ==========")

    print(df.round(2).to_string(index=False))

    print("\nTotal Monthly Footprint:",
          round(total_monthly, 2), "kg CO2")

    print("Total Annual Footprint:",
          round(total_annual, 2), "kg CO2")

    if total_monthly > 0:
        largest_source = df.loc[
            df["Monthly CO2 (kg)"].idxmax(),
            "Activity"
        ]

        print("\nLargest emission source:", largest_source)

    # Save results to CSV
    df.to_csv(
        "carbon_footprint_report.csv",
        index=False
    )

    print("\nReport saved as carbon_footprint_report.csv")

    show_charts(df)


if __name__ == "__main__":
    run_calculator()
