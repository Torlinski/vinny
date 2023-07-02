from flask import Flask, render_template, request

app = Flask(__name__)


items = ['Hello', 'How\n\n\n', 'Are', 'You']
progress = []
inter =0 

@app.route('/', methods=['GET', 'POST'])
def index():
    global inter
    if request.method == 'POST':
        if 'update_button' in request.form:
            inter+=1
        if 'reset' in request.form:
            inter=0
    return render_template('index.html', content=''.join(items[:inter]))


if __name__ == '__main__':
    app.run(debug=True)

