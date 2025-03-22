import pymysql
import shutil
import datetime

def twenty4_to_12(dt: str):
   if dt.endswith('AM'):
      return dt.split('AM')[0]
   hour = int(dt.split(':')[0].split(' ')[-1])
   if hour == 12:
      return dt.split('PM')[0]
   hour += 12
   return dt.split(':')[0].split(' ')[0] + ' ' + str(hour) + ':' + dt.split(':')[1] + ':' + dt.split(':')[2].split(' ')[0]

#꧁∙·▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫▫ᵒᵒ▫▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫·∙꧂#
#꧁∙·▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫꧁ Top Matter ꧂▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫·∙꧂#
#꧁∙·▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫▫ᵒᵒ▫▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫·∙꧂#

#  ≈☆≈Read in the passowrd.  Github won't allow you to have password in files even for stupid stuff nobody will ever break into.≈☆≈  #
with open ('Config.txt') as file:
   password = file.readline()

#  ≈☆≈Connection to SQL≈☆≈  #
timeout = 10
connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db="defaultdb",
  host="mysql-canvas.l.aivencloud.com",
  password=password,
  read_timeout=timeout,
  port=14461,
  user="avnadmin",
  write_timeout=timeout,)
cursor = connection.cursor()

#  ≈☆≈ Variables ≈☆≈  #
eat_the_frog_bool = False
user = 'Shannon'
EpicQuestsList = []
JourneyList = []
ActivitiesList = []
RepeatingActivitiesList = []

print('\033[48;2;240;240;255m')
print('\033[1m')
#꧁∙·▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫▫ᵒᵒ▫▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫·∙꧂#
#꧁∙·▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫꧁ Epic Quest ꧂▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫·∙꧂#
#꧁∙·▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫▫ᵒᵒ▫▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫·∙꧂#


#  ≈☆≈ Class definition of the top level category for organizing activities ≈☆≈  #
class EpicQuest:
   def __init__(self, name, color, priority):
      self.name = name
      self.color = color
      self.priority = priority
   
   def __repr__(self):
       return self.name

#  ≈☆≈ Get Quests from SQL database and put them into a list ≈☆≈  #
def FetchQuests():
   
   cursor.execute('SELECT * FROM EpicQuest')
   result = cursor.fetchall()
   for row in result:
      if user == 'Shannon':
         EpicQuestsList.append(EpicQuest(row['name'], row['color'], row['priority_Shannon']))
      elif user == 'Nathanael':
         EpicQuestsList.append(EpicQuest(row['name'], row['color'], row['priority_Nathanael']))

   EpicQuestsList.sort(key=lambda x: x.priority, reverse=True)
   

#  ≈☆≈ Adds a new Quest into the SQL database ≈☆≈  #
def AddEpicQuest(name, color, priority_Nathanael=5, priority_Shannon=25):
   cursor.execute('INSERT INTO EpicQuest (name, color, priority_Nathanael, priority_Shannon) VALUES (\'' 
                  + name + '\', \'' + str(color) + '\', ' + str(priority_Nathanael) + ', ' + str(priority_Shannon) + ')')
   connection.commit()


#꧁∙·▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫·∙꧂#
#꧁∙·▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫꧁ Journey ꧂▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫·∙꧂#
#꧁∙·▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫·∙꧂#


#  ≈☆≈ Class definition of the second level category for organizing activities.  Each quest consists of multiple journeys. ≈☆≈  #
class Journey:
   def __init__(self, name, under_quest):
      self.name = name
      self.under_quest = under_quest
   
   def __repr__(self):
       return self.name

#  ≈☆≈ Get Journies from SQL database and put them into a list ≈☆≈  #
def FetchJournies():
   cursor.execute('SELECT * FROM Journey')
   result = cursor.fetchall()
   for row in result:
      if row['is_active'] and user in row['users'].split(','):
         JourneyList.append(Journey(row['name'], row['under_quest']))

#  ≈☆≈ Adds a new Journey into the SQL database ≈☆≈  #
def AddJourney(name, under_quest, user='Shannon,Nathanael'):
   cursor.execute('INSERT INTO Journey (name, under_quest, is_active, users) VALUES (\'' + name + '\', \'' + under_quest + '\', true, \'' + user + '\')')
   connection.commit()


#꧁∙·▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫▫ᵒᵒ▫▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫·∙꧂#
#꧁∙·▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫꧁ Activities ꧂▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫·∙꧂#
#꧁∙·▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫▫ᵒᵒ▫▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫·∙꧂#


