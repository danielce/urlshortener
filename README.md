# urlshortener

Simple URL shortening service wrtitten in Python/Django

DEMO: http://vps338532.ovh.net/

Note: This app is treated as self-study project which gives way to improve my coding skills. Sometimes I'm making sth in more complicated way just to show that I have some knowledge in given topic, but I'm doing my best to keep code clean. There are also parts of legacy code that need refactorization. PR's are welcomed anytime ;) 

*FEATURES*

* fast, simple, user-friendly
* automatically scrapes title from shortened urls
* detailed stats about clicks and visits of each url thanks to collecting UserAgent data
* lists of most popular urls
* admin can monetize web traffic passed through shotened url by placing ads in ladning pages which is displayed to visitor for certain amount of time before redirect is proceded
* Rest API that allows authenticated user to create shortened links and get lists of created urls.
