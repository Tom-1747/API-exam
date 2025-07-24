from dataclasses import dataclass, asdict
from fastapi import FastAPI, Path, HTTPException
from typing import Dict
import json
import os


DATA_FILE = "taches.json"

def read_tasks() -> Dict[int, dict]:
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            taches_list = json.load(f)
            return {i + 1: t for i, t in enumerate(taches_list)}
        except json.JSONDecodeError:
            return {}

def write_tasks(task_dict: Dict[int, dict]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(list(task_dict.values()), f, indent=4)


@dataclass
class Tache:
    id: int
    description: str


list_taches = read_tasks()
app = FastAPI()


@app.get("/total_tasks")
def get_total_tasks():
    return {"total": len(list_taches)}

@app.get("/tasks")
def all_tasks():
    return [Tache(**t) for t in list_taches.values()]

@app.get("/task/{id}")
def get_task_by_id(id: int = Path(..., ge=1)):
    if id not in list_taches:
        raise HTTPException(status_code=404, detail="Tâche n'existe pas")
    return Tache(**list_taches[id])

@app.post("/task/")
def create_task(new_task: Tache):
    if new_task.id in list_taches:
        raise HTTPException(status_code=400, detail=f"Tâche {new_task.id} existe déjà")
    list_taches[new_task.id] = asdict(new_task)
    write_tasks(list_taches)
    return new_task

@app.put("/task/{id}")
def update_task(id: int, updated_task: Tache):
    if id not in list_taches:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    list_taches[id] = asdict(updated_task)
    write_tasks(list_taches)
    return updated_task

@app.delete("/task/{id}")
def delete_task(id: int):
    if id not in list_taches:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    deleted = list_taches.pop(id)
    write_tasks(list_taches)
    return {"message": f"Tâche {id} supprimée", "task": deleted}
