from django.contrib import admin
from django.forms.models import BaseModelFormSet
from django.forms.models import BaseInlineFormSet
from django import forms

from datetime import datetime, timedelta, date

from apps.spt.models import Player
from apps.spt.models import Season
from apps.spt.models import Game
from apps.spt.models import Play
from apps.spt.models import NewsFlash

class PlayInlineFormSet(BaseInlineFormSet):
        def __init__(self, *args, **kwargs):
                #print "PlayInlineFormSet"
                super(PlayInlineFormSet, self).__init__(*args, **kwargs)
                
		for i in range(0,self.total_form_count()):
			form = self.forms[i]
			form.fields['placement'].initial = str(i + 1)
			if i > 3:
				form.fields['placement'].initial = '0'
	
class PlayInlineAdminForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		#print "PlayInlineAdminForm"
                super(PlayInlineAdminForm, self).__init__(*args, **kwargs)
		#self.fields['players'].initial = Player.objects.get(firstname='Arlindo')


class PlayInline(admin.TabularInline):
	#form = PlayInlineAdminForm
	model = Play
	extra = 7
	readonly_fields = ('point',)
	formset = PlayInlineFormSet
	
	def get_formset(self,request,obj=None, **kwargs):
                print "get_formset"
                formset = super(PlayInline,self).get_formset(request,obj,**kwargs)
		print self.fields
		return formset	

class GameAdmin(admin.ModelAdmin):
	list_display = ('gamedate', 'gamenumber', 'finalseasongame')
 	ordering = ('gamedate','gamenumber')
	inlines = (PlayInline,)
	def save_formset(self, request, form, formset, change):
		obj = form.instance 
		#print obj.cancelledgame
		#print formset.cancelledgame

		instances = formset.save(commit=False)
		for instance in instances:
			if instance.placement == '1':
    				instance.point = 5
			elif instance.placement == '2':
    				instance.point = 3
			elif instance.placement == '3':
    				instance.point = 2
			elif instance.placement == '4':
    				instance.point = 1
			else:
				instance.point = 0
			if instance.sptmember == True:
                                instance.buyinamount = 60
                        else:
                                instance.buyinamount = 50
			if instance.games.finalseasongame == True:
				instance.buyinamount = 0
				instance.point = 0
			#if instance.games.cancelledgame == True:
			#	print "YES"
                        #        instance.buyinamount = 0
                        #        instance.point = 0
			#        instance.players.firstname = 'dummy'
			instance.save()
		formset.save_m2m()
	
	def save_model(self, request, obj, form, change):
        	
                #obj = form.instance
                #print obj.cancelledgame
        	obj.save()

 	def get_form(self,request,obj=None, **kwargs):
                form = super(GameAdmin,self).get_form(request,obj,**kwargs)
		
		strgmdate1 = str(Game.objects.latest('gamedate'))
		gmdate1 = datetime.strptime(strgmdate1[:10],'%Y-%m-%d')
		lower_limit = gmdate1
    		upper_limit = lower_limit + timedelta(days=2)
		cdatetime = datetime.now()

		strcdatetime = str(cdatetime)
		strcdatetime = strcdatetime[:10]
		cdatetime = datetime.strptime(strcdatetime,'%Y-%m-%d')
		if cdatetime.weekday() == 4:
                       	form.base_fields['gamedate'].initial = strcdatetime 
		else:
			previousfriday = cdatetime - timedelta(days=(cdatetime.weekday() - 4) % 7, weeks=0)
			form.base_fields['gamedate'].initial = previousfriday


    		if lower_limit <= cdatetime <= upper_limit:
			form.base_fields['gamenumber'].initial = '2'
		else:
			form.base_fields['gamenumber'].initial = '1'
	
		form.base_fields['seasons'].initial = Season.objects.latest('seasonnumber')
                
		return form
		
admin.site.register(NewsFlash)
admin.site.register(Season)
admin.site.register(Player)
admin.site.register(Game, GameAdmin)
