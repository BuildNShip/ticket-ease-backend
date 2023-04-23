import json
import os
from uuid import uuid4

from rest_framework.exceptions import ValidationError


def get_question_details():
    with open(f"./data/questions.json", 'r') as f:
        return json.load(f)


def load_form_data(form_name):
    with open(f"./data/submissions/{form_name}.json", 'r') as f:
        return json.load(f)


def load_tickets_data():
    with open(f"./data/tickets.json", 'r') as f:
        return json.load(f)


def load_attendance_data():
    with open(f"./data/attendance.json", 'r') as f:
        return json.load(f)


def save_json(full_name, email, job_title, interests, event_source, additional_comments):
    forms_dir = f"./data/submissions/"
    os.makedirs(forms_dir, exist_ok=True)
    data = {
        "fullName": full_name,
        "email": email,
        "jobTitle": job_title,
        "interests": interests,
        "eventSource": event_source,
        "additionalComments": additional_comments
    }
    with open(forms_dir + f"{full_name}.json", "w") as f:
        return json.dump(data, f)


def generate_ticket():
    files = os.listdir(f'./data/submissions/')
    forms_list = [file.replace('.json', '') for file in files if file.endswith('.json')]
    tickets = []
    for form_name in forms_list:
        form_data = load_form_data(form_name)
        tickets.append({
            "id": str(uuid4()),
            "email": form_data.get("email"),
            "event_name": "Pygrammers Meet 2023",
            "date": "2023-06-15",
            "time": "9:00 AM - 5:00 PM",
            "location": "San Francisco, CA",
            "ticket_type": "General Admission",
            "confirmation_page": {
                "message": "Thank you for your purchase! We look forward to seeing you at the event.",
                "details": {
                    "parking_information": "There is ample parking available at the venue.",
                    "event_schedule": "The event will include keynote speeches, breakout sessions, and networking opportunities.",
                    "special_instructions": "Please bring a photo ID with you to the event."
                }
            },
            "ticket_delivery": {
                "format": "Digital",
                "download_link": "https://example.com/tickets/12345"
            }
        })

    with open('./data/tickets.json', 'w') as f:
        json.dump(tickets, f)

    return tickets


def mark_attendance(email):
    tickets_list = load_tickets_data()
    attendance_data_list = load_attendance_data()

    for marked in attendance_data_list:
        if marked.get("email") == email:
            return False

    for ticket in tickets_list:
        if ticket.get("email") == email:
            ticket["attendance"] = True
            del ticket["ticket_delivery"]
            del ticket["confirmation_page"]
            attendance_data_list.append(ticket)
            with open('./data/attendance.json', 'w') as f:
                json.dump(attendance_data_list, f)
            return True

    raise ValidationError("Ticket Not Exists")
