#!/bin/bash
ps aux | grep `pwd`/app.py | grep ython | awk '{print $2}' | xargs kill -9
