# web-image-crawler

This repo includes code to download images from google web image search results. You can modify the javascript embedded in the python code so that it works for bing, yandex, flikr etc. also. They more or less follow the same DOM.

`interactive.py` lets you download images in an interactive fashion.
`api.py` takes a text file (like sample.txt) where queries can be mentioned to download.

Since everything is in python, the dependencies can be easily installed. You can change the driver from Firefox to Chrome. Note that driver preferences will need to be changed if you switch the browser.

Since I got a few e-mails asking how I downloaded images from the internet for a couple of my papers, I decided to make the code public. However, I would recommend that you do not use it for commercial purposes and use the API which the search engines provide. This API is made available so that correct web-data is collected for research purposes. I observed that the results from the Google/Bing/Flickr APIs is different from what is shown in the browser. This code gets you the data what a user will actually see in a browser.
