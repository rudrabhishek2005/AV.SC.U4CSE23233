from fastapi import FastAPI
from depot_service import fetch_depots
from scheduler import optimize_tasks

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Vehicle Scheduler Running"
    }

@app.post("/schedule")
def schedule_tasks(mechanic_hours: int):

    data = fetch_depots()

    if "error" in data:
        return {
            "api_error": data["error"]
        }

    depots = data.get("depots", [])

    tasks = []

    for depot in depots:

        for task in depot.get("tasks", []):

            tasks.append(task)

    if len(tasks) == 0:
        return {
            "message": "No tasks found"
        }

    result = optimize_tasks(tasks, mechanic_hours)

    return result