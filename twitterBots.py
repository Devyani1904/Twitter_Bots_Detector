from flask import Flask, render_template, url_for, flash, redirect, request
from forms import FindUserForm
from flask_mysqldb import MySQLdb
import Functions
import tweepy
from tweepy import TweepError
app = Flask(__name__)
app.config['SECRET_KEY'] = 'c3bd296c9264bc0c857cc7c18cac762a'


@app.route("/home", methods=['GET', 'POST'])
def home():
    form = FindUserForm()
    if form.is_submitted():
        try:
            Functions.submitUser(form.username.data)
            return redirect(url_for('userInfo', userName=form.username.data))
        except tweepy.error.TweepError:
            flash(f'User {form.username.data} was nof found!', 'danger')
    return render_template('home.html', form=form)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/team")
def team():
    return render_template('team.html', title='Team')

@app.route("/userInfo", methods=['GET', 'POST'])
def userInfo():
    userName = request.args.get('userName')
    if userName[0] == "@":
        userName = userName[1:]
    UserInfo = Functions.getUserInfo(userName)
    if UserInfo != None:
        flash(f'Searched user {userName} successfully!', 'success')
        Functions.deleteMatrixInfo(userName)
        Functions.insertMatrixInfo(userName)
        PercentagesInfo = Functions.getPercentagesInfo(userName)
        GenuineInfo = Functions.getFollowersExampleInfo(userName, "genuine")
        SuspiciousInfo = Functions.getFollowersExampleInfo(userName, "suspicious")
        BotsInfo = Functions.getFollowersExampleInfo(userName, "bot")
    else:
        flash(f'User {userName} was nof found!', 'danger')
        PercentagesInfo = None
        GenuineInfo = None
        SuspiciousInfo = None
        BotsInfo = None

    return render_template('userInfo.html', title='User Info', userInfo=UserInfo, percentagesInfo=PercentagesInfo, genuineInfo=GenuineInfo, suspiciousInfo=SuspiciousInfo, botsInfo=BotsInfo)


if __name__ == '__main__':
    app.run(debug=True)
