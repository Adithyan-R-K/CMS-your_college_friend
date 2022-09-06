"""cmsproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = {
    path('', views.index, name='homepage'),
    path('admin', views.admin, name='admin'),
    path('alogin', views.admin_login, name='admin'),
    path('parent', views.parent_signin, name='parent'),
    path('plogin', views.parent_login, name='parent'),
    path('parent_', views.parent_signup, name='parents'),
    path('parents', views.parent_, name='parents'),
    path('student', views.student_login, name='student'),
    path('students', views.student, name='student'),
    path('students_', views.student_, name='student'),
    path('success', views.success, name='success'),
    path('teachers', views.teachers_signin, name='teacher'),
    path('teacher_login', views.teachers_login, name='teacher'),
    path('teachers_', views.teachers_signup, name='teachers'),
    path('teachers_signup', views.teachers_signups, name='teachers'),
    path('wait', views.wait, name='wait'),
    path('wait_login', views.wait_login, name='wait'),
    path('index', views.index, name='homepage'),

    #admin dashboard
    path('a_index', views.a_index, name='admin_index'),
    path('add_fee', views.add_fee, name='add_fee'),
    path('add_fee_', views.add_fee_, name='added_fee'),
    path('courses', views.courses, name='course'),
    path('courses_', views.courses_, name='added_course'),
    path('courses_update', views.courses_update, name='delete_course'),
    path('a_profile', views.a_profile, name='admin_index'),
    path('student_detail', views.student_details, name='student_details'),
    path('student_fee', views.student_fee, name='student_fee'),
    path('student_list', views.student_list, name='student_list'),
    path('student_approve', views.student_approve, name='student_approve'),
    path('subject', views.subject, name='sub'),
    path('add_subject', views.add_subject, name='Add sub'),
    path('sub_update', views.sub_update, name='Update sub'),
    path('s_update', views.s_update, name='Update'),
    path('teacher_list', views.teacher_list, name='teacher_list'),
    path('teacher_approve', views.teacher_approve, name='teacher_approve'),

    #parent dashboard
    path('p_index', views.p_index, name='parent_index'),
    path('p_fee', views.p_fee, name='fee'),
    path('p_interaction', views.p_interaction, name='interaction'),
    path('p_payment', views.p_payment, name='payment'),
    path('p_payment_', views.p_payment_, name='payment'),
    path('p_profile', views.p_profile, name='profile'),
    path('s_pic', views.s_pic, name='pic'),
    path('p_result', views.p_result, name='result'),
    path('p_uexam', views.p_uexam, name='uexam_result'),
    path('pout', views.pout, name='parent log out'),

    #student dashboard
    path('s_index', views.s_index, name='student_index'),
    path('s_exam', views.s_exam, name='exam'),
    path('s_exam_update', views.s_exam_update, name='upload answer exam'),
    path('s_exam_answer', views.s_exam_answer, name='upload'),
    path('s_interaction', views.s_interaction, name='interaction'),
    path('s_inter', views.s_inter, name='select user'),
    path('s_send', views.s_send, name='send message'),
    path('s_notes', views.s_notes, name='notes'),
    path('s_profile', views.s_profile, name='profile'),
    path('s_result', views.s_result, name='result'),
    path('s_fee', views.s_fee, name='fee'),
    path('s_teachers', views.s_teachers, name='teachers'),
    path('s_tinfo', views.s_tinfo, name='s_tdetails'),
    path('s_tdetail', views.s_tdetail, name='student_detail'),
    path('s_uexam', views.s_uexam, name='uexam_result'),
    path('logout', views.out, name='logged_out_successfully'),

    #teacher dashboard
    path('t_index', views.t_index, name='teacher_index'),
    path('t_courses', views.t_courses, name='courses'),
    path('t_exam', views.t_exam, name='exam'),
    path('t_exam_', views.t_exam_, name='exam'),
    path('viewpdf', views.viewpdf, name='pdf'),
    path('t_exam_update', views.t_exam_update, name='update_exam'),
    path('t_interaction', views.t_interaction, name='interaction'),
    path('t_inter', views.t_inter, name='select user'),
    path('t_send', views.t_send, name='send message'),
    path('t_notes', views.t_notes, name='notes'),
    path('t_notes_', views.t_notes_, name='added_notes'),
    path('t_notes_update', views.t_notes_update, name='update_notes'),
    path('t_plist', views.t_plist, name='parents_list'),
    path('parent_approve', views.parent_approve, name='parent_approve'),
    path('t_profile', views.t_profile, name='profile'),
    path('t_pic', views.t_pic, name='update pic'),
    path('t_sdetail', views.t_sdetail, name='student_detail'),
    path('tstudent_approve', views.tstudent_approve, name='student_detail'),
    path('t_sfee', views.t_sfee, name='student_fee'),
    path('t_slist', views.t_slist, name='student_list'),
    path('tout', views.tout, name='index'),


}
