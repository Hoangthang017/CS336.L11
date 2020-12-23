from flask import Flask, render_template, request
import main_search_football as msf
import create_tfidf
import os

def Read(paths):
	title_ = msf.fi[paths].replace(".txt","").upper()
	file_path = create_tfidf.find_file_path(title_,msf.files_path)
	print(title_,file_path)
	str_ = create_tfidf.get_content(file_path)
	print (str_)
	return title_, str_

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
	if request.method == "GET":
		a = request.args.get('key')
		if a == None:
			return render_template("home.html")
		else:
			yu = []
			yu = msf.search(a)
			title_1, str_1 = Read(yu[0][0])
			title_2, str_2 = Read(yu[1][0])
			title_3, str_3 = Read(yu[2][0])
			title_4, str_4 = Read(yu[3][0])
			title_5, str_5 = Read(yu[4][0])
			title_6, str_6 = Read(yu[5][0])
			title_7, str_7 = Read(yu[6][0])
			title_8, str_8 = Read(yu[7][0])
			title_9, str_9 = Read(yu[8][0])
			title_10, str_10 = Read(msf.files_path[yu[9][0]])
			return render_template("home.html", q = a, a1=title_1, b1=str_1
													, a2=title_2, b2=str_2
													, a3=title_3, b3=str_3
													, a4=title_4, b4=str_4
													, a5=title_5, b5=str_5
													, a6=title_6, b6=str_6
													, a7=title_7, b7=str_7
													, a8=title_8, b8=str_8
													, a9=title_9, b9=str_9
													, a10=title_10, b10=str_10)
@app.route("/about", methods=['GET', 'POST'])
def about():
	if request.method == 'GET':
	    return render_template("about.html")
	else:
	    code = request.form['code']
	    yu = []
	    yu = search(code)
	    l = msf.files_path[yu[0][0]]
	    return render_template('about.html', a1=yu[0][1], a2=l)
if __name__ == "__main__":
    app.run(debug=True)