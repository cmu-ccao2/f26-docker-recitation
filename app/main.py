from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# Recitation times per section, "HH:MM~HH:MM".
# TODO: replace with THIS semester's real times (check SIO / Canvas).
RECITATION_HOURS = {"a": "10:00~10:50", "b": "10:00~10:50",
                    "c": "13:00~13:50", "d": "13:00~13:50",
                    "e": "14:00~14:50", "f": "14:00~14:50"}
MICROSERVICE_LINK = "https://cmu-313.github.io/section_info/"


@app.get("/section_info/{section_id}")
def get_section_info(section_id: str):
    if not section_id:
        raise HTTPException(status_code=404, detail="Missing section id")

    section_id = section_id.lower()

    # Only sections we have a time for are valid
    if section_id not in RECITATION_HOURS:
        raise HTTPException(status_code=404, detail="Invalid section id")

    # Ask the existing microservice which TAs run this section
    response = requests.get(MICROSERVICE_LINK + section_id + ".json")
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Invalid section id")

    data = response.json()
    ta_name_list = data["ta"]  # some sections have only one TA

    start_time, end_time = RECITATION_HOURS[section_id].split("~")

    return {
        "section": data["section"],
        "start_time": start_time,
        "end_time": end_time,
        "ta": ta_name_list,
    }