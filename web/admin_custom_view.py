#_*_coding:utf-8_*_
__author__ = 'jieli'
from django.shortcuts import render,HttpResponse
from django.db import IntegrityError
import models
class BindHostsMultiHandle(object):
    def __init__(self,request):
        self.request = request
        self.err_dic ={}
        self.result = {'success':[],'failed':[]}


    def  is_valid(self):
        self.clean_data = {
             'host_user' :self.request.POST.get('host_user'),
            'hosts' : self.request.POST.getlist('hosts'),
            'host_groups' : self.request.POST.getlist('host_group'),
        }

        for k,v in self.clean_data.items():
            if not v:
                self.err_dic[k] = "field [%s] must be selected!" % k



        if self.clean_data['host_user']: self.clean_data['host_user'] = int(self.clean_data['host_user'])
        if self.clean_data['hosts']: self.clean_data['hosts'] = [int(i) for i in self.clean_data['hosts']]
        if self.clean_data['host_groups']: self.clean_data['host_groups'] = [int(i) for i in self.clean_data['host_groups']]

        #print self.clean_data,self.err_dic
        '''
        obj_list = models.BindHosts.objects.filter(
            host_user_id= clean_data.get('host_user'),
            host_group__id__in = clean_data.get('host_groups'),
            host_id__in = clean_data.get('hosts'),
        )
        print(obj_list)'''
        if self.err_dic:
            return False
        else:

            return True
    def save(self):

        for host in self.clean_data['hosts']:
            try:
                obj = models.BindHosts(
                    host_user_id = self.clean_data['host_user'],
                    host_id = host
                )
                obj.save()
                obj.host_group.add(*self.clean_data['host_groups'])
                self.result['success'].append(obj)
            except IntegrityError,e:

                exist_obj = models.BindHosts.objects.get(host_id=host,host_user_id= self.clean_data['host_user'])
                exist_obj.host_group.add(*self.clean_data['host_groups'])
                self.result['failed'].append(exist_obj)

        #print self.result
    def delete(self):
        pass