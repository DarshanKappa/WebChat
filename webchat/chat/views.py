from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, JsonResponse
from .models import chat_list, chat
from datetime import datetime, timedelta
from threading import Timer

# Create your views here.

def friend_list(request):

    current_user = request.user

    sent_request = [ ]
    friend_request = [ ]
    friend_list = [ ]

    for i in chat_list.objects.all():
        if current_user.id == i.user_id and True == i.user_want and False == i.second_user_want:
            print(i.user_id)
            print(i.second_user_id)
            sent_request.append(User.objects.get(id=i.second_user_id))
        if current_user.id == i.user_id and False == i.user_want and True == i.second_user_want:
            friend_request.append(User.objects.get(id=i.second_user_id))
        if current_user.id == i.user_id and True == i.user_want and True == i.second_user_want:
            friend_list.append(User.objects.get(id=i.second_user_id))


    if request.method == 'POST':

        search = request.POST.get('friend','')
        print(search)
        
        if User.objects.filter(username=search).exists():

            user = User.objects.get(username=str(search))

            print(user.username)
      

            return render(request,'friend_list.html',{'friend':user,'sent_request':sent_request,'friend_request':friend_request,'friend_list':friend_list})
        else:
            messages.info(request,'Not find')
            return redirect('friend_list')

    return render(request,'friend_list.html',{'sent_request':sent_request,'friend_request':friend_request,'friend_list':friend_list})

def send_request(request):

    current_user = request.user
    name = request.GET['first_name']
    id = request.GET['id']
    print(name)
    print(id)

    if chat_list.objects.filter(user_id=current_user.id,second_user_id=id):
        print('yes')
        chat1 = chat_list.objects.get(user_id=current_user.id,second_user_id=id)
        chat2 = chat_list.objects.get(user_id=id,second_user_id=current_user.id)
        chat1.user_want = True
        chat2.second_user_want = True
        chat1.save()
        chat2.save()

    else:
        print('no')
        chat1 = chat_list(user_id=current_user.id,second_user_id=id,user_want=True)
        chat2 = chat_list(user_id=id,second_user_id=current_user.id,second_user_want=True)

        chat1.save()
        chat2.save()

        for i in chat_list.objects.all():
            print(i.user_id)
            print(i.second_user_id)
            print(i.user_want)
            print(i.second_user_want)


          
    return JsonResponse({'name':'sahil Chauhan'}, status=200)


def accept_request(request):
    
    current_user = request.user
    username = request.GET.get('id',False)
    action = request.GET.get('action',False)
    print(username)

    user = User.objects.get(username=username)
    print(user.id)

    chat1 = chat_list.objects.get(user_id=current_user.id,second_user_id=user.id)
    chat2 = chat_list.objects.get(user_id=user.id,second_user_id=current_user.id)

    if action == 'accept':
        print(action)

        chat1.user_want = True
        chat2.second_user_want = True

        chat1.save()
        chat2.save()

    if action == 'reject':
        print(action)

        chat1.second_user_want = False
        chat2.user_want = False

        chat1.save()
        chat2.save()


    return JsonResponse({'name':action}, status=200)





def chats(request):

    current_user = request.user
    id = request.GET.get('id',False)

    user1 = User.objects.get(id=current_user.id)
    user2 = User.objects.get(id=id)
    print(user1.first_name)
    print(user2.first_name)

    chat_list1 = chat_list.objects.get(user_id=current_user.id,second_user_id=id)
    chat_list2 = chat_list.objects.get(user_id=id,second_user_id=current_user.id)


    return render(request,'chat.html',{'user1':user1,'user2':user2,'chatlist1':chat_list1,'chatlist2':chat_list2})


def sendmessage(request):
    dt = datetime.now()
    message = request.GET.get('message',False)
    schat_id1 = request.GET.get('chat_id1',False)
    rchat_id2 = request.GET.get('chat_id2',False)


    c = chat(chat_id=schat_id1,message=message,date=dt)
    c.save()


    chats = [ ]
    no = 0
    s = chat.objects.all()
    for i in s:
        chats.append(i.message)
        no = no + 1

    return JsonResponse({'chat':chats,'no':no})




