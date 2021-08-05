import alltweets

tweets = alltweets.get("#フィールドホッケー #春から筑波", "2020-03-20", "2021-04-03", "36.111389,140.103889,5km")

for tweet in tweets:
    print(vars(tweet))