# Software-Eng-trivia - The rainy app.
## Deployment
https://the-rainy-app.herokuapp.com/

## About
The rainy app is a web site built and deployed with the purpose of creating a space to do some knowlegde testing, regarding various Software Engineering related concepts.
In this site you can ask for some quizes (you can choose the topic, difficulty and number of questions), and once you submit your answers you can check how many you got right
and what the right anwers where. 

The normal user flow is, you login, and then make a request for a quizz, choose the answer for each question, picking from a select list, and finally check your score and where you went wrong.

## Api: QuizAPI
https://quizapi.io/
This API is a simple REST API with only one endpoint. It also requires an API_KEY, wich you can get for free by just registering. The API offers 800 requests per month, with one single key. Some errors have been detected, such as some questions not having a right answer or spelling mistakes, but these are not common at all.

## Tech-stack
The back end is handled with Python-Flask with WTforms-Jinja, with PosgtgresQL and SQLAlchemy for database usage. For now the only data being used is a Users table.
The front end is handled with JS-jQuery, CSS-Bootstrap 5 and of course HTML. Several icons are requested from FontAwesome, and the animated rain backgroung was forked from codepen.io (Thank you Aaron Rickle).

## Context
The rainy context is purely arbitrary. Or maybe you can think about it like it's raining knowlegde, your choice.
Future functionality will be added shortly, regarding JavaScript Gotchas: small snippets of code, design to trick your mind and confuse you about what the return will be. Cooming soon.
