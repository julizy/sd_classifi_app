from utils import *

app = Flask(__name__)

# route 1: homepage
@app.route('/')
def home():
    # return a simple string
    return '<html><body><h1>Welcome to Singapore Sleep Society!</h1></body></html>'


# route 2: show a form to the user to submit their sleep experience
@app.route('/form')
def form():
    # use flask's render_template function to display an html page
    return render_template('form.html')


# route 3: accept the form submission and show the prediction result
@app.route('/submit')
def make_predictions():
    # load in the form data from the incoming request
    user_input = request.args
    
    # manipulate data into a format that we pass to our model
    txt = user_input['UserExperiences']
    lst_stopwords = create_stopwords(["english"], 
                                 lst_add_words=["sleep","sleeping","slept","apnea","paralysis","sleepapnea","sleepparalysis","sp","know","think","thought","thinking","feel","felt","feeling","like",
                                                "fall","falling","fell","asleep","night","similar","experience","https","www","com","really","maybe","u","im","ive","thats","dont","didnt","yeah","ha","wa",
                                                "time","hour","day","year","month","week","ago"],
                                 lst_keep_words=[])
    X_test = [utils_preprocess_text(txt, slang=False, lst_stopwords=lst_stopwords)]

    # load in pickled model
    model = pickle.load(open('assets/model.p', 'rb'))

    # make predictions
    prediction = model.predict(X_test)[0]
    if prediction == 0:
        prediction = 'Sleep Paralysis'
    else:
        prediction = 'Sleep Apnea'

    # return the results template with our prediction value filled in
    return render_template('results.html', prediction=prediction)


if __name__ == '__main__':
    app.run(debug=True)








