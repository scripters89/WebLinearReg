import os
from flask import Flask, request, redirect, url_for, render_template
import AnalyticalEngine as AE

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
variable_list = []
g_file_name =""
target_variable = ""
@app.route('/')
def index():
    return render_template('index.html',output="")

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        try:
            file_name = request.form.getlist('File_type')[0]
        except:
            print "Error in Select Statement"

        if allowed_file(file.filename):
            filename = str(file.filename)
            try:
                fileextn = filename.split('.')
            except:
                print "Error in fileextn"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name+"."+fileextn[1]))
            global g_file_name
            g_file_name = file_name+"."+fileextn[1]
            if file_name == "DataDef":
                return render_template('index.html', output="Data Defintion is uploaded")
            else:
                global variable_list
                variable_list = AE.data_read_proc(file_name+"."+fileextn[1], UPLOAD_FOLDER)
                return render_template('list.html', vlist=variable_list)
        else:
            return render_template('index.html', output="Upload Failed Only CSV Can be uploaded")

@app.route('/list')
def listm():
    return render_template('list.html')

@app.route('/listaction', methods=['POST'])
def lisaction():
    t_var = request.form.getlist('targetvariable')
    global target_variable
    global variable_list
    target_variable = t_var[0]
    excluded_varaible = request.form.getlist('excludevariable')
    result = AE.binomial_logit_proc(app.config['UPLOAD_FOLDER'],g_file_name,excluded_varaible,variable_list,target_variable)
    print result
    return render_template('output.html', summaryoutput=result)

def allowed_file(filename):
    print filename
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

app.run(host="localhost", port=2001, debug=True)