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
import logging
import models

# [START imports]
from flask import Flask, render_template, request
from models import Judge, Score, Team, Category
# [END imports]

# [START create_app]
app = Flask(__name__)
# [END create_app]


# [START start]
@app.route('/login', methods=['POST', 'GET'])
@app.route('/')
def start():
    return render_template('login.html')
# [END start]


# [START judge_form]
@app.route('/signin', methods=['POST'])
def judge_form():
    judges = Judge.GetSorted()
    return render_template('signed_in.html',
      judges=judges)
# [END judge_form]

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
    scores = Score.GetSorted()
    summaries = []
    for team in Team.GetSorted():
      total_score = 0
      for score in Score.GetScoresForTeam(team.name):
        total_score += score.score
      summaries.append([team.name, team.members, team.contact, total_score])
    return render_template('all_scores.html',
      summaries = summaries,
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
@app.route('/reset', methods=['POST', 'GET'])
def reset_form():
    models.SetupStaticData()
    judges = Judge.GetAll()
    categories = Category.GetAll()
    teams = Team.GetAll()
    return render_template('reset.html',
      judges = judges,
      teams = teams,
      categories = categories)
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