def allchat(request):

    print('ok')
    schat_id1 = request.GET.get('chat_id1',False)
    rchat_id2 = request.GET.get('chat_id2',False)
    lastmessage = request.GET.get('lastmessage',False)
    nlastyear = request.GET.get('lastyear',False)
    nlastmonth = request.GET.get('lastmonth',False)
    nlastdate = request.GET.get('lastdate',False)
    nlasthour = request.GET.get('lasthour',False)
    nlastminute = request.GET.get('lastminute',False)
    nlastsecond = request.GET.get('lastsecond',False)

    print(lastmessage)
    print(nlastyear)
    print(nlastmonth)
    print(nlastdate)
    print(nlasthour)
    print(nlastminute)
    print(nlastsecond)
    
    
    #print((datetime(2021,5,10,3,30,30)).strftime("%I:%M %p"))
    
    #sent messages
    # chats1 = [ ]
    # date1 = [ ]
    # time1 = [ ]
    # no1 = 0
    # for i in s:
    #     if i.chat_id == int(schat_id1):
    #         chats1.append(i.message)
    #         date1.append((i.date).time())
    #         #print((i.date).day,(i.date).strftime("%B"),(i.date).year)
    #         #print((i.date).strftime("%I:%M %p"))
    #         no1 = no1 + 1

    
    #sent and recieved messages
    chats = [ ]
    chat_id = [ ]
    message = [ ]
    dates = [ ]
    times = [ ]

    lastyear = 0
    lastmonth = 0
    lastdate = 0
    lasthour = 0
    lastminute = 0
    lastsecond = 0
    oldnew = 0
    
    t = (datetime(2021,1,1)).microsecond


    s = chat.objects.all()
        
    
    print('in')
    for i in s:
        if i.chat_id == int(schat_id1) or i.chat_id == int(rchat_id2):
            if not((i.date).date() == t):
                t = (i.date).date()

                chat_id.append(i.chat_id)
                message.append(i.message)
                if (i.date).date() == (datetime.now().date() - timedelta(days=1)):
                    print('yesterday')
                    dates.append((i.date).strftime("Yesterday"))
                elif (i.date).date() == datetime.now().date():
                    print('today')
                    dates.append((i.date).strftime("Today"))
                else:
                    dates.append((i.date).strftime("%d"+" "+"%B"+" "+"%Y"))

                times.append('date')
            
                
            chat_id.append(i.chat_id)
            message.append(i.message)
            dates.append((i.date).strftime("%d"+" "+"%B"+" "+"%y"))
            times.append((i.date).strftime("%I:%M %p"))
            lastyear = (i.date).year
            lastmonth = (i.date).month
            lastdate = (i.date).day
            lasthour = (i.date).hour
            lastminute = (i.date).minute
            lastsecond = (i.date).second
              
    oldnew = 'nothing'
            

                #print((i.date).day,(i.date).strftime("%B"),(i.date).year)
                #print((i.date).strftime("%I:%M %p"))

    # if lastmessage == '0':

    #     d = datetime(lastyear,lastmonth,lastdate,lasthour,lastminute,lastsecond)
    #     n = datetime(int(nlastyear),int(nlastmonth),int(nlastdate),int(nlasthour),int(nlastminute),int(nlastsecond))
            
    #     print(d)
    #     print(n)

    #     if not(d > n):
    #         print('old')
    #         oldnew = 'old'


    #     else:
    #         print('new')
    #         oldnew = 'new'
  

    # print(lastyear)
    # print(lastmonth)
    # print(lastdate)
    # print(lasthour)
    # print(lastminute)
    # print(lastsecond)
    
 

    return JsonResponse({
                        'chat_id':chat_id,
                        'chat':message,
                        'date':dates,
                        'time':times,
                        'lastyear':lastyear,
                        'lastmonth':lastmonth,
                        'lastdate':lastdate,
                        'lasthour':lasthour,
                        'lastminute':lastminute,
                        'lastsecond':lastsecond
                        })



