from flask import Blueprint


admin = Blueprint(
    'admin', 
    __name__,     
    static_folder='static',
    template_folder='template'
)


from .model_admin import ModelsView, ModelView
from . import views