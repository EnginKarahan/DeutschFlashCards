import web, json, random

urls = ('/', 'Index', '/type', 'WordType', '/game', 'GameEngine')

app = web.application(urls, globals())

with open('static/A2verbs') as json_file:
    A2verb = json.load(json_file)

with open('static/A2nouns') as json_file:
    A2noun = json.load(json_file)

with open('static/A2others') as json_file:
    A2other = json.load(json_file)

with open('static/A2verbs') as json_file:
    B1verb = json.load(json_file)

with open('static/A2nouns') as json_file:
    B1noun = json.load(json_file)

with open('static/A2others') as json_file:
    B1other = json.load(json_file)

game_modes = {'A2': None, 'B1': None, 'B2': None}

if web.config.get('_session') is None:
    store = web.session.DiskStore('sessions')
    session = web.session.Session(app, store,
                           initializer={'game_type': None, 'word_type': None})
    web.config._session = session
else:
    session = web.config._session

render = web.template.render('templates/', base="layout")


class Index(object):
    def GET(self):
        return render.game_selector()

    def POST(self):
        form = web.input(game_type=None)
        session.game_type = form.game_type
        if (form.game_type == 'A2') or (form.game_type == "B1"):
            session.score = 0
            web.seeother("/type")
        else:
            return render.game_selector()

class WordType(object):

    def GET(self):
        return render.word_game_selector()

    def POST(self):
        form = web.input(word_type=None)
        session.word_type = form.word_type
        session.score = 0
        web.seeother("/game")

class GameEngine(object):

    def GET(self):
        if session.game_type == "A2":
            if session.word_type == 'verb':
                d_word = random.choice(list(A2verb))
            elif session.word_type == 'noun':
                d_word = random.choice(list(A2noun))
            elif session.word_type == 'other':
                d_word = random.choice(list(A2other))
        elif session.game_type == "B1":
            if session.word_type == 'verb':
                d_word = random.choice(list(B1verb))
            elif session.word_type == 'noun':
                d_word = random.choice(list(B1noun))
            elif session.word_type == 'other':
                d_word = random.choice(list(B1other))
        return render.word_game(score=session.score, d_word=d_word, e_word=None)

    def POST(self):
        form = web.input(trans=None)
        session.score += 1
        if session.game_type == "A2":
            if session.word_type == 'verb':
                e_word = A2verb[form.trans]
            elif session.word_type == 'noun':
                e_word = A2noun[form.trans]
            elif session.word_type == 'other':
                e_word = A2other[form.trans]
        elif session.game_type == "B1":
            if session.word_type == 'verb':
                e_word = B1verb[form.trans]
            elif session.word_type == 'noun':
                e_word = B1noun[form.trans]
            elif session.word_type == 'other':
                e_word = B1other[form.trans]

        return render.word_game(score=session.score, d_word=None, e_word=e_word)

if __name__ == "__main__":
    app.run()