#  ≈☆≈ Class definition of the lowest level category for organizing activities.  Each journey contains activities. ≈☆≈  #
class Activity:
    def __init__(self, name, hard_due_date_bool, due_date, suggested_date, urgency, notes,
                  physical_activity_required, mental_capacity_required, anxiety_level_evoked, under_quest, under_journey):
      self.name = name
      self.hard_due_date_bool = hard_due_date_bool
      self.due_date = due_date
      self.suggested_date = suggested_date
      self.urgency = urgency
      self.notes = notes
      self.physical_activity_required = physical_activity_required
      self.mental_capacity_required = mental_capacity_required
      self.anxiety_level_evoked = anxiety_level_evoked
      self.under_quest = under_quest
      self.under_journey = under_journey

    def __str__(self):
       return self.name

    def __repr__(self):
       return self.name

#  ≈☆≈ Get Activities from SQL database and put them into a list ≈☆≈  #
def FetchActivities():
   cursor.execute('SELECT * FROM Activities')
   result = cursor.fetchall()
   for row in result:
      if row['is_active']:
         if user in row['user'].split(','):
            ActivitiesList.append(Activity(row['name'], row['hard_due_date_bool'], row['due_date'], row['suggested_date'], row['urgency'], row['notes'],
                     row['physical_activity_required'], row['mental_capacity_required'], row['anxiety_level_evoked'], row['under_quest'], row['under_journey']))

#  ≈☆≈ Adds a new Activity into the SQL database ≈☆≈  #
def AddActivity(name, hard_due_date_bool, due_date, suggested_date, urgency, notes, physical_activity_required, mental_capacity_required, anxiety_level_evoked, user, under_quest, under_journey):
   cursor.execute('INSERT INTO Activities (name, hard_due_date_bool, due_date, suggested_date, urgency, notes, physical_activity_required, mental_capacity_required, anxiety_level_evoked, user, is_active, under_quest, under_journey) VALUES (\'' 
                  + name + '\', ' + hard_due_date_bool + ', \'' + due_date + '\', \'' + suggested_date + '\', ' + urgency + ', \'' + notes + '\', ' + physical_activity_required 
                  + ', ' + mental_capacity_required + ', ' + anxiety_level_evoked + ',\'' + user + '\', true, \'' + under_quest + '\', \'' + under_journey +'\')')
   connection.commit()

#  ≈☆≈ Class definition of the lowest level category for organizing repeating activities ≈☆≈  #
class RepeatingActivity:
    def __init__(self, name, hard_due_date_bool, due_date, suggested_date, urgency, notes,
                  physical_activity_required, mental_capacity_required, anxiety_level_evoked,
                  days_of_the_week, under_quest, under_journey):
      self.name = name
      self.hard_due_date_bool = hard_due_date_bool
      self.due_date = due_date
      self.suggested_date = suggested_date
      self.urgency = urgency
      self.notes = notes
      self.physical_activity_required = physical_activity_required
      self.mental_capacity_required = mental_capacity_required
      self.anxiety_level_evoked = anxiety_level_evoked
      self.days_of_the_week = days_of_the_week
      self.under_quest = under_quest
      self.under_journey = under_journey

      def __repr__(self):
       return self.name

#  ≈☆≈ Get Repaeating Activities from SQL database and put them into a list ≈☆≈  #
def FetchRepeatingActivities():
   cursor.execute('SELECT * FROM RepeatingActivities')
   result = cursor.fetchall()
   for row in result:
      RepeatingActivitiesList.append(RepeatingActivity(row['name'], row['hard_due_date_bool'], row['due_date'], row['suggested_date'], row['urgency'], row['notes'],
                     row['physical_activity_required'], row['mental_capacity_required'], row['anxiety_level_evoked'],
                     row['days_of_the_week'], row['under_quest'], row['under_journey']))

#  ≈☆≈ Adds a new Repeating Activity into the SQL database ≈☆≈  #
def AddRepeatingActivity(name, hard_due_date_bool, due_date, suggested_date, urgency, notes, physical_activity_required, mental_capacity_required, anxiety_level_evoked, days_of_the_week, under_quest, under_journey):
   cursor.execute('INSERT INTO Journey (name, under_quest) VALUES (\'' + name + '\', ' + hard_due_date_bool + ', \'' + due_date + '\', \'' + suggested_date + '\', ' + urgency 
                  + ', \'' + notes + '\', ' + physical_activity_required + ', ' + mental_capacity_required + ', ' + anxiety_level_evoked + ', \''+ days_of_the_week + '\', \'' 
                  + under_quest + '\', \'' + under_journey +'\')')
   connection.commit()


