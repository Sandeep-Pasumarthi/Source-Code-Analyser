from flask import Flask, request, redirect, url_for, render_template, session

from src.mongo_operations.loginops import LoginOperations
from src.mongo_operations.dashboard_ops import DashBoardOperations
from src.data_ingestion.github import clone_repo
from src.embeddings_generator.embeddings import EmbeddingsGenerator
from src.llm.gemini import ChatWithGemini, get_session_history

import os


app = Flask(__name__)
app.secret_key = "arjuna-source-code-analyser"


@app.route('/', methods=["GET"])
def home():
    return redirect(url_for("login"))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = LoginOperations()
        user_mail = request.form.get("email")
        password = request.form.get("password")

        if login.is_user_present(user_mail):
            status = login.validate_user(user_mail, password)
            if status:
                session["user_id"] = status
                return redirect("user_dashboard")
            return render_template("login.html", message="Password is incorrect!!!", message_class="error")
        return render_template("login.html", message="Email not registered. Please signup!!!", message_class="error")
    return render_template("login.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        login = LoginOperations()
        user_mail = request.form.get("email")
        password = request.form.get("password")
        user_name = request.form.get("name")

        if login.is_user_present(user_mail):
            return redirect('login')
        status = login.add_user(user_mail, user_name, password)
        if status:
            return render_template("signup.html", message="Signup Successfull", message_class="success")
        return render_template("signup.html", message="Something went wrong. Please try again!!!", message_class="error")
    return render_template("signup.html")

@app.route('/user_dashboard', methods=["GET"])
def user_dashboard():
    dashboard = DashBoardOperations()
    conversations = dashboard.find_conversations(user_id=session["user_id"])
    return render_template("dashboard.html", conversations=conversations, length=len(conversations))

@app.route('/add_conversation', methods=["POST"])
def add_conversation():
    # try:
        conversation_name = request.form.get("name")
        conversation_source = request.form.get("source")
        conversation_programming_language = request.form.get("language")
        clone_repo(conversation_source, "repo")
        dashboard = DashBoardOperations()
        conversation_id = dashboard.add_conversation(session["user_id"], conversation_name=conversation_name, source=conversation_source, source_language=conversation_programming_language)
        embeddings_generator = EmbeddingsGenerator("repo", "main", conversation_programming_language, namespace=session["user_id"], repo_id=conversation_id)
        embeddings_generator.run()
        embeddings_generator.remove_repo()
        return redirect(url_for("chat_conversation"))
    # except Exception as e:
    #     print(e)
    #     dashboard.delete_conversation(session["user_id"], conversation_id)
    #     return redirect(url_for("user_dashboard"))

@app.route('/conversation/<conversation_id>/chat', methods=["GET", "POST"])
def chat_conversation(conversation_id):
    chat=get_session_history(conversation_id).messages
    if request.method == "POST":
        query = request.form.get("message")
        llm = ChatWithGemini(namespace=session["user_id"], repo_id=conversation_id)
        llm.initiate_chat()
        answer = llm.chat(query, session_id=conversation_id)
        return render_template("chat.html", conversation_id=conversation_id, chat=[message.content for message in chat], length=len(chat))
    return render_template("chat.html", conversation_id=conversation_id, chat=[message.content for message in chat], length=len(chat))


if __name__ == '__main__':
    app.run(debug=True)
