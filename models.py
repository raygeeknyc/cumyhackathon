import sys
from google.appengine.ext import ndb
from static_data import TEAMS, JUDGES, CATEGORIES, INITIAL_SCORE, INITIAL_NOTES

class _JudgingEntity(ndb.Model):
  @classmethod
  def AddExample(cls):
    pass

  @classmethod
  def DeleteAll(cls):
    print("Deleting {}".format(cls.__name__))
    all_instances = cls.query()
    instance_count = 0
    for key in all_instances.iter(keys_only=True):
      print("Deleting {}".format(key))
      key.delete()
      instance_count += 1
    print("Deleted {} of {}".format(instance_count, cls.__name__))
 
  @classmethod
  def GetAll(cls):
    print("Finding all {}".format(cls.__name__))
    instance_query = cls.query()
    instances = instance_query.iter()
    entities = []
    for instance in instances:
      entities.append(instance)
      print("found: {}".format(instance))
    print("Found {} instances".format(len(entities)))
    return entities

class _NamedJudgingEntity(_JudgingEntity):
  @classmethod
  def PersistInstance(cls, value_list):
    instance = cls()
    for i in range(0, len(value_list), 2):
      setattr(instance, value_list[i], value_list[i+1])
    existing_instances = cls.FindByName(instance.name)
    if not existing_instances:
      key = instance.put()

  @classmethod
  def FindByName(cls, object_name):
    print("Finding {} '{}'".format(cls.__name__, object_name))
    instance_query = cls.query(cls.name == object_name )
    instances = instance_query.iter()
    entities = []
    for instance in instances:
      entities.append(instance)
      print("found: {}".format(instance))
    print("Found {} instances".format(len(entities)))
    return entities

  @staticmethod
  def _NameOf(entity):
    return entity.name.upper()

  @classmethod
  def GetSorted(cls):
    entities = cls.GetAll()
    return sorted(entities, key=cls._NameOf)

class Team(_NamedJudgingEntity):
  name = ndb.StringProperty()
  members = ndb.StringProperty()
  contact = ndb.StringProperty()

class Category(_NamedJudgingEntity):
  name = ndb.StringProperty()
  description = ndb.StringProperty()

class Judge(_NamedJudgingEntity):
  name = ndb.StringProperty()
  contact = ndb.StringProperty()

class Score(_JudgingEntity):
  team = ndb.StringProperty()
  judge = ndb.StringProperty()
  category = ndb.StringProperty()
  score = ndb.IntegerProperty()
  notes = ndb.StringProperty()

  @staticmethod
  def SaveTeamScores(team, judge, items):
    old_scores = Score.GetScoresForTeam(team)
    for score in [s for s in old_scores if s.judge == judge]:
      score.key.delete()
    for item in items:
      Score.Add(team=team, judge=judge, category = item["category"],
        score = item["score"], notes = item["notes"])

  @staticmethod
  def _ScoreKey(score):
    return "{:10.10}".format(score.team)+"{:10.10}".format(score.judge)+"{:10.10}".format(score.category)

  @classmethod
  def GetScoresForTeam(cls, team):
    print("Finding {} for '{}'".format(cls.__name__, team))
    instance_query = cls.query(cls.team == team )
    instances = instance_query.iter()
    scores = []
    for score in instances:
      scores.append(score)
    print("Found {} instances".format(len(scores)))
    scores = sorted(scores, key=cls._ScoreKey)
    return scores

  @classmethod
  def AddAllTeamTemplateScores(cls):
    print("Filling in scores for team {}".format(cls.__name__))
    team_names = [team.name for team in Team.GetAll()]
    judge_names = [judge.name for judge in Judge.GetAll()]
    category_names = [category.name for category in Category.GetAll()]

    all_scores = cls.GetAll()
   
    for team in team_names:
      for judge in judge_names:
        for category in category_names:
          found = False
          for score in all_scores:
            if score.category == category and score.judge == judge and score.team == team:
              found = True
          if not found:
            cls.Add(team, judge, category, INITIAL_SCORE, INITIAL_NOTES)
  
  @staticmethod
  def Add(team, judge, category, score, notes):
    score = Score(team = team, judge = judge, category = category,
      score = score, notes = notes)
    key = score.put()
    print("Added {}".format(key))
    retrieved_copy = key.get()
    print("Retrieved {}".format(retrieved_copy))

  @classmethod
  def FindExample(cls):
    print("Finding the example {}".format(cls.__name__))
    instance_query = cls.query(Score.team == "team 1",
      Score.judge == 'judge 1')
    print("query {}".format(instance_query))
    instances = instance_query.iter()
    instance_count = 0
    for instance in instances:
        instance_count += 1
        print("found: {} {}".format(instance_count, instance))
    print("Found {} instances".format(instance_count))
    return instance_count

def _SetupStaticData():
  print("Setting up data")
  Judge.DeleteAll()
  for judge in JUDGES:
    Judge.PersistInstance(judge)
  while len(Judge.GetAll()) < len(JUDGES):
    pass
  print("Js {}".format(Judge.GetAll()))

  Category.DeleteAll()
  for category in CATEGORIES:
    Category.PersistInstance(category)
  while len(Category.GetAll()) < len(CATEGORIES):
    pass
  print("Cs {}".format(Category.GetAll()))

  Team.DeleteAll()
  for team in TEAMS:
    Team.PersistInstance(team)
  while len(Team.GetAll()) < len(TEAMS):
    pass
  print("Ts {}".format(Team.GetAll()))

  Score.AddAllTeamTemplateScores()

_SetupStaticData()
