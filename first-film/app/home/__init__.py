from flask import Blueprint


home = Blueprint(
    name='home', 
    import_name= __name__,
    static_folder='static',
    template_folder='templates'
)


from . login import *
from . views import *