import fresh_tomatoes
import media

toy_story = media.Movie("Toy Story", "A story of a boy and his toys that come to life.",\
            "https://upload.wikimedia.org/wikipedia/en/thumb/1/13/Toy_Story.jpg/220px-Toy_Story.jpg",\
            "www.youtube.com/watch?v=KYz2wyBy3kc")

#print (toy_story.storyline)

avatar = media.Movie("Avatar", "A marine on an alien planet.",\
            "https://upload.wikimedia.org/wikipedia/en/thumb/b/b0/Avatar-Teaser-Poster.jpg/220px-Avatar-Teaser-Poster.jpg",\
            "www.youtube.com/watch?v=cRdxXPV9GNQ")

#avatar.show_trailer()
titanic = media.Movie("Titanic", "A great love story",\
                      "https://upload.wikimedia.org/wikipedia/en/thumb/2/22/Titanic_poster.jpg/220px-Titanic_poster.jpg",\
                      "")

idiots = media.Movie("3 Idiots","","https://upload.wikimedia.org/wikipedia/en/thumb/d/df/3_idiots_poster.jpg/220px-3_idiots_poster.jpg"\
                      ,"")

ff7 = media.Movie("Fast and Furious 7","","https://upload.wikimedia.org/wikipedia/en/thumb/b/b8/Furious_7_poster.jpg/220px-Furious_7_poster.jpg"\
                  ,"")


movies = [toy_story, avatar, titanic, idiots, ff7]
#fresh_tomatoes.open_movies_page(movies)
print media.Movie.__module__
