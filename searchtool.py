import praw
from prawcore import NotFound
from textwrap import wrap

reddit = praw.Reddit(client_id="",
                     client_secret="",
                     user_agent="Subreddit questions search tool",
                     username="",
                     password="")

# Gets user input for subreddit and search criteria
foundSubreddit = False
while not foundSubreddit:
    school = input("Enter the schools subreddit you would like to search: ")
    try:  # Checks if sub reddit exists
        reddit.subreddits.search_by_name(school, exact=True)
        foundSubreddit = True
    except NotFound:
        print("Subreddit not found")

search = input("Enter the topic you would like to search, the more specific the better results: ")

titles = []
topResponse = []

subreddit = reddit.subreddit(school)

# Runs through the top 5 submissions of the search criteria
for submission in subreddit.search(search, "relevance", limit=6):
    # If there are no responses to the post it will be skipped over
    if submission.num_comments == 0:
        continue

    titles.append(submission.title)

    topScore = 0
    topComment = ""
    for comment in submission.comments:  # Runs through every comment in the post to find the most upvoted one
        commentText = comment.body
        currentScore = comment.score
        if currentScore > topScore:
            topComment = commentText
            topScore = comment.score
    wrappedComment = wrap(topComment, 85)  # Wraps comments to format text file
    topResponse.append(wrappedComment)


# Writes all data from the posts to a file for viewing
file = open("responses.txt", "w")
file.write("Responses for \"" + search + "\" search in the " + school + " subreddit\n")
file.write("----------------------------------------------------------\n")
for k in range(0, len(titles)):
    file.write("Submission " + str(k + 1) + ": " + titles[k] + "\n")
    file.write("Top response: ")
    for x in topResponse[k]:
        file.write(x + "\n")
    file.write("\n")
file.close()
