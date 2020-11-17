from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug = DebugToolbarExtension(app)


# as people answer questions, store in responses list.
# should look like: ['Yes', 'No', 'Less than $10000', 'Yes']

#When user goes to root route: render a page that shows the user the title of the first survey, the instructions and a button to start the survey
# button should serve as a link that directs the user to /questions/0
QUESTIONS = {}
@app.route('/')
def index():
    '''Return Homepage '''
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    for i,question in enumerate(satisfaction_survey.questions):
        QUESTIONS[i] = question
    
    return render_template('index.html', title=title, instructions=instructions)

@app.route('/questions/<int:question_id>')
def show_question(question_id):
    "show a question given int id"
    responses = session['responses']
    if question_id != len(responses):
        flash('Invalid question', 'error')
        return redirect(f'/questions/{len(responses)}')
    
    if len(responses) == len(QUESTIONS.keys()):
        flash("You have completed the questions", 'completed')
        return redirect('/thankyou')
    question = QUESTIONS[question_id].question
    choices = QUESTIONS[question_id].choices
    return render_template('question.html',question=question,choices=choices)

@app.route('/answer', methods=["POST"])
def add_answer():
    '''Add user answer to answer, redirect'''
    #get answer from form
    answer = request.form['question']
    #make responses variable equal the session responses(list)
    responses = session['responses']
    #update repsonses list
    responses.append(answer)
    # overwrite responses list, to equal session['responses']
    session['responses'] = responses

    next_question = len(responses)
    if next_question > len(QUESTIONS.keys()) - 1:
        return redirect('/thankyou')
    return redirect(f'/questions/{next_question}')

@app.route('/thankyou')
def show_thankyou():

    return render_template('thankyou.html')

@app.route('/questions', methods=["POST"])
def first_question():
    session['responses'] = []
    return redirect(f'/questions/0')
    