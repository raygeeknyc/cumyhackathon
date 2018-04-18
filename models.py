import sys
from google.appengine.ext import ndb

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

  @classmethod
  def AddExample(cls):
    cls.Add(name = "team 1", members = "", contact = "raygeeknyc@gmail.com")

  @classmethod
  def Add(cls, name, members, contact):
    print("Adding a {}".format(cls.__name__))
    team = Team(name = name, members = members, contact = contact)
    print("Created {}".format(team))
    key = team.put()
    print("Added {}".format(key))
    retrieved_copy = key.get()
    print("Retrieved {}".format(retrieved_copy))

class Category(_NamedJudgingEntity):
  name = ndb.StringProperty()
  description = ndb.StringProperty()

  @classmethod
  def AddExample(cls):
    print("Adding an example {}".format(cls.__name__))
    category_one = Category(name = "category 1", description = "a cat Category")
    print("Created {}".format(category_one))
    key = category_one.put()
    print("Added {}".format(key))
    retrieved_copy = key.get()
    print("Retrieved {}".format(retrieved_copy))

class Judge(_NamedJudgingEntity):
  name = ndb.StringProperty()
  contact = ndb.StringProperty()

  @classmethod
  def AddExample(cls):
    cls.Add(name = "judge 1", contact = "none@nonesuch.com")

  @classmethod
  def Add(cls, name, contact):
    print("Adding a {}".format(cls.__name__))
    judge = Judge(name = name, contact = contact)
    print("Created {}".format(judge))
    key = judge.put()
    print("Added {}".format(key))
    retrieved_copy = key.get()
    print("Retrieved {}".format(retrieved_copy))

class Score(_JudgingEntity):
  team = ndb.StringProperty()
  judge = ndb.StringProperty()
  category = ndb.StringProperty()
  score = ndb.IntegerProperty()
  notes = ndb.StringProperty()

  @staticmethod
  def SaveTeamItems(team, items):
   old_scores = Score.GetScoresForTeam(team)
   for score in old_scores:
     score.key.delete()
   for item in items:
     Score.Add(team, item['judge'], item['category'], item['score'], item['notes'])

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
  def AddExample(cls):
    print("Adding an example {}".format(cls.__name__))
    score_one = cls.Add(team = "team 1",
      judge = "judge 1",
      category = "category 1",
      score = 2,
      notes = "did not do it well")

  @classmethod
  def Add(cls, team, judge, category, score, notes):
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
  print("Deleting old data")
  for score in Score.GetAll():
    print("Score: {}".format(score))
  Score.DeleteAll()
  Category.DeleteAll()
  Team.DeleteAll()
  Judge.DeleteAll()
  Team.AddExample()
  Judge.AddExample()
  Judge.Add("Raymondo", "646-236-6743")
  Judge.Add("Justin", "justin@cunystartups.com")
  print("sorted", Judge.GetSorted())
  Category.AddExample()
  Score.AddExample()
  Score.Add(team = 'team 1', judge = 'judge 1', category = 'cat 2', score = 1, notes = 'two')
  Score.Add(team = 'team 1', judge = 'judge 2', category = 'cat 1', score = 1, notes = 'two')
  Score.Add(team = 'team 1', judge = 'judge 2', category = 'cat 2', score = 1, notes = 'two')
  Score.Add(team = 'team 2', judge = 'judge 1', category = 'category 1', score = 2, notes = 'uno')
  Score.Add(team = 'team 2', judge = 'judge 1', category = 'cat 2', score = 5, notes = 'FIVE!!!')
  Score.Add(team = 'team 2', judge = 'judge 2', category = 'cat 2', score = 1, notes = 'two')
  Score.Add(team = 'team 2', judge = 'judge 2', category = 'cat 1', score = 1, notes = 'two')

#if __name__ == "__main__":
_SetupStaticData()
while not Team.GetAll():
  pass
while not Judge.FindByName("judge 1"):
  pass
while not Score.FindExample():
  pass
