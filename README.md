# Reddit API Development
 Development work against the Reddit public REST API.

 Scratch style notes:
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
