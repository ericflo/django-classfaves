API Documentation for django-classfaves Views
---------------------------------------------

This app provides three class-based views for easy integration into your site.
These three views share nearly identical interfaces for the initializer, which
will be described next.

Common Initializer Arguments
============================

Required Arguments
~~~~~~~~~~~~~~~~~~

``favorite``
    This is the first argument to all of the views, and it's your custom
    ``Favorite`` class.

``content_model``
    This is the second argument to all of the views, and it's the model class
    of your domain object.

Optional Arguments
~~~~~~~~~~~~~~~~~~

``fk_name``
    If your ``Favorite`` class has more than one ``ForeignKey`` to your domain
    object, then you will need to specify the name of the field that links
    between the two.

``extra_context``
    Any extra context that you want to be passed into the templates can be
    passed in to this keyword argument.

``context_init``
    A callback function that will create your ``Context`` subclass.  By default
    this is set to ``RequestContext``.  It will be given the request and
    nothing else.  Almost never will you want to change this.

``next_field``
    Defaults to ``next``, if this is included in your POST, then after
    performing an action, the user will be redirected to the given url.  Again,
    this will almost never need to be changed.

``response_mapping``
    Maps ``HTTP_ACCEPT`` parameters to callback functions.  Again, this will
    almost never need to be changed.

``use_transactions``
    Defaults to ``True``.  If ``True``, django-classfaves will wrap any data
    changing actions inside one transaction.


CreateFavorite API
==================

This is a class that allows for the favoriting of your content objects.


Optional Arguments
~~~~~~~~~~~~~~~~~~

``template_name``
    Defaults to ``favorites/created.html``. The name of the template that you
    would like to render.


Required URL Keywords
~~~~~~~~~~~~~~~~~~~~~

``pk``:
    The primary key of your domain object that you would like to create a
    favorite for.


DeleteFavorite API
==================

This is a class that allows for the un-favoriting of your content objects.


Optional Arguments
~~~~~~~~~~~~~~~~~~

``template_name``
    Defaults to ``favorites/deleted.html``. The name of the template that you
    would like to render.


Required URL Keywords
~~~~~~~~~~~~~~~~~~~~~

``pk``:
    The primary key of your domain object that you would like to un-favorite.


UserFavorites API
==================

This is a class that can produce a list of a user's favorite content objects.


Optional Arguments
~~~~~~~~~~~~~~~~~~

``template_name``
    Defaults to ``favorites/list.html``. The name of the template that you
    would like to render.

``extra_filter``
    A function that is given a ``QuerySet`` instance and must return another
    ``QuerySet``.  It can be useful for limiting the results that are returned
    to only the ones that match a certain specification.  Defaults to
    ``lambda x: x``.


Optional URL Keywords
~~~~~~~~~~~~~~~~~~~~~

``username``:
    The ``username`` of the user whose favorites you would like to view.  If
    this parameter is left out, then this view will list the favorites for the
    currently logged-in user.