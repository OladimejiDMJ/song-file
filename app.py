from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from datetime import datetime
from marshmallow_sqlalchemy import ModelSchema
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/songfiles'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Songfile(db.Model):
    __tablename__='songfiles'
    id=db.Column(db.Integer,unique=True,primary_key=True)
    song_title=db.Column(db.String(100),nullable=False)
    duration_in_seconds=db.Column(db.Integer,nullable=False)
    uploaded_time=db.Column(db.DateTime,default=datetime.now(),nullable=False)
    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,song_title,duration_in_seconds,uploaded_time):
        self.song_title=song_title
        self.duration_in_seconds=duration_in_seconds
        self.uploaded_time=uploaded_time
    def __repr__(self):
        return '' % self.id
db.create_all()


class SongSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Songfile
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    song_title = fields.String(required=True)
    duration_in_seconds = fields.Number(required=True)
    uploaded_time = datetime.now()


@app.route('/songfile', methods = ['POST'])
def create_song():
    data=request.get_json()
    song_schema=SongSchema()
    song=song_schema.load(data)
    result=song_schema.dump(song.create())
    return make_response(jsonify({"song":result}),200)


@app.route('/songfile/<id>', methods = ['DELETE'])
def delete_song_by_id(id):
    get_song_by_id=Songfile.query.get(id)
    db.session.delete(get_song_by_id)
    db.session.commit()
    return make_response("",200)

@app.route('/songfile/', methods = ['GET'])
def get_all_songfile():
    all_songfile = Songfile.query.all()
    song_schema = SongSchema(many=True)
    songs= song_schema.dump(all_songfile)
    return make_response(jsonify({"songfiles": songs}),200)

@app.route('/songfile/<id>', methods = ['GET'])
def get_a_songfile(id):
    songfile = Songfile.query.get(id)
    song_schema = SongSchema()
    song= song_schema.dump(songfile)
    return make_response(jsonify({"songfile": song}),200)

@app.route('/songfile/<id>', methods = ['PUT'])
def update_songfile_by_id(id):
    
    data = request.get_json()
    get_song = Songfile.query.get(id)
    if data.get('song_title'):
        get_song.song_title = data['song_title']
    if data.get('duration_in_seconds'):
        get_song.duration_in_seconds = data['duration_in_seconds']
    if data.get('uploaded_time'):
        get_product.uploaded_time = data['uploaded_time']   
    db.session.add(get_song)
    db.session.commit()
    try:
        song_schema = SongSchema(only=['id', 'song_title','uploaded_time','duration_in_seconds'])
        song = song_schema.dump(get_song)
        return make_response(jsonify({"song": song}))
    except:
        abort(400)

if __name__ == "__main__":
    app.run(debug=True)