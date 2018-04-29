# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]

# [START imports]
from flask import Flask, render_template, request, abort
from models import Judge, Score, Team, Category
from static_data import SUPERUSER_EMAIL
import logging
import models
from google.appengine.api import users

# [END imports]

# [START create_app]
app = Flask(__name__)
# [END create_app]

# [START login]
@app.route('/login', methods=['POST', 'GET'])
def login_form():
  user = users.get_current_user()
  if user:
    auth_url = users.create_logout_url('/')
    auth_action = "logout {}".format(user.nickname())
  else:
    auth_url = users.create_login_url('/')
    auth_action = "login"
  return render_template('login.html',
    auth_url=auth_url,
    auth_action=auth_action)
# [END login]

# [START start]
@app.route('/user', methods=['POST', 'GET'])
@app.route('/')
def user_form():
  user = users.get_current_user()
  if not user:
    flask.redirect("/login")
  print("user {}".format(user))
  admin = "N/A"
  if user:
    if users.is_current_user_admin():
      print("You are an administrator.")
      admin = "yes"
    else:
      print("You are not an administrator.")
      admin = "no"
  else:
    print("You are not logged in.")
  return render_template('signed_in.html',
    username = str(user),
    admin = admin)
# [END start]

def save_scores():
  print("saving scores")
  judge = request.form['judge']
  team = request.form['team']
  items = []
  print("collecting scores")
  for i in range(len(request.form.getlist('score'))):
    item = {}
    item['judge'] = judge
    item['category'] = request.form.getlist('category')[i]
    item['score'] = int(request.form.getlist('score')[i])
    item['notes'] = request.form.getlist('notes')[i]
    items.append(item)
  Score.SaveTeamScores(team, judge, items)

# [START all_scores_form]
@app.route('/all_scores', methods=['POST', 'GET'])
def all_scores_form():
    scores = []
    summaries = []
    for team in Team.GetAll():
      total_score = 0
      team_judged_by = []
      all_team_scores = Score.GetScoresForTeam(team.name)
      scores += all_team_scores
      judges = [j.name for j in Judge.GetAll()]
      for judge in judges:
        judge_scores = sum([score.score for score in all_team_scores if score.judge == judge])
        total_score += judge_scores
        if judge_scores:
          team_judged_by.append(judge)
      judge_names = ','.join(team_judged_by)
      summaries.append([team.name, team.members, team.contact, total_score, judge_names])
    summaries.sort(reverse=True, key=lambda x: int(x[3]))
    team_count = len(summaries)
    return render_template('all_scores.html',
      summaries = summaries,
      team_count = team_count,
      scores=scores)
# [END all_scores_form]

def save_team():
  Team.PersistInstance(request.form['name'],
    ["members", request.form['members'],
    "contact", request.form['contact']])
  while not len(Team.FindByName(request.form['name'])):
    pass
  Score.AddAllTeamTemplateScores()

# [START reset_data_form]
@app.route('/reset', methods=['GET'])
def reset_form():
  user = users.get_current_user()
  if user.email() != SUPERUSER_EMAIL:
    print("user is {}".format(user.email()))
    abort(403)
  print("request args {}".format(request.args))
  if 'scores' in request.args:
    print("Deleting scores")
    Score.DeleteAll()
  if 'team' in request.args:
    print("Deleting teams")
    Team.DeleteAll()
  models.SetupStaticData()
  judges = Judge.GetSorted()
  categories = Category.GetSorted()
  teams = Team.GetSorted()
  scores = Score.GetSorted()
  return render_template('reset.html',
    judges = judges,
    teams = teams,
    categories = categories,
    scores = scores)
# [END reset_data_form]

# [START team_form]
@app.route('/team', methods=['POST', 'GET'])
def team_form():
    if request.method == 'POST' and request.form.getlist('save'):
      save_team()
      name = request.form['name']
      members = request.form['members']
      contact = request.form['contact']
    else:
      name = ''
      members = ''
      contact = ''
    return render_template('team.html',
      name = name,
      members = members,
      contact = contact)
# [END team_form]

# [START scores_form]
@app.route('/scores', methods=['POST', 'GET'])
def scores_form():
    if request.form.getlist('save'):
      save_scores()
      saved = True
    else:
      saved = False
    if request.form and request.form.getlist('judge'):
      judge = request.form.getlist('judge')[0]
    else:
      judge = ''
    if request.form and request.form.getlist('team'):
      team = request.form.getlist('team')[0]
    else:
      team = ''
    print("***** j '{}' t '{}'".format(judge, team))
    judges = [j.name for j in Judge.GetAll()]
    teams = [t.name for t in Team.GetAll()]
    if team and judge:
      scores = [score for score in Score.GetScoresForTeam(team) if score.judge == judge]
    else:
      scores = []
    return render_template('scores.html',
      team = team,
      judge = judge,
      teams = teams,
      judges = judges,
      scores=scores,
      saved = saved)
# [END scores_form]

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
