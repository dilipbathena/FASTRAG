from fastapi import FastAPI, HTTPException
import pandas as pd
import os

app = FastAPI()

# Check if the file exists
file_path = "cpu_data.xlsx"
if os.path.exists(file_path):
    try:
        df = pd.read_excel(file_path)
        # Convert all columns to numeric where possible, non-convertible values will become NaN
        df.iloc[:, 1:13] = df.iloc[:, 1:13].apply(pd.to_numeric, errors="coerce")
    except Exception as e:
        raise RuntimeError(f"Error reading the Excel file: {e}")
else:
    raise RuntimeError("The file 'cpu_data.xlsx' does not exist in the directory.")

@app.get("/")
def root():
    """
    Root endpoint to provide basic information about the API.
    """
    return {"message": "Welcome to the CPU Monitoring API. Use /summary, /highcpu, or /capacity_summary endpoints."}

@app.get("/summary")
def summary():
    """
    Endpoint to calculate the average CPU usage across all servers and months.
    """
    try:
        # Ensure columns 1 to 12 are numeric and drop rows with all NaN values
        numeric_columns = df.iloc[:, 1:13].dropna(how="all")
        avg_cpu = numeric_columns.mean().mean()
        return {"avg_cpu": round(avg_cpu, 2)}
    except Exception as e:
        print(f"Error in /summary: {e}")
        raise HTTPException(status_code=500, detail=f"Error calculating summary: {e}")

@app.get("/highcpu")
def high_cpu():
    """
    Endpoint to find servers with CPU usage greater than 80% in any month.
    """
    try:
        servers = []
        for index, row in df.iterrows():
            # Ensure numeric data is used for comparison
            numeric_data = pd.to_numeric(row.iloc[1:13], errors="coerce")
            if numeric_data.max() > 80:
                servers.append(row["Server_Name"])
        return {"servers": servers}
    except Exception as e:
        print(f"Error in /highcpu: {e}")
        raise HTTPException(status_code=500, detail=f"Error identifying high CPU servers: {e}")

@app.get("/capacity_summary")
def capacity_summary():
    """
    Endpoint to provide a summary of CPU capacity, including average and high CPU servers.
    """
    try:
        # Calculate average CPU usage
        numeric_columns = df.iloc[:, 1:13].dropna(how="all")
        avg_cpu = numeric_columns.mean().mean()

        # Find servers with high CPU usage
        servers = []
        for index, row in df.iterrows():
            numeric_data = pd.to_numeric(row.iloc[1:13], errors="coerce")
            if numeric_data.max() > 80:
                servers.append(row["Server_Name"])

        return {
            "avg_cpu": round(avg_cpu, 2),
            "high_cpu_servers": servers
        }
    except Exception as e:
        print(f"Error in /capacity_summary: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating capacity summary: {e}")