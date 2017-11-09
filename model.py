from sklearn.externals import joblib
from pandas import DataFrame

COLUMNS=['albums', 'alcohol', 'audios', 'city', 'country', 'followers_count', 'friends',
           'groups',
           'has_mobile', 'has_photo', 'langs', 'life_main',
           'notes',
           'pages', 'people_main', 'photos', 'political', 'relation',
           'schools',
           'sex', 'smoking', 'uid', 'universities',
           'videos', "wall_posts","age"]

model1 = joblib.load('clf1.pkl')
model2 = joblib.load('clf2.pkl')

#

def predict(dicter):
	#print(dicter)
	# dicter = preprocess(dicter)
	#print(dicter)
	todel = []
	for key, value in dicter.items():
		if key not in COLUMNS:
			todel.append(key)
	for i in todel:
		dicter.pop(i, None)
	df = DataFrame(dicter, index=[0])
	#print(df)
	cl1 = model1.predict(df)[0]
	cl2 = model2.predict(df)[0]
	print(cl1, cl2)
	return [cl1, cl2]
