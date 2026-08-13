import streamlit as st
import requests

# Set the FastAPI base URL
BASE_URL = "http://127.0.0.1:8000"

# Title of the dashboard
st.title("Server Utilization Dashboard")

# Section: Average CPU Usage
st.header("Average CPU Usage")
if st.button("Get Average CPU Usage"):
    try:
        response = requests.get(f"{BASE_URL}/summary")
        if response.status_code == 200:
            data = response.json()
            st.write(f"Average CPU Usage: {data['avg_cpu']}%")
        else:
            st.error(f"Failed to fetch data: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {e}")

# Section: High CPU Servers
st.header("High CPU Servers")
if st.button("Get High CPU Servers"):
    try:
        response = requests.get(f"{BASE_URL}/highcpu")
        if response.status_code == 200:
            data = response.json()
            servers = data.get("servers", [])
            if servers:
                st.write("Servers with CPU usage > 80%:")
                st.write(servers)
            else:
                st.write("No servers with high CPU usage.")
        else:
            st.error(f"Failed to fetch data: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {e}")

# Section: Capacity Summary
st.header("Capacity Summary")
if st.button("Get Capacity Summary"):
    try:
        response = requests.get(f"{BASE_URL}/capacity_summary")
        if response.status_code == 200:
            data = response.json()
            st.write(f"Average CPU Usage: {data['avg_cpu']}%")
            st.write("High CPU Servers:")
            st.write(data["high_cpu_servers"])
        else:
            st.error(f"Failed to fetch data: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {e}")