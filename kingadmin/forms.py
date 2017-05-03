#_*_coding:utf-8_*_
from django.forms import ModelForm
from django import forms


class FormTest(forms.Form):
    name = forms.CharField(max_length=32)
    age = forms.IntegerField()


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


    return ModelForm.__new__(cls)


def default_clean(self):
    '''form defautl clean method'''
    # print("\033[41;1mrun form defautl clean method...\033[0m",dir(self))
    # print(self.Meta.admin.readonly_fields)
    print("cleaned_dtat:",self.cleaned_data)
    # print("validataion errors:",self.errors)
    if self.Meta.admin.readonly_table is True:
        raise forms.ValidationError(("This is a readonly table!"))
    if self.errors:
        raise forms.ValidationError(("Please fix errors before re-submit."))
    if self.instance.id is not None :#means this is a change form ,should check the readonly fields
        for field in self.Meta.admin.readonly_fields:
            old_field_val = getattr(self.instance,field)
            form_val = self.cleaned_data.get(field)
            print("filed differ compare:",old_field_val,form_val)
            if old_field_val != form_val:
                if self.Meta.partial_update: #for list_editable feature
                    if field not in  self.cleaned_data:
                        #因为list_editable成生form时只生成了指定的几个字段，所以如果readonly_field里的字段不在，list_ediatble数据里，那也不检查了
                        continue #

                self.add_error(field,"Readonly Field: field should be '{value}' ,not '{new_value}' ".\
                                     format(**{'value':old_field_val,'new_value':form_val}))

    # #check unique contrains
    # for field in self.Meta.fields:
    #     field_obj = self.Meta.model._meta.get_field(field)
    #     if field_obj.unique:
    #

def create_form(model,fields,admin_class,form_create=False,**kwargs):
    class Meta:
        pass
    setattr(Meta,'model',model)
    setattr(Meta,'fields',fields)
    setattr(Meta,'admin',admin_class)
    setattr(Meta,'form_create',form_create)
    setattr(Meta,'partial_update',kwargs.get("partial_update"))  #for list_editable feature, only do partial check

    attrs = {'Meta':Meta}

    name = 'DynamicModelForm'
    baseclasess = (ModelForm,)
    model_form = type(name, baseclasess,attrs)
    setattr(model_form,'__new__',__new__)
    if kwargs.get("request"): #for form validator
        setattr(model_form,'_request',kwargs.get("request"))
    #print(model_form)
    return model_form
