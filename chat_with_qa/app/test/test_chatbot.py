import pytest
import requests

BASE_URL = "http://localhost:7000"

@pytest.mark.parametrize("status", [True, False])
def test_update_question_status_success(status):
    question_id = 7
    status = status
    response = requests.put(f"{BASE_URL}/update_status_unanswered_questions/{question_id}", json={"is_resolved": status})
    assert response.status_code == 200
    assert response.json() == "Status updated successfully"

def test_update_nonexistent_question():
    nonexistent_id = 12345
    response = requests.put(f"{BASE_URL}/update_status_unanswered_questions/{nonexistent_id}", json={"is_resolved": True})
    assert response.status_code == 404
    assert response.json() == {"detail": "Question not found"}

def test_get_unanswered_questions_success():
    response = requests.get(f"{BASE_URL}/get_unanswered_questions")
    assert response.status_code == 200

def test_update_json_data_success(tag_name="testpurpose"):
    tag_name = tag_name
    update_data = {
                    "patterns": ["checking22"],
                    "responses": ["checking22"]
                }
    response = requests.put(f"{BASE_URL}/json-data/{tag_name}", json=update_data)
    assert response.status_code == 200
    assert response.json()["patterns"] == update_data["patterns"]
    assert response.json()["responses"] == update_data["responses"]

def test_update_nonexistent_intent():
    nonexistent_tag = "invalid_tag"
    response = requests.put(f"{BASE_URL}/json-data/{nonexistent_tag}", json={"description": "Should not update"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Intent not found"}

def test_get_chatbot_db_success():
    response = requests.get(f"{BASE_URL}/chatbot_db")
    assert response.status_code == 200

def test_create_intent_success():
    valid_data = {
        "tag": "string",
        "patterns": ["string"],
        "responses": ["string"]
        }
    response = requests.post(f"{BASE_URL}/create_question_answer", json=valid_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Intent inserted successfully"}

@pytest.mark.parametrize("tag", ["test-case", "end-to-end-testing", "greeting"])
def test_create_intent_existent_intent(tag):
    data = {
        "tag": tag,
        "patterns": ["Hi", "Hello"],
        "responses": ["Hello there!", "Greetings!"]
    }
    response = requests.post(f"{BASE_URL}/create_question_answer", json=data)
    assert response.status_code == 409
    assert response.json() == {"detail": "Intent tag already exists"}

def test_simple_message():
    message = "Hello!"
    response = requests.post(f"{BASE_URL}/chat/{message}")
    assert response.status_code == 200
