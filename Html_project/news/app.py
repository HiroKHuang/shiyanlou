from flask import Flask, render_template
import os, json

app = Flask(__name__)

class File(object):
    directory = os.path.join(os.path.abspath(os.path.dirname(__name__)),'..','files')
    def __init__(self):
        self._file = self._get_files()

    def _get_files(self):
        result = {}
        for filename in os.listdir(self.directory):
            with open(self.directory + '/' + filename) as f:
                result[filename.split('.')[0]] = json.load(f)
        return result
    
    def _get_title(self):
        title_dict = {}
        for key, value in self._file.items():
            title_dict[key] = value['title']
        return title_dict
    
    def _get_content(self, f_name):
        return self._file.get(f_name)

files = File()

@app.route('/')
def index():
    return render_template('index.html', ll = files._get_title())

@app.route('/files/<c>')
def cc_index(c):
    return render_template('file.html', cc = files._get_content(c))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
    
