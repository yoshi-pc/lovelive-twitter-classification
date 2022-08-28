import joblib

tweet_contents = joblib.load("./tweet_contents.jblb")


page_data = {}
content_dict = dict(
    mus_content = "mus",
    aqours_content = "aqours",
    nijigaku_content = "nijigaku",
    liella_content = "liella",
    others_content = "others"
)

for cont, group in content_dict.items():
    temp_text = []
    for single_tweet in tweet_contents[group]:
        img_class = "p-2 col-md-3"
        img_link = "".join(["<img src=\"" + item + f"\" class=\"{img_class}\" />" for item in single_tweet["images"]])
        text_origin = single_tweet["text"].replace("\n", "<br />")
        temp_text.append(
            f"""
            <span class=\"mt-2 mb-2\"><a href=\"https://twitter.com/LoveLive_staff/status/{single_tweet['id']}/\" class="btn btn-primary">original tweet</a></span><br />
            <p class=\"pt-1\">{text_origin}</p>
            {img_link}<br />
            <span class="badge rounded-pill bg-secondary">{single_tweet['time']}</span>
            """
        )
    page_data[cont] = temp_text

with open("./server/index_template.html", "r") as f:
    html = f.read()

for cont, group in content_dict.items():
    html = html.replace("{% " + cont + " %}", "<hr />".join(page_data[cont]))

with open("./server/index.html", "w") as f:
    f.write(html)
pass