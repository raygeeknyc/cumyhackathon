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
from models import Judge, Score
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

# [START save_scores]
@app.route('/save_scores', methods=['POST'])
def save_scores():
  items = []
  for i in range(len(request.form.getlist('judge'))):
    items.append([request.form.getlist('judge')[i], request.form.getlist('category')[i],
      request.form.getlist('score')[i], request.form.getlist('notes')[i]])
  return render_template('saved.html',
    team=request.form['team'],
    data=items)
# [END save_scores]

# [START scores_form]
@app.route('/scores', methods=['POST', 'GET'])
def scores_form():
    team = 'team 1'
    scores = Score.GetScoresForTeam(team)
    return render_template('scores.html',
      team = team,
      scores=scores)
# [END scores_form]

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
