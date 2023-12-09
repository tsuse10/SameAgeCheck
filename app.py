from flask import Flask,render_template,request,redirect
import wikipedia
import os
import re
import datetime
from datetime import datetime


app = Flask(__name__)

wikipedia.set_lang('ja')
today = datetime.today()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result1' ,methods=["POST"])
def celebrities_result():
    if request.method == "POST":
        cbr_name1 = request.form['name1']
        cbr_name2 = request.form['name2']

        try:
            page1 = wikipedia.page(cbr_name1)
            page2= wikipedia.page(cbr_name2)
        except Exception as de:
            suggest = re.findall(r'may refer to:\s*(.*)\s*(.*)\s*(.*)',str(de)) 
            dict = {
                "candidate1" : suggest[0][0],
                "candidate2" : suggest[0][1],
                "candidate3" : suggest[0][2],    
            }
            return render_template('suggestion.html',dict = dict)
        
        bd_list1 = re.findall('(\d{1,4})年.*?(\d{1,2})月(\d{1,2})日', page1.summary)
        bd_list2 = re.findall('(\d{1,4})年.*?(\d{1,2})月(\d{1,2})日', page2.summary)
        bd_str1 = bd_list1[0][0] + '年' + bd_list1[0][1] + '月' + bd_list1[0][2] + '日'
        bd_str2 = bd_list2[0][0] + '年' + bd_list2[0][1] + '月' + bd_list2[0][2] + '日'

        bd1_date = datetime.strptime(bd_str1,"%Y年%m月%d日")
        bd2_date = datetime.strptime(bd_str2,"%Y年%m月%d日")
        age1 = (int(today.strftime("%Y%m%d")) - int(bd1_date.strftime("%Y%m%d"))) // 10000
        age2 = (int(today.strftime("%Y%m%d")) - int(bd2_date.strftime("%Y%m%d"))) // 10000

        images1 = []
        found = False
        for image in page1.images:
            if os.path.splitext(image)[1][1:] in 'jpg':
                found = True
                images1.append(image)
                continue
        if not found:
            print('画像が見つかりませんでした')
        
        images2 = []
        found = False
        for image in page2.images:
            if os.path.splitext(image)[1][1:] in 'jpg':
                found = True
                images2.append(image)
                continue
        if not found:
            print('画像が見つかりませんでした')

        dict = {
            "cbr_name1":cbr_name1,
            "cbr_name2":cbr_name2,
            "birthday1":bd_str1,
            "birthday2":bd_str2,
            "year1":bd_list1[0][0],
            "month1":bd_list1[0][1],
            "year2":bd_list2[0][0],
            "month2":bd_list2[0][1],
            "age1":age1,
            "age2":age2,
            "images1":images1,
            "images2":images2,
        }
    return render_template('result1.html',dict=dict)


@app.route('/result2' ,methods=["POST"])
def user_result():
    if request.method == "POST":
        cbr_name = request.form['name3']
        user_year = request.form['year']
        user_month = request.form['month']
        user_day = request.form['day']


        page1 = wikipedia.page(cbr_name)
        cbr_bd_list = re.findall('(\d{4})年.*?(\d{1,2})月(\d{1,2})日', page1.summary)
        cbr_bd_str = cbr_bd_list[0][0] + '年' + cbr_bd_list[0][1] + '月' + cbr_bd_list[0][2] + '日'
        cbr_bd_date = datetime.strptime(cbr_bd_str,"%Y年%m月%d日")
        cbr_age = (int(today.strftime("%Y%m%d")) - int(cbr_bd_date.strftime("%Y%m%d"))) // 10000

        user_birthday = user_year + user_month + user_day
        user_bd_list = re.findall("(\d{4})年(\d{1,2})月(\d{1,2})日",user_birthday)
        user_bd_date = datetime.strptime(user_birthday,"%Y年%m月%d日")
        user_age = (int(today.strftime("%Y%m%d")) - int(user_bd_date.strftime("%Y%m%d"))) // 10000

        dict = {
                "cbr_name":cbr_name,
                "cbr_birthday":cbr_bd_str,
                "cbr_year":cbr_bd_list[0][0],
                "cbr_month":cbr_bd_list[0][1],
                "cbr_age":cbr_age,
                "user_birthday":user_birthday,
                "user_year":user_bd_list[0][0],
                "user_month":user_bd_list[0][1],
                "user_age":user_age,
                }
        
    return render_template('result2.html',dict=dict)

if __name__ == '__main__':
    app.run()


