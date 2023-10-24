from flask import Blueprint, render_template, request, jsonify, redirect
from helpers import token_required
from forms import AddMemeForm
from models import db, User, UserMemes, Memes, meme_schema, memes_schema, template_schema, templates_schema

api = Blueprint('api', __name__, url_prefix="/api", template_folder='api_templates')

@api.route("/getTemplates", methods=["GET"])
def getTemplates():
    templates = Memes.query.all()
    response = templates_schema.dump(templates)
    return render_template("showTemplates.html", data=response)

@api.route("/addTemplates", methods=["GET", "POST"])
def addTemps():
    form = AddMemeForm()
    if form.validate_on_submit():
        img_src = form.img_src.data
        template = Memes(img_src)
        db.session.add(template)
        db.session.commit()
        redirect("/profile")
    return render_template('addTemplates.html', form=form)

@api.route("/getTemps", methods=["GET"])
def getTemps():
    memes = Memes.query.all()
    response = templates_schema.dump(memes)
    return jsonify(response)

@api.route("/getMemes", methods=["GET"])
@token_required
def getMemes(current_user_token):
    a_user = current_user_token.token
    memes = UserMemes.query.filter_by(user_token=a_user).all()

    response = memes_schema.dump(memes)
    return jsonify(response)

@api.route('/addMeme', methods = ["POST"])
@token_required
def addMeme(current_user_token):
    img_src = request.json["img_src"]
    caption = request.json["caption"]
    meme = UserMemes(img_src, caption, current_user_token.token)
    db.session.add(meme)
    db.session.commit()

    response = meme_schema.dump(meme)
    return jsonify(response)

@api.route('/updateMeme/<id>', methods = ["PUT"])
@token_required
def updateMeme(current_user_token, id):
    meme = UserMemes.query.get(id)
    meme.img_src = request.json["img_src"]
    meme.caption = request.json["caption"]
    db.session.commit()

    response = meme_schema.dump(meme)
    return jsonify(response)

@api.route("/deleteMeme/<id>", methods=["DELETE"])
@token_required
def deleteMeme(current_user_token,id):
    meme = UserMemes.query.get(id)
    db.session.delete(meme)
    db.session.commit()

    response = meme_schema.dump(meme)
    return jsonify(response)
