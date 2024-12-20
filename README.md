# Reddit API Development
 Development work against the Reddit public REST API.

 Scratch style notes:
    - 12/19
    Have a working script to push relevant fields over target timeline to a local sql server. Two potential things to look at today, docker and apache airflow. Current plan is to get all 4 services (sql, python, docker, airflow) setup locally before attempting to migrate.
    - 12/18
    Cleaned + commented code was pushed to github. Going to attempt to settup sql server locally
    on my mac, then have the predefined script push to sql.

    Going to start with general clean up + code commenting
    - 12/17
    Got a script working that can pull up to a years worth of data [post_title, post_sub, post_upvote_count, post_upvote_ratio, post_text_body] from the 10
    target subs, only thing that is missing is comments. Considering comments
    have a 1:M relationship with posts, querying will need to be slightly different. Likely will tackle this later.

    Found the bug!:
    For whatever reason, when you use a postID in the 'after' parameter it will return an empty result when the postID
    gets old enough. For the life of me I cannot explain why that might be, however, by testing using datetime values
    in the 'before' and 'after' parameters in the url, I am able to pull the correct amount of historical data. 

    Main goal today is to explore different url parameter options for API calls. (I think) using the '/new/ parameter limits
    to the first 1000 requests.

    - 12/16
    EOD: got a lot closer to creating a script that populates a full years worth of data. I am using the 'after' clause
    within the request URL to filter, but I read online that this only applies to the first 1000 items in a list. I will
    need to shift my filtering strategy to timedate specific queries.

    Switched devn enviroments from PC to mac, setup libraries/authentication/ect.
    Today's goal is to create some type of loop that generates a list of 'postID' (unique identifier for a reddit post) over
    a set duration. Since in a single call I can only pull the most recent 100 posts, the loop will have to modify the url
    and add a time complexity to pull in posts from different dates. Ideal state is a script that pulls postIDs from 10 subs
    over the last year.

    - 12/12
    Currently have a script to authenticate to the reddit API, today if I am able to wrap that into a function and write some GET requests to get some post related data,
    that would be good progress.

    This project will strictly focus on batch data processing, as API call limits do exist against the Reddit API. In order to avoid processing the same posts multiple times
    I aim to implement a store of post ID's that include each new post from the 10 targeted subreddits (most popular for stock analysis). Once a list of postIDs is aggriegated

    Two scripts need to be generated, first a script to pull roughly a weeks (or months?) worth of posts in the 10 target subs, second, a script to run daily (scheduled) to keep
    the data available and up to date. Since I currently do not have a remote server settup (I realize my raspberry pi wont be enough), I need to figure out how to host these
    services prior to scheduled scripts.  

    - 12/11
    Going to start with creating a few simple functions, first targeting GET requests for authentication and pulling relevant data about hot posts.