def refreshchat(request):

    schat_id1 = request.GET.get('chat_id1',False)
    rchat_id2 = request.GET.get('chat_id2',False)
    lastmessage = request.GET.get('lastmessage',False)
    nlastyear = request.GET.get('lastyear',False)
    nlastmonth = request.GET.get('lastmonth',False)
    nlastdate = request.GET.get('lastdate',False)
    nlasthour = request.GET.get('lasthour',False)
    nlastminute = request.GET.get('lastminute',False)
    nlastsecond = request.GET.get('lastsecond',False)
    
    print('in refreshchat')

    chats = [ ]
    chat_id = [ ]
    message = [ ]
    dates = [ ]
    times = [ ]

    lastyear = 0
    lastmonth = 0
    lastdate = 0
    lasthour = 0
    lastminute = 0
    lastsecond = 0
    oldnew = 0
    
    t = (datetime(int(nlastyear),int(nlastmonth),int(nlastdate))).date()
  


    s = chat.objects.all()

    start = 0
        
    
    print('in')
    for i in s:
        if i.chat_id == int(schat_id1) or i.chat_id == int(rchat_id2):
            if start == 'start':
                if not((i.date).date() == t):
                    t = (i.date).date()

                    chat_id.append(i.chat_id)
                    message.append(i.message)
                    if (i.date).date() == (datetime.now().date() - timedelta(days=1)):
                        print('yesterday')
                        dates.append((i.date).strftime("Yesterday"))
                    elif (i.date).date() == datetime.now().date():
                        print('today')
                        dates.append((i.date).strftime("Today"))
                    else:
                        dates.append((i.date).strftime("%d"+" "+"%B"+" "+"%Y"))

                    times.append('date')
                
                    
                chat_id.append(i.chat_id)
                message.append(i.message)
                dates.append((i.date).strftime("%d"+" "+"%B"+" "+"%y"))
                times.append((i.date).strftime("%I:%M %p"))

            lastyear = (i.date).year
            lastmonth = (i.date).month
            lastdate = (i.date).day
            lasthour = (i.date).hour
            lastminute = (i.date).minute
            lastsecond = (i.date).second
            if datetime(lastyear,lastmonth,lastdate,lasthour,lastminute,lastsecond) == datetime(int(nlastyear),int(nlastmonth),int(nlastdate),int(nlasthour),int(nlastminute),int(nlastsecond)):
                start = 'start'
          
    for i in message:
        print(i)
    d = datetime(lastyear,lastmonth,lastdate,lasthour,lastminute,lastsecond)
    n = datetime(int(nlastyear),int(nlastmonth),int(nlastdate),int(nlasthour),int(nlastminute),int(nlastsecond))
            
    print(d)
    print(n)

    value = 1

    def time():
        value = 1
    
    start_time = datetime.now()
    seconnd_chage = 3
    def_time = 4

    # while 1:
    #     cur_time = datetime.now()

    #     def_time = (cur_time - start_time).seconds
    #     if def_time > 3:
    #         print('hello darshan')
    #         start_time = cur_time


        

       

    if d>n:
        print('new sms')
        oldnew = 'new'
        return JsonResponse({
                            'chat_id':chat_id,
                            'chat':message,
                            'date':dates,
                            'time':times,
                            'oldnew':oldnew,
                            'lastyear':lastyear,
                            'lastmonth':lastmonth,
                            'lastdate':lastdate,
                            'lasthour':lasthour,
                            'lastminute':lastminute,
                            'lastsecond':lastsecond
                            })
    else:
        print('not new sms')
        oldnew = 'old'
        return JsonResponse({
                            'chat_id':chat_id,
                            'chat':message,
                            'date':dates,
                            'time':times,
                            'oldnew':oldnew,
                            'lastyear':lastyear,
                            'lastmonth':lastmonth,
                            'lastdate':lastdate,
                            'lasthour':lasthour,
                            'lastminute':lastminute,
                            'lastsecond':lastsecond
                            })