import os
from functools import wraps

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    Response,
)

from database import (
    get_all_contacts,
    get_stats,
    delete_contact,
    get_content_dict,
    save_content,
    get_all_pricing_admin,
    save_pricing_plans,
)

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "admin")


def check_auth(username, password):
    return username == ADMIN_USER and password == ADMIN_PASS


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return Response(
                "Требуется авторизация",
                401,
                {"WWW-Authenticate": 'Basic realm="Admin"'},
            )
        return f(*args, **kwargs)
    return decorated


@admin_bp.before_request
@auth_required
def before_request():
    pass


@admin_bp.route("/")
def index_redirect():
    return redirect(url_for("admin.contacts"))


@admin_bp.route("/contacts")
def contacts():
    all_contacts = get_all_contacts()
    stats = get_stats()
    return render_template("admin/contacts.html", contacts=all_contacts, stats=stats)


@admin_bp.route("/contacts/delete/<int:contact_id>", methods=["POST"])
def contact_delete(contact_id):
    delete_contact(contact_id)
    return redirect(url_for("admin.contacts"))


@admin_bp.route("/content", methods=["GET", "POST"])
def content():
    if request.method == "POST":
        for key in request.form:
            save_content(key, request.form[key])
        return redirect(url_for("admin.content"))
    c = get_content_dict()
    return render_template("admin/content.html", c=c)


@admin_bp.route("/pricing", methods=["GET", "POST"])
def pricing():
    if request.method == "POST":
        save_pricing_plans(request.form)
        save_content("pricing_title", request.form.get("pricing_title", ""))
        save_content("pricing_description", request.form.get("pricing_description", ""))
        return redirect(url_for("admin.pricing"))
    plans = get_all_pricing_admin()
    c = get_content_dict()
    return render_template("admin/pricing.html", plans=plans, c=c)
