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

def default_clean(self):
    '''form defautl clean method'''
    # print("\033[41;1mrun form defautl clean method...\033[0m",dir(self))
    # print(self.Meta.admin.readonly_fields)
    # print("cleaned_dtat:",self.cleaned_data)
    # print("form instance",self.instance)
    # print("form instance",self.instance.id)
    # print("validataion errors:",self.errors)
    if self.Meta.admin.readable_table is True:
        raise forms.ValidationError(("This is a readonly table!"))
    if self.errors:
        raise forms.ValidationError(("Please fix errors before re-submit."))
    if self.instance.id is not None :#means this is a change form ,should check the readonly fields
        for field in self.Meta.admin.readonly_fields:
            old_field_val = getattr(self.instance,field)
            form_val = self.cleaned_data[field]
            print("filed differ compare:",old_field_val,form_val)
            if old_field_val != form_val:
                self.add_error(field,"Readonly Field: field should be '{value}' ,not '{new_value}' ".\
                                     format(**{'value':old_field_val,'new_value':form_val}))

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
        #for validators
        if hasattr(cls.Meta.model,"clean_%s" % field_name):
            clean_field_func = getattr(cls.Meta.model,"clean_%s" % field_name)
            setattr(cls,"clean_%s" % field_name,clean_field_func)
    else:
        if hasattr(cls.Meta.model, "clean2"): #clean2 is kingadmin's own clean method
            clean_func = getattr(cls.Meta.model, "clean")
            setattr(cls, "clean" , clean_func)
        else:# use default clean method
            setattr(cls, "clean", default_clean)

    #print("modelf form admin class:",dir(cls.Meta))

    return ModelForm.__new__(cls)


def create_form(model,fields,admin_class,form_create=False,**kwargs):
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
    if kwargs.get("request"): #for form validator
        setattr(model_form,'_request',kwargs.get("request"))
    print(model_form)
    return model_form
