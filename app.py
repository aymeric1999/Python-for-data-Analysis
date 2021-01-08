from flask import Flask, render_template,request,redirect,session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField,IntegerField, SelectField,SubmitField
from wtforms.validators import DataRequired, InputRequired, NumberRange

app=Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"]="hard to guess string"

#formulaire

class enteryourinput(FlaskForm):
	ProductRelated=FloatField("Veuillez entrer le nombres de pages web visitées concernant les produits",validators=[DataRequired()])
	Administrative=FloatField("Combien de pages sur l'administration ?",validators=[DataRequired()])
	Informational=FloatField("Et pour vous informer ?",validators=[DataRequired()])
	PageValues=FloatField("Quelles sont les valeurs de votre pages ?(entre 0 et 370)",validators=[DataRequired(),NumberRange(min=0,max=370)])
	submit=SubmitField("Soumettre")

@app.route("/")
def index():
	return render_template('base.html')

@app.route('/predict',methods=["GET","POST"])
def prediction():
	form=enteryourinput()
	if request.method=="POST" and form.validate_on_submit():
		import joblib
		load_model=joblib.load("./modele_saved")
		prediction=load_model.predict([[form.ProductRelated.data,form.Administrative.data,form.Informational.data,form.PageValues.data]]).tolist()
		session["result"]=prediction
		return redirect ("/results")
	return render_template('prediction_form.html',form=form)

@app.route('/results')
def show_result():
	pred=session["result"]
	return render_template('result.html',pred=pred)


if __name__ == '__main__':
	print(app.url_map)
	app.run(host='127.0.0.1',port=5000,debug=True)

