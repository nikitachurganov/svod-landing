import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

from database import create_contact, get_content_dict, get_pricing

main_bp = Blueprint("main", __name__)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _contact_wants_json():
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


@main_bp.context_processor
def inject_content():
    return {
        "content": get_content_dict(),
        "pricing_plans": get_pricing(),
    }


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/contact", methods=["POST"])
def contact():
    full_name = request.form.get("full_name", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()
    industry = request.form.get("industry", "").strip()
    position = request.form.get("position", "").strip()

    errors = []
    if not full_name:
        errors.append("Укажите ФИО")
    if not phone:
        errors.append("Укажите номер телефона")
    if not email or not EMAIL_RE.match(email):
        errors.append("Укажите корректный email")
    if not industry:
        errors.append("Укажите сферу деятельности")
    if not position:
        errors.append("Укажите должность / специализацию")

    if errors:
        if _contact_wants_json():
            return jsonify({"ok": False, "errors": errors}), 400
        for e in errors:
            flash(e, "error")
        return redirect(url_for("main.index"))

    create_contact(full_name, phone, email, industry, position)
    if _contact_wants_json():
        return jsonify({"ok": True})
    return redirect(url_for("main.success"))


@main_bp.route("/success")
def success():
    return render_template("success.html")
