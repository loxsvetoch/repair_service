# serviceproj\views\backup.py
import os
import glob
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy.sql import func, text
from datetime import datetime

from serviceproj import db
from serviceproj.views.main import menu
from serviceproj.models import Device, ServiceDevice, Service, WorkshopService, ServiceList, Role, Order

backup_bp = Blueprint('backup', __name__)

@backup_bp.route("/admin_backup", methods=['GET', 'POST'])
@login_required
def admin_backup():
    role = Role.query.filter_by(id=current_user.role_id).first()
    if role.role_name != "admin":
        abort(403)
    dump_dir = '/tmp/'
    dump_files = glob.glob(os.path.join(dump_dir, "*.dump"))
    return render_template("admin_backup.html", pathes=dump_files)

@backup_bp.route("/create_backup", methods=['POST'])
@login_required
def create_backup():
    now = datetime.now()
    filepath = '/tmp/dump-' + now.strftime("%Y-%m-%d-%H") + '.dump'
    db.session.execute(text(f"SELECT public.create_dump('{filepath}')"))
    flash("Бэкап успешно создан", "success")
    return redirect(url_for("backup.admin_backup"))

@backup_bp.route("/delete_backup/<path:path>", methods=['POST'])
@login_required
def delete_backup(path):
    db.session.execute(text(f"SELECT public.delete_dump('{"/"+path}')"))
    flash(f"Бэкап '{path}' успешно удалён!", "success")
    return redirect(url_for("backup.admin_backup"))
