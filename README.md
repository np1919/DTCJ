
- February 2022 

Check out my campaign app on Heroku -- [https://dunnhumby-app.herokuapp.com/](https://dunnhumby-app.herokuapp.com/)

Beyond struggling to produce a reproducible pipeline for both new households and incoming sales data; I vaguely understand the irony of implementing an app on Heroku (a salesforce application). But I digress..

Eventually I hope to implement the RecommenderSystem class to produce recommendations for each household in a smarter way; I'm exploring automating model testing using XGBoost to derive labels.


# DunnHumby: The Complete Journey -- An Incomplete Offering

## IN THIS REPO:
------------
Hello, and welcome to my capstone rework. I've phrased the notebooks as if I was talking to a client, coworker or a teammate, and explored them from the perspective of...a newcomer to the data science field talking to a Client who has not yet invested in data infrastructure; but is now coming to me and asking me to make sense of this data set that is full of holes and errors and build them a whole new data infrastructure; which will also be immediately implementable to produce business value. Of course. Had to keep it interesting.

Something from my weak education and unrelated work experience tells me that **good modelling results come at the intersection of quality data extraction and excellent business questions**; but along the path (get it) that must involve *data acquisition*, agreed? But, unlike their underlying phenomena in the real world, the cyber-world of *tabular and unstructured data* is not immediately obvious, apparent, or available to the senses. In order to understand this new world, I needed to gain a deeper understanding of my tools -- or maybe weapons -- against the massive onslaught of data in our world today.

I've always wanted to know what stuff was made of. And in the past two years of learning Python, my curiosity has been often insatiable -- but if you asked me, I'd have said my capstone project was a flunk. I tried to take on more than I could chew -- and implement processes that I had no experience with. Even after comprehensive cleaning and analysis in my jupyter notebook, I struggled with the awkward sizes of the data; maintaining it's integrity in *storage* while accessing it in *memory* to perform transformations over and over again...which might or might not correctly phrase the business question in a context that the appropriate model (or group of models?) can understand.  

Data Science is about models. It's about jupyter notebooks. But more than that, it seems to me that it's about automation, **Version Control**, continuity of purpose, and co-operation. If you're analyzing or sciencing data, you're gonna need some data infrastructure, and probably some good teamwork, too. I didn't want to mess up anybody's cloud, so I bashed my head on my own keyboard for a while, instead. That's why they call it gitbash, right? What's a shell script? Anyway.

This project has a couple of large data files; and I'm perhaps now overly-cogniscent of the fact that it could have (should have) been implemented primarily in simple SQL and/or to utilize the cloud -- but I decided to go a different route, and here I am. I do love how adaptive Python can be -- I want to be able to help out where I'm needed. 

In the end, this project is going to be (a set of) Heroku app(s), a baby development(?) package, and about 25 notebooks. I'm going to try to learn more about memory/compute on remote servers; although I'm not exactly sure why yet. 

The premise for this sometimes embarassing showcase is to show that I understand that an ML/AI model is only as good as the data that goes in -- and how effectively it can serve the needs of the client. And holy moly **it's so much work!** Building my own functions and classes to accomplish my needs for this project has given me a whole new perspective.

I thought a double shift every friday was bad, but this stuff never ends. It seems that with every new thing I learn, there are some exponent of O more things that I need to know about. Foing it this way has let me make a lot of mistakes; but learning how to provide data-based analysis and visualization on a remote server using (some) tools that I made, that I might deploy in production (someday) has been a hell of a ride. 

I love empowering others, and being someone that my team can rely on -- and I feel that I'm getting close to being able to start learning about what that entails in the world of data. I will get better at data viz -- now that I know how to work with basic Python and Git. The objective, of course, is to provide answers to client-facing questions, whether that is an organization or a team making data-driven decisions. By using a static piece of data but embracing an increasingly abstracted workflow, I hope to show some of my perspective as a newcomer to data. 


# GET THE DATA:
-----------

To download the dataset through the command line you can use the Kaggle API to get the data; follow the docs here (you need to get a Token):
https://www.kaggle.com/docs/api

and then run the command 

  kaggle datasets download -d frtgnn/dunnhumby-the-complete-journey

to download the .zip file to the current directory.


cheers!
