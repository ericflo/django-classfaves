from setuptools import setup, find_packages

VERSION = '0.1'

LONG_DESCRIPTION = """
Overview of django-classfaves
-----------------------------

This app provides everything that you need to add favoriting abilities to
your site!  There are just a few steps that you need to go through to add
this functionality to your site.

Installation at a Glance
========================

1.  Create a favorite model that has a ``ForeignKey`` to the domain object
    that you would like to be able to favorite or unfavorite.

2.  Instantiate ``CreateFavorite``, ``DeleteFavorite``, and ``UserFavorites``
    in one of your url configurations, and map them into your urlpatterns.

3.  Integrate into your domain object's templates and views.


Installation Example: Arcade Site
=================================

This installation example comes from `Radiosox`_, for which this application
was originally written.  The site is a free online arcade site that allows
users to mark certain games as their favorite ones.  They are allowed to
un-favorite those games if they change their mind.  Finally, they are allowed
to see a list of their favorite games.

Step 1: Creating our Model
~~~~~~~~~~~~~~~~~~~~~~~~~~

We already have a domain object that looks a little bit like this:

.. sourcecode:: python

    from django.db import models

    class Game(models.Model):
        name = models.CharField(max_length=64)
        slug = models.SlugField(max_length=64)
        description = models.TextField(blank=True)
        # ... there are many more fields here

Now what we want to do is in that same models.py file, we will create our
favorite model, like shown here:

.. sourcecode:: python

    from classfaves.models import FavoriteBase

    class GameFavorite(FavoriteBase):
        game = models.ForeignKey(Game)

What this does is use our ``FavoriteBase`` abstract base class, provide by
django-classfaves, and ensure that it's got a link to our ``Game`` domain
object.  This model is equivalent to manually writing this:

.. sourcecode:: python

    import datetime
    
    from django.db import models
    from django.contrib.auth.models import User

    class GameFavorite(models.Model):
        game = models.ForeignKey(Game)
        user = models.ForeignKey(User)
        date_created = models.DateTimeField(default=datetime.datetime.now)

In fact, you could write that model if you prefer.  I prefer to subclass
``FavoriteBase``, since it's easier.

Step 2: Attaching our Views
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In our ``urls.py`` file for that arcade app whose models we were using in the
previous step, we have something that, right now, looks like this:

.. sourcecode:: python

    from django.conf.urls.defaults import patterns, url

    urlpatterns = patterns('arcade.views',
        url(r'^popular/$', 'popular', name='arcade_popular'),
        url(r'^new/$', 'new', name='arcade_new'),
        # ... there are more URLs here
    )

What we want to do first is instantiate our views provided by the
django-classfaves app:

.. sourcecode:: python

    from arcade.models import GameFavorite, Game
    from classfaves.views import CreateFavorite, DeleteFavorite, UserFavorites

    create_favorite = CreateFavorite(GameFavorite, Game)
    delete_favorite = DeleteFavorite(GameFavorite, Game)
    public_games = lambda qs: qs.filter(game__enabled=True)
    user_favorites = UserFavorites(GameFavorite, Game, extra_filter=public_games)

What this does is give us views to create, delete, and get user favorites for
all games in the system.  You'll note that we're passing an argument named
``extra_filter`` to ``UserFavorites`` which limits the view to only showing
games with ``enabled`` set to ``True``.  This can be used to limit the
``QuerySet`` arbitrarily.  Kinda cool, huh?

Anyway, the next step is to modify our ``urlpatterns`` so that it maps to these
views:

..sourcecode:: python

    urlpatterns = patterns('arcade.views',
        url(r'^popular/$', 'popular', name='arcade_popular'),
        url(r'^new/$', 'new', name='arcade_new'),
        # ... vvv THE NEW URLS ARE BELOW vvv
        url(r'^favorites/create/(?P<pk>\d+)/$', create_favorite, name='arcade_favorite_create'),
        url(r'^favorites/delete/(?P<pk>\d+)/$', delete_favorite, name='arcade_favorite_delete'),
        url(r'^favorites/list/$', user_favorites, name='arcade_my_favorites'),
        url(r'^favorites/list/(?P<username>[a-zA-Z0-9_-]+)/$', user_favorites, name='arcade_user_favorites'),
    )

Note how we were able to give the new views proper URL names, and how we were
able to easily place them where they logically fit in the URL structure--under
the URL space of the arcade app.  Also note that we've ensured to have a ``pk``
for the create and delete views.

Step 3: Integration
~~~~~~~~~~~~~~~~~~~

Admittedly, this part is the part where django-classfaves helps you out the
least.  Well, basically, django-classfaves doesn't help you out at all.  The
reason for this is by design: we don't know how your app is structured or how
you want to use it, so we want to leave this bit completely up to you.

So here's how we did it.  First, on the page where you actually play the game,
we want you to be able to decide that you like it and favorite it.  We also
wanted to make sure that you could do this while you are still playing the
game, so it needed to be asynchronous using JavaScript.

Our first step was to modify the view function for the game playing page.

..sourcecode:: python

    from arcade.models import GameFavorite

    def play(request, game_slug=None):
        # ... some of our view code here
        favorite = False
        if request.user.is_authenticated():
            favorite = GameFavorite.objects.filter(user=request.user,
                game=game).count() > 0
        context = {
            # ... other context here
            'favorite': favorite,
        }
        # ... the rest of our view code here

Just a few lines of code, and we now know whether the user has a favorite on
that specific domain object (the game) or not.

Now, in the template, we do this with the information:

..sourcecode:: python

    {% if user.is_authenticated %}
        {% if favorite %}
            <a href="#" id="favorite_{{ game.id }}" class="favorite fav unfave">Remove as Favorite</a>
        {% else %}
            <a href="#" id="favorite_{{ game.id }}" class="favorite fav fave">Add as Favorite</a>
        {% endif %}
    {% else %}
        <a href="{% url arcade_favorite_create game.id %}" class="fav" id="favorite_{{ game.id }}" class="favorite">Add as Favorite</a>
    {% endif %}

In other words, based on whether the user is authenticated and based on whether
or not they have already favorited the game, we set some classes and urls and
messages on the links.

We also have a bit of JavaScript, that looks like this:

..sourcecode:: javascript

    var add_favorite_handlers = function(base_create, base_delete) {
        $('a.favorite.fave').live('click', function(e) {
            var pk = $(this).attr('id').replace('favorite_', '');
            var url = base_create + pk + '/';
            $.getJSON(url, function(data, textStatus) {
                $('#favorite_' + pk).removeClass('fave').addClass('unfave').text('Remove as Favorite');
            });
            return false;
        });
        $('a.favorite.unfave').live('click', function(e) {
            var pk = $(this).attr('id').replace('favorite_', '');
            var url = base_delete + pk + '/';
            $.getJSON(url, function(data, textStatus) {
                $('#favorite_' + pk).removeClass('unfave').addClass('fave').text('Add as Favorite');
            });
            return false;
        });
    };

I'm not going to go into too much detail about this JavaScript code, except to
say that it takes the base URL for the create and the delete pages, and turns
links with certain classes into AJAX calls into the create and delete views.

Finally, at the bottom of the page, we initialize this JavaScript like so:

.. sourcecode:: html

    <script type="text/javascript">
    $(function() {
        add_favorite_handlers('/games/favorites/create/', '/games/favorites/delete/');
    });
    </script>

And with that, we're done!  Not too bad, huh?  You can browse around `Radisox`
and play a game to see it in action.  Look up at the top right of any game
page to see the favorite/un-favorite button.

.. _`Radiosox`: http://radiosox.com/
"""

setup(
    name='django-classfaves',
    version=VERSION,
    description='django-classfaves is a reusable Django app which uses class-based views for maximum flexibility',
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Django',
        'Environment :: Web Environment',
    ],
    keywords='favorites,faves,django,class-based',
    author='Eric Florenzano',
    author_email='floguy@gmail.com',
    url='http://github.com/ericflo/django-classfaves',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools'],
)