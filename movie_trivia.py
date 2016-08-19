# author: Chia-An Chen
# CIT 590, Spring 2015, HW4
# Date: 02/13/2015

### movie_trivia.py ###

### Create Dictionaries ###
import csv
def create_actors_DB(actor_file):
    '''Create a dictionary keyed on actors from a text file'''
    f = open(actor_file)
    movieInfo = {}
    for line in f:
        line = line.rstrip().lstrip()
        actorAndMovies = line.split(',')
        actor = actorAndMovies[0]
        movies = [x.lstrip().rstrip() for x in actorAndMovies[1:]]
        movieInfo[actor] = set(movies)
    f.close()
    return movieInfo

def create_ratings_DB(ratings_file):
    '''make a dictionary from the rotten tomatoes csv file'''
    scores_dict = {}
    with open(ratings_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            scores_dict[row[0]] = [row[1], row[2]]
    return scores_dict

### Utility Functions ###
def insert_actor_info(actor, movies, movie_Db):
    '''insert/update new movies to their list if actor is already present'''
    movies_set = movie_Db.get(actor, set([]))
    movies_set.add(movies)
    movie_Db[actor]=movies_set

def insert_rating(movie, ratings, ratings_Db):
    '''insert/update ratings_Db'''
    ratings_Db[movie] = list(ratings)

def delete_movie(movie, movie_Db, ratings_Db):
    '''delete all information from the database that corresponds to this movie'''
    # delete movie in {actor: movies} in movie_Db
    listOfActors = select_where_movie_is(movie, movie_Db)
    for i in range (0,len(listOfActors)):
        # print listOfActors[i]
        movie_Db[listOfActors[i]].remove(movie)
        
    # delete ratings in {movie: ratings} in rating_Db
    if_movie_present = ratings_Db.get(movie,0)
    if if_movie_present !=0:
        # instead of del ratings_Db[movie], keep the key in dictionary
        ratings_Db[movie]=[]
    
def select_where_actor_is(actorName, movie_Db):
    '''given an actor return the list of all movies'''
    listOfMovies=[]
    for name in movie_Db.keys():
        if actorName.lower()== name.lower():
            listOfMovies=list(movie_Db[actorName])
    return listOfMovies

def select_where_movie_is(movieName, movie_Db):
    '''given a movie, return the list of all actors'''
    listOfActors=[]
    for i in range (0, len(movie_Db)):
        if list(movie_Db.values()[i]).count(movieName) != 0:
            listOfActors.append(movie_Db.keys()[i])                  
    return listOfActors
    
def select_where_rating_is(targeted_rating, comparison, is_critic, ratings_Db):
    '''return a list of movies that satisfy an inequality or equlity
    based on the comparison argument and the targeted rating argument'''
    idx = 0
    if is_critic is False:
        idx=1
        
    listOfMovies=[]
    for movie, rating in ratings_Db.items():
        if comparison is '>':
            if int(rating[idx]) > targeted_rating:
                listOfMovies.append(movie)
        elif comparison is '<':
            if int(rating[idx]) < targeted_rating:
                listOfMovies.append(movie)
        elif comparison is '=':
            if int(rating[idx]) == targeted_rating:
                listOfMovies.append(movie)
    return listOfMovies

### Functions for User and Helper Funtions ###
def get_co_actors(actorName, moviedb):
    '''get co-actors of an actor'''
    coActors=set([])
    listOfMovies = select_where_actor_is(actorName, moviedb)
    for movie in listOfMovies:
        actors = set(select_where_movie_is(str(movie), moviedb))
        coActors = coActors.union(actors)
    # removie actor itself from the set
    coActors.discard(actorName)
    return list(coActors)
        
def get_common_movie(actor1, actor2, moviedb):
    '''find common movies in two actors'''
    movie1 = set(select_where_actor_is(actor1, moviedb))
    movie2 = set(select_where_actor_is(actor2, moviedb))
    return list(movie1.intersection(movie2))

def critics_darling(movie_Db, ratings_Db):
    '''finding the actor whose movies have the highest average rating, as per the critics'''
    return find_highest_ratings(movie_Db, ratings_Db, 0)

def audience_darling(movie_Db, ratings_Db):
    '''finding the actor whose movies have the highest average rating, as per the audience'''
    return find_highest_ratings(movie_Db, ratings_Db, 1)

def find_highest_ratings(movie_Db, ratings_Db, is_critic):
    '''find highest average ratings in the database for actors'''
    actor_rating={}
    for actor in movie_Db.keys():
        listOfMovies = select_where_actor_is(actor, movie_Db)
        rating=[]
        for i in range (0,len(listOfMovies)):
            movie=listOfMovies[i]
            if movie in ratings_Db.keys():
                rating.append(ratings_Db[movie][is_critic])
        if len(rating) !=0:
            rating=map(float, rating)
            # average the ratings
            average_rating=sum(rating)/len(rating)
        else:
            # if no ratings, assign to be 0
            average_rating=0
        actor_rating[actor]=average_rating
    # find the actors with highest average_rating
    highRatingActors = find_keys(actor_rating)
    return highRatingActors
       
def find_keys(dic):
    '''find keys with highest values in a dictionary'''
    max_val=max(dic.values())
    keys = [key for key,value in  dic.items() if value == max_val]
    return keys
    
def good_movies(ratings_Db):
    '''return a set of movies that has ratings >= 85 from both critics and audience'''
    set_critic = set(select_where_rating_is(84,'>', True, ratings_Db))
    set_audi = set(select_where_rating_is(84,'>', False, ratings_Db))
    setOfMovies=set_critic.intersection(set_audi)
    return setOfMovies

def get_common_actors(movie1, movie2, movie_Db):
    '''find common actors in two movies'''
    actor1 = set(select_where_movie_is(movie1, movie_Db))
    actor2 = set(select_where_movie_is(movie2, movie_Db))
    return list(actor1.intersection(actor2))

def all_movies(movie_Db, rating_Db):
    '''list all movies in both database'''
    setOfMovies=set()
    for i in range (0, len(movie_Db)):
        movie_set = movie_Db.values()[i]
        setOfMovies=setOfMovies.union(movie_set)
    movies_in_ratings_Db=set(rating_Db.keys())
    allMovies=list(setOfMovies.union(movies_in_ratings_Db))
    return allMovies

def enterActor(movie_Db):
    '''ask user to input actor'''
    checkActor = False
    while checkActor is False:
        actor = raw_input("Please enter an actor: ")
        for actorName in movie_Db.keys():
            if actorName.lower() == actor.lower():
                checkActor = True
                return actorName
        print "not present"

def enterMovie(allMovies):
    '''ask user to input movie'''
    checkMovie = False
    while checkMovie is False:
        movie = raw_input("Please enter a movie: ")
        for movieName in allMovies:
            if movie.lower() == movieName.lower():
                checkMoive = True
                return movieName
        print "not present"

def get_bacon(actor, movieDb):
    '''get the Bacon number of an actor'''
    co_actor = {}
    # Kevin Bacon himself has a bacon number of 0
    if actor == 'Kevin Bacon':
        return len(co_actor)

    else:
        # the first degree actors
        co_actor[1] = get_co_actors(actor, movieDb)
        if 'Kevin Bacon' in co_actor[1]:
            return len(co_actor)
        
        # coactors of (N-1)th degree coactor
        else:
            N = 2
            while N != 0:
                co_actor[N] = []
                for actorName in co_actor[N-1]:
                    co_actor[N].extend(get_co_actors(actorName, movieDb))
                co_actor[N] = list(set(co_actor[N]))
                if 'Kevin Bacon' in co_actor[N]:               
                    N = 0 
                else:
                    N += 1
            return len(co_actor)
        
def print_intro():
    '''print introduction paragraph'''
    print'''
Here are some options for you: \n
enter 1 for a list of all actors that an actor of your choice has ever worked with
enter 2 for a list of common movies where both two actors of your choice were cast
enter 3 for a list of common actors in two movies of your choice
enter 4 for a list of the actors with highest average critic ratings 
enter 5 for a list of the actors with highest average audience ratings
enter 6 for movies of our recommendation
enter 7 to get an actor's Bacon number
enter q to quit the program
        '''

### Main Code ###
def main():
    '''main code'''
    # create databases
    movie_Db = create_actors_DB('movies.txt')
    ratings_Db = create_ratings_DB('moviescores.csv')

    # get a list all movies from both databases
    allMovies=all_movies(movie_Db, ratings_Db)

    # print welcome message   
    print'''
Welcome to the movie database!
This database contains actor info and movie ratings'''

    # provide user with options
    run = True
    while run is True:
        print_intro()
        option = raw_input("Please enter an option.\n")
        if option =='1':
            # list all actors that an actor of user's choice has ever worked with
            actorName = enterActor(movie_Db)
            coActors = get_co_actors(actorName, movie_Db)
            if coActors ==[]:
                print "Oops! In our database,", actorName, "has worked with no one."
            else:
                print actorName, "has worked with:",coActors
        
        elif option =='2':
            # list common movies where both two actors of user's choice were cast
            actor1 = enterActor(movie_Db)
            actor2 = enterActor(movie_Db)
            while actor2 == actor1:
                print "Please enter a different actor from the first one."
                actor2 = enterActor(movie_Db)
                
            listOfMovies = get_common_movie(actor1, actor2, movie_Db)
            if listOfMovies ==[]:
                print "There's no common movies between",actor1, "&", actor2
            else:
                verb=' are: '
                if len(listOfMovies)==1:
                    verb=' is: '
                print "The common movies that", actor1, "&", actor2, verb, listOfMovies
                       
        elif option =='3':
            # list of common actors in two movies of user's choice
            movie1 = enterMovie(allMovies)
            movie2 = enterMovie(allMovies)
            while movie2 == movie1:
                print "Please enter a different movie from the first one."
                movie2 = enterMovie(allMovies)

            listOfCommonActors = get_common_actors(movie1, movie2, movie_Db)
            if listOfCommonActors ==[]:
                print "There's no common actors between", movie1, "&", movie2
            else:
                print listOfCommonActors, "starred in both", movie1, "&", movie2
           
        elif option =='4':
            # list of the actors with highest average critic ratings
            print critics_darling(movie_Db, ratings_Db), "is critics' fav actor!"
            
        elif option =='5':
            # list of the actors with highest average audience ratings
            print audience_darling(movie_Db, ratings_Db), "is audiences' fav actor!"
            
        elif option =='6':
            # movies of our recommendation (both ratings >= 85 )
            print list(good_movies(ratings_Db))
            print '''\n Our recomendations are based on high ratings from both critics and audiences.\n Hope you will like it :)\n'''
           
        elif option =='7':
            # get an actor's Bacon number
            actorName = enterActor(movie_Db)
            bacon_number = get_bacon(actorName, movie_Db)
            print actorName, "has a bacon number of", bacon_number

        elif option =='q':
            # to quit the program
            print "quit the program"
            run = False

        else:
            print "Sorry, please enter a valid option."

if __name__ == '__main__':
    main()
