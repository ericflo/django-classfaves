Philosophy behind django-classfaves
-----------------------------------

There are many other favoriting apps in existence in the Django reusable app
ecosystem.  django-classfaves is not the easiest to use.  This project was born
out of an increasing dissatisfaction with the way that most reusable apps are
being constructed.  That is, all models have ``GenericForeignKeys`` attached to
them, and you're allowed to attach those generic keys to anything in any of
your apps.

What this leaves us with is a situation where even large sites have just a few
domain objects, and everything else is generically attached to those objects.
This makes the database schema confusing and can lead to some very complex
queries, as well as making performance suffer.

For an app like favorites, in my experience there's usually only one domain
object that needs to be favorited, so all of those generic keys have no real
value beyond that they are easy to set up and use.  This project attempts to
address this by providing you with the ability to very simply create your own
``Favorite`` models, and place them where they make sense: in the app where
your domain objects live.

This project is very much still an experiment.  I do not think that this is
the be-all end-all way of doing things, but I do think that it is a step
in the right direction.