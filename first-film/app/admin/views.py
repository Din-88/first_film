
from flask import make_response, request, render_template, redirect, url_for
from . import admin
from app.models import *
from flask_login import fresh_login_required
from app.utils import admin_required
from . import ModelsView, ModelView
from flask import current_app as app


models_view = ModelsView()
models_view.append(ModelView(model=User,    session=db.session,
    view_exclude_list=['password'],
    form_exclude_list=['password']
))
models_view.append(ModelView(model=Film,    session=db.session,
    view_include_list=[
        'id', 
        'nameRu', 
        'year',
        'ratingKinopoisk',
        'time_created',
        'time_updated'],
    form_include_list=[
        'id', 
        'nameRu', 
        'year', 
        'genres',
        'countries',
        'videos',
        'description',
        'shortDescription',
        'time_created',
        'time_updated']
))
models_view.append(ModelView(model=Genre,   session=db.session))
models_view.append(ModelView(model=Country, session=db.session))
models_view.append(ModelView(model=Video,   session=db.session))
models_view.append(ModelView(model=Review,  session=db.session))
models_view.append(ModelView(model=Similar, session=db.session))
models_view.append(ModelView(model=Fact,    session=db.session))
models_view.append(ModelView(model=Request, session=db.session))


@admin.route('/')
@fresh_login_required
@admin_required
def index():
    return render_template('admin/admin.html', models_view=models_view)


@admin.route('/view')
@fresh_login_required
@admin_required
def view(model_name='', page=1):
    model_name = request.args.get('model_name', default='users', type=str)
    page       = request.args.get('page',       default=request.cookies.get(f'{model_name}_page', type=int),      type=int)
    sort       = request.args.get('sort',       default=request.cookies.get(f'{model_name}_sort', type=str),      type=str)
    sort_type  = request.args.get('sort_type',  default=request.cookies.get(f'{model_name}_sort_type', type=str), type=str)

    view_data = models_view.dict_models[model_name].get_view_data(page=page, sort=sort, sort_type=sort_type)

    res = make_response(render_template('admin/admin_view.html', view_data=view_data))
    res.set_cookie(key=f'{model_name}_page',      value=str(page),      path='/admin')
    res.set_cookie(key=f'{model_name}_sort',      value=str(sort),      path='/admin')
    res.set_cookie(key=f'{model_name}_sort_type', value=str(sort_type), path='/admin')

    return res


@admin.route('/edit', methods=['GET', 'POST'])
@fresh_login_required
@admin_required
def edit():
    model_name = request.args.get('model_name')
    id = request.args.get('id')
    model = models_view.dict_models[model_name].model.query.get(id)

    if model is None:
        return redirect(url_for('.view'))

    if request.method == 'GET':
        form = models_view.dict_models[model_name].form(obj=model)

    elif request.method == 'POST':
        form = models_view.dict_models[model_name].form(formdata=request.form)

        if form.validate():
            form.populate_obj(model)

            if request.form['action'] == 'Save':
                db.session.add(model)
            elif request.form['action'] == 'Delete':
                db.session.delete(model)
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                finally:
                    return redirect(url_for('.view'))

            try:
                db.session.commit()
            except:
                db.session.rollback()

    return render_template('admin/admin_edit.html', form=form, model_name=model_name, id=id)
