#!/usr/local/bin/python3
# coding: utf-8

import sys
from stip import app

if __name__ == "__main__":
  app.run(host='localhost', port=8080, debug=True)
