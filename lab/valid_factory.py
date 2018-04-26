# -*- coding: utf-8 -*-
from lab import notify
from datetime import datetime

class ValidFactory():

    def __init__(self, temp=None, request=None, formsets_POST=None, username=None,):
        self.temp = temp
        self.request = request
        self.formsets_POST = formsets_POST
        self.username = username