#_*_coding:utf-8_*_
__author__ = 'jieli'

from web import models
from django.forms import ModelForm
from django import forms

class UserProfileForm(ModelForm):

    class Meta:
        model = models.UserProfile
        fields = ['name','department','valid_begin_time','valid_end_time']


class IDCForm(ModelForm):

    class Meta:
        model = models.IDC
        fields = ['name']

#Test below

class RegistrationForm(forms.Form):
    username = forms.CharField(label="Username", max_length=32,required=True)
    name = forms.CharField(label="Real Name", max_length=32,widget=forms.TextInput(attrs={'class' : 'btn-success'}))
    email = forms.EmailField()
    passwd = forms.CharField(widget=forms.PasswordInput)




# class KingModelForm(ModelForm):
#     def __init__(self, model, *args, **kwargs):
#         super(KingModelForm,self).__init__(*args,**kwargs)
#         self.model = model
#         print("--->modelform ",model, args,kwargs)
#
#     class Meta:
#         model = self.model
#         #print(s)


def __new__(cls, *args, **kwargs):
    # super(CustomerForm, self).__new__(*args, **kwargs)
    # self.fields['customer_note'].widget.attrs['class'] = 'form-control'
    #disabled_fields = ['qq', 'consultant']
    for field_name in cls.base_fields:
        field = cls.base_fields[field_name]
        #print("field repr",field_name,field.__repr__())
        attr_dic = {'placeholder': field.help_text}
        if 'BooleanField' not in field.__repr__():
            attr_dic.update({'class': 'form-control'})
            #print("-->field",field)
            if 'ModelChoiceField' in field.__repr__(): #fk field
                attr_dic.update({'data-tag':field_name})
            # if 'DateTimeField' in field.__repr__():
            #     attr_dic.update({'placeholder': field_name})
        if cls.Meta.form_create is False:
            if field_name in cls.Meta.admin.readonly_fields:
                attr_dic['disabled'] = True
                #print('----read only:',field_name)
        field.widget.attrs.update(attr_dic)

    print("modelf form admin class:",dir(cls.Meta))

    return ModelForm.__new__(cls)


def create_form(model,fields,admin_class,form_create=False):
    class Meta:
        pass
    setattr(Meta,'model',model)
    setattr(Meta,'fields',fields)
    setattr(Meta,'admin',admin_class)
    setattr(Meta,'form_create',form_create)

    attrs = {'Meta':Meta}

    name = 'DynamicModelForm'
    baseclasess = (forms.ModelForm,)
    model_form = type(name, baseclasess,attrs)
    setattr(model_form,'__new__',__new__)
    print(model_form)
    return model_form
