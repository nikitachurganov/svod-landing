import os
import sqlite3
from datetime import datetime

DB_DIR = os.environ.get("DB_DIR", os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(DB_DIR, "data", "db.sqlite3")

CONTENT_DEFAULTS = {
    # Hero
    "hero_title": (
        'Превратите поток <span class="hero__title-accent">заявок</span><br>'
        "в управляемую систему"
    ),
    "hero_description": (
        "Сервис собирает все запросы в одном месте, структурирует"
        "<br>их и автоматически распределяет задачи по команде"
    ),
    "hero_btn_primary": "Начать бесплатно",
    "hero_btn_secondary": "Связаться с нами",

    # How it works
    "how_title": "Как это работает",
    "how_description": (
        "Сервис собирает все запросы в одном месте, структурирует "
        "их и автоматически распределяет задачи по команде"
    ),
    "how_step_1_title": "Соберите все заявки в одном месте",
    "how_step_1_with": "Получайте запросы через формы вместо хаоса в чатах, почте и таблицах",
    "how_step_1_without": "Заявки теряются в чатах, почте и таблицах — нет единого места для контроля",
    "how_step_2_title": "Структурируйте входящий поток",
    "how_step_2_with": "Теги, статусы и единый формат заявок — сразу видно, что в работе и что просрочено",
    "how_step_2_without": "Разрозненные треды и файлы: сложно понять приоритет и не потерять запрос",
    "how_step_3_title": "Автоматически распределяйте задачи",
    "how_step_3_with": "Правила и очереди назначают исполнителя без ручных пересылок и уточнений",
    "how_step_3_without": "Кто возьмёт задачу — решается в переписке, нагрузка на команду распределяется неравномерно",
    "how_step_4_title": "Контролируйте выполнение",
    "how_step_4_with": "Сроки, напоминания и история по каждой заявке — статус прозрачен для всех",
    "how_step_4_without": "Сложно отследить, на каком этапе запрос и кто за него отвечает",

    # Usage scenarios
    "usecase_title": "Сценарий использования",
    "usecase_1_title": "Студия или агентство",
    "usecase_1_text": (
        "Клиенты оставляют бриф через форму: тип проекта, бюджет, сроки. "
        "Заявки не теряются в переписке — всё в одной ленте для менеджеров."
    ),
    "usecase_2_title": "Фрилансер и эксперт",
    "usecase_2_text": (
        "Заказы с сайта или соцсетей попадают в единый список: контакт, услуга, удобное время. "
        "Вы отвечаете по приоритету, а не по тому, кто громче написал в мессенджер."
    ),
    "usecase_3_title": "Сервис и поддержка",
    "usecase_3_text": (
        "Обращения с формы «Помощь» классифицируются по теме и попадают нужной линии поддержки. "
        "История видна всей команде, эскалации прозрачны."
    ),
    "usecase_4_title": "Малый бизнес",
    "usecase_4_text": (
        "Запись на услугу, предзаказ, обратный звонок — всё через одну форму на сайте. "
        "Владелец видит очередь заявок и статусы без таблиц и ручного учёта."
    ),

    # Value headline
    "less_work_title": "Меньше ручной работы —<br>больше результата",
    "less_work_description": "Система обрабатывает заявки<br>и распределяет задачи без участия человека",

    # Team changes
    "team_title": "Как меняется работа команды",
    "team_description": "От разрозненных заявок к управляемому потоку задач",
    "team_metric_1": "−70%",
    "team_label_1": "времени на сбор и пересылку заявок из разных каналов",
    "team_metric_2": "100%",
    "team_label_2": "заявок попадают в единую очередь с назначенным статусом",
    "team_metric_3": "Авто",
    "team_label_3": "распределение задач по правилам без ручной сортировки",
    "team_metric_4": "1 экран",
    "team_label_4": "для контроля потока: кто взял задачу и до какого срока",

    # CTA
    "cta_title": "Возьмите заявки под контроль",
    "cta_description": (
        "Единая лента заявок, автоматическое распределение задач "
        "и прозрачные сроки — без хаоса в чатах и почте."
    ),
    "cta_btn_primary": "Начать бесплатно",
    "cta_btn_secondary": "Связаться с нами",

    # Верхний баннер (опрос)
    "survey_url": "https://example.com/survey",

    # Секция тарифов (заголовок)
    "pricing_title": "Управляйте заявками<br>без лишних затрат",
    "pricing_description": (
        "Экономьте время команды и ускоряйте<br>"
        "выполнение задач с помощью автоматизации"
    ),
}


def _get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = _get_conn()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name  TEXT    NOT NULL,
            phone      TEXT    NOT NULL,
            email      TEXT    NOT NULL,
            industry   TEXT    NOT NULL,
            position   TEXT    NOT NULL,
            rating     INTEGER,
            created_at TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS content (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            key   TEXT    NOT NULL UNIQUE,
            value TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS pricing (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            price_month TEXT    NOT NULL,
            price_year  TEXT    NOT NULL,
            description TEXT    NOT NULL DEFAULT '',
            features    TEXT    NOT NULL DEFAULT '',
            is_active   INTEGER NOT NULL DEFAULT 1,
            sort_order  INTEGER NOT NULL DEFAULT 0
        );
        """
    )
    for key, value in CONTENT_DEFAULTS.items():
        conn.execute(
            "INSERT OR IGNORE INTO content (key, value) VALUES (?, ?)",
            (key, value),
        )
    _seed_pricing_if_empty(conn)
    _ensure_contact_rating_column(conn)
    _ensure_contact_name_columns(conn)
    _ensure_contact_comment_column(conn)
    conn.commit()
    conn.close()


def _ensure_contact_rating_column(conn):
    cols = {row[1] for row in conn.execute("PRAGMA table_info(contacts)").fetchall()}
    if "rating" not in cols:
        conn.execute("ALTER TABLE contacts ADD COLUMN rating INTEGER")


def _split_ru_full_name(full_name: str):
    parts = (full_name or "").split()
    if len(parts) >= 3:
        return parts[0], parts[1], " ".join(parts[2:])
    if len(parts) == 2:
        return parts[0], parts[1], None
    if len(parts) == 1:
        return parts[0], "", None
    return "", "", None


def _ensure_contact_name_columns(conn):
    cols = {row[1] for row in conn.execute("PRAGMA table_info(contacts)").fetchall()}
    if "last_name" in cols:
        return
    conn.execute("ALTER TABLE contacts ADD COLUMN last_name TEXT")
    conn.execute("ALTER TABLE contacts ADD COLUMN first_name TEXT")
    conn.execute("ALTER TABLE contacts ADD COLUMN patronymic TEXT")
    rows = conn.execute("SELECT id, full_name FROM contacts").fetchall()
    for r in rows:
        ln, fn, pt = _split_ru_full_name(r["full_name"] or "")
        conn.execute(
            "UPDATE contacts SET last_name=?, first_name=?, patronymic=? WHERE id=?",
            (ln or "", fn or "", pt, r["id"]),
        )


def _ensure_contact_comment_column(conn):
    cols = {row[1] for row in conn.execute("PRAGMA table_info(contacts)").fetchall()}
    if "comment" not in cols:
        conn.execute("ALTER TABLE contacts ADD COLUMN comment TEXT")


def _seed_pricing_if_empty(conn):
    n = conn.execute("SELECT COUNT(*) FROM pricing").fetchone()[0]
    if n > 0:
        return
    rows = [
        (
            "Персональный",
            "12 000 \u20bd",
            "115 200 \u20bd",
            "Для одного специалиста или небольшой команды.",
            "5 участников\nПолный функционал",
            1,
            0,
        ),
        (
            "Команда",
            "Бесплатно / 2 мес",
            "Бесплатно / 2 мес",
            "",
            "5 участников\nПолный функционал",
            1,
            1,
        ),
        (
            "Организация",
            "Бесплатно / 2 мес",
            "Бесплатно / 2 мес",
            "",
            "5 участников\nПолный функционал",
            1,
            2,
        ),
    ]
    for name, pm, py, desc, feat, active, sort in rows:
        conn.execute(
            """INSERT INTO pricing (name, price_month, price_year, description, features, is_active, sort_order)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (name, pm, py, desc, feat, active, sort),
        )


# --- Contacts ---

def create_contact(last_name, first_name, patronymic, phone, email, rating, comment):
    conn = _get_conn()
    pt = (patronymic or "").strip() or None
    full_display = " ".join(p for p in (last_name, first_name, pt) if p)
    cm = (comment or "").strip() or None
    conn.execute(
        """INSERT INTO contacts (
               last_name, first_name, patronymic,
               full_name, phone, email, industry, position, rating, comment, created_at
           )
           VALUES (?, ?, ?, ?, ?, ?, '', '', ?, ?, ?)""",
        (
            last_name,
            first_name,
            pt,
            full_display,
            phone,
            email,
            rating,
            cm,
            datetime.now().isoformat(sep=" ", timespec="seconds"),
        ),
    )
    conn.commit()
    conn.close()


def get_all_contacts():
    conn = _get_conn()
    rows = conn.execute("SELECT * FROM contacts ORDER BY created_at DESC").fetchall()
    conn.close()
    return rows


def delete_contact(contact_id):
    conn = _get_conn()
    conn.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()


def get_stats():
    conn = _get_conn()
    total = conn.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
    conn.close()
    return {"total": total}


# --- Content ---

def get_content_dict():
    conn = _get_conn()
    rows = conn.execute("SELECT key, value FROM content").fetchall()
    conn.close()
    result = {row["key"]: row["value"] for row in rows}
    for key, default in CONTENT_DEFAULTS.items():
        result.setdefault(key, default)
    return result


def get_all_content():
    conn = _get_conn()
    rows = conn.execute("SELECT * FROM content ORDER BY id").fetchall()
    conn.close()
    return rows


def save_content(key, value):
    conn = _get_conn()
    existing = conn.execute("SELECT id FROM content WHERE key = ?", (key,)).fetchone()
    if existing:
        conn.execute("UPDATE content SET value = ? WHERE key = ?", (value, key))
    else:
        conn.execute("INSERT INTO content (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()


def update_content(key, value):
    save_content(key, value)


# --- Pricing ---

def get_pricing():
    conn = _get_conn()
    rows = conn.execute(
        """SELECT * FROM pricing WHERE is_active = 1 ORDER BY sort_order ASC, id ASC"""
    ).fetchall()
    conn.close()
    return rows


def get_all_pricing_admin():
    conn = _get_conn()
    rows = conn.execute(
        """SELECT * FROM pricing ORDER BY sort_order ASC, id ASC"""
    ).fetchall()
    conn.close()
    return rows


def save_pricing_plans(form):
    conn = _get_conn()
    for row in conn.execute("SELECT id FROM pricing").fetchall():
        pid = row["id"]
        prefix = f"plan_{pid}_"
        name = (form.get(prefix + "name") or "").strip()
        if not name:
            continue
        conn.execute(
            """UPDATE pricing SET name = ?, price_month = ?, price_year = ?, description = ?, features = ?, is_active = ?, sort_order = ?
               WHERE id = ?""",
            (
                name,
                (form.get(prefix + "price_month") or "").strip(),
                (form.get(prefix + "price_year") or "").strip(),
                (form.get(prefix + "description") or "").strip(),
                (form.get(prefix + "features") or "").strip(),
                1 if form.get(prefix + "is_active") == "1" else 0,
                int(form.get(prefix + "sort_order") or 0),
                pid,
            ),
        )
    conn.commit()
    conn.close()
