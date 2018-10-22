from flask import (
    Blueprint,
    render_template,
    flash,
    abort,
    current_app,
    redirect, request, url_for)

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models.abitur_inf import db, Abitur_inf

import psycopg2


def getInf():
    try:
        conn = psycopg2.connect(dbname='abit', password='123', user='postgres')
        cur = conn.cursor()
        cur.execute("""
        SELECT i.id_user, i.political, i.alcohol, i.religion, i.smoking, i.life_main, i.people_main, i.sex, i.id_faculty, f.id_side
	FROM public.faculty as f
	JOIN informations as i on i.id_faculty=f.id
	Where f.id_side<4 and (case when political = '' then 0 else 1 end+
case when alcohol = '' then 0 else 1 end+
case when people_main = '' then 0 else 1 end+
case when life_main = '' then 0 else 1 end+
case when smoking = '' then 0 else 1 end+
case when religion = '' then 0 else 1 end+
case when sex is null then 0 else 1 end) > 5""")

        train_data = []
        test_data = []
        train_labels = []
        test_labels = []
        id_user = []

        quer = cur.fetchall()
        print(len(quer))
        for i in quer:
            political = 0
            alcohol = 0
            religion = 0
            smoking = 0
            life_main = 0
            people_main = 0

            if i[1] == '':
                political = 0
            elif i[2] == '':
                alcohol = 0
            elif i[4] == '':
                smoking = 0
            elif i[5] == '':
                life_main = 0
            elif i[6] == '':
                people_main = 0

            if i[3] == "":
                religion = 0;
            elif i[3] == "Иудаизм":
                religion = 1;
            elif i[3] == "Православие":
                religion = 2;
            elif i[3] == "Католицизм":
                religion = 3;
            elif i[3] == "Протестантизм":
                religion = 4;
            elif i[3] == "Ислам":
                religion = 5;
            elif i[3] == "Буддизм":
                religion = 6;
            elif i[3] == "Конфуцианство":
                religion = 7;
            elif i[3] == "Светский гуманизм":
                religion = 8;
            elif i[3] == "Пастафарианство":
                religion = 9;
            else:
                religion = 10;
            print(religion)
            id_user.append(int(i[0]))
            train_data.append(
                [int(political), int(alcohol), int(religion), int(smoking), int(life_main), int(people_main),
                 int(i[7])])
            train_labels.append(int(i[9]))
            print(i)

    except Exception as e:
        print('ERRORRRR', e)
        flash('There was error while querying database', 'danger')
        abort(500)
    print(id_user)
    print(train_labels)
    print(train_data)
    return True
