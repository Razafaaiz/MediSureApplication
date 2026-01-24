import uuid

def create_zoom_meeting():
    meeting_id = uuid.uuid4().int % 10000000000
    return f"https://zoom.us/j/{meeting_id}"
