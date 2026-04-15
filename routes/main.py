import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

from database import create_contact, get_content_dict, get_pricing

main_bp = Blueprint("main", __name__)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _normalize_phone_ru(phone: str):
    """10 цифр после кода страны, первая — 9. Принимает +7, 7, 8."""
    d = re.sub(r"\D", "", (phone or "").strip())
    if len(d) == 11 and d.startswith("8"):
        d = "7" + d[1:]
    if len(d) == 11 and d.startswith("7"):
        d = d[1:]
    if len(d) != 10 or d[0] != "9":
        return None
    return d


def _format_phone_ru_masked(d10: str) -> str:
    return f"+7 ({d10[0:3]}) {d10[3:6]} - {d10[6:8]} - {d10[8:10]}"


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
    last_name = request.form.get("last_name", "").strip()
    first_name = request.form.get("first_name", "").strip()
    patronymic = request.form.get("patronymic", "").strip()
    phone_raw = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()
    comment = request.form.get("comment", "").strip()
    rating_raw = request.form.get("rating", "").strip()

    errors = []
    if not last_name:
        errors.append("Укажите фамилию")
    if not first_name:
        errors.append("Укажите имя")
    phone_digits = _normalize_phone_ru(phone_raw)
    if not phone_raw.strip():
        errors.append("Укажите номер телефона")
    elif phone_digits is None:
        errors.append("Введите номер в формате +7 (9__) ___ - __ - __ (мобильный, с 9)")
    phone = _format_phone_ru_masked(phone_digits) if phone_digits else ""
    if not email or not EMAIL_RE.match(email):
        errors.append("Укажите корректный email")
    if len(comment) > 2000:
        errors.append("Комментарий не длиннее 2000 символов")
    try:
        rating = int(rating_raw)
    except (TypeError, ValueError):
        rating = None
    if rating is None or rating < 1 or rating > 10:
        errors.append("Выберите оценку от 1 до 10")

    if errors:
        if _contact_wants_json():
            return jsonify({"ok": False, "errors": errors}), 400
        for e in errors:
            flash(e, "error")
        return redirect(url_for("main.index"))

    create_contact(last_name, first_name, patronymic, phone, email, rating, comment)
    if _contact_wants_json():
        return jsonify({"ok": True})
    return redirect(url_for("main.success"))


@main_bp.route("/success")
def success():
    return render_template("success.html")
