import twint

def get(keyword, since, until, geo):
    c = twint.Config()

    c.Search = keyword
    c.Since = since
    c.Until = until
    if geo is not None:
        c.Geo = geo
    c.Limit = 10  # Not working.
    c.Store_object = True
    twint.run.Search(c)
    tweets = twint.output.tweets_list

    return tweets