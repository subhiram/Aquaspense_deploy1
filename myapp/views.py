from django.shortcuts import render, HttpResponse, redirect,reverse
from .models import *
import pandas as pd
import datetime
from django.contrib import messages
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.db.models import Avg
import smtplib, ssl
from email.message import EmailMessage
import math
import random
from django.views.decorators.cache import never_cache
#subhi subhi subhiram Subhiram123
# product landing page
def landing_page(request):
    return render(request,'landing1.html')

#signup page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['password1']
        email = request.POST['email']
        first_name = request.POST['first']
        last_name = request.POST['second']
        mobile = request.POST['mobile']
        if password == confirm:

            try:
                a = User.objects.get(username=username)
                messages.info(request,"user already exists")
                return redirect(user_login)
            except:
                user_type = False
                digits = [i for i in range(0, 10)]
                random_str = ""
                for i in range(6):
                    index = math.floor(random.random() * 10)
                    random_str += str(digits[index])
                otp = random_str

                is_verified = False
                sender_email = "subhiram.com@gmail.com"  # Enter your address
                receiver_email = email  # Enter receiver address
                msg = EmailMessage()
                ms = "your otp is " + otp
                msg.set_content(ms)
                msg['Subject'] = "Hello user, Your single-use code for website"
                msg['From'] = sender_email
                msg['To'] = receiver_email

                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login("subhiram.com@gmail.com", "ccdmwlifsunsguds")
                s.send_message(msg)
                s.quit()
                a = temp_user.objects.create(username=username, password=password, first_name=first_name,
                                             last_name=last_name,
                                             email=email, mobile=mobile, is_verified=is_verified, user_type=user_type,
                                             otp=otp)
                a.save()
                temp_id = a.temp_id
                context = {
                    'temp_id': temp_id,
                    'otp': otp
                }
                # messages.success(request, 'your otp is',otp)
                # return redirect(verify(request,temp_id))
                return render(request, 'verify.html', context=context)
                #user = User.objects.create_user(username=username,password=password, email=email, first_name=first_name, last_name=last_name)
                #user.save()
                #messages.success(request, 'Sign up successful!')
                #return redirect(user_login)
        else:
            messages.success(request, 'password and confirm password does not match!!')
            return redirect(signup)

    return render(request,'register.html')

