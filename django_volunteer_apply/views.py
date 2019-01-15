from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import ActivityManager, Activity, Choice, Person
from django.http import Http404
from .forms import PersonForm
# activity manager list
def index(request):
    latest_activity_manager_list = ActivityManager.objects.all()
    template = loader.get_template('apply/activity_list.html')
    context = {
        'latest_activity_manager_list': latest_activity_manager_list,
    }
    return HttpResponse(template.render(context, request))
    
def decode_position_id(position_id_text):
    '''
        given position_id_text like 'activity_id # choice_id',
        detect any errors and return the actual activity and choice
        return type: tuple object like (activity, choice, error_string)
    '''
    if(position_id_text.find('#')<0):
        return ('no # found', None, None)
    activity_id,choice_id = position_id_text.split('#')
    activity = None
    error_str = ''
    try:
        activity = Activity.objects.get(id=int(activity_id))
    except ValueError as e:
        error_str += 'invalid position_id_text %s.'%activity_id
        pass
    except Activity.DoesNotExist:
        error_str += 'nonexistent activity with id = %s.'%activity_id
        pass
    choice = None
    try:
        choice = Choice.objects.get(id=int(choice_id))
    except ValueError as e:
        error_str += 'invalid position_id_text %s.'%choice_id
        pass
    except Choice.DoesNotExist:
        error_str += 'nonexistent choice with id = %s.'%choice_id
        pass        
    return (error_str, activity, choice)
    
# application form
def detail(request, activity_manager_id):
    try:
        activity_manager = ActivityManager.objects.get(pk=activity_manager_id)
    except ActivityManager.DoesNotExist:
        raise Http404("ActivityManager does not exist")
    rq=request.POST
    if(rq):     # 'post' method processing   
        volunteer_name=rq.get('vn','$0')
        position_id_text_list=rq.get('id','$1') #format: activity_id_1 # choice_id_1 , activity_id_2 # choice_id_2
        operating_type = rq.get('type','1') # default is apply
        # check whether volunteer name exists in the table
        p = None
        try:
            p = Person.objects.get(name=volunteer_name)
        except Person.DoesNotExist:
            return HttpResponse('Name %s does not exist in the database.'%volunteer_name)
        choices = []
        for position_id_text in position_id_text_list.split(','):
            error_str, a, c = decode_position_id(position_id_text)
            if(error_str!=''):
                return HttpResponse(error_str)
            other_choices = a.choice_set.all().filter(person=p)
            if(operating_type == '1' and other_choices): # cannot apply for other choice in this group of activity            
                error_str = 'you apply two choices for activity. The conflict is (%s,%s). The second choice is not recorded.'%(other_choices[0].name, c.name)                
                break
            elif(operating_type == '0' and len(other_choices)==0):
                error_str = 'you cannot cancel a choice %s which you haven\'t applied yet'%(c.name)
                break
            elif(operating_type == '1'):
                # for non-null person, activity and choice, we add the person to the choice
                c.person_set.add(p)
                choices.append(c.name)
            else: # type = '0'
                c.person_set.remove(p)
                #print('------------',p.choices.all())
                choices.append(c.name)
        if(error_str):
            return HttpResponse(error_str)
        elif(operating_type == '1'):
            result_str = 'You apply %s successfully'%(','.join(choices))
        else: # type = '0'
            result_str = 'You cancel %s successfully'%(','.join(choices))
        return HttpResponse(result_str)
        
    context = {}                
    choices = []
    for activity in activity_manager.activity_set.all():
        for choice in activity.choice_set.all():
            # get left number of this choice
            name_list = []
            for person in choice.person_set.all():
                name_list.append(person.name)
            left_number = choice.left_number()
            choices.append({'content':activity.name + choice.name,'code':str(activity.id)+'#'+str(choice.id),'left_number':left_number,'name_list':','.join(name_list)})        
    template = loader.get_template('apply/activity.html')
    context['positions'] = choices
    context['activity_manager_name'] = activity_manager.name
    context['activity_manager_id'] = activity_manager_id
    return HttpResponse(template.render(context, request))

