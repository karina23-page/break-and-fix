from movies import app, db, Movie, Scene


with app.app_context():

    # prevents duplicates
    if Movie.query.filter_by(
        slug="pans-labyrinth"
    ).first():

        print("Movies already seeded.")
        exit()

    pan = Movie(
        title="Pan's Labyrinth",
        slug="pans-labyrinth",

        poster="/static/images/movie2.jpg",
        background="/static/images/movie1.jpg",

        short_description="""
        A dark fantasy story about childhood,
        war and the painful journey into adulthood.
        """,

        soundtrack="Javier Navarrete - Nana de la Princesa",

        snack="Grapes, pomegranates and a ham sandwich",

        main_thoughts="""
I absolutely love this movie. Its atmosphere feels magical,
yet deeply dark and heartbreaking at the same time.

The way I interpret Pan's Labyrinth is as a story about
the painful transition from childhood into adulthood.

Throughout the film, magical creatures represent childhood,
imagination and innocence, while the brutality of war,
embodied by Captain Vidal, represents the harsh reality
of adulthood.

Ofelia's three tasks symbolize important steps in growing up.
This is not merely a fantasy film, but a deeply symbolic story
about morality, identity, sacrifice and maturity.

It is a true work of art and a movie I will always come back to.
"""
    )

    db.session.add(pan)
    db.session.commit()

    scenes = [

        Scene(
            movie_id=pan.id,

            title="The Giant Toad (The Gold Key)",

            image="/static/images/toad.webp",

            description="""
Ofelia enters the roots of the sacred tree and confronts
the giant poisonous toad.

To me, this scene represents confronting one's shadow.
The tree symbolizes the self, while the toad represents
the hidden parts of ourselves that we deny or fear.

Facing these truths is unpleasant, yet necessary for growth.
"""
        ),

        Scene(
            movie_id=pan.id,

            title="The Pale Man (The Silver Dagger)",

            image="/static/images/pale-man.webp",

            description="""
Despite being forbidden from touching the feast,
Ofelia eats two grapes and awakens the Pale Man.

I interpret this scene as a lesson in temptation and sacrifice.
Sometimes we must say no to immediate pleasures in order
to achieve something greater.

What makes this scene beautiful is that Ofelia fails.
It reminds us that mistakes are part of being human.
"""
        ),

        Scene(
            movie_id=pan.id,

            title="The Ultimate Sacrifice (The Portal)",

            image="/static/images/pan.webp",

            description="""
Pan asks Ofelia to sacrifice her baby brother.

Instead, she refuses.

This moment represents true maturity and moral independence.
Even when promised another world, she trusts her own judgment
and chooses compassion over self-preservation.
"""
        )
    ]

    db.session.add_all(scenes)

    db.session.commit()

    print("Pan's Labyrinth seeded successfully.")