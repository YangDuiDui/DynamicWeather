from flask import Flask, url_for, render_template
from flask_restful import Api, Resource, reqparse, inputs
import pymysql

app = Flask(__name__)
api = Api(app)


db = pymysql.connect("localhost","root","123456","weather")

cursor = db.cursor(pymysql.cursors.DictCursor)

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
        sql = "SELECT * FROM APP_weather WHERE city='{}' and yer='{}' and month='{}'".format(address, year, months)
        # sql = "DESC APP_weather"
        print(sql)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            print("当月天气的列表:",results)
            return {"weather_list":results}
        except:
            import traceback  # 打印出报错具体信息
            traceback.print_exc()
            return "Error: unable to fetch data"

api.add_resource(LoginView, "/login/")

@app.route('/')
def hello_world():
    try:
        sql = "SELECT DISTINCT city FROM APP_weather;"
        # sql = "DESC APP_weather"
        cursor.execute(sql)
        results = cursor.fetchall()
        print("第一个页面的访问数据:",results)
        return render_template("index.html", results=results)
    except:
        import traceback  # 打印出报错具体信息
        traceback.print_exc()
        return "没有当天气"
    # return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=8887)