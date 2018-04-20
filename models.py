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
  def SaveTeamItems(team, items):
   old_scores = Score.GetScoresForTeam(team)
   for score in old_scores:
     score.key.delete()
   for item in items:
     Score.PersistInstance( ["team", team,
       "judge", item["judge"], "category", item["category"],
       "score", item["score"], "notes", item["notes"] ])

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
  Judge.DeleteAll()
  Judge.PersistInstance(["name", "Raymond B", "contact", "raygeeknyc@gmail.com"])
  Judge.PersistInstance(["name", "Christina A", "contact", "nonesuch@starz.com"])
  Judge.PersistInstance(["name", "Justin H", "contact", "theotherguy@gmail.com"])
  Judge.PersistInstance(["name", "Faith Hope", "contact", "faith@gmail.com"])
  while len(Judge.GetAll()) < 4:
    pass
  print("Js {}".format(Judge.GetAll()))

  Category.DeleteAll()
  Category.PersistInstance(["name", "ingenious", "description", "how clever?"])
  Category.PersistInstance(["name", "originality", "description", "how new?"])
  Category.PersistInstance(["name", "freshness", "description", "how surprising?"])
  Category.PersistInstance(["name", "difficulty", "description", "how hard is it?"])
  while len(Category.GetAll()) < 4:
    pass
  print("Cs {}".format(Category.GetAll()))

  Team.DeleteAll()
  Team.PersistInstance(["name", "The best team", "members", "Tm1,tm2,tm3", "contact", "tbt@gmail.com"])
  Team.PersistInstance(["name", "The good team", "members", "gTm1,gtm2", "contact", "gbt@gmail.com"])
  Team.PersistInstance(["name", "The Okay team", "members", "ok1", "contact", "ok@gmail.com"])
  Team.PersistInstance(["name", "The Fair team", "members", "fair1,fair2,fair3,fair4", "contact", "fair1@gmail.com"])
  Team.PersistInstance(["name", "The meh team", "members", "meh1,meh2,meh3,meh4,meh5", "contact", "meh@gmail.com"])
  Team.PersistInstance(["name", "The team we don't talk about", "members", "m1,m2,m3", "contact", "dontcallus@gmail.com"])
  while len(Team.GetAll()) < 6:
    pass
  print("Ts {}".format(Team.GetAll()))
_SetupStaticData()
