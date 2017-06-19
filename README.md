# web-image-crawler

This repo includes code to download images from google web image search results. You can modify the javascript embedded in the python code so that it works for bing, yandex, flikr etc. also. They more or less follow the same DOM.

`interactive.py` lets you download images in an interactive fashion.
`api.py` takes a text file (like sample.txt) where queries can be mentioned to download.

Since everything is in python, the dependencies can be easily installed. You can change the driver from Firefox to Chrome. Note that driver preferences will need to be changed if you switch the browser.

Since I got a few e-mails asking how I downloaded images from the internet for a couple of my papers (mentioned below), I decided to make the code public. However, I would recommend that you do not use it for commercial purposes and use the API which the search engines provide. This API is made available so that correct web-data is collected for research purposes. I observed that the results from the Google/Bing/Flickr APIs is different from what is shown in the browser. This code gets you the data what a user will actually see in a browser.


    @inproceedings{singh2015selecting,
      title={Selecting relevant web trained concepts for automated event retrieval},
      author={Singh, Bharat and Han, Xintong and Wu, Zhe and Morariu, Vlad I and Davis, Larry S},
      booktitle={Proceedings of the IEEE International Conference on Computer Vision},
      pages={4561--4569},
      year={2015}
    }
  
    @article{han2017vrfp,
      title={VRFP: On-the-fly video retrieval using web images and fast fisher vector products},
      author={Han, Xintong and Singh, Bharat and Morariu, Vlad and Davis, Larry S},
      journal={IEEE Transactions on Multimedia},
      year={2017},
      publisher={IEEE}
    }
