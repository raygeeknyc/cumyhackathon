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
    print("Adding an example {}".format(cls.__name__))
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
    print("Adding an example {}".format(cls.__name__))
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

  @classmethod
  def AddExample(cls):
    print("Adding an example Judge")
    score_one = Score(team = "team 1",
      judge = "judge 1",
      category = "category 1",
      score = 2,
      notes = "did not do it well")
    print("Created {}".format(score_one))
    key = score_one.put()
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

#if __name__ == "__main__":
_SetupStaticData()
while not Team.GetAll():
  pass
while not Judge.FindByName("judge 1"):
  pass
while not Score.FindExample():
  pass