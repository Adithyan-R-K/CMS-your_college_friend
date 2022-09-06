import functools
import operator
import os.path

import mysql.connector
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.cache import cache
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, Http404
from django.http import HttpResponse
from datetime import date, datetime
import os
# Create your views here


def admin(request):
    return render(request, 'cmsapp/admin_login.html')


def index(request):
    return render(request, 'cmsapp/index.html')


def parent_signin(request):
    return render(request, 'cmsapp/parent_signin.html')


def parent_signup(request):
    return render(request, 'cmsapp/parent_signup.html')


def student_login(request):
    return render(request, 'cmsapp/student_login.html')


def success(request):
    return render(request, 'cmsapp/success_pay.html')


def teachers_signin(request):
    return render(request, 'cmsapp/teachers_signin.html')


def teachers_signup(request):
    return render(request, 'cmsapp/teachers_signup.html')


def wait(request):
    return render(request, 'cmsapp/wait.html')


def wait_login(request):
    return render(request, 'cmsapp/wait_login.html')


# admin dashboard
def a_index(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
    mycursor = conn.cursor()
    p = "select count(id) from parents where status='Admitted'"
    mycursor.execute(p)
    count = mycursor.fetchone()
    pa = (count[0])
    s = "select count(id) from student where status='Admitted'"
    mycursor.execute(s)
    count = mycursor.fetchone()
    sa = (count[0])
    t = "select count(id) from teacher where status='Admitted'"
    mycursor.execute(t)
    count = mycursor.fetchone()
    tc = (count[0])
    print(pa, sa, tc)
    #name = request.session['admin']
    return render(request, 'cmsapp/admin/index.html', {'prnt': pa, 'std': sa, 'tchr': tc})


def add_fee(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
    mycursor = conn.cursor()
    query = "select crs_name from course"
    mycursor.execute(query)
    records = mycursor.fetchall()
    v = functools.reduce(operator.add, (records))
    print(v)
    return render(request, 'cmsapp/admin/add_fee.html', {'records': v})
    #return render(request, 'cmsapp/admin/add_fee.html')


# add fee
def add_fee_(request):
    if request.method == 'POST':
        c = request.POST["course"]
        s = request.POST["sem"]
        dd = request.POST["ddate"]
        df = request.POST["fdate"]
        d = request.POST["details"]
        f = request.POST["fee"]
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        query = "insert into fee (`course`, `sem`, `due`, `final date`, `details`, `fee`) values ('" + c + "','" + s + "','" + dd + "','" + df + "','" + d + "','" + f + "')"
        mycursor.execute(query)
        conn.commit()
        query1 = "select crs_name from course"
        mycursor.execute(query1)
        records = mycursor.fetchall()
        v = functools.reduce(operator.add, (records))
        messages.success(request, 'Fee added successfully')
        return render(request, 'cmsapp/admin/add_fee.html', {'mes': 'fee added successfully', 'records': v})


def courses(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
    mycursor = conn.cursor()
    query = "select id, crs_id, crs_name, crs_duration, core_sub from course"
    mycursor.execute(query)
    if mycursor.rowcount == 0:
        return render(request, 'cmsapp/admin/courses.html', {'mes': 'no courses found'})
    else:
        records = mycursor.fetchall()
        return render(request, 'cmsapp/admin/courses.html', {'records': records})


# add course
def courses_(request):
    if request.method == 'POST':
        c = request.POST["course_id"]
        n = request.POST["name"]
        d = request.POST["duration"]
        cs = request.POST["core_sub"]
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        query = "insert into course (`crs_id`, `crs_name`, `crs_duration`, `core_sub`) values ('" + c + "','" + n + "','" + d + "','" + cs + "')"
        mycursor.execute(query)
        conn.commit()
        mycursor = conn.cursor()
        s = "select id, crs_id, crs_name, crs_duration, core_sub from course"
        mycursor.execute(s)
        records = mycursor.fetchall()
        messages.success(request, " Course Added. ")
        return render(request, 'cmsapp/admin/courses.html', {'records': records})


def courses_update(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
    mycursor = conn.cursor()

    if request.method == 'POST':
        if request.POST.get('delete'):
            id = request.POST["c_id"]
            print(id)
            query = "delete from course where id =" + id + " "
            mycursor.execute(query)
            conn.commit()
            query1 = "select id, crs_id, crs_name, crs_duration, core_sub from course"
            mycursor.execute(query1)
            records = mycursor.fetchall()
            messages.error(request, "Course deleted.")
            return render(request, 'cmsapp/admin/courses.html', {'records': records})
        # elif request.POST.get('edit'):
        #     id = request.POST["c_id"]
        #     print(id)
        #     query = "delete from course where id =" + id + " "
        #     mycursor.execute(query)
        #     conn.commit()
        #     query1 = "select id, crs_id, crs_name, crs_duration, core_sub from course"
        #     mycursor.execute(query1)
        #     records = mycursor.fetchall()
        #     messages.error(request, "Course deleted.")
        #     return render(request, 'cmsapp/admin/courses.html', {'records': records})

    return render(request, 'cmsapp/admin/courses.html')


def a_profile(request):
    return render(request, 'cmsapp/admin/profile.html')


def student_details(request):
    return render(request, 'cmsapp/admin/student_detail.html')


def student_fee(request):
    return render(request, 'cmsapp/admin/student_fee.html')


def student_list(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
    mycursor = conn.cursor()
    query = "select id, stdnt_name, stdnt_crsname, stdnt_adm, stdnt_sem, status from student"
    mycursor.execute(query)
    if mycursor.rowcount == 0:
        return render(request, 'cmsapp/admin/student_list.html', {'mes': 'no courses found'})
    else:
        records = mycursor.fetchall()
        return render(request, 'cmsapp/admin/student_list.html', {'records': records})


def student_approve(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
    mycursor = conn.cursor()
    id = request.POST["s_id"]
    s = "Admitted"
    s1 = "Denied"

    if request.method == 'POST':
        if request.POST.get("status"):
            query = "update student set status ='" + s + "' where id =" + id + " "
            mycursor.execute(query)
            conn.commit()
            query1 = "select id, stdnt_name, stdnt_crsname, stdnt_adm, stdnt_sem, status from student"
            mycursor.execute(query1)
            records = mycursor.fetchall()
            messages.success(request, "Approved.")
            return render(request, 'cmsapp/admin/student_list.html', {'records': records})

        elif request.POST.get("status1"):
            query = "update student set status ='" + s1 + "' where id =" + id + " "
            mycursor.execute(query)
            conn.commit()
            query1 = "select id, stdnt_name, stdnt_crsname, stdnt_adm, stdnt_sem, status from student"
            mycursor.execute(query1)
            records = mycursor.fetchall()
            messages.error(request, "Denied.")
            return render(request, 'cmsapp/admin/student_list.html', {'records': records})

    return render(request, 'cmsapp/admin/student_list.html')


def subject(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
    mycursor = conn.cursor()
    q = "select * from subject"
    mycursor.execute(q)
    tab = mycursor.fetchall()
    q1 = "select crs_name from course"
    mycursor.execute(q1)
    records = mycursor.fetchall()
    v = functools.reduce(operator.add, (records))
    q2 = "select id, tchr_name from teacher where status = 'Admitted'"
    mycursor.execute(q2)
    wa = mycursor.fetchall()
    #w = functools.reduce(operator.add, (wa))
    print( wa)
    return render(request, 'cmsapp/admin/subject.html', {'table': tab, 'crs': v, 'tchr': wa})
    #return render(request, 'cmsapp/admin/subject.html')


def add_subject(request):
    if request.method == 'POST':
        c = request.POST["course"]
        s = request.POST["sub_name"]
        t = request.POST["tchr"]
        se = request.POST["sem"]
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        query = "insert into subject (`crs`, `sub`, `teacher`, `sem`) values ('" + c + "','" + s + "','" + t + "','" + se + "')"
        mycursor.execute(query)
        conn.commit()
        q1 = "select crs_name from course"
        mycursor.execute(q1)
        records = mycursor.fetchall()
        v = functools.reduce(operator.add, (records))
        q2 = "select id, tchr_name from teacher where status = 'Admitted'"
        mycursor.execute(q2)
        w = mycursor.fetchall()
        # w = functools.reduce(operator.add, (wa))
        q = "select * from subject"
        mycursor.execute(q)
        tab = mycursor.fetchall()
        messages.success(request, 'New subject "' + s + '" added successfully.')
        return render(request, 'cmsapp/admin/subject.html', {'table': tab, 'crs': v, 'tchr': w})


def sub_update(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
    mycursor = conn.cursor()
    q = "select * from subject"
    mycursor.execute(q)
    tab = mycursor.fetchall()

    if request.method == 'POST':
        if request.POST.get('delete'):
            id = request.POST["s_id"]
            query = "delete from subject where id =" + id + " "
            mycursor.execute(query)
            conn.commit()
            #for continuity
            q = "select * from subject"
            mycursor.execute(q)
            tab = mycursor.fetchall()
            q1 = "select crs_name from course"
            mycursor.execute(q1)
            records = mycursor.fetchall()
            v = functools.reduce(operator.add, (records))
            q2 = "select id, tchr_name from teacher where status = 'Admitted'"
            mycursor.execute(q2)
            w = mycursor.fetchall()
            # w = functools.reduce(operator.add, (wa))
            messages.error(request, "Course deleted.")
            return render(request, 'cmsapp/admin/subject.html', {'table': tab, 'crs': v, 'tchr': w})
        elif request.POST.get('edit'):
            id = request.POST["s_id"]
            print(id)
            query = "SELECT crs FROM subject WHERE id =" + id + " "
            mycursor.execute(query)
            ((c,),) = mycursor.fetchall()
            query = "SELECT sub FROM subject WHERE id =" + id + " "
            mycursor.execute(query)
            ((s,),) = mycursor.fetchall()
            query = "SELECT teacher FROM subject WHERE id =" + id + " "
            mycursor.execute(query)
            ((t,),) = mycursor.fetchall()
            query = "SELECT sem FROM subject WHERE id =" + id + " "
            mycursor.execute(query)
            ((se,),) = mycursor.fetchall()
            print(id, c, s, t, se)
            request.session['sid'] = id
            request.session['scrs'] = c
            request.session['ssub'] = s
            request.session['stech'] = t
            request.session['ssem'] = se

            q1 = "select crs_name from course"
            mycursor.execute(q1)
            records = mycursor.fetchall()
            v = functools.reduce(operator.add, (records))
            q2 = "select id, tchr_name from teacher where status = 'Admitted'"
            mycursor.execute(q2)
            w = mycursor.fetchall()
            # w = functools.reduce(operator.add, (wa))
            #messages.error(request, "Course Edited.")
            return render(request, 'cmsapp/admin/sub_update.html', {'id': id, 'c': c, 's': s, 't': t, 'se': se, 'crs': v, 'tchr': w, })

    #return render(request, 'cmsapp/admin/subject.html', {'table': tab})


def s_update(request):
    id = request.session['sid']
    #c = request.session['scrs']
    s = request.session['ssub']
    #t = request.session['stech']
    #se = request.session['ssem']
    #form data
    cr = request.POST["course"]
    sub = request.POST["sub_name"]
    tr = request.POST["tchr"]
    sem = request.POST["sem"]
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
    mycursor = conn.cursor()
    query = "update subject set crs ='" + cr + "',sub ='" + sub + "',teacher ='" + tr + "',sem ='" + sem + "' where id =" + id + " "
    mycursor.execute(query)
    conn.commit()
    q1 = "select crs_name from course"
    mycursor.execute(q1)
    records = mycursor.fetchall()
    v = functools.reduce(operator.add, (records))
    q2 = "select id,tchr_name from teacher where status = 'Admitted'"
    mycursor.execute(q2)
    w = mycursor.fetchall()
    # w = functools.reduce(operator.add, (wa))
    q = "select * from subject"
    mycursor.execute(q)
    tab = mycursor.fetchall()
    messages.success(request, "Updated the subject '" + s + "'.")
    return render(request, 'cmsapp/admin/subject.html', {'table': tab, 'crs': v, 'tchr': w})


def teacher_list(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
    mycursor = conn.cursor()
    query = "select id, tchr_name, tchr_address, tchr_phone, tchr_email, tchr_dept, status from teacher"
    mycursor.execute(query)
    if mycursor.rowcount == 0:
        return render(request, 'cmsapp/admin/teacher_list.html', {'mes': 'no courses found'})
    else:
        records = mycursor.fetchall()
        return render(request, 'cmsapp/admin/teacher_list.html', {'records': records})


def teacher_approve(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
    mycursor = conn.cursor()
    id = request.POST["t_id"]
    s = "Admitted"
    s1 = "Denied"

    if request.method == 'POST':
        if request.POST.get("status"):
            query = "update teacher set status ='" + s + "' where id =" + id + " "
            mycursor.execute(query)
            conn.commit()
            query1 = "select id, tchr_name, tchr_address, tchr_phone, tchr_email, tchr_dept, status from teacher"
            mycursor.execute(query1)
            records = mycursor.fetchall()
            messages.success(request, "Approved.")
            return render(request, 'cmsapp/admin/teacher_list.html', {'records': records})
        elif request.POST.get("status1"):
            query = "update teacher set status ='" + s1 + "' where id =" + id + " "
            mycursor.execute(query)
            conn.commit()
            query1 = "select id, tchr_name, tchr_address, tchr_phone, tchr_email, tchr_dept, status from teacher"
            mycursor.execute(query1)
            records = mycursor.fetchall()
            messages.error(request, "Denied.")
            return render(request, 'cmsapp/admin/teacher_list.html', {'records': records})

    return render(request, 'cmsapp/admin/teacher_list.html')

# parent dashboard
def p_index(request):
    if 'pnam' in request.session:
        xox = request.session['sadmno']
        pn = request.session['pnam']
        return render(request, 'cmsapp/parent/index.html', {'sadmno': xox, 'pnam': pn,})
    else:
        return render(request, 'cmsapp/parent_signin.html', {'mes': 'Login to Enter'})


def p_fee(request):
    if 'pnam' in request.session:
        xox = request.session['sadmno']
        pn = request.session['pnam']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        query = "select id,course, sem, due, details, fee from fee"
        mycursor.execute(query)
        if mycursor.rowcount == 0:
            return render(request, 'cmsapp/parent/fee.html',)
        else:
            records = mycursor.fetchall()
            return render(request, 'cmsapp/parent/fee.html', {'records': records, 'sadmno': xox, 'pnam': pn,})
    else:
        return render(request, 'cmsapp/parent_signin.html', {'mes': 'Login to Enter'})


def p_payment(request):
    if 'pnam' in request.session:
        xox = request.session['sadmno']
        pn = request.session['pnam']
        return render(request, 'cmsapp/parent/payment.html', {'sadmno': xox, 'pnam': pn,})
    else:
        return render(request, 'cmsapp/parent_signin.html', {'mes': 'Login to Enter'})

#payment
def p_payment_(request):
    if request.method == "POST":
        n = request.POST["no"]
        na = request.POST["name"]
        m = request.POST["month"]
        y = request.POST["year"]
        c = request.POST["cvv"]
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        query = "select * from card where no. ='" + n + "' ,name ='" + na + "' ,month='" + m + "' ,year ='" + y + "' and cvv ='" + c + "' "
        mycursor.execute(query)
        mycursor.fetchall()
        print(mycursor.rowcount)
        if mycursor.rowcount == 0:
            return render(request, 'cmsapp/parent/payment.html')
        else:
            return render(request, 'cmsapp/success.html')


def p_interaction(request):
    if 'pnam' in request.session:
        xox = request.session['sadmno']
        pn = request.session['pnam']
        return render(request, 'cmsapp/parent/interaction.html', {'sadmno': xox, 'pnam': pn,})
    else:
        return render(request, 'cmsapp/parent_signin.html', {'mes': 'Login to Enter'})


def p_profile(request):
    if 'pnam' in request.session:
        xox = request.session['sadmno']
        pn = request.session['pnam']
        return render(request, 'cmsapp/parent/profile.html', {'sadmno': xox, 'pnam': pn,})
    else:
        return render(request, 'cmsapp/parent_signin.html', {'mes': 'Login to Enter'})


def p_result(request):
    if 'pnam' in request.session:
        xox = request.session['sadmno']
        pn = request.session['pnam']
        return render(request, 'cmsapp/parent/result.html', {'sadmno': xox, 'pnam': pn,})
    else:
        return render(request, 'cmsapp/parent_signin.html', {'mes': 'Login to Enter'})


def p_uexam(request):
    if 'pnam' in request.session:
        xox = request.session['sadmno']
        pn = request.session['pnam']
        return render(request, 'cmsapp/parent/uexam_result.html', {'sadmno': xox, 'pnam': pn,})
    else:
        return render(request, 'cmsapp/parent_signin.html', {'mes': 'Login to Enter'})


# student dashboard
def s_index(request):
    if 'username' in request.session:
        name = request.session['username']
        sp = request.session['usrep']
        return render(request, 'cmsapp/student/index.html', {'nam': name, 'spic': sp})
    else:
        return render(request, 'cmsapp/student_login.html', {'mes': 'Login to Enter'})


def s_exam(request):
    if 'username' in request.session:
        name = request.session['username']
        e = request.session['usremail']
        s = "Visible"
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        query = "select id,name, file, subject, exam_date, details, status from exam where status = '" + s + "' and crs in (select stdnt_crsname from student where stdnt_name= '" + name + "' and stdnt_email= '" + e + "' ) and sem in (select stdnt_sem from student where stdnt_name= '" + name + "' and stdnt_email= '" + e + "' )"
        mycursor.execute(query)
        records = mycursor.fetchall()
        if mycursor.rowcount == 0:
            sp = request.session['usrep']
            return render(request, 'cmsapp/student/exam.html', {'nam': name, 'spic': sp})
        else:
            sp = request.session['usrep']
            return render(request, 'cmsapp/student/exam.html', {'records': records, 'nam': name, 'spic': sp})
    else:
        return render(request, 'cmsapp/student_login.html', {'mes': 'Login to Enter'})


def s_exam_update(request):
    if 'username' in request.session:
        if request.method == 'POST':
            name = request.session['username']
            e = request.session['usremail']
            sp = request.session['usrep']
            eid = request.POST["e_id"]
            s = "Visible"
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
            mycursor = conn.cursor()
            query = "select id,name, file, subject, exam_date, details, status from exam where status = '" + s + "' and crs in (select stdnt_crsname from student where stdnt_name= '" + name + "' and stdnt_email= '" + e + "' ) and sem in (select stdnt_sem from student where stdnt_name= '" + name + "' and stdnt_email= '" + e + "' )"
            mycursor.execute(query)
            records = mycursor.fetchall()
            if request.POST.get("upload"):
                request.session['examid'] = eid
                return render(request, 'cmsapp/student/exam_up.html', {'records': records, 'nam': name, 'spic': sp, 'examid': eid})

            return render(request, 'cmsapp/student/exam_up.html', {'records': records, 'nam': name, 'spic': sp, 'examid': eid})
    else:
        return render(request, 'cmsapp/student_login.html', {'mes': 'Login to Enter'})


def s_exam_answer(request):
    if 'username' in request.session:
        if request.method == 'POST' and request.FILES['ans']:
            name = request.session['username']
            e = request.session['usremail']
            sp = request.session['usrep']
            eid = request.POST["exid"]
            myfile = request.FILES['ans']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            s = "Visible"
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
            mycursor = conn.cursor()
            query = "select id,name, file, subject, exam_date, details, status from exam where status = '" + s + "' and crs in (select stdnt_crsname from student where stdnt_name= '" + name + "' and stdnt_email= '" + e + "' ) and sem in (select stdnt_sem from student where stdnt_name= '" + name + "' and stdnt_email= '" + e + "' )"
            mycursor.execute(query)
            records = mycursor.fetchall()
            q1 = "select id from student where stdnt_name= '" + name + "' and stdnt_email= '" + e + "' "
            mycursor.execute(q1)
            ((sd,),) = mycursor.fetchall()
            sid = str(sd)
            qs = "select subject from exam where id= '" + eid + "' "
            mycursor.execute(qs)
            ((sj,),) = mycursor.fetchall()
            subject = str(sj)
            qsd = "select sub_date from exam where id= '" + eid + "' "
            mycursor.execute(qsd)
            ((subd,),) = mycursor.fetchall()
            #check already submitted or not
            qst = "select sub_time from exam where id= '" + eid + "' "
            mycursor.execute(qst)
            subtx = (mycursor.fetchone()[0])
            subt = str(subtx)
            print(subt)
            today = date.today()
            print(today)
            now = datetime.now()
            time = str(now.strftime('%H:%M:%S'))
            print(time)

            #check already submitted or not
            qch = "select id from answer where exam_id= '" + eid + "' and stdnt_id= '" + sid + "'  "
            mycursor.execute(qch)
            ch = mycursor.fetchall()
            if mycursor.rowcount == 0:
                if today <= subd:
                    if time <= subt:
                        qin = "INSERT INTO answer (`exam_id`, `stdnt_id`, `ans`) VALUES ('" + eid + "','" + sid + "','" + filename + "') "
                        mycursor.execute(qin)
                        conn.commit()
                        messages.success(request, "Successfully uploaded answer for '" + subject + "'.")
                        return render(request, 'cmsapp/student/exam_up.html', {'records': records, 'nam': name, 'spic': sp,})
                    else:
                        messages.error(request, " You are late ! Can't upload answer for '" + subject + "'.")
                        return render(request, 'cmsapp/student/exam_up.html', {'records': records, 'nam': name, 'spic': sp,})

                messages.error(request, " You are late ! Can't upload answer for '" + subject + "'.")
                return render(request, 'cmsapp/student/exam_up.html',{'records': records, 'nam': name, 'spic': sp, })
            else:
                messages.warning(request, "You already submitted answer for '" + subject + "'.")
                return render(request, 'cmsapp/student/exam_up.html', {'records': records, 'nam': name, 'spic': sp, })
    else:
        return render(request, 'cmsapp/student_login.html', {'mes': 'Login to Enter'})


def s_interaction(request):
    if 'username' in request.session:
        name = request.session['username']
        e = request.session['usremail']
        sp = request.session['usrep']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        q1 = "select id from student where stdnt_name= '" + name + "' and stdnt_email= '" + e + "' "
        mycursor.execute(q1)
        vm = (mycursor.fetchone()[0])
        a = str(vm)
        print("sid", a)
        q2 = "select stdnt_crsname from student where stdnt_name= '" + name + "' and stdnt_email= '" + e + "' "
        mycursor.execute(q2)
        xm = (mycursor.fetchone()[0])
        c = str(xm)
        q3 = "select stdnt_sem from student where stdnt_name= '" + name + "' and stdnt_email= '" + e + "' "
        mycursor.execute(q3)
        ym = (mycursor.fetchone()[0])
        s = str(ym)
        q4 = "select id,tchr_name,pic from teacher where id in  (select teacher from subject where crs= '" + c + "' and sem= '" + s + "' group by teacher ) and status = 'Admitted' "
        mycursor.execute(q4)
        ab = mycursor.fetchall()
        print("a", ab)
        return render(request, 'cmsapp/student/interaction.html', {'nam': name, 'tchrname': ab, 'spic': sp})
    else:
        return render(request, 'cmsapp/student_login.html', {'mes': 'Login to Enter'})


def s_inter(request):
    if 'username' in request.session:
        #select user
        if request.method == 'POST':
            tchri = request.POST["id"]
            tchrn = request.POST["name"]
            name = request.session['username']
            e = request.session['usremail']
            sp = request.session['usrep']
            print('hi', tchri, tchrn)
            request.session['tsenderid'] = tchri
            request.session['tsendername'] = tchrn
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
            mycursor = conn.cursor()
            q = "select stdnt_sem from student where stdnt_name= '" + name + "' and stdnt_email= '" + e + "' "
            mycursor.execute(q)
            nft = (mycursor.fetchone()[0])
            xo = str(nft)
            q1 = "select sub from subject where teacher= '" + tchri + "' and sem= '" + xo + "' "
            mycursor.execute(q1)
            ((ak,),) = mycursor.fetchall()
            print("tsub", ak)
            q3 = "select pic from teacher where id= '" + tchri + "'  "
            mycursor.execute(q3)
            ((p,),) = mycursor.fetchall()
            print("pic", p)
            #user list start
            qq = "select id from student where stdnt_name= '" + name + "' and stdnt_email= '" + e + "' "
            mycursor.execute(qq)
            vm = (mycursor.fetchone()[0])
            a = str(vm)
            print("sid", a)
            qw = "select stdnt_crsname from student where stdnt_name= '" + name + "' and stdnt_email= '" + e + "' "
            mycursor.execute(qw)
            xm = (mycursor.fetchone()[0])
            c = str(xm)
            qe = "select stdnt_sem from student where stdnt_name= '" + name + "' and stdnt_email= '" + e + "' "
            mycursor.execute(qe)
            ym = (mycursor.fetchone()[0])
            s = str(ym)
            qr = "select id,tchr_name,pic from teacher where id in  (select teacher from subject where crs= '" + c + "' and sem= '" + s + "' group by teacher ) and status = 'Admitted' "
            mycursor.execute(qr)
            ab = mycursor.fetchall()
            print("a", ab)
            qt = "select snd_id,recv_id,msg,time from message where snd_id= '" + tchri + "' or snd_id= '" + a + "' and recv_id= '" + a + "' or recv_id= '" + tchri + "' "
            mycursor.execute(qt)
            abc = mycursor.fetchall()
            # user list end
            print("msg", abc)
            i = int(tchri)
            o = int(a)
            return render(request, 'cmsapp/student/interaction.html', {'spic': sp, 'i': i, 'o': o, 'tchri': tchri, 'tpic': p, 'tchrn': tchrn, 'tsub': ak, 'nam': name, 'tchrname': ab, 'msg': abc})
    else:
        return render(request, 'cmsapp/student_login.html', {'mes': 'Login to Enter'})


def s_send(request):
    if 'username' in request.session:
        if request.method == 'POST':
            #start of insertion
            m = request.POST["msg"]
            tchri = request.session['tsenderid']
            tchrn = request.session['tsendername']
            tr = str(tchri)
            name = request.session['username']
            e = request.session['usremail']
            sp = request.session['usrep']
            s = datetime.now()
            d = s.strftime("%d/%m/%Y")
            print("is the date", d)
            t = s.strftime(" %H:%M:%S")
            print("the is date", t)
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
            mycursor = conn.cursor()
            qsel = "select id from student where stdnt_name= '" + name + "' and stdnt_email= '" + e + "' "
            mycursor.execute(qsel)
            av = (mycursor.fetchone()[0])
            a = str(av)
            qin = "insert into message (`snd_id`, `recv_id`, `msg`, `date`, `time`) values ('" + a + "','" + tr + "','" + m + "','" + d + "','" + t + "') "
            mycursor.execute(qin)
            conn.commit()
            # end of insertion
            # code user list start
            q1 = "select id from student where stdnt_name= '" + name + "' and stdnt_email= '" + e + "' "
            mycursor.execute(q1)
            vm = (mycursor.fetchone()[0])
            a = str(vm)
            print("sid", a)
            q2 = "select stdnt_crsname from student where stdnt_name= '" + name + "' and stdnt_email= '" + e + "' "
            mycursor.execute(q2)
            xm = (mycursor.fetchone()[0])
            c = str(xm)
            q3 = "select stdnt_sem from student where stdnt_name= '" + name + "' and stdnt_email= '" + e + "' "
            mycursor.execute(q3)
            ym = (mycursor.fetchone()[0])
            s = str(ym)
            q4 = "select id,tchr_name,pic from teacher where id in  (select teacher from subject where crs= '" + c + "' and sem= '" + s + "' group by teacher ) and status = 'Admitted' "
            mycursor.execute(q4)
            ao = mycursor.fetchall()
            print("a", ao)
                # sub = request.session['tchrs']
                # q1 = "select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' "
                # mycursor.execute(q1)
                # vm = (mycursor.fetchone()[0])
                # am = str(vm)
                # print("tid", am)
                # q2 = "select id,stdnt_name,stdnt_crsname,pic from student where id in  (select snd_id from message where recv_id= '" + am + "' group by snd_id )"
                # mycursor.execute(q2)
                # ao = mycursor.fetchall()
                # print("a", ao)
            # code user list end
            # code for message start
            qt = "select snd_id,recv_id,msg,time from message where snd_id= '" + tchri + "' or snd_id= '" + a + "' and recv_id= '" + a + "' or recv_id= '" + tchri + "' "
            mycursor.execute(qt)
            abc = mycursor.fetchall()
            print("msg", abc)
            i = int(tchri)
            o = int(a)
            # code for message end
            # code for userifo start
            q = "select stdnt_sem from student where stdnt_name= '" + name + "' and stdnt_email= '" + e + "' "
            mycursor.execute(q)
            nft = (mycursor.fetchone()[0])
            xo = str(nft)
            q1 = "select sub from subject where teacher= '" + tchri + "' and sem= '" + xo + "' "
            mycursor.execute(q1)
            ((ak,),) = mycursor.fetchall()
            print("tsub", ak)
            q3 = "select pic from teacher where id= '" + tchri + "'  "
            mycursor.execute(q3)
            ((p,),) = mycursor.fetchall()
            print("pic", p)
            # print("stdnt_sem", p)
            # code for userifo end
            return render(request, 'cmsapp/student/interaction.html', {'spic': sp, 'nam': name, 'tchrname': ao, 'i': i, 'o': o, 'msg': abc, 'tchri': tchri, 'tpic': p, 'tchrn': tchrn, 'tsub': ak})
    else:
        return render(request, 'cmsapp/student_login.html', {'mes': 'Login to Enter'})


def s_notes(request):
    if 'username' in request.session:
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        query = "select sub, file, details, date from note"
        mycursor.execute(query)
        if mycursor.rowcount == 0:
            name = request.session['username']
            sp = request.session['usrep']
            return render(request, 'cmsapp/student/notes.html', {'nam': name, 'spic': sp})
        else:
            records = mycursor.fetchall()
            name = request.session['username']
            sp = request.session['usrep']
            return render(request, 'cmsapp/student/notes.html', {'spic': sp, 'records': records, 'nam': name})
    else:
        return render(request, 'cmsapp/student_login.html', {'mes': 'Login to Enter'})


def s_profile(request):
    if 'username' in request.session:
        i = request.session['usremail']
        name = request.session['username']
        sp = request.session['usrep']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        m = "select stdnt_name, stdnt_address, stdnt_phone, stdnt_email, stdnt_crsname, stdnt_sem, stdnt_adm from student where  stdnt_email = '" + i + "' and  stdnt_name = '" + name + "' "
        mycursor.execute(m)
        records = mycursor.fetchall()
        q = "select pic from student where  stdnt_email = '" + i + "' and  stdnt_name = '" + name + "' "
        mycursor.execute(q)
        ((v,),) = mycursor.fetchall()
        print(v)
        return render(request, 'cmsapp/student/profile.html', {'spic': sp, 'nam': name, 'userinfo': records, 'userpic': v})
    else:
        return render(request, 'cmsapp/student_login.html', {'mes': 'Login to Enter'})


def s_pic(request):
    if 'username' in request.session:
        if request.method == 'POST' and request.FILES['pic']:
            myfile = request.FILES['pic']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            #p = request.POST["img"]
            i = request.session['usremail']
            name = request.session['username']
            sp = request.session['usrep']
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
            mycursor = conn.cursor()
            request.session['usrep'] = uploaded_file_url
            t = "update student set pic ='" + uploaded_file_url + "' where  stdnt_email = '" + i + "' and  stdnt_name = '" + name + "' "
            mycursor.execute(t)
            conn.commit()
            m = "select stdnt_name, stdnt_address, stdnt_phone, stdnt_email, stdnt_crsname, stdnt_sem, stdnt_adm from student where  stdnt_email = '" + i + "' and  stdnt_name = '" + name + "' "
            mycursor.execute(m)
            records = mycursor.fetchall()
            q = "select pic from student where  stdnt_email = '" + i + "' and  stdnt_name = '" + name + "' "
            mycursor.execute(q)
            ((v,),) = mycursor.fetchall()
            return render(request, 'cmsapp/student/profile.html', {'spic': sp, 'nam': name, 'userinfo': records, 'userpic': v})
    else:
        return render(request, 'cmsapp/student_login.html', {'mes': 'Login to Enter'})


def s_result(request):
    if 'username' in request.session:
        name = request.session['username']
        sp = request.session['usrep']
        return render(request, 'cmsapp/student/result.html', {'nam': name, 'spic': sp})
    else:
        return render(request, 'cmsapp/student_login.html', {'mes': 'Login to Enter'})


def s_fee(request):
    if 'username' in request.session:
        name = request.session['username']
        sp = request.session['usrep']
        return render(request, 'cmsapp/student/stud_fee.html', {'nam': name, 'spic': sp})
    else:
        return render(request, 'cmsapp/student_login.html', {'mes': 'Login to Enter'})


def s_teachers(request):
    if 'username' in request.session:
        i = request.session['usremail']
        name = request.session['username']
        sp = request.session['usrep']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        s = "select stdnt_crsname from student where  stdnt_email = '" + i + "' and  stdnt_name = '" + name + "' "
        mycursor.execute(s)
        ((crs,),) = mycursor.fetchall()
        mycursor = conn.cursor()
        print(crs)
        query = "select id,tchr_name, tchr_dept, tchr_dept from teacher where status='Admitted' and tchr_dept = '" + crs + "' "
        mycursor.execute(query)
        if mycursor.rowcount == 0:
            name = request.session['username']
            return render(request, 'cmsapp/student/teacher_list.html', {'nam': name})
        else:
            records = mycursor.fetchall()
            name = request.session['username']
            return render(request, 'cmsapp/student/teacher_list.html', {'records': records, 'nam': name, 'spic': sp})
    else:
        return render(request, 'cmsapp/student_login.html', {'mes': 'Login to Enter'})


def s_tinfo(request):
    if 'username' in request.session:
        id = request.POST["t_id"]
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        if request.method == 'POST':
            # if request.POST.get("view"):
            query1 = "select tchr_name, tchr_address, tchr_phone, tchr_email, tchr_dept,pic from teacher where id= '" + id + "' "
            mycursor.execute(query1)
            record = mycursor.fetchall()
                # return render(request, 'cmsapp/student/teacher_detail.html', {'records': record})

            return render(request, 'cmsapp/student/teacher_detail.html', {'records': record})
    else:
        return render(request, 'cmsapp/student_login.html', {'mes': 'Login to Enter'})


def s_tdetail(request):
    if 'username' in request.session:
        name = request.session['username']
        sp = request.session['usrep']
        return render(request, 'cmsapp/student/teacher_detail.html', {'nam': name, 'spic': sp})
    else:
        return render(request, 'cmsapp/student_login.html', {'mes': 'Login to Enter'})


def s_uexam(request):
    if 'username' in request.session:
        name = request.session['username']
        sp = request.session['usrep']
        return render(request, 'cmsapp/student/uxam_result.html', {'nam': name, 'spic': sp})
    else:
        return render(request, 'cmsapp/student_login.html', {'mes': 'Login to Enter'})


# teacher dashboard
def t_index(request):
    if 'tchrn' in request.session:
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        p = "select count(id) from parents where status='Admitted'"
        mycursor.execute(p)
        count = mycursor.fetchone()
        pa = (count[0])
        s = "select count(id) from student where status='Admitted'"
        mycursor.execute(s)
        count = mycursor.fetchone()
        sa = (count[0])
        t = "select count(id) from teacher where status='Admitted'"
        mycursor.execute(t)
        count = mycursor.fetchone()
        tc = (count[0])
        print(pa, sa, tc)
        name = request.session['tchrn']
        tchrp = request.session['tchrp']
        return render(request, 'cmsapp/teacher/index.html', {'trpic': tchrp, 'prnt': pa, 'std': sa, 'tchr': tc, 'trn': name})
    else:
        return render(request, 'cmsapp/teachers_signin.html', {'mes': 'Login to Enter'})


def t_courses(request):
    if 'tchrn' in request.session:
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        query = "select crs_id, crs_name from course"
        mycursor.execute(query)
        if mycursor.rowcount == 0:
            name = request.session['tchrn']
            tchrp = request.session['tchrp']
            return render(request, 'cmsapp/teacher/courses.html', {'trpic': tchrp, 'trn': name})
        else:
            records = mycursor.fetchall()
            name = request.session['tchrn']
            tchrp = request.session['tchrp']
            return render(request, 'cmsapp/teacher/courses.html', {'trpic': tchrp, 'records': records, 'trn': name})
    else:
        return render(request, 'cmsapp/teachers_signin.html', {'mes': 'Login to Enter'})


def t_exam(request):
    if 'tchrn' in request.session:
        name = request.session['tchrn']
        e = request.session['tchre']
        tsub = request.session['tchrs']
        tchrp = request.session['tchrp']
        print(tsub)
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        query = "select id, name, file, subject, exam_date, details, sub_date, sub_time, status from exam where subject in (select sub from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' ))"
        mycursor.execute(query)
        records = mycursor.fetchall()
        q1 = "select crs from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' )"
        mycursor.execute(q1)
        cr = mycursor.fetchall()
        crs = functools.reduce(operator.add, (cr))
        q2 = "select sub from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' )"
        mycursor.execute(q2)
        su = mycursor.fetchall()
        sub = functools.reduce(operator.add, (su))
        q3 = "select sem from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' )"
        mycursor.execute(q3)
        sm = mycursor.fetchall()
        sem = functools.reduce(operator.add, (sm))
        if mycursor.rowcount == 0:
            name = request.session['tchrn']
            return render(request, 'cmsapp/teacher/exam.html', {'trpic': tchrp, 'trn': name, 'tsubj': tsub, 'crs': crs, 'sub': sub, 'sem': sem})
        else:
            name = request.session['tchrn']
            return render(request, 'cmsapp/teacher/exam.html', {'trpic': tchrp, 'records': records, 'trn': name, 'tsubj': tsub, 'crs': crs, 'sub': sub, 'sem': sem})
    else:
        return render(request, 'cmsapp/teachers_signin.html', {'mes': 'Login to Enter'})


def t_exam_(request):
    if 'tchrn' in request.session:
        if request.method == 'POST' and request.FILES['file_upload']:
            myfile = request.FILES['file_upload']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            ex = request.POST["exam"]
           # c = request.POST["file"]
            cors = request.POST["crs"]
            s = request.POST["sub"]
            sem = request.POST["sem"]
            sda = request.POST["date"]
            tym = request.POST["time"]
            ko = date.today()
            da = ko.strftime("%Y/%m/%d")
            d = request.POST["details"]
            st = request.POST["status"]
            tsub = request.session['tchrs']
            tchrp = request.session['tchrp']
            name = request.session['tchrn']
            e = request.session['tchre']
            print(tsub)
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
            mycursor = conn.cursor()
            query = "insert into exam (`name`, `file`,`crs`, `subject`, `sem`, `exam_date`, `details`, `sub_date`, `sub_time`, `status`) values ('" + ex + "','" + filename + "','" + cors + "','" + s + "','" + sem + "','" + da + "','" + d + "','" + sda + "','" + tym + "','" + st + "')"
            mycursor.execute(query)
            conn.commit()
            query1 = "select id, name, file, subject, exam_date, details, sub_date, sub_time, status from exam where subject in (select sub from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' ))"
            mycursor.execute(query1)
            records = mycursor.fetchall()
            q1 = "select crs from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' )"
            mycursor.execute(q1)
            cr = mycursor.fetchall()
            crs = functools.reduce(operator.add, (cr))
            q2 = "select sub from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' )"
            mycursor.execute(q2)
            su = mycursor.fetchall()
            sub = functools.reduce(operator.add, (su))
            q3 = "select sem from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' )"
            mycursor.execute(q3)
            sm = mycursor.fetchall()
            sem = functools.reduce(operator.add, (sm))
            if mycursor.rowcount == 0:
                return render(request, 'cmsapp/teacher/exam.html', {'trpic': tchrp, 'trn': name, 'tsubj': tsub, 'crs': crs, 'sub': sub, 'sem': sem})
            else:
                messages.success(request, "Exam questions added successfully.")
                return render(request, 'cmsapp/teacher/exam.html', {'trpic': tchrp, 'records': records, 'trn': name, 'tsubj': tsub, 'crs': crs, 'sub': sub, 'sem': sem})
    else:
        return render(request, 'cmsapp/teachers_signin.html', {'mes': 'Login to Enter'})


def viewpdf(request):
    path = request.GET["filenam"]
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    else:
        raise Http404


def t_exam_update(request):
    if 'tchrn' in request.session:
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        id = request.POST["e_id"]
        s = "Visible"
        s1 = "Hidden"
        name = request.session['tchrn']
        e = request.session['tchre']
        tchrp = request.session['tchrp']
        q1 = "select crs from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' )"
        mycursor.execute(q1)
        cr = mycursor.fetchall()
        crs = functools.reduce(operator.add, (cr))
        q2 = "select sub from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' )"
        mycursor.execute(q2)
        su = mycursor.fetchall()
        sub = functools.reduce(operator.add, (su))
        q3 = "select sem from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' )"
        mycursor.execute(q3)
        sm = mycursor.fetchall()
        sem = functools.reduce(operator.add, (sm))

        if request.method == 'POST':
            if request.POST.get("view"):
                query = "update exam set status ='" + s + "' where id =" + id + " "
                mycursor.execute(query)
                conn.commit()
                query1 = "select id, name, file, subject, exam_date, details, sub_date, sub_time, status from exam where subject in (select sub from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' ))"
                mycursor.execute(query1)
                records = mycursor.fetchall()
                messages.warning(request, "Now the question is VISIBLE to students.")
                name = request.session['tchrn']
                return render(request, 'cmsapp/teacher/exam.html', {'trpic': tchrp, 'records': records, 'trn': name, 'crs': crs, 'sub': sub, 'sem': sem})
            elif request.POST.get("hide"):
                query = "update exam set status ='" + s1 + "' where id =" + id + " "
                mycursor.execute(query)
                conn.commit()
                query1 = "select id, name, file, subject, exam_date, details, sub_date, sub_time, status from exam where subject in (select sub from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' ))"
                mycursor.execute(query1)
                records = mycursor.fetchall()
                messages.success(request, "Now the question is HIDDEN to students.")
                name = request.session['tchrn']
                return render(request, 'cmsapp/teacher/exam.html', {'trpic': tchrp, 'records': records, 'trn': name, 'crs': crs, 'sub': sub, 'sem': sem})
            elif request.POST.get('delete'):
                id = request.POST["e_id"]
                print(id)
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
                mycursor = conn.cursor()
                query = "delete from exam where id =" + id + " "
                mycursor.execute(query)
                conn.commit()
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
                mycursor = conn.cursor()
                query1 = "select id, name, file, subject, exam_date, details, sub_date, sub_time, status from exam where subject in (select sub from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' ))"
                mycursor.execute(query1)
                records = mycursor.fetchall()
                messages.error(request, "Exam questions deleted.")
                name = request.session['tchrn']
                return render(request, 'cmsapp/teacher/exam.html', {'trpic': tchrp, 'records': records, 'trn': name, 'crs': crs, 'sub': sub, 'sem': sem})

        name = request.session['tchrn']
        return render(request, 'cmsapp/teacher/exam.html', {'trpic': tchrp, 'trn': name, 'crs': crs, 'sub': sub, 'sem': sem})
    else:
        return render(request, 'cmsapp/teachers_signin.html', {'mes': 'Login to Enter'})


def t_interaction(request):
    if 'tchrn' in request.session:
        name = request.session['tchrn']
        e = request.session['tchre']
        sub = request.session['tchrs']
        tchrp = request.session['tchrp']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        q1 = "select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' "
        mycursor.execute(q1)
        vm = (mycursor.fetchone()[0])
        a = str(vm)
        print("tid", a)
        q2 = "select id,stdnt_name,stdnt_crsname,pic from student where id in  (select snd_id from message where recv_id= '" + a + "' group by snd_id ) and status = 'Admitted'"
        mycursor.execute(q2)
        ab = mycursor.fetchall()
        print("a", ab)
        return render(request, 'cmsapp/teacher/interaction.html', {'trpic': tchrp, 'trn': name, 'usrname': ab})
    else:
        return render(request, 'cmsapp/teachers_signin.html', {'mes': 'Login to Enter'})


def t_inter(request):
    if 'tchrn' in request.session:
        #select user
        if request.method == 'POST':
            stdnti = request.POST["id"]
            stdntn = request.POST["name"]
            print('hi', stdnti, stdntn)
            request.session['senderid'] = stdnti
            request.session['sendername'] = stdntn
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
            mycursor = conn.cursor()
            q1 = "select stdnt_crsname from student where id= '" + stdnti + "'  "
            mycursor.execute(q1)
            ((ak,),) = mycursor.fetchall()
            print("stdnt_crsname", ak)
            q2 = "select stdnt_sem from student where id= '" + stdnti + "'  "
            mycursor.execute(q2)
            ((bk,),) = mycursor.fetchall()
            print("stdnt_sem", bk)
            q3 = "select pic from student where id= '" + stdnti + "'  "
            mycursor.execute(q3)
            ((p,),) = mycursor.fetchall()
            print("stdnt_sem", p)
            # query = "insert into message (`snd_id`, `recv_id`, `msg`, `date`, `time`) values ('" + s + "','" + r + "','" + m + "','" + d + "','" + t + "')"
            # mycursor.execute(query)
            # conn.commit()
            #code for listing user
            name = request.session['tchrn']
            e = request.session['tchre']
            sub = request.session['tchrs']
            q1 = "select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' "
            mycursor.execute(q1)
            vm = (mycursor.fetchone()[0])
            a = str(vm)
            print("tid", a)
            q2 = "select id,stdnt_name,stdnt_crsname,pic from student where id in  (select snd_id from message where recv_id= '" + a + "' group by snd_id ) and status = 'Admitted'"
            mycursor.execute(q2)
            ab = mycursor.fetchall()
            print("id,stdnt_name,stdnt_crsname", ab)
            request.session['tid'] = a
            # q3 = "select snd_id,recv_id,msg from message where snd_id= '" + stdnti + "' and recv_id= '" + a + "' "
            # mycursor.execute(q3)
            # abc = mycursor.fetchall()
            # print("msg", abc)
            q3 = "select snd_id,recv_id,msg,time from message where snd_id= '" + stdnti + "' or snd_id= '" + a + "' and recv_id= '" + a + "' or recv_id= '" + stdnti + "' "
            mycursor.execute(q3)
            abc = mycursor.fetchall()
            print("msg", abc)
            i = int(stdnti)
            o = int(a)
            tchrp = request.session['tchrp']
            return render(request, 'cmsapp/teacher/interaction.html', {'trpic': tchrp, 'i': i, 'o': o, 'stdnti': stdnti, 'stdntpic': p, 'stdntn': stdntn, 'stdntc': ak, 'stdnts': bk, 'trn': name, 'usrname': ab, 'msg': abc, 'tid': a})
    else:
        return render(request, 'cmsapp/teachers_signin.html', {'mes': 'Login to Enter'})


def t_send(request):
    if 'tchrn' in request.session:
        if request.method == 'POST':
            #start of insertion
            m = request.POST["msg"]
            stdnti = request.session['senderid']
            stdntn = request.session['sendername']
            std = str(stdnti)
            name = request.session['tchrn']
            e = request.session['tchre']
            tchrp = request.session['tchrp']
            s = datetime.now()
            d = s.strftime("%d/%m/%Y")
            t = s.strftime(" %H:%M:%S")
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
            mycursor = conn.cursor()
            qsel = "select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' "
            mycursor.execute(qsel)
            av = (mycursor.fetchone()[0])
            a = str(av)
            qin = "insert into message (`snd_id`, `recv_id`, `msg`, `date`, `time`) values ('" + a + "','" + std + "','" + m + "','" + d + "','" + t + "') "
            mycursor.execute(qin)
            conn.commit()
            # end of insertion
            # code user list start
            sub = request.session['tchrs']
            q1 = "select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' "
            mycursor.execute(q1)
            vm = (mycursor.fetchone()[0])
            am = str(vm)
            print("tid", am)
            q2 = "select id,stdnt_name,stdnt_crsname,pic from student where id in  (select snd_id from message where recv_id= '" + am + "' group by snd_id ) and status = 'Admitted'"
            mycursor.execute(q2)
            ao = mycursor.fetchall()
            print("a", ao)
            # code user list end
            # code for message start
            request.session['tid'] = a
            q3 = "select snd_id,recv_id,msg,time from message where snd_id= '" + stdnti + "' or snd_id= '" + a + "' and recv_id= '" + a + "' or recv_id= '" + stdnti + "' "
            mycursor.execute(q3)
            abc = mycursor.fetchall()
            print("msg", abc)
            i = int(stdnti)
            o = int(a)
            # code for message end
            # code for userifo start
            qa = "select stdnt_crsname from student where id= '" + stdnti + "'  "
            mycursor.execute(qa)
            ((ak,),) = mycursor.fetchall()
            print("stdnt_crsname", ak)
            qs = "select stdnt_sem from student where id= '" + stdnti + "'  "
            mycursor.execute(qs)
            ((bk,),) = mycursor.fetchall()
            print("stdnt_sem", bk)
            qd = "select pic from student where id= '" + stdnti + "'  "
            mycursor.execute(qd)
            ((p,),) = mycursor.fetchall()
            print("stdnt_sem", p)
            # code for userifo end
            return render(request, 'cmsapp/teacher/interaction.html', {'trpic': tchrp, 'trn': name, 'usrname': ao, 'i': i, 'o': o, 'msg': abc, 'stdntpic': p, 'stdntn': stdntn, 'stdntc': ak, 'stdnts': bk})
    else:
        return render(request, 'cmsapp/teachers_signin.html', {'mes': 'Login to Enter'})


def t_notes(request):
    if 'tchrn' in request.session:
        name = request.session['tchrn']
        e = request.session['tchre']
        tchrp = request.session['tchrp']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        query = "select id, sub, sem, file, details, date from note"
        mycursor.execute(query)
        records = mycursor.fetchall()
        q1 = "select crs from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' )"
        mycursor.execute(q1)
        cr = mycursor.fetchall()
        crs = functools.reduce(operator.add, (cr))
        q2 = "select sub from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' )"
        mycursor.execute(q2)
        su = mycursor.fetchall()
        sub = functools.reduce(operator.add, (su))
        q3 = "select sem from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' )"
        mycursor.execute(q3)
        sm = mycursor.fetchall()
        sem = functools.reduce(operator.add, (sm))
        if mycursor.rowcount == 0:
            return render(request, 'cmsapp/teacher/notes.html', {'trpic': tchrp, 'trn': name, 'crs': crs, 'sub': sub, 'sem': sem})
        else:
            return render(request, 'cmsapp/teacher/notes.html', {'trpic': tchrp, 'records': records, 'trn': name, 'crs': crs, 'sub': sub, 'sem': sem})
    else:
        return render(request, 'cmsapp/teachers_signin.html', {'mes': 'Login to Enter'})


def t_notes_(request):
    if 'tchrn' in request.session:
        if request.method == 'POST' and request.FILES['file']:
            myfile = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            crt = request.POST["crs"]
            s = request.POST["sub"]
            se = request.POST["sem"]
            # c = request.POST["file"]
            d = request.POST["details"]
            # da = request.POST["date"]
            ko = date.today()
            da = ko.strftime("%Y/%m/%d")
            # da = ko
            # print(da)
            name = request.session['tchrn']
            e = request.session['tchre']
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
            mycursor = conn.cursor()
            query = "insert into note (`crs`, `sub`, `sem`, `file`, `details`, `date`) values ('" + crt + "','" + s + "','" + se + "','" + filename + "','" + d + "','" + da + "')"
            mycursor.execute(query)
            conn.commit()
            query = "select id, sub, sem, file, details, date from note"
            mycursor.execute(query)
            records = mycursor.fetchall()
            q1 = "select crs from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' )"
            mycursor.execute(q1)
            cr = mycursor.fetchall()
            crs = functools.reduce(operator.add, (cr))
            q2 = "select sub from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' )"
            mycursor.execute(q2)
            su = mycursor.fetchall()
            sub = functools.reduce(operator.add, (su))
            q3 = "select sem from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' )"
            mycursor.execute(q3)
            sm = mycursor.fetchall()
            sem = functools.reduce(operator.add, (sm))
            if mycursor.rowcount == 0:
                tchrp = request.session['tchrp']
                return render(request, 'cmsapp/teacher/notes.html', {'trpic': tchrp, 'trn': name, 'crs': crs, 'sub': sub, 'sem': sem})
            else:
                messages.success(request, "Notes added successfully.")
                tchrp = request.session['tchrp']
                return render(request, 'cmsapp/teacher/notes.html', {'trpic': tchrp, 'records': records, 'trn': name, 'crs': crs, 'sub': sub, 'sem': sem})
    else:
        return render(request, 'cmsapp/teachers_signin.html', {'mes': 'Login to Enter'})


def t_notes_update(request):
    if 'tchrn' in request.session:
        name = request.session['tchrn']
        e = request.session['tchre']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        query = "select id, sub, sem, file, details, date from note"
        mycursor.execute(query)
        record = mycursor.fetchall()
        q1 = "select crs from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' )"
        mycursor.execute(q1)
        cr = mycursor.fetchall()
        crs = functools.reduce(operator.add, (cr))
        q2 = "select sub from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' )"
        mycursor.execute(q2)
        su = mycursor.fetchall()
        sub = functools.reduce(operator.add, (su))
        q3 = "select sem from subject where teacher in (select id from teacher where tchr_name= '" + name + "' and tchr_email= '" + e + "' )"
        mycursor.execute(q3)
        sm = mycursor.fetchall()
        sem = functools.reduce(operator.add, (sm))
        if request.POST.get('remove'):
            id = request.POST["n_id"]
            print(id)
            query = "delete from note where id =" + id + " "
            mycursor.execute(query)
            conn.commit()
            query1 = "select id, sub, sem, file, details, date from note"
            mycursor.execute(query1)
            records = mycursor.fetchall()
            messages.error(request, "Notes deleted.")
            name = request.session['tchrn']
            tchrp = request.session['tchrp']
            return render(request, 'cmsapp/teacher/notes.html', {'trpic': tchrp, 'records': records, 'trn': name, 'crs': crs, 'sub': sub, 'sem': sem})
        # elif request.POST.get('edit'):
        #     id = request.POST["n_id"]
        #     print(id)
        #     conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        #     mycursor = conn.cursor()
        #     query = "select file, details, date from note"
        #     mycursor.execute(query)
        #     if mycursor.rowcount == 0:
        #         tchrp = request.session['tchrp']
        #         return render(request, 'cmsapp/teacher/notes.html', {'trpic': tchrp, 'trn': name, 'crs': crs, 'sub': sub, 'sem': sem})
        #     else:
        #         record = mycursor.fetchall()
        #         tchrp = request.session['tchrp']
        #         return render(request, 'cmsapp/teacher/notes.html', {'trpic': tchrp, 'record': record, 'trn': name, 'crs': crs, 'sub': sub, 'sem': sem})
    else:
        return render(request, 'cmsapp/teachers_signin.html', {'mes': 'Login to Enter'})


def t_plist(request):
    if 'tchrn' in request.session:
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        query = "select id,prnt_name, prnt_address, prnt_phone, prnt_email, stdnt_name,status from parents"
        mycursor.execute(query)
        if mycursor.rowcount == 0:
            name = request.session['tchrn']
            tchrp = request.session['tchrp']
            return render(request, 'cmsapp/teacher/parent_list.html', {'trpic': tchrp, 'trn': name})
        else:
            records = mycursor.fetchall()
            name = request.session['tchrn']
            tchrp = request.session['tchrp']
            return render(request, 'cmsapp/teacher/parent_list.html', {'trpic': tchrp, 'records': records, 'trn': name})
    else:
        return render(request, 'cmsapp/teachers_signin.html', {'mes': 'Login to Enter'})


def parent_approve(request):
    if 'tchrn' in request.session:
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        id = request.POST["p_id"]
        s = "Admitted"
        s1 = "Denied"

        if request.method == 'POST':
            if request.POST.get("status"):
                query = "update parents set status ='" + s + "' where id =" + id + " "
                mycursor.execute(query)
                conn.commit()
                query1 = "select id,prnt_name, prnt_address, prnt_phone, prnt_email, stdnt_name,status from parents"
                mycursor.execute(query1)
                records = mycursor.fetchall()
                messages.success(request, "Admitted.")
                name = request.session['tchrn']
                tchrp = request.session['tchrp']
                return render(request, 'cmsapp/teacher/parent_list.html', {'trpic': tchrp, 'records': records, 'trn': name})
            elif request.POST.get("status1"):
                query = "update parents set status ='" + s1 + "' where id =" + id + " "
                mycursor.execute(query)
                conn.commit()
                query1 = "select id,prnt_name, prnt_address, prnt_phone, prnt_email, stdnt_name,status from parents"
                mycursor.execute(query1)
                records = mycursor.fetchall()
                messages.error(request, "Denied.")
                name = request.session['tchrn']
                tchrp = request.session['tchrp']
                return render(request, 'cmsapp/teacher/parent_list.html', {'trpic': tchrp, 'records': records, 'trn': name})

        name = request.session['tchrn']
        tchrp = request.session['tchrp']
        return render(request, 'cmsapp/teacher/parent_list.html', {'trpic': tchrp, 'trn': name})
    else:
        return render(request, 'cmsapp/teachers_signin.html', {'mes': 'Login to Enter'})


def t_profile(request):
    if 'tchrn' in request.session:
        name = request.session['tchrn']
        e = request.session['tchre']
        tchrp = request.session['tchrp']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        m = "select tchr_name, tchr_address, tchr_phone, tchr_email, tchr_dept from teacher where  tchr_email = '" + e + "' and  tchr_name = '" + name + "' "
        mycursor.execute(m)
        records = mycursor.fetchall()
        t = "select pic from teacher where  tchr_email = '" + e + "' and  tchr_name = '" + name + "' "
        mycursor.execute(t)
        ((v,),) = mycursor.fetchall()
        return render(request, 'cmsapp/teacher/profile.html', {'trpic': tchrp, 'userinfo': records, 'trn': name, 'userpic': v})
    else:
        return render(request, 'cmsapp/teachers_signin.html', {'mes': 'Login to Enter'})


def t_pic(request):
    if 'tchrn' in request.session:
        if request.method == 'POST' and request.FILES['tpic']:
            myfile = request.FILES['tpic']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            #p = request.POST["img"]
            name = request.session['tchrn']
            e = request.session['tchre']
            tchrp = request.session['tchrp']
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
            mycursor = conn.cursor()
            request.session['tchrp'] = uploaded_file_url
            t = "update teacher set pic ='" + uploaded_file_url + "' where  tchr_email = '" + e + "' and  tchr_name = '" + name + "' "
            mycursor.execute(t)
            conn.commit()
            m = "select tchr_name, tchr_address, tchr_phone, tchr_email, tchr_dept from teacher where  tchr_email = '" + e + "' and  tchr_name = '" + name + "' "
            mycursor.execute(m)
            records = mycursor.fetchall()
            t = "select pic from teacher where  tchr_email = '" + e + "' and  tchr_name = '" + name + "' "
            mycursor.execute(t)
            ((v,),) = mycursor.fetchall()
            return render(request, 'cmsapp/teacher/profile.html', {'trpic': tchrp, 'userinfo': records, 'trn': name, 'userpic': v})
    else:
        return render(request, 'cmsapp/teachers_signin.html', {'mes': 'Login to Enter'})


def t_sdetail(request):
    if 'tchrn' in request.session:
        name = request.session['tchrn']
        tchrp = request.session['tchrp']
        return render(request, 'cmsapp/teacher/student_detail.html', {'trpic': tchrp, 'trn': name})
    else:
        return render(request, 'cmsapp/teachers_signin.html', {'mes': 'Login to Enter'})


def t_sfee(request):
    if 'tchrn' in request.session:
        #return render(request, 'cmsapp/teacher/student_fee.html')
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        query = "select stdnt_name, crs, sem, adm_no, status from payment"
        mycursor.execute(query)
        if mycursor.rowcount == 0:
            name = request.session['tchrn']
            tchrp = request.session['tchrp']
            return render(request, 'cmsapp/teacher/student_fee.html', {'trpic': tchrp, 'trn': name})
        else:
            records = mycursor.fetchall()
            name = request.session['tchrn']
            tchrp = request.session['tchrp']
            return render(request, 'cmsapp/teacher/student_fee.html', {'trpic': tchrp, 'records': records, 'trn': name})
    else:
        return render(request, 'cmsapp/teachers_signin.html', {'mes': 'Login to Enter'})


def t_slist(request):
    if 'tchrn' in request.session:
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        query = "select id, stdnt_name, stdnt_crsname, stdnt_adm, stdnt_sem, status from student"
        mycursor.execute(query)
        if mycursor.rowcount == 0:
            name = request.session['tchrn']
            tchrp = request.session['tchrp']
            return render(request, 'cmsapp/teacher/student_list.html', {'trpic': tchrp, 'mes': 'no courses found', 'trn': name})
        else:
            records = mycursor.fetchall()
            name = request.session['tchrn']
            tchrp = request.session['tchrp']
            return render(request, 'cmsapp/teacher/student_list.html', {'trpic': tchrp, 'records': records, 'trn': name})
    else:
        return render(request, 'cmsapp/teachers_signin.html', {'mes': 'Login to Enter'})


def tstudent_approve(request):
    if 'tchrn' in request.session:
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        id = request.POST["s_id"]
        s = "Admitted"
        s1 = "Denied"
        tchrp = request.session['tchrp']

        if request.method == 'POST':
            if request.POST.get("status"):
                query = "update student set status ='" + s + "' where id =" + id + " "
                mycursor.execute(query)
                conn.commit()
                query1 = "select id, stdnt_name, stdnt_crsname, stdnt_adm, stdnt_sem, status from student"
                mycursor.execute(query1)
                records = mycursor.fetchall()
                messages.success(request, "Approved.")
                name = request.session['tchrn']
                return render(request, 'cmsapp/teacher/student_list.html', {'trpic': tchrp, 'records': records, 'trn': name})

            elif request.POST.get("status1"):
                query = "update student set status ='" + s1 + "' where id =" + id + " "
                mycursor.execute(query)
                conn.commit()
                query1 = "select id, stdnt_name, stdnt_crsname, stdnt_adm, stdnt_sem, status from student"
                mycursor.execute(query1)
                records = mycursor.fetchall()
                messages.error(request, "Denied.")
                name = request.session['tchrn']
                return render(request, 'cmsapp/teacher/student_list.html', {'trpic': tchrp, 'records': records, 'trn': name})

        name = request.session['tchrn']
        return render(request, 'cmsapp/teacher/student_list.html', {'trpic': tchrp, 'trn': name})
    else:
        return render(request, 'cmsapp/teachers_signin.html', {'mes': 'Login to Enter'})



# admin_login
def admin_login(request):
    if request.method == "POST":
        username = request.POST["email"]
        password = request.POST["password"]
        print(username + password)
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        query = "select * from admin where username='" + username + "' and password='" + password + "' "
        mycursor.execute(query)
        mycursor.fetchall()
        print(mycursor.rowcount)
        if mycursor.rowcount == 0:
            name = request.session['tchrn']
            messages.error(request, "invalid username and password.")
            return render(request, 'cmsapp/admin_login.html')
        else:
            return render(request, 'cmsapp/admin/index.html')


# teacher_login
def teachers_signups(request):
    if request.method == 'POST':
        tchr_name = request.POST["name"]
        tchr_address = request.POST["address"]
        tchr_phone = request.POST["phone"]
        tchr_email = request.POST["email"]
        tchr_dept = request.POST["department"]
        tchr_pass = request.POST["password"]
        status = "Pending"
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        query = "insert into teacher (`tchr_name`, `tchr_address`, `tchr_phone`, `tchr_email`, `tchr_dept`, `tchr_pass`, `status`) values ('" + tchr_name + "','" + tchr_address + "','" + tchr_phone + "','" + tchr_email + "','" + tchr_dept + "','" + tchr_pass + "','" + status + "')"
        mycursor.execute(query)
        conn.commit()
        return render(request, 'cmsapp/wait.html', {'mes': 'account created successfully'})


def teachers_login(request):
    if request.method == "POST":
        e = request.POST["email"]
        p = request.POST["password"]
        status = "Admitted"
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        query = "select * from teacher where tchr_email='" + e + "' and tchr_pass='" + p + "' "
        mycursor.execute(query)
        mycursor.fetchall()
        print(mycursor.rowcount)
        if mycursor.rowcount == 0:
            return render(request, 'cmsapp/teachers_signin.html', {'mes': 'invalid username or password'})
        else:
            query1 = "select * from teacher where tchr_email='" + e + "' and tchr_pass='" + p + "' and status='" + status + "' "
            mycursor.execute(query1)
            mycursor.fetchall()
            print(mycursor.rowcount)
            if mycursor.rowcount == 0:
                return render(request, 'cmsapp/wait_login.html')
            else:
                query1 = "select tchr_name from teacher where tchr_email='" + e + "' and tchr_pass='" + p + "' "
                mycursor.execute(query1)
                r = (mycursor.fetchone()[0])
                login_required()
                #request.session['username'] = r
                query2 = "select tchr_email from teacher where tchr_email='" + e + "' and tchr_pass='" + p + "'  "
                mycursor.execute(query2)
                i = (mycursor.fetchone()[0])
                q2 = "select id from teacher where tchr_email='" + e + "' and tchr_pass='" + p + "'  "
                mycursor.execute(q2)
                rtr = (mycursor.fetchone()[0])
                rr = str(rtr)
                q4 = "select pic from teacher where tchr_email='" + e + "' and tchr_pass='" + p + "'  "
                mycursor.execute(q4)
                ro = (mycursor.fetchone()[0])
                query3 = "select sub from subject where teacher ='" + rr + "'"
                mycursor.execute(query3)
                sub = (mycursor.fetchone()[0])
                login_required()
                request.session['tchrn'] = r
                request.session['tchre'] = i
                request.session['tchrp'] = ro
                request.session['tchrs'] = sub
                #print(r, i)
                return render(request, 'cmsapp/teacher/index.html', {'trn': r, 'trpic': ro})


# parent_login
def parent_(request):
    if request.method == 'POST':
        u = request.POST["name"]
        t = request.POST["address"]
        r = request.POST["father"]
        s = request.POST["admission"]
        k = request.POST["phone"]
        l = request.POST["email"]
        q = request.POST["password"]
        status = "Pending"
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        query = "insert into parents (`prnt_name`, `prnt_address`,`stdnt_name`, `stdnt_admno`, `prnt_phone`, `prnt_email`, `prnt_pass`, `status`) values ('" + u + "','" + t + "','" + k + "','" + l + "','" + r + "','" + s + "','" + q + "','" + status + "')"
        mycursor.execute(query)
        conn.commit()
        return render(request, 'cmsapp/wait.html', {'mes': 'account created successfully'})


def parent_login(request):
    if request.method == "POST":
        t1 = request.POST["email"]
        r1 = request.POST["password"]
        status = "Admitted"
        print(t1 + r1)
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        query = "select * from parents where prnt_email='" + t1 + "' and prnt_pass='" + r1 + "' "
        mycursor.execute(query)
        mycursor.fetchall()
        print(mycursor.rowcount)
        if mycursor.rowcount == 0:
            messages.warning(request, " invalid username or password ")
            return render(request, 'cmsapp/parent_signin.html', {'mes': 'invalid username and password'})
        else:
            query1 = "select * from parents where prnt_email='" + t1 + "' and prnt_pass='" + r1 + "' and status='" + status + "' "
            mycursor.execute(query1)
            mycursor.fetchall()
            query2 = "select stdnt_admno from parents where prnt_email='" + t1 + "' and prnt_pass='" + r1 + "' and status='" + status + "' "
            mycursor.execute(query2)
            adm = mycursor.fetchone()
            query3 = "select prnt_name from parents where prnt_email='" + t1 + "' and prnt_pass='" + r1 + "' and status='" + status + "' "
            mycursor.execute(query3)
            nm = mycursor.fetchone()
            request.session['sadmno'] = adm
            request.session['pnam'] = nm
            if mycursor.rowcount == 0:
                return render(request, 'cmsapp/wait_login.html')
            else:
                return render(request, 'cmsapp/parent/index.html')


# student signup
def student(request):
    if request.method == 'POST':
        n = request.POST["name"]
        a = request.POST["address"]
        f = request.POST["fname"]
        m = request.POST["mname"]
        p = request.POST["phone"]
        e = request.POST["email"]
        c = request.POST["course"]
        s = request.POST["sem"]
        pas = request.POST["password"]
        adm = request.POST["adm"]
        status = "Pending"
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        query = "insert into student (`stdnt_name`, `stdnt_address`, `stdnt_faname`, `stdnt_moname`, `stdnt_phone`, `stdnt_email`, `stdnt_crsname`, `stdnt_sem`, `stdnt_pass`, `stdnt_adm`, `status`) values ('" + n + "','" + a + "','" + p + "','" + e + "','" + f + "','" + m + "','" + c + "','" + s + "','" + pas + "','" + adm + "','" + status + "')"
        mycursor.execute(query)
        conn.commit()
        return render(request, 'cmsapp/wait.html', {'mes': 'account created successfully'})


# student login

def student_(request):
    if request.method == "POST":
        e = request.POST["email"]
        p = request.POST["password"]
        status = "Admitted"
        #print(e + p)
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
        mycursor = conn.cursor()
        query = "select * from student where stdnt_email='" + e + "' and stdnt_pass='" + p + "'  "
        mycursor.execute(query)
        mycursor.fetchall()
        if mycursor.rowcount == 0:
            messages.warning(request, " invalid username or password ")
            return render(request, 'cmsapp/student_login.html', {'mes': 'invalid username or password'})
        else:
            query1 = "select * from student where stdnt_email='" + e + "' and stdnt_pass='" + p + "' and status='" + status + "' "
            mycursor.execute(query1)
            mycursor.fetchall()
            if mycursor.rowcount == 0:
                return render(request, 'cmsapp/wait_login.html')
            else:
                query1 = "select stdnt_name from student where stdnt_email='" + e + "' and stdnt_pass='" + p + "' "
                mycursor.execute(query1)
                r = (mycursor.fetchone()[0])
                login_required()
                #request.session['username'] = r
                query2 = "select stdnt_email from student where stdnt_email='" + e + "' and stdnt_pass='" + p + "' "
                mycursor.execute(query2)
                i = (mycursor.fetchone()[0])
                query3 = "select id from student where stdnt_email='" + e + "' and stdnt_pass='" + p + "' "
                mycursor.execute(query3)
                o = (mycursor.fetchone()[0])
                login_required()
                query3 = "select pic from student where stdnt_email='" + e + "' and stdnt_pass='" + p + "' "
                mycursor.execute(query3)
                sp = (mycursor.fetchone()[0])
                request.session['username'] = r
                request.session['usremail'] = i
                request.session['usreid'] = o
                request.session['usrep'] = sp
                #print(r, i)
                if'nam' in request.POST:
                    return redirect(request.POST['nam'])
                return render(request, 'cmsapp/student/index.html', {'nam': r, 'spic': sp})




#logout for student
def out(request):
    request.session.flush()
    request.session.flush()
    cache.clear()
    return render(request, 'cmsapp/index.html')


#logout for teacher
def tout(request):
    del request.session['tchrn']
    del request.session['tchre']
    request.session.flush()
    cache.clear()
    return render(request, 'cmsapp/index.html')


#logout for parent
def pout(request):
    del request.session['sadmno']
    del request.session['pnam']
    request.session.flush()
    cache.clear()
    return render(request, 'cmsapp/index.html')

