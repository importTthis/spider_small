from db import MySQL
from snownlp import SnowNLP
from snownlp import sentiment

mysql = MySQL()


# praise_f = open("data/praise_small_1.txt", "w" ,encoding='utf-8')


for i in range(13, 14):
    sql = f"select * from small_{i}"

    mysql.cursor.execute(sql)
    results = mysql.cursor.fetchall()
    bad_review_f = open(f"data/bad_review_small_{i}_test.txt", "w", encoding='utf-8')
    # bad_review_f = open(f"train/bad_review.txt", "a", encoding='utf-8')

    for result in results:
        content = result.get("rateContent")
        if "没有填写" not in content:
            obj = SnowNLP(content)

            # f = praise_f if obj.sentiments > 0.4 else bad_review_f
            # f.write(f'{content}  {obj.sentiments} \n')
            # data = {
            #     "content": content,
            #     "sentiment_coefficient": obj.sentiments
            # }
            # mysql.insert('small_bad_review_1', data)
            if obj.sentiments < 0.1:
                bad_review_f.write(f'{content} {obj.sentiments}\n')
                score = round(obj.sentiments, 6)
                if score == 0:
                    score = 0
                data = {
                    "content": content,
                    "sentiment_coefficient": score
                }
                mysql.insert(f'small_bad_review_{i}', data)
    bad_review_f.close()

# praise_f.close()
