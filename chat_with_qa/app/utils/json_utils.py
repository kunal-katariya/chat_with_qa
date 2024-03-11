from fastapi import HTTPException
import json
from starlette.responses import JSONResponse

FILE_PATH = "D:/PychrmProjects/chat_with_qa/app/utils/intents.json"

def insert_intent(data):
    try:
        with open(FILE_PATH, "r") as f:
            json_data = json.load(f)
        for intent in json_data["intents"]:
            if intent["tag"] == data.tag:
                return "Intent tag already exists"
        json_data["intents"].append({
            "tag": data.tag,
            "patterns": data.patterns,
            "responses": data.responses
        })
        with open(FILE_PATH, "w") as f:
            json.dump(json_data, f)
        return {"message": "Intent inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting intent: {str(e)}")

def read_json():
    try:
        with open(FILE_PATH, "r") as file:
            data = json.load(file)
        return JSONResponse(content=data)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="JSON file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")

def read_specific_intent(target_tag):
    try:
        with open(FILE_PATH, "r") as file:
            data = json.load(file)
            target_record = None
            for intent in data["intents"]:
                if intent["tag"] == target_tag:
                    target_record = intent
                    break
            if target_record:
                return JSONResponse(content=target_record)
            else:
                raise HTTPException(status_code=404, detail="Record with this tag name not found")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="JSON file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")

def update_specific_intent(intent_tag,update_data):
    try:
        with open(FILE_PATH, "r+") as file:
            data = json.load(file)
            target_intent = None
            for i, intent in enumerate(data["intents"]):
                if intent["tag"] == intent_tag:
                    target_intent = intent
                    data["intents"][i] = {**intent, **update_data}
                    break
            if target_intent:
                file.seek(0)
                json.dump(data, file, indent=4)
                return JSONResponse(content=data["intents"][i])
            else:
                raise HTTPException(status_code=404, detail="Intent not found")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="JSON file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
