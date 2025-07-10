from flask import Flask,request,session,flash,redirect,url_for,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os


app = Flask(__name__)
app.secret_key = 'secret'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'notes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)

@app.route("/")
def home():
    return redirect(url_for("dashboard"))


@app.route("/add",methods=["GET",'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        note = Note(title=title,content=content)
        db.session.add(note)
        db.session.commit()
        flash("Note Added Successfully",'success')
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/dashboard')
def dashboard():
    notes = Note.query.order_by(Note.created_at.desc()).all()
    return render_template("dashboard.html",notes=notes)


@app.route('/edit/<int:note_id>',methods=['GET','POST'])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        db.session.commit()
        flash('Note Updated Sucessfully!','success')
        return redirect(url_for('dashboard'))
    return render_template('edit_note.html',note=note)

@app.route('/search')
def search_notes():
    query = request.args.get('query')
    if query:
        notes = Note.query.filter(Note.title.contains(query) | Note.content.contains(query)).all()
        return render_template('dashboard.html',notes=notes)
    else:
        redirect(url_for('dashboard'))

@app.route('/delete/<int:note_id>',methods=['POST'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash("Note Deleted Successfully",'success')
    return redirect(url_for('dashboard'))


if __name__ == "__main__":
    app.run(debug=True)

