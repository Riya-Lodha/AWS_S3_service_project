from flask import Flask, render_template, request, redirect, send_file,jsonify
import os
# from Miniproject1.s3_func import create_bucket,list_buckets,upload_file,delete_bucket
from s3_func import create_bucket,list_buckets,upload_file,delete_bucket,download_file,list_files
app=Flask(__name__)
UPLOAD_FOLDER = "uploads"
BUCKET = "riya-source2-bucket"

@app.route("/")
def hello_world():
    # return '<h1>Welcome to S3 services</h1>'
    return render_template('index.html')
    

@app.route("/create")
def create():
    return render_template('c_bucket.html')


@app.route("/createb",methods=['POST'])
def create1():
    if request.method == "POST":
        name=request.form['name']
        region=request.form['region']

        create_bucket(name,region)
        return '<h1>Inside create bucket...Bucketcreated</h1>'

@app.route("/listb",methods=['GET'])
def list_b():
    if request.method == "GET":
        res=list_buckets()
    # return jsonify(res['Buckets'][10]['Name'])
    # result=jsonify(res)
    # render_template('list_bucket.html',result=result)
        return jsonify(res)






# @app.route("/uploadfb")
# def upload_f_b():

#     # upload_file('nature.jpeg','demobucket-riyal',)
#     return '<h1>File uploaded</h1>'

@app.route("/listf")
def list_f():
    return render_template('list_files.html')

@app.route("/storage",methods=['POST','GET'])
def list_files1():
    if request.method == "POST":
        bucket_name=request.form['name']
        contents = list_files(bucket_name)
        return render_template('storage.html', contents=contents)

    
@app.route("/upload")
def upload():
    return render_template('upload_bucket.html')


@app.route("/uploadfb", methods=['POST'])
def upload1():
    if request.method == "POST":
        bucket_name=request.form['name']
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        upload_file(f"uploads/{f.filename}", bucket_name,)
        return '<h1>File uploaded</h1>'
        # return redirect("/storage")

@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)

        return send_file(output, as_attachment=True)

@app.route("/delete")
def delete():
    return render_template('d_bucket.html')


@app.route("/deleteb",methods=['POST'])
def delete_b():
    if request.method == "POST":
        name=request.form['name']
        
        result=delete_bucket(name)
        
        return '<h1>Bucket Deleted</h1>'
        



if __name__=="__main__":
    app.run(debug=True)