import uuid
import asyncio
from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename
from chatbot.agent import agent
from vertexai.preview.reasoning_engines import AdkApp
from google.genai.types import Content, Part

# Wrap your agent in AdkApp to enable local session APIs
app_adk = AdkApp(agent=agent)

chatbot_bp = Blueprint('chatbot', __name__, template_folder='../templates')

@chatbot_bp.route('/', methods=['GET'])
def chatbot_page():
    return render_template('chatbot.html')

@chatbot_bp.route('/query', methods=['POST'])
def chatbot_query():
    user_id = request.remote_addr or "default_user"
    payload_text = request.form.get('message', '').strip()
    name = request.form.get('name', '').strip()
    file = request.files.get('image')
    temp_path = None

    if file:
        fname = secure_filename(f"{uuid.uuid4()}_" + file.filename)
        temp_path = fname
        # Save into upload folder just like other uploads

    # Create or ensure session
    session = app_adk.create_session(user_id=user_id)

    # Build message content
    parts = [Part(text=payload_text)]
    content = Content(role="user", parts=parts)

    # If reference image provided, include metadata in session state
    state_update = {}
    if temp_path:
        state_update = {'name': name, 'image_path_local': temp_path}
        # You may also store these in adk_app memory via app_adk.patch_session

    # Stream query asynchronously
    events = app_adk.stream_query(user_id=user_id, session_id=session.id, message=payload_text)

    # Collect streamed events and their outputs
    content_parts = []
    for ev in events:
        if ev.content and ev.content.parts:
            for p in ev.content.parts:
                content_parts.append(p.text)

    response = {"content": {"parts": [{"text": t} for t in content_parts]}}
    return jsonify(response)

@chatbot_bp.route('/sessions', methods=['GET'])
def list_sessions():
    user_id = request.args.get('user_id', request.remote_addr or "default_user")
    resp = app_adk.list_sessions(user_id=user_id)
    return jsonify({"session_ids": resp.session_ids})

@chatbot_bp.route('/session/<session_id>', methods=['GET'])
def get_session(session_id):
    user_id = request.args.get('user_id', request.remote_addr or "default_user")
    sess = app_adk.get_session(user_id=user_id, session_id=session_id)
    return jsonify({
        "id": sess.id,
        "user_id": sess.user_id,
        "state": sess.state,
        "events": [e.dict() for e in sess.events],
        "last_update": sess.last_update_time
    })
