import csv, re

from match import app, db
from match.models import User, Option, Ranking, History, State


class MatchController(object):
    def __init__(self, allocation=None, notification=None):
        self.allocation = allocation
        self.notification = notification

        if State.query.count() < 1:
            s = State(is_open=True)

            try:
                db.session.add(s)
                db.session.commit()
            except:
                db.session.rollback()
                raise

    @property
    def is_open(self):
        return State.query.one().is_open

    def rank(self, user, *args):
        """
        Casts a ballot (a series of rankings) in the the order specified.
        """
        if not self.is_open:
            raise Exception('Rankings are closed.')

        if len(args) != len(set(args)):
            raise Exception('Rankings must be unique.')

        try:
            # Delete user's rankings and history first.
            user.rankings.delete()
            user.history.delete()
            db.session.commit()
        except:
            db.sesion.rollback()
            raise

        for index, option in enumerate(args):
            rank = index + 1        # First choice is #1, then #2, etc.
            try:
                o = Option.query.filter(Option.name == option).one()
            except:
                # Sometimes (most of the time) the category will also be
                # included. This is a terribly lazy way to handle this, Gem.
                option = re.sub(' \(.*\)$', '', option)
                o = Option.query.filter(Option.name == option).one()

            # Create vote and history objects. (History is used to re-populate
            # new ballots with old votes, to save the user time in subsequent
            # rounds of voting. It's kind of a hack.)
            r = Ranking(rank=rank)
            h = History(rank=rank)

            # Associate ranking and history objects with the option and user.
            o.rankings.append(r)
            o.history.append(h)
            user.rankings.append(r)
            user.history.append(h)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

    def notify(self, users):
        """
        Notifies users of the results of the match, using the notification
        function provided on initialization.
        """
        if self.notification:
            self.notification(users)

    def clear(self, user=None):
        """
        If a user is provided, removes the specified user's rankings from the
        database. Otherwise, removes all rankings from the database.
        """
        try:
            if user:
                # Delete the specified user's rankings.
                user.rankings.delete()
            else:
                # Delete all rankings.
                Ranking.query.delete()

            db.session.commit()
        except:
            db.session.rollback()
            raise

    def close(self):
        """
        Determines matches based on the selection algorithm provided at
        initialization, saves this information to the database, issues the
        appropriate notification (if any), and then clears rankings.
        """
        if not self.is_open:
            raise Exception('Ranking is already closed.')

        users = self.list_users(ranked=True)
        print('Rankings:')
        for u in users:
            print(f'{u.name}: ' + ', '.join(x.name for x in u.rank_order))

        print(f'Performing match by {self.allocation.__name__}...')

        # Get results.
        self.allocation(self.list_users())

        print('Matches:')
        for u in users:
            print(f'{u.name}: {u.match_name}')

        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

        # Delete current rankings and close voting.
        self.clear()

        State.query.one().is_open = False;
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

        # Notify.
        self.notify(users)

    def open(self):
        """
        Opens the match session, which allows rankings to be made.
        """
        if self.is_open:
            raise Exception('Voting is already open.')

        State.query.one().is_open = True;
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

    def add_option(self, name):
        """
        Adds a new option to the database.
        """
        o = Option(name=name)

        try:
            db.session.add(o)
            db.session.commit()
        except:
            db.session.rollback()
            raise

    def import_options(self, file_name):
        """
        Imports a list of options into the database from a text file. This file
        should have one option on every line
        """
        with open(file_name) as file:
            reader = csv.reader(file)
            for row in reader:
                option = row[0] if row else None

                if option:
                    print('Adding new option: {}'.format(option['name']))
                    o = Option(name=option)

                    try:
                        db.session.add(o)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print (
                            'Unable to add {} to the database: {}'
                            .format(option['name'], e)
                        )

    def add_user(self, user_id, name, email):
        """
        Adds a new user to the database.
        """
        u = User(id=user_id, name=name, email=email)

        try:
            db.session.add(u)
            db.session.commit()
        except:
            db.session.rollback()
            raise

    def delete_option(self, name):
        """
        Removes an option to the database.
        """
        try:
            Option.query.filter(Option.name == name).delete()
            db.session.commit()
        except:
            db.session.rollback()
            raise

    def list_options(self):
        """
        Returns a list of all options.
        """
        return Option.query.order_by(Option.category).all()

    def list_users(self, ranked=None, matched=None):
        """
        Returns a list of all users. If ranked is set to True or False, only
        return a list of users who have (or have not) submitted rankings.
        """
        if ranked is not None:
            return [u for u in User.query.all() if u.ranked == ranked]

        if matched is not None:
            return [u for u in User.query.all() if u.matched == matched]

        return User.query.all()

    def results(self):
        return self.list_users(matched=True)

    def list_rankings(self, user=None, as_dict=False):
        """
        If a user is provided, returns a list of the specified user's votes (as
        Option objects, not Vote objects). Otherwise, returns a dict with
        usernames as keys and lists of votes (Options) as values.
        """
        if user:
            # List the specified user's votes.
            return user.ranking

        # List all votes.
        if as_dict:
            return {u.id: u.ranking for u in User.query.all()}

        return [u.ranking for u in User.query.all()]

