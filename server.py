#!/usr/bin/python3 

from fileinput import filename
import os 
import sys 
import base64
from genericpath import exists
from flask import Flask, request, send_file, after_this_request, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
from mimetypes import MimeTypes

sys.path.insert(1, './stega_api')
from stega_api.stega import stega_function
from stega_api.unstega import unstega_function

app = Flask(__name__)
CORS(app)
mime = MimeTypes()
uploads_dir = os.path.join(app.instance_path, 'stega_uploads')

# exceptions 
class NotAllowedException(Exception): 
    pass

# functions 
def check_extension(extension): 
    allowed_extensions = [".png", ".jpg"]
    extension = extension.lower() 

    if extension in allowed_extensions: 
        return True

    return False

def make_url(mime_type, bin_data):
    return 'data:'+mime_type+';base64, '+bin_data

# routes 
@app.route('/stega', methods=['GET', 'POST'])
def stega():
    try: 
        stega_data = request.form.get("data")
        stega_image = request.files.get("file")

        stega_data = stega_data.strip() 

        if (0 >= len(stega_data)): 
            raise NotAllowedException("Please input some data to hide inside the given image.")

        file_name, file_extension = os.path.splitext(stega_image.filename)

        if (not check_extension(file_extension)): 
            raise NotAllowedException("File Extension not allowed!")

        file_location = os.path.join(uploads_dir, secure_filename(stega_image.filename))

        stega_image.save(file_location)

        stega_output = stega_function(stega_data, file_location)
        hidden_image_location = stega_output["Message"]

        if (stega_output["Type"] != "Success"): 
            raise Exception(stega_output["Message"])

        # remove files after request 

        @after_this_request
        def remove_file(response):
            try:
                os.remove(file_location) # remove the old file 
                os.remove(hidden_image_location) # remove the stega file
            except Exception as e:
                raise Exception(str(e))
            
            return response

        # send the stega file back
        return send_file(hidden_image_location, mimetype="image/png")

    except NotAllowedException as e: 
        return str(e)

    except Exception as e:
        print (str(e))
        return "Server error, please report this problem to Osamu"

@app.route("/unstega", methods=['POST'])
def unstega(): 
    try: 
        
        stega_image = request.files.get("file")

        file_name, file_extension = os.path.splitext(stega_image.filename)

        if (not check_extension(file_extension)): 
            raise NotAllowedException("File Extension not allowed!")

        file_location = os.path.join(uploads_dir, secure_filename(stega_image.filename))

        stega_image.save(file_location)

        unstega_output = unstega_function(file_location)

        # remove files after request 
        @after_this_request
        def remove_file(response):
            try:
                os.remove(file_location) # remove the old file 
            except Exception as e:
                raise Exception(str(e))
            
            return response

        # send the stega file back
        return str(unstega_output)

    except NotAllowedException as e: 
        return str(e)

    except Exception as e:
        print (str(e))
        return "Server error, please report this problem to Osamu"

@app.route("/")
def index(): 
    return render_template("index.html")

if __name__ == '__main__':

    # prepare the environment 
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)

    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)