#꧁∙·▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫▫ᵒ▫▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫·∙꧂#
#꧁∙·▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫꧁ Rendering ꧂▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫·∙꧂#
#꧁∙·▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫▫ᵒ▫▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫·∙꧂#


#  ≈☆≈ Main rendering function, obviously. ≈☆≈  #
def render():
   FetchFetchingFunctions()
   screen_size = shutil.get_terminal_size()
   screen_size_cute = screen_size[0]-1
   screen_size_cute = screen_size_cute//5
   screen_size_edges = screen_size[0]-7

   print('\033[38;2;250;220;150m')

   for i in range(screen_size_cute):
   
      print('✧ *˚⋆',end='')
   print('\n✧', end='')
   for i in range(screen_size_edges):
      print(' ', end='')
   print(' ', end='')
   print('✧')
   print('✧ ', end='')

   Frog()
   WhatsNext()
   Dailies()

   for quest in EpicQuestsList:
      rgb_color = quest.color
      red = rgb_color[0:3]
      green = rgb_color[3:6]
      blue = rgb_color[6:9]
      print('\033[38;2;'+ red + ';' + green + ';' + blue + 'm' + quest.name)
      for journey in JourneyList:
         if journey.under_quest == quest.name:
            print('  ' + journey.name)
            for activity in ActivitiesList:
               if activity.under_quest == quest.name and activity.under_journey == journey.name:
                  print('    ' + activity.name)

#  ≈☆≈ Calculate frog.  What is the frog?  That's a good google search. ≈☆≈  #
def Frog():
   todays_frog = 'OMG you\'re done'
   highest_burden = 0
   for activity in ActivitiesList:
      burden = activity.anxiety_level_evoked + activity.physical_activity_required + activity.mental_capacity_required
      if burden > highest_burden:
         highest_burden = burden
         todays_frog = str(activity)
   print('\033[38;2;100;200;100m Today\'s frog is: ' + todays_frog + '\n')

def Dailies():
   dailies = []
   with open(user + '.txt') as file:
      file.readline()
      dailies = [string.strip('\n') for string in file.readlines()]
   morning_list = dailies[:dailies.index('Evening:')]
   evening_list = dailies[dailies.index('Evening:') + 1 :]

   max_list_width = max(len(string) for string in morning_list) + 5

   print('Morning:'.ljust(max_list_width), 'Evening:')

   if len(morning_list) >= len(evening_list):
      for i in range(len(evening_list)):
         print(morning_list[i].ljust(max_list_width), evening_list[i])
      for i in range(len(evening_list), len(morning_list)):
         print(morning_list[i])
   else:
      for i in range(len(morning_list)):
         print(morning_list[i].ljust(max_list_width) + evening_list[i])
      for i in range(len(morning_list), len(evening_list)):
         print(''.ljust(max_list_width), evening_list[i])

def WhatsNext():
   next_hard_date = datetime.datetime(2362,10,4,12,0,0)
   next_hard_date_activity = ''
   next_soft_date = datetime.datetime(2362,10,4,12,0,0)
   next_soft_date_activity = ''
   for activity in ActivitiesList:
      if activity.due_date < next_hard_date:
         next_hard_date_activity = activity
         next_hard_date = activity.due_date
      if activity.suggested_date < next_soft_date:
         next_soft_date_activity = activity
         next_soft_date = activity.suggested_date
   print('Next hard due date: ' + next_hard_date_activity.name + '   ' + next_hard_date_activity.due_date.strftime('%Y-%m-%d %I:%M'))
   print('Next soft due date: ' + next_soft_date_activity.name + '   ' + next_soft_date_activity.suggested_date.strftime('%Y-%m-%d %I:%M') + '\n')


   

def FetchFetchingFunctions():
   FetchQuests()
   FetchJournies()
   FetchActivities()
   FetchRepeatingActivities()
   print(EpicQuestsList)
   print(JourneyList)
   print(ActivitiesList)
   print(RepeatingActivitiesList)

