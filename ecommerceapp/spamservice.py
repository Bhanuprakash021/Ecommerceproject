from ecommerceapp.models import CommentModel, RegistrationModel
from ecommerceapp.sentimentanalyzer import getCommentSentiment

def isspamuserbasedonproduct(pid):

    spamusers=[]

    for user in RegistrationModel.objects.all():

        print("in for 1",user.username)
        isspamuser=False

        comments = CommentModel.objects.filter(user=user.username,product=pid)

        dates =set()
        for comment in comments:
            print("in for 2",comment)
            dates.add(str(comment.datetime.date().day)+"_"+str(comment.datetime.date().month)+"_"+str(comment.datetime.date().year))

        print("dates",dates)

        for date in dates:

            print("in for 3",date)

            reviews = []

            for cmt in comments:
                cmtdate=str(cmt.datetime.date().day)+"_"+str(cmt.datetime.date().month)+"_"+str(cmt.datetime.date().year)
                if cmtdate == date:
                    reviews.append(cmt)

            print("reviews:",reviews)

            sentimentlist = []

            for rev in reviews:
                sentiment = getCommentSentiment(rev.text)
                sentimentlist.append(sentiment)

            print("Sentiment:",sentimentlist)

            positives = sentimentlist.count("positive")
            negitives = sentimentlist.count("negative")

            if positives >= 5 and negitives == 0:
                isspamuser = True

            if negitives >= 5 and positives == 0:
                isspamuser =True

            if isspamuser:
                spamusers.append(user.username)

    users=[]
    for user in RegistrationModel.objects.all():
        if user.username in spamusers:
            users.append(user)

    return users