from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
import tornado.ioloop
import tornado.web
import os
import re
import requests
import json
import interactive




class MainHandler(tornado.web.RequestHandler):
    def post(self):
        data=tornado.escape.json_decode(self.request.body)
        question = data['question']
        print(question)
        response = findQuestionId(question)

        print(response)
        self.write(tornado.escape.json_encode(response))

def findQuestionId(question):
    global cases_dict
    max_score=0
    max_key = 0
    for key in cases_dict.keys():
        para_score = interactive.process(cases_dict[key], question)
        if para_score > max_score:
            max_score = para_score
            max_key = key
    return str(max_key)+":"+str(max_score)



def make_app():
    #open case file, add each paragraph as an item to list of paragraphs above
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":

    global cases_dict
    cases_dict = {}

    with open('cases.txt', 'r') as f: my_lines = f.readlines()
    print(len(my_lines))
    print(type(my_lines))
    for i in my_lines:
        id_text = i.split(' ', maxsplit=1)
        cases_dict[id_text[0]] = id_text[1]

    app = make_app()
    app.listen(9090)
    tornado.ioloop.IOLoop.current().start()
