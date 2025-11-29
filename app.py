import os
from flask import Flask, request, jsonify
import requests

# BOT_TOKEN и ADMIN_CHAT_ID будем задавать на Render в Environment
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")

app = Flask(__name__)


@app.route("/submit", methods=["POST"])
def submit():
    if not BOT_TOKEN or not ADMIN_CHAT_ID:
        return jsonify({"ok": False, "error": "BOT_TOKEN or ADMIN_CHAT_ID not set"}), 500

    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    comment = request.form.get("comment", "").strip()

    text_lines = [
        "📩 Новая заявка с сайта",
        "",
        f"👤 Имя: {name or '—'}",
        f"📱 Телефон: {phone or '—'}",
        f"💬 Комментарий: {comment or '—'}",
    ]
    text = "\n".join(text_lines)

    tg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    resp = requests.post(tg_url, data={"chat_id": ADMIN_CHAT_ID, "text": text})

    if resp.status_code != 200:
        return jsonify({"ok": False, "error": resp.text}), 500

    # Простая страница "спасибо"
    return """
    <html>
      <body style="font-family: -apple-system, system-ui, sans-serif;
                   background:#020617; color:#e5e7eb;
                   text-align:center; padding:40px;">
        <h2>Спасибо! Заявка отправлена.</h2>
        <p>Я свяжусь с вами в ближайшее время.</p>
        <a href="/" style="color:#38bdf8; text-decoration:none;">Вернуться на сайт</a>
      </body>
    </html>
    """


if __name__ == "__main__":
    # Локальный запуск (для тестов)
    app.run(host="0.0.0.0", port=5000, debug=True)
