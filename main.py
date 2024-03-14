from forms.form_login import Login
from pathlib import Path
import util.generic as util

script_location = Path(__file__).absolute().parent
util.obtener_path(script_location)
Login()