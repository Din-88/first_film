
from sqlalchemy import desc
from app import db
from app.admin.fields import MySelectMultipleField
from app.models import *
from wtforms import validators
from wtforms import IntegerField, FloatField, StringField, BooleanField
from wtforms import DateTimeField, EmailField, PasswordField, TextAreaField
from flask_wtf import FlaskForm
from flask import current_app as app


class ModelView:

    def __init__(self, model, session, view_include_list=None, view_exclude_list=None,
                                       form_include_list=None, form_exclude_list=None):
        self.model = model
        self.session = session
        self.view_include_list = view_include_list
        self.view_exclude_list = view_exclude_list
        self.form_include_list = form_include_list
        self.form_exclude_list = form_exclude_list

        self.name =  self.model.__tablename__
        self.page = 1
        self.entries_per_page = app.config["ENTRIES_PER_PAGE"]

        _columns = [{'key': column.key, 'value': column } \
             for column in self.model._sa_class_manager.mapper.attrs]
        
        self.view_columns = ModelView.in_ex_clude_list_process(_columns, 
                                                                view_include_list, 
                                                                view_exclude_list)

        self.form_columns = ModelView.in_ex_clude_list_process(_columns, 
                                                                form_include_list, 
                                                                form_exclude_list)


        class MyForm(FlaskForm):
            pass

        self.form = MyForm

        self.create_form()

    @classmethod
    def in_ex_clude_list_process(cls, origin_list, include_list, exclude_list):
        columns = origin_list.copy()

        if include_list:
            columns = [c for c in columns if c['key'] in include_list]
        if exclude_list:
            columns = [c for c in columns if c['key'] not in exclude_list]
        
        if not columns:
            raise ValueError('include_list and exclude_list completely intersect')
        
        return columns

    def query_factory(self, name, ids):
        table = db.metadata.tables[name]
        id = table.columns._all_columns[0]
        query = self.session.query(table).filter(id.in_(ids))

        return query

    def db_session_merge(self, obj):
        return self.session.merge(obj)

    def is_unique(self):
        self.form_columns[2]['value'].class_attribute.impl.parent_token.parent.columns._all_columns[2].expression.unique
        self.form_columns[2]['value'].class_attribute.impl.parent_token.columns[0].unique
        self.form_columns[2]['value'].class_attribute.impl.parent_token.parent.columns._all_columns[2].expression.nullable
        pass

    def create_form(self):
        for column in self.form_columns:
            field_class = None
            
            if hasattr(column['value'], 'columns'):
                validator = None

                if column['value'].expression.nullable == False:
                    validator = [validators.DataRequired]

                column_type = column['value'].columns[0].type

                if isinstance(column_type, db.Integer):
                    field_class = IntegerField(column['key'])
                elif isinstance(column_type, db.Float):
                    field_class = FloatField(column['key'])  
                elif isinstance(column_type, db.String):
                    field_class = StringField(column['key'])
                    if isinstance(column_type, db.Text) or column_type.length > 80:
                        field_class = TextAreaField(column['key'])
                elif isinstance(column_type, db.Text):
                    field_class = TextAreaField(column['key'])
                elif isinstance(column_type, db.Boolean):
                    field_class = BooleanField(column['key'])
                elif isinstance(column_type, db.DateTime):
                    field_class = DateTimeField(
                        column['key'], 
                        validators=[validators.Optional()], 
                        render_kw={'readonly': True}
                        )

                if column['value'].columns[0].primary_key:
                    field_class = IntegerField(column['key'], render_kw={'readonly': True})
                
                field_class.validators = validators.DataRequired

            elif hasattr(column['value'], 'direction'):
                if column['value'].direction.name == 'ONETOMANY':
                    pass
                elif column['value'].direction.name == 'MANYTOMANY':
                    table = column['value'].mapper

                    choices = db.session.query(table).all()
                    choices = [(c.id, c) for c in choices]

                    field_class = MySelectMultipleField(
                        session=self.session,
                        query_factory=self.query_factory, 
                        label=column['key'], 
                        coerce=int,
                        choices=choices, validate_choice=False
                        )

            setattr(self.form, column['key'], field_class)
        pass
        
    def get_paginate(self, query, page):
        paginate = query.paginate(page=page, per_page=self.entries_per_page, error_out=False)
        return paginate

    def get_sort(self, query, key, sort_type):
        key = next((col for col in self.view_columns if col['key'] == key), None)
        if key:
            key = key['value']
            if hasattr(key, 'direction'):
                sort_type = None
                return query, sort_type

            if sort_type == 'dsc':
                key = desc(key)  

            query = query.order_by(key)
    
        return query, sort_type

    def get_view_data(self, page=1, sort=None, sort_type=None):
        data = {}
        key = next((col for col in self.view_columns if col['key'] == sort), None)
        if key:
            key = key['value']
            
        query = self.model.query
        sort_query, sort_type = self.get_sort(query=query, key=sort, sort_type=sort_type)
        paginate = self.get_paginate(query=sort_query, page=page)
        
        data['name'] = self.name
        data['sort'] = sort
        data['sort_type'] = sort_type
        data['column_names'] = [c['key'] for c in self.view_columns]
        data['values'] = paginate.items
        data['paginate'] = paginate

        return data


class ModelsView:
    def __init__(self):
        self.dict_models = {}
        pass

    def append(self, model_view):
        self.dict_models[model_view.name] = model_view
        pass
    