
import matplotlib.pyplot as plt
import pandas as pd
import snscrape
import snscrape.modules.twitter as sntwitter
import itertools




def twitter_scraper_old(keystring, start_date, end_date, place_name='', from_tweet ='',n_tweets=100):
    """
    keystring (str): word or expression to make a query (always use ingle comma , exemple => 'Car' )
    start_dare (str) : begin of the search (%Y-%m-%d) (always use ingle comma , exemple => '2022-02-01' )
    end_date (str) : end of the search (%Y-%m-%d) (always use ingle comma , exemple => '2022-02-02' )
    from_tweet (str) : account to make the search on (always use ingle comma , exemple => 'fea_dev'  , it does not need the @)
    n_tweets (int)  : maximum numbers of tweets to download

    return => Dataframe

    """



    search = f"{keystring} from:{from_tweet} near:{place_name} since:{start_date} until:{end_date}"

    # the scraped tweets, this is a generator
    scraped_tweets = sntwitter.TwitterSearchScraper(search).get_items()

    # slicing the generator to keep only the first 100 tweets
    sliced_scraped_tweets = itertools.islice(scraped_tweets, n_tweets)

    # convert to a DataFrame and keep only relevant columns
    #df = pd.DataFrame(sliced_scraped_tweets)[['date', 'content']]
    df = pd.DataFrame(sliced_scraped_tweets)

    return(df)

def twitter_scraper_old_v2(keystring, start_date, end_date, place_name='', from_tweet ='',n_tweets=100):
    """
    keystring (str): word or expression to make a query (always use ingle comma , exemple => 'Car' )
    start_dare (str) : begin of the search (%Y-%m-%d) (always use ingle comma , exemple => '2022-02-01' )
    end_date (str) : end of the search (%Y-%m-%d) (always use ingle comma , exemple => '2022-02-02' )
    from_tweet (str) : account to make the search on (always use ingle comma , exemple => 'fea_dev'  , it does not need the @)
    n_tweets (int)  : maximum numbers of tweets to download

    return => Dataframe

    """



    search = f"{keystring} from:{from_tweet} near:{place_name} since:{start_date} until:{end_date}"

    tweets_list3 = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(search).get_items()):
        if i>n_tweets:
            break

        tt_dict = tweet.__dict__ #transforming the Tweet object in a dict

        classes_sns_names = snscrape.modules.twitter.__all__  #names of sntwitter objects 

        #transforming these objects in  dicts
        problematic_columns = [] 
        
        for k in tt_dict.keys():
            if tt_dict[k].__class__.__name__ in classes_sns_names:
                problematic_columns.append({k:tt_dict[k].__dict__})

        #wrapping all together in a better way
        itens_to_remove = [list(x)[0] for x in problematic_columns]
        
        for n in itens_to_remove :
            tt_dict.pop(n)
        
        for j in problematic_columns:
            tt_dict.update(j)
                
        #Transforming the dicts into DataFrame and then appending it to a list
        tweets_list3.append(pd.json_normalize(tt_dict))
        
    # Creating a dataframe from the list of tweets dfs above
    tweets_df3 = pd.concat(tweets_list3,axis=0)


    return(tweets_df3)

def twitter_scraper_old_v3(search,n_tweets=100):
    """
    keystring (str): word or expression to make a query (always use ingle comma , exemple => 'Car' )
    start_dare (str) : begin of the search (%Y-%m-%d) (always use ingle comma , exemple => '2022-02-01' )
    end_date (str) : end of the search (%Y-%m-%d) (always use ingle comma , exemple => '2022-02-02' )
    from_tweet (str) : account to make the search on (always use ingle comma , exemple => 'fea_dev'  , it does not need the @)
    n_tweets (int)  : maximum numbers of tweets to download

    return => Dataframe

    """
    
    # the scraped tweets, this is a generator
    scraped_tweets = sntwitter.TwitterSearchScraper(search).get_items()

    # slicing the generator to keep only the first 100 tweets
    sliced_scraped_tweets = itertools.islice(scraped_tweets, n_tweets)

    # convert to a DataFrame and keep only relevant columns
    #df = pd.DataFrame(sliced_scraped_tweets)[['date', 'content']]
    df = pd.DataFrame(sliced_scraped_tweets)

    return(df)

def twitter_scraper(search,n_tweets=100):
    """
    keystring (str): query for TwitterSearchScraper
    n_tweets (int)  : maximum numbers of tweets to download

    return => Dataframe

    """

    tweets_list3 = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(search).get_items()):
        if i>n_tweets:
            break

        tt_dict = tweet.__dict__ #transforming the Tweet object in a dict

        classes_sns_names = snscrape.modules.twitter.__all__  #names of sntwitter objects 

        #transforming these objects in  dicts
        problematic_columns = [] 
        
        for k in tt_dict.keys():
            if tt_dict[k].__class__.__name__ in classes_sns_names:
                problematic_columns.append({k:tt_dict[k].__dict__})

        #wrapping all together in a better way
        itens_to_remove = [list(x)[0] for x in problematic_columns]
        
        for n in itens_to_remove :
            tt_dict.pop(n)
        
        for j in problematic_columns:
            tt_dict.update(j)
                
        #Transforming the dicts into DataFrame and then appending it to a list
        tweets_list3.append(pd.json_normalize(tt_dict))
        
    # Creating a dataframe from the list of tweets dfs above
    tweets_df3 = pd.concat(tweets_list3,axis=0)


    return(tweets_df3)



#df_tweets = twitter_scraper('Bitcoin since:2014-01-01 until:2022-02-25',n_tweets=  100)
#df_tweets = twitter_scraper_old_v3("'Bitcoin' since:2020-01-01 until:2022-02-27",n_tweets=  1000)

df_tweets = twitter_scraper_old(keystring = 'Bitcoin' , start_date = '2014-01-01' ,end_date='2022-02-25',n_tweets =  100)

df_tweets.to_csv("bitcoin_tweets_complete_v3.csv",index=False)