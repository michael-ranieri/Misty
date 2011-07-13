#!/usr/bin/env python
# Copyright (C) 2011 Michael Ranieri <michael.d.ranieri at gmail.com>

import sys
import json
import random


def main(user):
    responses = [
        "Excuse me %s! I don't see you slaving around 24/7 in IRC.",
        "Whats up %s?",
        "Today is just one of those auto-pilot days. Don't you agree %s.",
        "%s, I can't do everything you know!",
        "You are looking good today %s!",
        "Did you get a new haircut %s?",
        "Can't answer right now %s, Andrew is calling me.",
        "Can someone please kick %s out of IRC.",
        "BLAH BLAH BLAH %s...",
        "I promise %s, I'm really not mean.",
        "%s, why am I always the one being yelled at in IRC.",
        "%s, shouldn't you be working instead of chatting?",
        "Being at your beck and call %s is really tiring.",
        "When do I get a vacation %s?",
        "It's a lovely day isn't it %s.",
        "How is everyone doing? I'm trying to ignore %s...",
        "Can't you get the interns to massage me %s."
    ]
    
    choice = random.choice(responses)
    
    print choice % user
    

if __name__ == '__main__':
    params = json.loads(sys.argv[1])
    msg, user, channel, users = params
    main(user)