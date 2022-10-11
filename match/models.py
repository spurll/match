from datetime import datetime

from match import app, db


class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, index=True)
    email = db.Column(db.String, index=True, unique=True)
    rankings = db.relationship('Ranking', backref='user', lazy='dynamic')
    history = db.relationship('History', backref='user', lazy='dynamic')
    match = db.relationship('Option', backref='match', uselist=False)

    def __repr__(self):
        return '<User {}>'.format(self.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def is_admin(self):
        return self.id in app.config.get('ADMIN_USERS', [])

    def get_id(self):
        return self.id

    @property
    def matched(self):
        return self.match is not None

    @property
    def ranked(self):
        return self.rankings.count() > 0

    @property
    def match_name(self):
        return self.match.name if self.match else 'None'

    @property
    def rank_order(self):
        return [r.option for r in self.rankings.order_by(Ranking.rank).all()]

    @property
    def preferences(self):
        return [h.option for h in self.history.order_by(History.rank).all()]

    @property
    def no_ranking(self):
        return [
            o for o in Option.query.order_by(Option.name).all()
            if o not in self.rank_order
        ]

    @property
    def no_preferences(self):
        return [
            o for o in Option.query.order_by(Option.name).all()
            if o not in self.preferences
        ]


class Option(db.Model):
    name = db.Column(db.String, primary_key=True)
    match_id = db.Column(db.String, db.ForeignKey('user.id'))
    rankings = db.relationship(
        'Ranking', backref='option', lazy='dynamic', cascade='all'
    )
    history = db.relationship(
        'History', backref='option', lazy='dynamic', cascade='all'
    )

    def __repr__(self):
        return '<Option {}>'.format(self.name)


class Ranking(db.Model):
    rank = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    option_id = db.Column(
        db.String, db.ForeignKey('option.name'), primary_key=True
    )

    def __repr__(self):
        return '<Ranking {}: {}>'.format(self.option.name, self.rank)


class History(db.Model):
    rank = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    option_id = db.Column(
        db.String, db.ForeignKey('option.name'), primary_key=True
    )

    def __repr__(self):
        return '<History {}: {}>'.format(self.option.name, self.rank)


class State(db.Model):
    is_open = db.Column(db.Boolean, default=True, primary_key=True)

    def __repr__(self):
        return '<State {}>'.format('Open' if self.is_open else 'Closed')
