#!/usr/bin/env python


def index(req, **vars):
        return "Hello world!"



def hello2(req, **vars):

        return_string = ""
        for key in vars:
                return_string += vars[key]

        return return_string

