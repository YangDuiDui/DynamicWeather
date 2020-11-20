from flask import Flask, render_template, redirect, url_for, request,session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, inputs
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
api = Api(app)
    # Grade 类名一般和表名一样，不过要大写

class Data_weather(db.Model):
    # grade 是表名
    __tablename__ = "data_weather"

    # 参数1:表示整数类型,  参数2:表示主键
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    ymd = db.Column(db.String(50), nullable=False)
    tianqi = db.Column(db.String(50), nullable=False)
    bWendu = db.Column(db.String(50), nullable=False)
    yWendu = db.Column(db.String(50), nullable=False)
    fenli = db.Column(db.String(50), nullable=False)
    fenxiang = db.Column(db.String(50), nullable=False)
    yer = db.Column(db.String(50), nullable=False)
    month = db.Column(db.String(50), nullable=False)


# result = db.session.query(Data_weather).filter(Data_weather.city == '咸阳',Data_weather.yer == '2018',Data_weather.month == '09').all()
#
# weather_list = []
# for i in range(len(result)):
#     weather_list.append(
#         {'id': result[i].id, 'city': result[i].city, 'ymd': result[i].ymd, 'tianqi': result[i].tianqi,
#          'bWendu': result[i].bWendu, 'yWendu': result[i].yWendu, 'fenli': result[i].fenli,
#          'fenxiang': result[i].fenxiang, 'yer': result[i].yer, 'month': result[i].month})
#
# print("当月天气的列表:", weather_list)


@app.route("/")
def index():
    # 查询地方
    city = list(set(db.session.query(Data_weather.city).filter().all()))
    li = []
    for i in city:
        j = str(i)
        m = j.replace("('","").replace("',)","")
        li.append({'city':m})
    # print("第一个页面的访问数据: ",li)
    return render_template("index.html", results=li)


class LoginView(Resource):
    address = '咸阳'
    year = '2017'
    months = '11'

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("address",required=True)
        parser.add_argument("year",required=True)
        parser.add_argument("months",required=True)

        args = parser.parse_args()
        address = args.get("address")
        year = args.get("year")
        months = args.get("months")
        print(address, year, months)

        result = db.session.query(Data_weather).filter(Data_weather.city == address,Data_weather.yer == year,Data_weather.month == months).all()

        weather_list = []
        for i in range(len(result)):
            weather_list.append(
                {'id': result[i].id, 'city': result[i].city, 'ymd': result[i].ymd, 'tianqi': result[i].tianqi,
                 'bWendu': result[i].bWendu, 'yWendu': result[i].yWendu, 'fenli': result[i].fenli,
                 'fenxiang': result[i].fenxiang, 'yer': result[i].yer, 'month': result[i].month})

        print("当月天气的列表:", weather_list)
        return {"weather_list": weather_list}

api.add_resource(LoginView, "/login/")

if __name__ == '__main__':


    app.run(debug=True)