def verify(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        temp_id = request.POST['id']
        print(otp)
        print(temp_id)
        a = temp_user.objects.get(temp_id=temp_id)
        email = a.email
        if a.otp == int(otp):
            print("otp matching")
            user = User.objects.create_user(username=a.username,password=a.password,first_name=a.first_name, last_name=a.last_name, email=a.email)
            user.save()
            j = User.objects.get(username=a.username)
            print("new user successfully created")
            user_dts = user_detail.objects.create(user_id=j.id,username=a.username,mobile=a.mobile,is_verified=True,user_type=a.user_type)
            user_dts.save()
            print("new user details successfully created")
            sender_email = "subhiram.com@gmail.com"  # Enter your address
            receiver_email = email  # Enter receiver address
            msg = EmailMessage()
            ms = "We are thrilled to have you onboard. your email has been successfully verified."
            msg.set_content(ms)
            msg['Subject'] = "Hello user, Aquaspense Welcomes you to the family"
            msg['From'] = sender_email
            msg['To'] = receiver_email

            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("subhiram.com@gmail.com", "ccdmwlifsunsguds")
            s.send_message(msg)
            s.quit()
            a.delete()
            messages.success(request, "successfully verified!")

            return redirect(user_login)
        else:
            print("otp not matching")
            messages.info(request, "otp does not match")
            context = {
                "temp_id":temp_id
            }
            return render(request, 'verify.html', context=context)

    return render(request, 'verify.html')

# user login page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)

        if user is not None:

            u = User.objects.get(username=username)
            print(u.id)
            try:
                j = user_detail.objects.get(user_id=u.id)
                if j.is_verified:
                    crop = main_crop.objects.filter(user_id=u.id).filter(status='ongoing')
                    print(crop)
                    login(request, user)
                    for c in crop:
                        print(c.crop_name)
                    crops1 = main_crop.objects.filter(user_id=u.id).filter(status='completed')
                    context = {
                        'crops': crop,
                        'crops1': crops1
                    }
                    messages.success(request, 'logged in successfully!')
                    return render(request, 'maindash.html', context=context)
                else:
                    messages.info(request, "email not verified, please contact the admin for more details!")
                    return render(request, 'login.html')
            except:
                messages.info(request,"email not verified, please contact the admin for more details!")
                return render(request, 'login.html')

        else:
            messages.info(request, "Invalid credentials, please try again!!")

    return render(request,'login.html')

#logout function
@login_required(redirect_field_name='userlogin')
def user_logout(request):
    logout(request)
    messages.success(request, 'logged out successfully!')
    return redirect(landing_page)

#user main dashboard
@login_required(redirect_field_name='userlogin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def crop_main_dashboard(request,pk):
    if request.user.is_authenticated:
        crop = main_crop.objects.filter(user_id=pk).filter(status='ongoing')
        try:
            crop1 = main_crop.objects.filter(user_id=pk).filter(status='completed')
        except:
            crop1=[]
        print(crop)
        for c in crop:
            print(c.crop_name)
        context = {
            'crops': crop,
            'crops1':crop1
        }
        return render(request, 'maindash.html', context=context)
    else:
        return redirect(user_login)

# add crop data to main crop table
@login_required(redirect_field_name='userlogin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create_crop(request,pk):
    if request.method == 'POST':
        crop_name = request.POST['crop_name']
        crop_date = request.POST['crop_date']
        crop_notes = request.POST['crop_notes']
        location = request.POST['location']
        print(crop_notes)
        print(crop_date)
        print(crop_name)
        status='ongoing'
        a = main_crop.objects.create(crop_name=crop_name, crop_date=crop_date, crop_notes=crop_notes,location=location, user_id=pk, status=status)
        a.save()
        print("new crop created")
        messages.success(request,"New crop created")

    return render(request, 'new_crop.html')

# main dash graph page
@login_required(redirect_field_name='userlogin')
def maindash_graph(request,pk):
    cr = main_crop.objects.filter(user_id=pk).distinct()
    ids = []
    crop_name = []
    for c in cr:
        ids.append(c.crop_id)
        crop_name.append(c.crop_name)
    crop_exp = []
    def total_exp(pk):
        a = expenses.objects.filter(crop_id=pk)
        j = []
        for i in a:
            j.append(i.exp_cost)
        expense_sum = sum(j)

        # getting information from worker expenses
        b = worker.objects.filter(crop_id=pk)
        work_exp = []
        for i in b:
            work_exp.append(i.amount)
        work_sum = sum(work_exp)
        e = ele_bill.objects.filter(crop_id=pk)
        ele = []
        for i in e:
            ele.append(i.bill_amount)
        ele_sum = sum(ele)
        total_expense = int(sum([expense_sum,work_sum,ele_sum]))
        return total_expense
    # for adding expenses
    for i in ids:
        x = total_exp(i)
        crop_exp.append(x)
        print(x)
    print(crop_exp)
    # labels = crop_name and data = crop_exp
    # for graph 2 comparing total feed used by the crops
    def total_feed(pk):
        x = daily_feed.objects.filter(crop_id=pk)
        if x:
            df = pd.DataFrame(list(x.values()))
            df['total'] = df['first'] + df['second'] + df['third'] + df['fourth']
            total_feed = df['total'].sum()
            total_bags = round(total_feed / 25)
            #print(total_bags)
        else:
            total_feed = 0
            total_bags = 0
        return total_feed,total_bags
    crop_feed = []
    for i in ids:
        x,y = total_feed(i)
        crop_feed.append(x)
    print(crop_feed)
    print(crop_name)
    # comparing the total no of days for the crops
    days=[]
    def get_days(pk):
        #getting the start date from the crop table
        d1 = main_crop.objects.get(crop_id=pk) # change the model after changing to the (ongoing and completed model)
        d1 = d1.crop_date

        # getting total no of days from the start date
        def numOfDays(date1, date2):
            return (date2 - date1).days
        # Driver program
        date2 = date.today()
        total_days = numOfDays(d1, date2)
        total_days = total_days+1
        return total_days
    for i in ids:
        x = get_days(i)
        days.append(x)
    print(days)
    # comparing the electricity expenses of the crops
    total_ele = []
    def get_ele_exp(pk):
        e = ele_bill.objects.filter(crop_id=pk)
        ele = []
        for i in e:
            ele.append(i.bill_amount)
        ele_sum = sum(ele)
        return ele_sum
    for i in ids:
        x = get_ele_exp(i)
        total_ele.append(x)
    print(total_ele)

    # getting the total export amount and material weight
    export_weight = []
    export_cost = []
    def get_export(pk):
        f = export.objects.filter(crop_id=pk)
        exp = []
        weight = []
        for i in f:
            exp.append(i.amount)
            weight.append(i.material_weight)
        export_sum = sum(exp)
        export_weight = sum(weight)
        print("the export sum is", export_sum)
        return export_weight,export_sum
    for i in ids:
        x,y = get_export(i)
        export_weight.append(x)
        export_cost.append(y)
    print(export_cost)
    print(export_weight)
    context={
        'graph1_labels':crop_name,
        'graph1_total':crop_exp,
        'graph2_labels':crop_name,
        'graph2_total': crop_feed,
        'graph3_labels':crop_name,
        'graph3_total': days,
        'graph4_labels': crop_name,
        'graph4_total':total_ele,
        'graph5_labels': crop_name,
        'graph5_total':export_cost,
        'graph6_labels': crop_name,
        'graph6_total':export_weight
    }

    return render(request,'maindash_graph.html',context=context)

# crop dashboard(sub dashboard)
@login_required(redirect_field_name='userlogin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request, pk):
    if request.user.is_authenticated:

        # getting the total expenses for that particular crop
        a = expenses.objects.filter(crop_id=pk)
        j = []
        for i in a:
            j.append(i.exp_cost)
        expense_sum = sum(j)

        # getting information from worker expenses
        b = worker.objects.filter(crop_id=pk)
        work_exp = []
        for i in b:
            work_exp.append(i.amount)
        work_sum = sum(work_exp)
        e = ele_bill.objects.filter(crop_id=pk)
        ele = []
        for i in e:
            ele.append(i.bill_amount)
        ele_sum = sum(ele)



        #getting the start date from the crop table
        d1 = main_crop.objects.get(crop_id=pk)
        d1 = d1.crop_date

        # getting total no of days from the start date
        def numOfDays(date1, date2):
            return (date2 - date1).days
        # Driver program
        date2 = date.today()
        total_days = numOfDays(d1, date2)
        total_days = total_days+1

        # getting the total feed used till now for that particular crop
        total_expense = int(sum([expense_sum, work_sum, ele_sum]))

        x = daily_feed.objects.filter(crop_id=pk)
        if x:
            print('true')
            df = pd.DataFrame(list(x.values()))
            df['total'] = df['first'] + df['second'] + df['third'] + df['fourth']
            total_feed = df['total'].sum()
            total_bags = round(total_feed/25)
            print(total_feed)
            print(total_bags)
        else:
            print('false')
            total_feed = '0'
            total_bags = '0'




        #graph1 content
        graph1_labels = ['Regular', 'Worker', 'Electrical']
        graph1_data = [expense_sum, work_sum, ele_sum]

        y = feed.objects.filter(crop_id=pk).filter(type='feed')
        try:
            x = []
            for i in y:
                x.append(i.quantity)
            print(sum(x), "is the total no of bags bought from amalapuram")
            s = sum(x) * 25
            print(s)

            if y:
                fee = []
                bags = []
                for i in y:
                    fee.append(i.bill_amount)
                    bags.append(i.quantity)
                feed_sum= sum(fee)
                feed_bags = sum(bags)
                graph1_labels = ['Regular', 'Worker', 'Electrical','Feed']
                graph1_data = [expense_sum, work_sum, ele_sum, feed_sum]

                z=feed.objects.filter(crop_id=pk).filter(type='other')
                other = []
                for i in z:
                    other.append(i.bill_amount)
                other_sum= sum(other)
                graph1_labels = ['Regular', 'Worker', 'Electrical', 'Feed', 'Other']
                graph1_data = [expense_sum, work_sum, ele_sum, feed_sum, other_sum]
                total_expense = int(sum([expense_sum, work_sum, ele_sum, feed_sum, other_sum]))
                t = abs(feed_bags - total_bags)
                print('total bags ia ', total_bags)
                print('feed bags', feed_bags)
        except:
            pass

        #graph 2 content
        f = export.objects.filter(crop_id=pk)
        exp = []
        for i in f:
            exp.append(i.amount)
        export_sum = sum(exp)
        print("the export sum is", export_sum)
        graph2_labels = ['Total spent', 'Total received']
        total_spent = sum(graph1_data)
        graph2_data = [total_spent,export_sum]

        d = main_crop.objects.get(crop_id=pk)
        user_id = d.user_id
        # getting the insights:
        #1 highest expense in that particular crop
        #2 highest daily feed in that particular crop

        if sum(graph1_data)==0:
            print("no data")
        crop = main_crop.objects.get(crop_id=pk)
        crops1 = main_crop.objects.filter(crop_id=pk).filter(status='completed')

        return render(request,'dashboard.html',{
            'total_expense':total_expense,
            'total_days':total_days,
            'total_feed': total_feed,
            'graph1_labels':graph1_labels,
            'graph1_total': graph1_data,
            'graph2_labels': graph2_labels,
            'graph2_total': graph2_data,
            'crop_id': pk,
            'user_id':user_id,
            'total_bags': total_bags,
            'crop':crop,
            'crops1':crops1
        })
    else:
        return redirect(user_login)

# data to be added by the user

@login_required(redirect_field_name='userlogin')
def create_expense(request, pk):
    crop_id=pk
    if request.method == 'POST':
        exp_name = request.POST['exp_name']
        exp_cost = request.POST['exp_cost']
        exp_date = request.POST['exp_date']
        exp_paidto = request.POST['exp_paidto']
        exp_notes = request.POST['exp_notes']
        crop_id = int(pk)

        e = expenses.objects.create(crop_id=crop_id, exp_name=exp_name, exp_cost=exp_cost, exp_date=exp_date,
                                    exp_paidto=exp_paidto, exp_notes=exp_notes)
        e.save()
        print("new expense created")
        msg = "new expense added"
        messages.success(request, 'New expense added successfully!')
        return render(request, 'expense_add.html', {
            'crop_id': crop_id,
        })
    return render(request, 'expense_add.html',
                  {
        'crop_id': crop_id
    })

@login_required(redirect_field_name='userlogin')
def create_workerexp(request, pk):
    if request.method == 'POST':
        worker_name = request.POST['worker_name']
        date = request.POST['date']
        amount = request.POST['amount']
        worker_notes = request.POST['worker_notes']
        crop_id = pk

        w = worker.objects.create(worker_name=worker_name, date=date, amount=amount, worker_notes=worker_notes,
                                  crop_id=crop_id)
        w.save()
        print("new workers expense created")
        messages.success(request, 'New worker expense added successfully!')
        return render(request, 'workexp_add.html', {
            'crop_id': pk,
        })

    return render(request, 'workexp_add.html',{
        'crop_id': pk,
    })

@login_required(redirect_field_name='userlogin')
def create_feed(request, pk):
    if request.method == 'POST':
        crop_id = pk
        date = request.POST['date']
        shop_name = request.POST['shop_name']
        bill_no = request.POST['bill_no']
        bill_amount = request.POST['bill_amount']
        feed_notes = request.POST['feed_notes']
        quantity = request.POST['quantity']
        type = request.POST['type']

        f = feed.objects.create(crop_id=crop_id, date=date, shop_name=shop_name, bill_no=bill_no,
                                bill_amount=bill_amount, feed_notes=feed_notes, quantity=quantity, type=type)
        f.save()
        print("new feed bill added")
        messages.success(request, 'New feed bill added successfully!')
        return render(request, 'feed_add.html', {'crop_id': pk})

    return render(request, 'feed_add.html', {'crop_id':pk})

@login_required(redirect_field_name='userlogin')
def create_medicine(request, pk):
    if request.method == 'POST':
        crop_id = pk
        med_name = request.POST['med_name']
        date = request.POST['date']
        bill_no = request.POST['bill_no']
        quantity = request.POST['quantity']
        amount = request.POST['amount']
        med_notes = request.POST['med_notes']

        m = medicine.objects.create(crop_id=crop_id, med_name=med_name, date=date, bill_no=bill_no, quantity=quantity,
                                    amount=amount, med_notes=med_notes)
        m.save()
        print("new medicine added")
        messages.success(request, 'New medicine bill added successfully!')
        return render(request, 'medicine_add.html', {'crop_id': pk})

    return render(request, 'medicine_add.html',{'crop_id':pk})

@login_required(redirect_field_name='userlogin')
def create_elebill(request, pk):
    if request.method == 'POST':
        crop_id = pk
        tranformer_type = request.POST['transformer_type']
        billed_date = request.POST['billed_date']
        start_read = request.POST['start_read']
        end_read = request.POST['end_read']
        bill_amount = request.POST['bill_amount']
        bill_notes = request.POST['bill_notes']

        print(crop_id)
        print(tranformer_type)
        print(billed_date)
        print(start_read)
        print(end_read)
        print(bill_amount)
        print(bill_notes)

        e = ele_bill.objects.create(crop_id=crop_id, tranformer_type=tranformer_type, billed_date=billed_date,
                                    start_read=start_read, end_read=end_read, bill_amount=bill_amount,
                                    bill_notes=bill_notes)
        e.save()
        print("new electrical bill added")
        messages.success(request, 'New electricity bill added successfully!')
        return render(request, 'elebill_add.html', {'crop_id': pk})

    return render(request, 'elebill_add.html', {'crop_id': pk})

@login_required(redirect_field_name='userlogin')
def create_export(request, pk):
    if request.method == 'POST':
        crop_id = pk
        date = request.POST['date']
        tank_no = request.POST['tank_no']
        material_weight = request.POST['material_weight']
        count = request.POST['count']
        amount = request.POST['amount']
        exp_notes = request.POST['exp_notes']

        print(crop_id)
        print(date)
        print(tank_no)
        print(material_weight)
        print(count)
        print(amount)
        print(exp_notes)

        exp = export.objects.create(crop_id=crop_id, date=date, tank_no=tank_no, material_weight=material_weight,
                                    count=count, amount=amount, exp_notes=exp_notes)
        exp.save()
        print("new export record added")
        messages.success(request, 'New export details added successfully!')
        return render(request, 'export_add.html', {'crop_id': pk})

    return render(request, 'export_add.html', {'crop_id':pk})

@login_required(redirect_field_name='userlogin')
def create_daily_feed(request, pk):
    if request.method == 'POST':
        crop_id = pk
        date = request.POST['date']
        tank_no = request.POST['tank_no']
        first = request.POST['first']
        second = request.POST['second']
        third = request.POST['third']
        fourth = request.POST['fourth']

        print(crop_id)
        print(date)
        print(tank_no)
        print(first)
        print(second)
        print(third)
        print(fourth)
        try:
            a = daily_feed.objects.get(crop_id=crop_id, date=date, tank_no=tank_no)
            if a:
                messages.info(request, "️the record already exists!")
        except:
            cr = daily_feed.objects.create(crop_id=crop_id, date=date, tank_no=tank_no, first=first, second=second,
                                           third=third, fourth=fourth)
            cr.save()
            messages.success(request, 'daily feed added successfully!')
            context= {
                'cropid':pk
            }
            #printing data
            print("new daily feed added")
        return render(request, 'dailyfeed_add.html', {'crop_id': pk})

    return render(request, 'dailyfeed_add.html', {'crop_id': pk})

@login_required(redirect_field_name='userlogin')
def complete_view(request, pk):
    # first getting the crop details
    if request.user.is_authenticated:

        maincrop = main_crop.objects.filter(crop_id=pk)

        # getting the information from expenses table
        expense = expenses.objects.filter(crop_id=pk)

        # getting the information from workers expenses table
        work_exp = worker.objects.filter(crop_id=pk)

        # getting the information from feed table
        feed_view = feed.objects.filter(crop_id=pk)

        # getting the information from medicine table
        med = medicine.objects.filter(crop_id=pk)

        # getting the information from electrical bill
        ele = ele_bill.objects.filter(crop_id=pk)

        # getting the information from export
        expo = export.objects.filter(crop_id=pk)

        # getting the information from daily feed
        daily = daily_feed.objects.filter(crop_id=pk).order_by('date')

        print(maincrop)
        print(expense)
        print(work_exp)
        print(feed_view)
        print(med)
        print(ele)
        print(expo)
        print(daily)
        context = {
            'maincrop': maincrop,
            'expense': expense,
            'work_exp': work_exp,
            'feed_view': feed_view,
            'med': med,
            'ele': ele,
            'expo': expo,
            'daily': daily,
            'crop_id': pk

        }

        for a in expense:
            print(a.exp_name)
            print(a.exp_cost)
            print(a.exp_date)
        for b in feed_view:
            print(b.date)

        return render(request, 'tables.html', context=context)
    else:
        return redirect(user_login)

@login_required(redirect_field_name='userlogin')
def graphs(request,pk):
    def get_label(a,pk,tank_no):
        x = a.objects.filter(crop_id=pk).filter(tank_no=tank_no).order_by('date')
        if x:
            df = pd.DataFrame(list(x.values()))
            df['total'] = df['first'] + df['second'] + df['third'] + df['fourth']
            a1_total = df['total'].to_list()
            a1_label = df['date'].to_list()
            s = []
            for i in a1_label:
                date_obj = datetime.datetime.strptime(str(i), "%Y-%m-%d")
                s.append(date_obj.strftime("%d-%B"))
            a1_label = s
        else:
            a1_label='no data available'
            a1_total=[0]
        return a1_label,a1_total
    # a1 tank graph1
    graph1_labels, graph1_total = get_label(daily_feed,pk,'A1')
    print(len(graph1_total))
    print(len(graph1_labels))
    # a2 tank graph2
    graph2_labels, graph2_total = get_label(daily_feed,pk,'A2')

    # B1 tank graph3
    graph3_labels, graph3_total = get_label(daily_feed,pk,'B1')

    # B2 tank graph 4:
    graph4_labels, graph4_total = get_label(daily_feed,pk,'B2')

    total = sum(graph1_total)+sum(graph2_total)+sum(graph3_total)+sum(graph4_total)
    print('total sum is',total)
    #electricity transformer comparision - graph 5
    graph5_label = ['40Kv', '100Kv']
    e = ele_bill.objects.filter(crop_id=pk).filter(tranformer_type='40kv')
    sum_40kv = []
    for i in e:
        sum_40kv.append(i.bill_amount)
    sum_40kv = sum(sum_40kv)
    sum_100kv = []
    e = ele_bill.objects.filter(crop_id=pk).filter(tranformer_type='100kv')
    for i in e:
        sum_100kv.append(i.bill_amount)
    sum_100kv = sum(sum_100kv)
    graph5_total = [sum_40kv,sum_100kv]

    #export details:
    f = export.objects.filter(crop_id=pk).filter(tank_no='A1')
    a1_amount = []
    for a in f:
        a1_amount.append(a.amount)
    a1_amount = sum(a1_amount)
    f = export.objects.filter(crop_id=pk).filter(tank_no='A2')
    a2_amount = []
    for a in f:
        a2_amount.append(a.amount)
    a2_amount = sum(a2_amount)
    f = export.objects.filter(crop_id=pk).filter(tank_no='B1')
    b1_amount = []
    for p in f:
        b1_amount.append(int(p.amount))
    b1_amount_final = sum(b1_amount)
    f = export.objects.filter(crop_id=pk).filter(tank_no='B2')
    b2_amount = []
    for a in f:
        b2_amount.append(a.amount)
    b2_amount = sum(b2_amount)

    graph6_label = ['A1', 'A2', 'B1', 'B2']
    graph6_data = [a1_amount,a2_amount,b1_amount_final,b2_amount]
    print(graph6_label)
    print(graph6_data)
    graph1_labels = graph1_labels[1:]
    graph1_total = graph1_total[1:]
    graph2_labels = graph2_labels[1:]
    graph2_total = graph2_total[1:]
    graph3_labels = graph3_labels[1:]
    graph3_total = graph3_total[1:]
    graph4_labels = graph4_labels[1:]
    graph4_total = graph4_total[1:]


    return render(request, 'charts.html', {
        'graph1_labels':graph1_labels,
        'graph1_total': graph1_total,
        'graph2_labels': graph2_labels,
        'graph2_total': graph2_total,
        'graph3_total': graph3_total,
        'graph3_labels': graph3_labels,
        'graph4_labels': graph4_labels,
        'graph4_total': graph4_total,
        'graph5_labels': graph5_label,
        'graph5_total': graph5_total,
        'graph6_labels': graph6_label,
        'graph6_total': graph6_data,
        'crop_id': pk,
    })

@login_required(redirect_field_name='userlogin')
def delete(request, name, pk):
    if name== 'expenses':
        m = expenses.objects.get(exp_no=pk)
        print(m.exp_name)
        m.delete()
        return redirect('complete_view',pk=m.crop_id)
    if name == 'worker':
        m = worker.objects.get(worker_no=pk)
        m.delete()
        return redirect('complete_view',pk=m.crop_id)
    if name == 'feed':
        m = feed.objects.get(feed_id=pk)
        m.delete()
        return redirect('complete_view',pk=m.crop_id)
    if name == 'med':
        m = medicine.objects.get(med_id=pk)
        m.delete()
        return redirect('complete_view',pk=m.crop_id)
    if name == 'ele':
        m = ele_bill.objects.get(bill_id=pk)
        m.delete()
        return redirect('complete_view', pk=m.crop_id)
    if name == 'export':
        m = export.objects.get(exp_id=pk)
        m.delete()
        return redirect('complete_view', pk=m.crop_id)
    if name == 'daily':
        m = daily_feed.objects.get(id=pk)
        m.delete()
        return redirect('complete_view', pk=m.crop_id)

# complete crop function
@login_required(redirect_field_name='userlogin')
def complete_btn_update(request,pk,days):
    c = main_crop.objects.get(crop_id=pk)
    c.status='completed'
    c.days=int(days)
    c.save()
    print("request executed")
    logout(request)
    messages.success(request, 'You have successfully completed the crop, please login again!')
    return redirect(user_login)
    #pk is the crop id

#complete crop dashboard
@login_required(redirect_field_name='userlogin')
def completed_crop_dashboard(request,pk):
    if request.user.is_authenticated:

        # getting the total expenses for that particular crop
        a = expenses.objects.filter(crop_id=pk)
        j = []
        for i in a:
            j.append(i.exp_cost)
        expense_sum = sum(j)

        # getting information from worker expenses
        b = worker.objects.filter(crop_id=pk)
        work_exp = []
        for i in b:
            work_exp.append(i.amount)
        work_sum = sum(work_exp)
        e = ele_bill.objects.filter(crop_id=pk)
        ele = []
        for i in e:
            ele.append(i.bill_amount)
        ele_sum = sum(ele)

        total_expense = int(sum([expense_sum,work_sum,ele_sum]))

        #getting the start date from the crop table
        d1 = main_crop.objects.get(crop_id=pk)
        d1 = d1.crop_date

        # getting total no of days from the start date
        def numOfDays(date1, date2):
            return (date2 - date1).days
        # Driver program
        date2 = date.today()
        total_days = numOfDays(d1, date2)
        total_days = total_days+1

        # getting the total feed used till now for that particular crop

        #graph1 content
        graph1_labels = ['Expenses', 'Worker Expenses', 'Electrical expenses']
        graph1_data = [expense_sum, work_sum, ele_sum]
        x = daily_feed.objects.filter(crop_id=pk)
        if x:
            print('true')
            df = pd.DataFrame(list(x.values()))
            df['total'] = df['first'] + df['second'] + df['third'] + df['fourth']
            total_feed = df['total'].sum()
            total_bags = round(total_feed/25)
            print(total_bags)
        else:
            print('false')
            total_feed = '0'
            total_bags = '0'
        y = feed.objects.filter(crop_id=pk).filter(type='feed')
        if y:
            fee = []
            bags = []
            for i in y:
                fee.append(i.bill_amount)
                bags.append(i.quantity)
            feed_sum= sum(fee)
            feed_bags = sum(bags)
            graph1_labels = ['Expenses', 'Worker Expenses', 'Electrical expenses','Feed expenses']
            graph1_data = [expense_sum, work_sum, ele_sum, feed_sum]

        #graph 2 content
        f = export.objects.filter(crop_id=pk)
        exp = []
        for i in f:
            exp.append(i.amount)
        export_sum = sum(exp)
        print("the export sum is", export_sum)
        graph2_labels = ['Total spent', 'Total received']
        total_spent = sum(graph1_data)
        graph2_data = [total_spent,export_sum]

        d = main_crop.objects.get(crop_id=pk)
        user_id = d.user_id
        # getting the insights:
        #1 highest expense in that particular crop
        #2 highest daily feed in that particular crop
        if sum(graph1_data)==0:
            print("no data")
        #crops1 = main_crop.objects.get
        crop = main_crop.objects.get(crop_id=pk)
        t = feed_bags-total_bags
        print(t)
        if t > 15:
            messages.info(request, 'The total no of feed bags does not match with daily feed!! please check if there is a discrepancy!')


        return render(request,'dashboard.html',{
            'total_expense':total_expense,
            'total_days':total_days,
            'total_feed': total_feed,
            'graph1_labels':graph1_labels,
            'graph1_total': graph1_data,
            'graph2_labels': graph2_labels,
            'graph2_total': graph2_data,
            'crop_id': pk,
            'user_id':user_id,
            'total_bags': total_bags,
            'crop':crop,
        })
    else:
        return redirect(user_login)

# 404 error page
def error_404_view(request, exception):
    # we add the path to the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')


#adding data through csv files (to be working on this)

# adding a profile page
# pk is the user id here
def profile(request,pk):
    s = User.objects.get(id=pk)
    print(s.username)
    print(s.email)
    print(s.first_name)
    print(s.last_name)

# cost estimation for the future crop
def estimate(request,pk):
    # pk is the crop id here
    # single_day_feed variable is for feed for single day (multiply with the no of days to get the total feed for the total days)
    if request.method == 'POST':
        count = int(request.POST['count']) #count label
        count_amt = int(request.POST['count_amt']) #cost of count
        count1 = int(request.POST['count1']) #label of count1
        count1_amt = int(request.POST['count1_amt']) #cost of count1
        total_weight = int(request.POST['weight']) # estimated weight of the tank
        predicted_weight = int(request.POST['pred_weight'])
        days = int(request.POST['days']) #no of days between count1 and count2
        bag_cost = int(request.POST['bag_cost']) # cost of a single feed bag
        print(count)
        print(count_amt)
        print(count1)
        print(count1_amt)
        print(total_weight)
        print(predicted_weight)
        print(days)
        print(bag_cost)
        #getting the base amount
        base_amt = total_weight*count_amt
        print(base_amt,"is the amount you will receive if you export now")


        # amount for total feed for the next x days
        electric = ele_bill.objects.filter(crop_id=pk).aggregate(Avg('bill_amount'))
        print(electric['bill_amount__avg'])
        electric_amt = electric['bill_amount__avg']
        print(electric_amt," is the electric expenses")
        x = daily_feed.objects.filter(crop_id=pk).order_by('date')
        if x:
            print('true')
            df = pd.DataFrame(list(x.values()))
            df['total'] = df['first'] + df['second'] + df['third'] + df['fourth']
            print(df['total'].mean()," is the average of the feed")
            total_feed = df['total'].sum()
            t = df.tail(1)
            single_day_feed = int(t['total'])
            print(single_day_feed)
            total_feed_kg= single_day_feed*days
            total_feed_cost = (total_feed_kg/25)*bag_cost
            print(total_feed_cost, "is the total feed cost for n days")
            #total_bags = round(total_feed / 25)
            #print(total_bags)
        #getting the exepenses average for that particular crop
        try:

            exp = expenses.objects.filter(crop_id=pk).aggregate(Avg('exp_cost'))
            work_exp = worker.objects.filter(crop_id=pk).aggregate(Avg('amount'))
            total_exp = exp['exp_cost__avg']+work_exp['amount__avg']
            print(total_exp)
        except:
            print("data not available")
            total_exp=0

        net1 = count1_amt*predicted_weight # estimated total amount
        net0 = total_exp+total_feed_cost+electric_amt # estimated expenses for the x number of days
        print(net1,"is the net1 amount which is the product of count and predicted weight")
        print(net0, "is the net0 amount which is the sum of expenses electrical and feed")
        final = net1-net0
        print(final, "is the final amount")
        profit_amt = final-base_amt
        print(profit_amt, "is the profit amount")
        context = {
            'current_returns': base_amt,
            'estimated_return': net1,
            'estimated_profit': profit_amt,
            'estimated_expenses': net0,
            'crop_id': pk
        }
        return render(request, 'estimate.html', context=context)
    context={
        'current_returns':'calculating',
        'estimated_return': 'calculating',
        'estimated_profit': 'calculating',
        'estimated_expenses': 'calculating',
        'crop_id':pk
    }
    return render(request,'estimate.html',context=context)






