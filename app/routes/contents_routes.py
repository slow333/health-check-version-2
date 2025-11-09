from flask import Blueprint, render_template as render

bp = Blueprint('main_home', __name__)

@bp.route('/')
@bp.route('/home')
def main_home():
  return render('project_set_v1.html')

@bp.route('/auth/')
def auth_home():
  return render('auth/auth_home.html')

@bp.route('/contents/start-set')
def home_ide():
  return render('contents/home/start-set.html')

@bp.route('/contents/linux')
def home_linux():
  return render('contents/home/linux.html')

# =========== databas ===================
@bp.route('/database/')
def database_home():
  return render('contents/database/00-database_index.html')

@bp.route('/database/datatype')
def database_datatype():
  return render('contents/database/01-datatype.html')

@bp.route('/database/crud')
def database_crud():
  return render('contents/database/02-crud.html')

@bp.route('/database/select')
def database_select():
  return render('contents/database/03-select.html')

@bp.route('/database/constraints')
def database_constraints():
  return render('contents/database/04-constraints.html')

@bp.route('/database/groupBy')
def database_groupBy():
  return render('contents/database/05-groupBy.html')

@bp.route('/database/join')
def database_join():
  return render('contents/database/06-join.html')

@bp.route('/database/aggregate')
def database_aggregate():
  return render('contents/database/07-aggregate.html')

@bp.route('/database/functions')
def database_functions():
  return render('contents/database/08-functions.html')

@bp.route('/database/procedureTrigger')
def database_procedure_trigger():
  return render('contents/database/09-procedure-trigger.html')

# ===========  /python ===========================

@bp.route('/python/')
@bp.route('/contents/')
def python_home():
  return render('contents/python/python_index.html')

@bp.route('/python/core/')
@bp.route('/python/core/datatype')
def python_datatype():
  return render('contents/python/core/01_datatype.html')

@bp.route('/python/core/print-format')
def python_print_format():
  return render('contents/python/core/02_print_format.html')

@bp.route('/python/core/loop')
def python_loop():
  return render('contents/python/core/03_loop.html')

@bp.route('/python/core/def-file')
def python_def_file():
  return render('contents/python/core/04_def_file.html')

@bp.route('/python/core/class-module')
def python_class_module():
  return render('contents/python/core/05_class_module.html')

@bp.route('/python/core/try-except')
def python_try_except():
  return render('contents/python/core/06_try_except.html')

@bp.route('/python/core/py-library')
def python_py_library():
  return render('contents/python/core/07_py_library.html')

@bp.route('/python/core/closer-decorator')
def python_closer_decorator():
  return render('contents/python/core/08_closer_decorator.html')

@bp.route('/python/core/regexp')
def python_regexp():
  return render('contents/python/core/09_regexp.html')

# ===========  python adv ================================
@bp.route('/python/adv/')
@bp.route('/python/adv/01_class')
def python_adv_class():
  return render('contents/python/adv/01_class.html')

@bp.route('/python/adv/02_module')
def python_adv_moudle():
  return render('contents/python/adv/02_module.html')

@bp.route('/python/adv/03_try_except')
def python_adv_try_except():
  return render('contents/python/adv/03_try_except.html')

@bp.route('/python/adv/04_py_library')
def python_adv_py_library():
  return render('contents/python/adv/04_py_library.html')

@bp.route('/python/adv/05_closer_decorator')
def python_adv_closer_decorator():
  return render('contents/python/adv/05_closer_decorator.html')

@bp.route('/python/adv/06_regexp')
def python_adv_regexp():
  return render('contents/python/adv/06_regexp.html')


# ===========  python flask ================================
@bp.route('/python/flask/')
@bp.route('/python/flask/db-setup')
def flask_db_setup():
  return render('contents/python/flask/db_setup.html')

@bp.route('/python/flask/core-crud')
def flask_core_crud():
  return render('contents/python/flask/core_crud.html')

@bp.route('/python/flask/install')
def flask_install():
  return render('contents/python/flask/install.html')

@bp.route('/python/flask/note')
def flask_note():
  return render('contents/python/flask/note.html')