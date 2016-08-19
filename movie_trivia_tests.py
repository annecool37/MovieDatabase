# author: Chia-An Chen
# CIT 590, Spring 2015, HW4
# Date: 02/13/2015

### movie_trivia_tests.py ###

from movie_trivia import *
import unittest

class TestMovies(unittest.TestCase):

    movieDb = {}
    ratingDb = {}

    def setUp(self):
        self.movieDb = create_actors_DB('movies.txt')
        self.ratingDb = create_ratings_DB('moviescores.csv')

    def testcreate_actors_DB(self):
        self.assertTrue('Sleepers' in self.movieDb.get('Brad Pitt'))
        self.assertTrue('Troy' in self.movieDb.get('Brad Pitt'))
        self.assertTrue("You've Got Mail" in self.movieDb.get('Tom Hanks'))

    def testcreate_ratings_DB(self):
        ratingDb = self.ratingDb
        self.assertTrue(['12','62'], ratingDb['Original Sin'])
        self.assertTrue(['100','98'], ratingDb['The Godfather'])
                                                           
    def testinsert_actor_info(self):
        # present actor, new movie
        insert_actor_info('Jennifer Lawrence', 'Hunger Games 2', self.movieDb)
        self.assertTrue(set(['Silver Linings Playbook', 'X Men: First Class', 'Hunger Games', 'Hunger Game 2', "Winter's Bone"]), self.movieDb['Jennifer Lawrence'])

        # present actor, present movie
        insert_actor_info('Jennifer Lawrence', 'Hunger Games', self.movieDb)
        self.assertTrue(set(['Silver Linings Playbook', 'X Men: First Class', 'Hunger Games', "Winter's Bone"]), self.movieDb['Jennifer Lawrence'])
        
        # new actor, new movie
        insert_actor_info('Anne Chen', 'Adventure Time', self.movieDb)
        self.assertTrue(set(['Adventure Time']), self.movieDb['Anne Chen'])
        
    def testinsert_rating(self):
        insert_rating('The Godfather', ['34','55'], self.ratingDb)
        self.assertTrue(['34','55'], self.ratingDb['The Godfather'])
        
    def testdelete_movie(self):
        delete_movie('The Godfather', self.movieDb, self.ratingDb)
        self.assertTrue(set(['Annie Hall', 'The Godfather Part II', "Something's Gotta Give"]), self.movieDb['Diane Keaton'])
        self.assertEqual([], self.ratingDb['The Godfather']) 

    def testselect_where_actor_is(self):
        self.assertEqual(set(['Silver Linings Playbook', 'X Men: First Class', 'Hunger Games', "Winter's Bone"]), set(select_where_actor_is('Jennifer Lawrence', self.movieDb)))
        self.assertEqual(set(['Seven', 'Sleepers', 'Mr & Mrs Smith', 'Troy', 'Meet Joe Black', 'Oceans Eleven']), set(select_where_actor_is('Brad Pitt', self.movieDb)))
        self.assertEqual(set([]), set(select_where_actor_is('Anne Chen', self.movieDb))) # return empty set if no such actor
        
    def testselect_where_movie_is(self):
        self.assertEqual(set(['Brad Pitt', 'Dustin Hoffman', 'Kevin Bacon']), set(select_where_movie_is('Sleepers', self.movieDb)))
        self.assertEqual(set(['Keira Knightley', 'Benedict Cumberbatch']), set(select_where_movie_is('The Imitation Game', self.movieDb)))
        self.assertEqual(set([]), set(select_where_actor_is('xhjfklnwh', self.movieDb))) # return empty set if no such movie 

    def testselect_where_rating_is(self):
        self.assertTrue(self.ratingDb.keys(), select_where_rating_is(0,'>',True, self.ratingDb))
        self.assertTrue(['Wild Wild West', 'Original Sin', 'Assassins'], select_where_rating_is(20,'<',True, self.ratingDb))
        self.assertEqual([], select_where_rating_is(0,'<',True, self.ratingDb))
        self.assertEqual([], select_where_rating_is(101,'>',True, self.ratingDb))
        self.assertTrue(['The Avengers', 'Mission Impossible', 'Ted'], select_where_rating_is(98,'>',False, self.ratingDb))

    def testget_co_actors(self):
        self.assertTrue('Amy Adams' in get_co_actors('Tom Hanks', self.movieDb))
        self.assertFalse('Killian Chou' in get_co_actors('Tom Hanks', self.movieDb))
        self.assertEqual([], get_co_actors('Louis Jordan', self.movieDb))
        
    def testget_common_movie(self):
        self.assertTrue('Catch Me If You Can' in get_common_movie('Amy Adams','Tom Hanks', self.movieDb))
        self.assertFalse('The Devil Wears Prada' in get_common_movie('Meryl Streep','Bradley Cooper',  self.movieDb))
        self.assertFalse('High School Musical'in get_common_movie('Leonardo Di Caprio','Tom Hanks',  self.movieDb))
        self.assertEqual([], get_common_movie('Jennifer Lawrence', 'Brad Pitt', self.movieDb))

    def testcritics_darling(self):
        self.assertTrue(['Joan Fontaine'], critics_darling(self.movieDb, self.ratingDb))
        self.assertFalse([],critics_darling(self.movieDb, self.ratingDb))
        
    def testaudience_darling(self):
        self.assertTrue(['Diane Keaton'], audience_darling(self.movieDb, self.ratingDb))
        self.assertFalse([],audience_darling(self.movieDb, self.ratingDb))
        
    def testfind_highest_ratings(self):
        self.assertTrue(['Joan Fontaine'],find_highest_ratings(self.movieDb, self.ratingDb,0))
        self.assertTrue(['Diane Keaton'],find_highest_ratings(self.movieDb, self.ratingDb,1))
        self.assertFalse([],find_highest_ratings(self.movieDb, self.ratingDb,0))
               
    def testfind_keys(self):
        dic={'a':12, 'b':13, 'c':15, 'd':15}
        self.assertEqual(['c', 'd'],find_keys(dic))
        
    def testget_common_actors(self):
        self.assertTrue('Amy Adams'in get_common_actors('Enchanted', 'Doubt', self.movieDb))
        self.assertFalse('Jennifer Lawerence'in get_common_actors('Hunger Games', 'Enchanted', self.movieDb))
        self.assertFalse('Amy Adams' in get_common_actors('High School Musical', 'Julie and Julia', self.movieDb))
        self.assertEqual([], get_common_actors('Ted', 'Seven', self.movieDb))
        
    def testgood_movies(self):
        # both ratings < 85
        self.assertFalse('Bone Colletor' in list(good_movies(self.ratingDb)))
        # only one rating >= 85
        self.assertFalse('I am Sam' in list(good_movies(self.ratingDb)))
        self.assertFalse('Titanic' in list(good_movies(self.ratingDb)))
        # both rating >= 85
        self.assertTrue('Rain Man' in list(good_movies(self.ratingDb)))
        
    def testall_movies(self):
        self.assertTrue('The Godfather' in all_movies(self.movieDb, self.ratingDb))
        self.assertFalse('Jennifer Lawerence' in all_movies(self.movieDb, self.ratingDb))

    def testget_bacon(self):
        self.assertEqual(0, get_bacon('Kevin Bacon', self.movieDb))
        self.assertEqual(1, get_bacon('Kevin Costner', self.movieDb))
        self.assertEqual(2, get_bacon('Shirley Maclaine', self.movieDb))
        
## no unittest for enterActor, enterMovie, and print_intro          ##
## because they either include raw_input nor only print statement   ##
                  
unittest.main()
