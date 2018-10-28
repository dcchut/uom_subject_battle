import web
import os
import sys

path = os.path.dirname(__file__)
sys.path.append(path)
os.chdir(path)
web.config.debug = True

urls = (
    '/top', 'top',
	'/(.*)', 'index',
	)

class top:
    def GET(self):
        # get the top five
        subjects = db.select('subjects', order='rating DESC',limit=10)
        
        return render.top(subjects)
        
    def POST(self):
        return self.GET()

class index:
	def GET(self,score):
		# did they score a previous one?
		if score == 'left' or score == 'right':
			if session.subjects is not None and len(session.subjects) == 2:
				with db.transaction():
					left_code  = dict(code=session.subjects[0])
					right_code = dict(code=session.subjects[1])
					 
					left  = db.select('subjects', vars=left_code, where="code = $code")[0]
					right = db.select('subjects', vars=right_code, where="code = $code")[0]
					
					# make sure these are floats
					left.rating  = float(left.rating)
					right.rating = float(right.rating)
					
					win_left  = 1/(10**((right.rating - left.rating)/400)+1)
					win_right = 1/(10**((left.rating - right.rating)/400)+1)
					
					if score == 'left':
						left_delta = 1
					else:
						left_delta = 0
						
					right_delta = 1 - left_delta

					# update the score
					db.update('subjects', vars=left_code, where="code = $code", rating = left.rating + 20*(left_delta - win_left))
					db.update('subjects', vars=right_code, where="code = $code", rating = right.rating + 20*(right_delta - win_right))
		
		# get two subjects at random
		subjects = list(db.select('subjects', order='RANDOM()', limit=2))
		
		# store them in the session
		session.subjects = [subjects[0].code, subjects[1].code]
		
		return render.index(subjects)

app     = web.application(urls, globals())
render  = web.template.render('templates', base='layout')
db	= web.database(dbn='sqlite', db='/home/dcc/subject_game/db')
store   = web.session.DBStore(db, 'sessions')
session = web.session.Session(app, store, initializer={'subjects':None})

application = app.wsgifunc()