#꧁∙·▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒ▫ᵒ▫ₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫·∙꧂#
#꧁∙·▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫꧁ Menus ꧂▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫·∙꧂#
#꧁∙·▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒ▫ᵒ▫ₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒₒ▫·∙꧂#


#  ≈☆≈ Main menu ≈☆≈  #
while True:
   EpicQuestsList=[]
   JourneyList=[]
   ActivitiesList=[]
   RepeatingActivitiesList=[]

   render()
#  ≈☆≈ K.  I know immediately copied code looks bad.  I know that.  But this fixes a glitch in Visual Studio Code's terminal.  It's not on me.  Talk to Microsoft. ≈☆≈  #
   EpicQuestsList=[]
   JourneyList=[]
   ActivitiesList=[]
   RepeatingActivitiesList=[]

   render()


   selection = input('''\033[38;2;0;0;0m
1.  Add Activity
2.  Add repeating Activity
3.  Add Journey
4.  Add Epic Quest
5.  Retire Activity
7.  Quit
8.  Options
9.  Retire Journey
10. Retire Quest
11. Rerender
''')

#  ≈☆≈ When the user chooses to add an activity ≈☆≈  #
   if selection == '1':
      #self, name, hard_due_date_bool, due_date, suggested_date, urgency, notes,
                     #physical_activity_required, mental_capacity_required, anxiety_level_evoked
      name = input('name:\n')
      hard_due_date_bool = input('Is there a hard due date? Input as bool.\n')
      if hard_due_date_bool == '0':
         due_date = "2363-10-4 12:00:00"
      else:
         due_date = input('Due date (yyyy-mm-dd hh:mm:ss AM/PM)')
         due_date = twenty4_to_12(due_date)
      suggested_date = input('When do you WANT to get it done, realistically? (yyyy-mm-dd hh:mm:ss AM/PM) or "idk yet".\n')
      if suggested_date == "idk yet":
         suggested_date = "2363-10-4 12:00:00 PM"
      suggested_date = twenty4_to_12(suggested_date)
      urgency = input('Urgency from 1 to 10\n')
      notes = input('Notes:\n')
      physical_activity_required = input('Physical activity required from 1-10\n')
      mental_capacity_required = input('Mental capacity required from 1-10\n')
      anxiety_level_evoked = input('Anxiety level evoked from 1-10\n')
      under_quest = input('What quest is this under?\n')
      under_journey = input('What journey is this under?\n')
      who = input('Is this for just you?')
      if who == 'no':
         AddActivity(name, hard_due_date_bool, due_date, suggested_date, urgency, notes,
                  physical_activity_required, mental_capacity_required, anxiety_level_evoked, 'Shannon,Nathanael', under_quest, under_journey)
      else:
         AddActivity(name, hard_due_date_bool, due_date, suggested_date, urgency, notes,
                  physical_activity_required, mental_capacity_required, anxiety_level_evoked, user, under_quest, under_journey)

#  ≈☆≈ When the user chooses to add a repeating activity ≈☆≈  #

#  ≈☆≈ When the user chooses to add a new journey ≈☆≈  #
   elif selection == '3':
      name = input('name:\n')
      under_quest = (input('Which Quest is this under?\n'))
      belongs_to = input('Who does this belong to? Leave blank for all.')
      if belongs_to =='':
         belongs_to = 'Shannon,Nathanael'
      AddJourney(name, under_quest, belongs_to)

#  ≈☆≈ When the user chooses to add a new quest ≈☆≈  #
   elif selection == '4':
      name = input('name:\n')
      color = input('color in rgb\n')
      priority = int(input('priority\n'))
      if user == 'Shannon':
         AddEpicQuest(name, color, priority_Shannon=priority)
      elif user == 'Nathanael':
         AddEpicQuest(name, color, priority)
   
   elif selection == '5':
      activity_to_retire = input('Which activity?')
      which_quest = input('Which Quest is this under?')
      which_journey = input('Which Journey is this under?')
      cursor.execute('UPDATE Activities SET is_active = false WHERE name = \'' + activity_to_retire + '\' AND under_quest = \'' + which_quest + '\' AND under_journey = \'' + which_journey + '\'')
   elif selection == '7':
      connection.close()
      exit()
   elif selection == '8':
      pass
   elif selection == '9':
      pass
   elif selection == '10':
      pass
   elif selection == '11':
      pass
      
#  ≈☆≈ Commits the changes in the SQL database ≈☆≈  #
   connection.commit()