from django import template
import mysql.connector
import functools
import operator
from datetime import date

register = template.Library()

@register.simple_tag
def my_tag():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='cms_database')
    mycursor = conn.cursor()
    query = "select crs_name from course"
    mycursor.execute(query)
    records = mycursor.fetchall()
    d = functools.reduce(operator.add, (records))
    return d

@register.simple_tag()
def tr(request):
    return {'session': request.session}
