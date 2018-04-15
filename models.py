import sys
from google.appengine.ext import ndb

class Team(ndb.Model):
  name = ndb.StringProperty()
  members = ndb.StringProperty()
  contact = ndb.StringProperty()

  @staticmethod
  def AddExample():
    print("Adding an example Team")
    team_one = Team(name = "team 1", members = "", contact = "raygeeknyc@gmail.com")
    print("Created {}".format(team_one))
    key = team_one.put()
    print("Added {}".format(key))
    retrieved_copy = key.get()
    print("Retrieved {}".format(retrieved_copy))

class Category(ndb.Model):
  name = ndb.StringProperty()
  description = ndb.StringProperty()

  @staticmethod
  def AddExample():
    print("Adding an example Category")
    category_one = Category(name = "category 1", description = "a cat Category")
    print("Created {}".format(category_one))
    key = category_one.put()
    print("Added {}".format(key))
    retrieved_copy = key.get()
    print("Retrieved {}".format(retrieved_copy))

class Judge(ndb.Model):
  name = ndb.StringProperty()
  contact = ndb.StringProperty()

  @staticmethod
  def AddExample():
    print("Adding an example Judge")
    judge_one = Judge(name = "judge 1", contact = "none@nonesuch.com")
    print("Created {}".format(judge_one))
    key = judge_one.put()
    print("Added {}".format(key))
    retrieved_copy = key.get()
    print("Retrieved {}".format(retrieved_copy))

class Score(ndb.Model):
  team = ndb.StringProperty()
  judge = ndb.StringProperty()
  category = ndb.StringProperty()
  score = ndb.IntegerProperty()
  notes = ndb.StringProperty()

  @staticmethod
  def AddExample():
    print("Adding an example Score")
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

  @staticmethod
  def FindExample():
    print("Finding the example Score")
    instance_query = Score.query(Score.team == "team 1",
      Score.judge == 'judge 1')
    print("query {}".format(instance_query))
    instances = instance_query.iter()
    instance_count = 0
    for instance in instances:
        instance_count += 1
        print("found: {} {}".format(instance_count, instance))
    print("Found {} instances".format(instance_count))
    return instance_count

def _FindByName(model_class, object_name):
  print("Finding {} '{}'".format(model_class.__name__, object_name))
  instance_query = model_class.query(model_class.name == object_name )
  print("query {}".format(instance_query))
  instances = instance_query.iter()
  instance_count = 0
  for instance in instances:
      instance_count += 1
      print("found: {} {}".format(instance_count, instance))
  print("Found {} instances".format(instance_count))
  return instance_count

def _DeleteExisting(model_class):
  print("Deleting {}".format(model_class))
  all_instances = model_class.query()
  instance_count = 0
  for instance in all_instances:
    print("Deleting {}".format(instance))
    instance.key.delete()
    instance_count += 1
  print("Deleted {} of {}".format(instance_count, model_class.__name__))
 
def _SetupStaticData():
  print("Setting up data")
  print("Deleting old data")
  _DeleteExisting(Score)
  _DeleteExisting(Category)
  _DeleteExisting(Team)
  _DeleteExisting(Judge)
  Team.AddExample()
  Judge.AddExample()
  Category.AddExample()
  Score.AddExample()

#if __name__ == "__main__":
_SetupStaticData()
while not _FindByName(Team, "team 1"):
  pass
while not Score.FindExample():
  pass
