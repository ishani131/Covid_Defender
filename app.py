from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from COVID import get_values
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resource.db'
app.config['SQLALCHEMY_BINDS'] = {
    'links' : 'sqlite:///links.db',
    'comments' : 'sqlite:///comments.db'
}

db = SQLAlchemy(app)

class Data(db.Model):
    contact = db.Column(db.Integer, primary_key = True)
    city = db.Column(db.String(25), nullable = False)
    description = db.Column(db.Text, nullable = False)
    supply = db.Column(db.String(100), nullable = False)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return 'New Dataset created :' + str(self.supply)



class Links(db.Model):
    __bind_key__ = 'links'
    links = db.Column(db.Text, primary_key = True)
    description = db.Column(db.Text, nullable = False,default ='N/A')

    def __repr__(self):
        return 'New link created : ' + self.links


class Comments(db.Model):
    __bind_key__ = 'comments'
    username = db.Column(db.String(20),primary_key = True)
    comment = db.Column(db.Text, nullable = False , default = 'Nothing to say...')

    def __repr__(self):
        return 'New comment added by : ' + str(self.username)


data = get_values()
@app.route("/",methods = ['GET',"POST"])
def route1():
    global data
    return render_template("home.html", data = data)


@app.route("/stateData", methods = ['GET', 'POST'])
def route2():
    stats = {'region': '', 'totalInfected': '', 'newInfected': '', 'recovered': '', 'newRecovered': '', 'deceased': '', 'newDeceased': ''}
    if request.method == 'POST':
        global data
        req = request.form['state']
        for region in get_values()['regionData']:
            if region['region'] == req :
                stats = region
                return render_template("stateData.html", data = stats)


    return render_template("stateData.html", data = stats)


@app.route("/resources",methods = ['GET','POST'])
def route3():
    if request.method == 'POST':
        req = request.form
        links = req['links']
        description = req['description']
        newdata = Links(links = links,description = description)
        db.session.add(newdata)
        db.session.commit()
        return redirect("/resources")
    else:
        all_posts = Links.query.all()
        return render_template("resources.html", data = all_posts)

@app.route("/database",methods = ['GET',"POST"])
def route4():
    if request.method == 'POST' :
        req = request.form
        contact = req['contact']
        city = req['city']
        description = req['description']
        supply = req['supply']
        newdata = Data(contact = contact, city = city, description = description, supply = supply)
        db.session.add(newdata)
        db.session.commit()
        return redirect('/database')
    else:
        all_posts = Data.query.order_by(Data.supply).all()
        
        return render_template("database.html", data = all_posts)
@app.route("/comments" ,  methods = ['GET','POST'])
def route5():
    if request.method == 'POST':
        req = request.form
        username = req['username']
        comment = req['comment']
        newdata = Comments(username = username , comment = comment)
        db.session.add(newdata)
        db.session.commit()
        return redirect('/comments')
    else:
        all_posts = Comments.query.all()
        return render_template("comments.html", data = all_posts)
    
if __name__ == "__main__":
    app.run(debug = True)

           