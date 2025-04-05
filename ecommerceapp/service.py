from ecommerceapp.beans import ProductBean
from ecommerceapp.models import LikeOrDisLikeModel, CommentModel, ProductModel, TransactionModel
from ecommerceapp.sentimentanalyzer import getCommentSentiment


def getAllProducts():

    products = []

    for product in ProductModel.objects.all():

        product.path = str(product.path).split("/")[1]

        comments = CommentModel.objects.filter(product=product.id)

        positive = 0
        negative = 0
        neutral = 0

        for comment in comments:

            centiment = getCommentSentiment(comment.text)

            if centiment == 'positive':
                positive = positive + 1

            if centiment == 'negative':
                negative = negative + 1

            if centiment == 'neutral':
                neutral = neutral + 1

        likes = 0
        dislikes = 0

        for likeordislike in LikeOrDisLikeModel.objects.filter(product=product.id):

            if int(likeordislike.status) == 0:
                dislikes = dislikes + 1
            elif int(likeordislike.status) == 1:
                likes = likes + 1

        bean = ProductBean(product, comments, likes, dislikes, positive, negative, neutral,product.description)

        products.append(bean)

    return products

''''
def findrecommendations(userid):

    myrasactions=TransactionModel.objects.filter(userid=userid)

    otherstrasactions = TransactionModel.objects.exclude(userid=userid)

    for mytransaction in myrasactions:

        for othertransaction in otherstrasactions:

            if mytransaction.productid in othertransaction.productid:

                myrating=TransactionModel.objects.filter(userid=userid,productid=mytransaction.productid).
'''


