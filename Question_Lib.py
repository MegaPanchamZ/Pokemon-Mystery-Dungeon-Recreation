from random import sample, choice

Bold_text = [["You seem to be..."],
             ["The Bold Type!-You're so brave, and you never back down from anything!"],
             ["And you're also gutsy and brash in a way that others aren't!"],
             ["You're not shy about asking to take home all the leftovers at restaurants, right?"],
             ["If someone's treating you to dinner, you have no problem with ordering lots of good stuff!"],
             ["And you aren't fazed by doing things that most others would think twice about doing."],
             ["Perhaps you don't even notice when others are upset with you!"],
             ["You know, you have the potential to become a truly great person..."],
             ["because you'll be the last one standing! So, a bold type like you..."]]

Brave_text = [["You seem to be..."],
              ["The Brave Type!-You don't know the meaning of fear!"],
              ["You're not afraid to keep moving forward in the face of danger."],
              ["You also have a strong sense of justice and can't turn a blind eye to someone in trouble."],
              ["But you sometimes push your own personal sense of justice a little too hard."],
              ["Be careful that you don't get too pushy! So, a brave type like you... "]]

Calm_text = [["You seem to be..."],
             ["The Clam Type!-You're very compassionate and considerate, and you put friends ahead of yourself. "],
             [
                 "You're so generous and kindhearted that you can laugh, forgive, and forget when your friends make mistakes."],
             [
                 "But be aware that your compassion can sometimes get the best of you, putting you too far behind everyone else!"],
             ["So, a clam type like you... "]]

Docile_text = [["You seem to be..."],
               [
                   "The Docile Type!-You're quite sensitive to others! You listen attentively and respectfully, and you're quick to pick up on things."],
               [
                   "Because you're so good at listening, do you find that your friends tell you their problems and concerns often?"],
               [
                   "Perhaps people laugh at you sometimes for being so earnest and not recognizing jokes for what they are."],
               ["But you're honestly surprised and bashful about this aspect of yourself..."],
               ["And then honestly laugh about it! So, a docile, sensitive type like you..."]]

Hardy_text = [["You seem to be..."],
              [
                  "The Hardy Type!-You're so determined! You don't whine or feel sorry for yourself, and you never need help with anything."],
              ["You also have a strong sense of responsibility."],
              ["You work toward your goals steadily and never require attention along the way."],
              ["Your resilient spirit is the only thing you need to guide you toward your goals."],
              ["But be careful! You risk wearing yourself out if you work too long all on your own!"],
              [
                  "You should recognize that sometimes you need help from friends. So, a hardy, determined type like you..."]]

Hasty_text = [["You seem to be..."],
              ["The Hasty Type!-You talk quickly! You eat quickly! You walk quickly!"],
              ["People often see you as a hard worker because you're always moving around so fast!"],
              ["But be careful!"],
              ["If you always rush so fast, you may make mistakes more often than others do."],
              ["And what a waste that would be! Relax every now and then with a nice, deep breath!"],
              ["So, a hasty type like you... "]]

Impish_text = [["You seem to be..."],
               [
                   "The Impish Type!-You really like to play a lot! And you enjoy eating a lot! You love competition,but you hate losing."],
               ["Your personality seems crystal clear to others. With you, what you see is what you get!"],
               ["You cheer others with your dazzling smile."],
               ["But you may be afraid of showing what's in your heart and revealing your true self."],
               ["You may not want to keep your worries to yourself."],
               ["You're only human, so ask your friends for advice when you need it. So, an impish type like you..."]]

Jolly_text = [["You seem to be..."],
              ["The Jolly Type!-You have a good sense of humor, and you're compassionate."],
              ["You're always making others around you laugh."],
              [
                  "You have a sunny, positive outlook, and you have a vitality that raises the lowest spirits to giddy heights!"],
              ["Yet, for all your great cheer, you're also open to tears..."],
              [
                  "But you bounce between laughter and tears so easily! What an adventure life must be like for you, bouncing around like that all day!"],
              ["So, a jolly type like you..."]]

Lonely_text = [["You seem to be..."],
               ["The Lonely Type!-At least a little bit!"],
               ["You might find that surprising, but do you think it might be a little true?"],
               ["You know what they say, though...We're all a bit lonely every now and then!"],
               ["You probably keep this fact of life to yourself, though."],
               ["But if there's one thing that brings us all together...it's our need to go it solo! "],
               ["So, a Lonely and solitary type like you..."]]

Quiet_text = [["You seem to be..."],
              ["The Quiet Type!-And very calm!"],
              ["You're great with numbers, and you analyze information before making decisions."],
              ["You rarely make mistakes, because you make decisions so calmly and rationally."],
              [
                  "You also may find it hard to guess what others are thinking, and they may find you a touch cold at times."],
              ["You may not want to keep your feelings to yourself so much of the time."],
              ["So, a quiet and calm type like you..."]]

Naive_text = [["You seem to be..."],
              ["The Naive Type!-You're so open and innocent!"],
              [" What a strong sense of curiosity you have!"],
              [" And you state your opinions purely, sharing exactly what you think."],
              [" You also have an artistic spirit that isn't restrained by social conventions!"],
              [" You startle people with your spontaneity and vision."],
              [" But when you overdo it, other people can have a hard time keeping up with you..."],
              ["Have you noticed people looking at you oddly? As if for no apparent reason?"],
              [" So, a naive, innocent type like you..."]]

Quirky_text = [["You seem to be..."],
               ["The Quirky Type!-You want to be on the cutting edge of fashion!"],
               [
                   "You want to own all the latest stuff, right? But you grow bored of your old things and only like new things!"],
               ["You're true to your emotions, and you follow your desires."],
               ["People have a hard time keeping up with you because you change so quickly."],
               ["You may want to reflect upon how your words and actions affect others. "],
               ["So, a quirky type like you..."]]

Rash_text = [["You seem to be..."],
             ["The Rash Type!-You seem to be even a bit hasty at times!"],
             ["You may run out of your house an forget to lock the door once in a while."],
             ["And you may leave things like umbrellas behind when you leave places."],
             ["Maybe you even dash outside in your slippers every now and then!"],
             ["Perhaps you even wear your shirts inside out all the time!"],
             ["Oh, is that even rasher than you really are? So sorry!"],
             ["But know that your friends think your funny little flubs are adorable!"],
             ["Oh, wait! One more thing!"],
             ["You also sometimes reveal your friends' secrets by accidents, don't you! "],
             ["Sorry. Had to be said!"],
             ["So, without further ado...a rash and hasty type like you..."]]

Relaxed_text = [["You seem to be..."],
                ["The Relaxed type!-You're so casual, leisurely, and carefree."],
                ["You don't rush or stress yourself out, and you don't worry about anything."],
                ["You like to take a seat and kick up your feet!"],
                ["You definitely have an easygoing personality, and you don't sweat the details."],
                ["People naturally flock to you because they find you to be a free spirit, which is so refreshing!"],
                ["So, a relaxed type like you..."]]

Sassy_text = [["You seem to be..."],
              ["The Sassy Type!-Or at least somewhat sassy!"],
              ["You don't like taking orders. "],
              ["You're a little rebellious and like to disagree."],
              ["You're a lone wolf! You like to keep your distance from groups and go off to do things on your own."],
              ["Older folks may be ones who find you the most disagreeable, even selfish."],
              ["But people younger than you tend to really admire you! "],
              ["So, a sassy type like you..."]]

Timid_text = [["You seem to be..."],
              ["The Timid type!-You're quite gentle!"],
              ["You're sometimes a little shy about new things, aren't you? "],
              ["Do you miss out on some experiences because you get worried about the newness of the challenge?"],
              ["Of course, there's also a great benefit in being cautious, isn't there?"],
              ["After all, it keeps you nice and safe!"],
              ["You live life at your own speed, with no hurries and no worries!"],
              ["So, a timid and gentle type like you...."]]

Group1 = [
    ["You're in the final mile of a marathon, but the last stretch is exhausting! What will you do?",
     ['Hang in there and finish', 'Hardy +4; Brave +2'], ['Stop running', 'Quirky +4'], ['Find a shortcut',
                                                                                         'Rash +2; Bold +4']],

    ['Would you ever consider sticking to a plan to do ten sit-ups a day?', ["Yes! That's easy", 'Impish +4; Sassy +2'],
     ['Yes. Hard work, though', 'Hardy +4'], ["No! Who'd want to do that?", 'Quirky +4']],

    ['What do you do with your allowance?', ['Save it', 'Hardy +4'], ['Spend it', 'Hasty +2; Quirky +4'],
     ['Spend half, save half', 'Quiet +2'], ["I don't get an allowance", 'Lonely +4']],

    ['You have to move a heavy suitcase. What will you do?', ['Carry it by myself', 'Brave +2; Hardy +4'],
     ['Ask someone to help', 'Docile +2'], ['Make someone else do it', 'Bold +4; Sassy +2']]
]

Group2 = [
    ["If you don't know something, do you come clean and admit it?", ['Of course', 'Bold +2; Docile +4'],
     ["That's not easy to admit", 'Lonely +2; Timid +4']],

    ["You're on a walk when you smell something delicious. What do you do?", ['Try to imagine what it is', 'Docile +4'],
     ['Find out what it is', 'Naive +4; Rash +2'], ['Think about how hungry I am..', 'Impish +4']],

    ['A fortune-teller says that you have a bad future ahead of you. How do you react?', ['Worry about it',
                                                                                          'Docile +4; Timid +2'],
     ['Forget about it', 'Bold +2; Jolly +4; Relaxed +2']],

    ['You hear a rumor that might make you rich! What do you do?', ['Keep it all to myself', 'Bold +4; Timid +2'],
     ['Share it with friends', 'Docile +4; Rash +4'], ['Spread a different rumor', 'Impish +4']]
]

Group3 = [
    ['How do you blow up a balloon?', ['As close to breaking as possible', 'Brave +4; Impish +4'],
     ['Big...but not too big', 'Quiet +2'], ["I don't... It could pop", 'Docile +2; Timid +4']],

    ["Do you state your opinion even when it's not what everyone else thinks?", ['Yes', 'Bold +2; Brave +4'], ['No',
                                                                                                               'Lonely +4; Timid +2'],
     ['It depends on the situation', 'Quiet +2; Quirky +2']],

    ['You want to reveal that you like someone a whole bunch! What do you do?', ['Show it a little by playing together',
                                                                                 'Jolly +4; Quiet +2'],
     ['Make it obvious by...playing a prank', 'Lonely +4; Naive +2'],
     ['State it clearly for all to hear', 'Bold +2; Brave +4; Impish +4'], ["Keep it to myself! It's too risky",
                                                                            'Timid +2']],

    ["You're on a stroll when a TV crew pounces on you for an interview. What do you do?",
     ['Run away! How embarrassing',
      'Timid +4'], ['Answer questions properly', 'Brave +4; Sassy +4'], ["Yuck it up! Woo-hoo! I'm on TV",
                                                                         'Bold +2; Naive +4']]
]

Group4 = [
    ['You feel a burst of happiness! How about expressing it with a little dance?', ['Yes', 'Jolly +4; Lonely +2'],
     ['No',
      'Quiet +2']],

    ['You see a parade coming down the street. What do you do?', ['Stay on the sidelines', 'Calm +2'],
     ['Join the parade', 'Jolly +4; Naive +4'], ['Walk away', 'Lonely +2; Sassy +4']],

    ["Your friend tells a joke that's horribly corny! How do you react?", ['Slap my forehead and groan', 'Brave +4'],
     ['Roll around the floor laughing', 'Jolly +4; Naive +2'], ['Just let it go by..', 'Docile +2; Impish +2']],

    ['Can you strike up conversations with new people easily?', ['Yes', 'Bold +4; Jolly +4'],
     ['No', 'Docile +2; Timid +2']]
]

Group5 = [
    ['Do you get injured a lot?', ['Yes', 'Impish +4; Rash +4'], ['No', 'Calm +2']],

    ['You see a ball on the ground. What do you do?', ['Kick it', 'Hasty +2; Sassy +2'], ['Throw it', 'Impish +4'],
     ['Spiff it up, shiny and new', 'Lonely +4']],

    ['What do you think of jungle exploration?', ['Sounds fun', 'Impish +4; Naive +2'], ['Not interested',
                                                                                         'Quirky +4; Timid +2']],

    ['You discover a secret passage in a basement. What do you do?', ['Go through it',
                                                                      'Brave +4; Hasty +4; Impish +4; Rash +2'],
     ['Stay away from it', 'Timid +2']]
]

Group6 = [
    ['Your friend takes a spectacular fall! What do you do?', ['Help my friend up', 'Brave +4; Lonely +2'],
     ["Laugh! It's too funny", 'Impish +4; Naive +4; Rash +2']],

    ["You're daydreaming...when your friend sprays you with water! What do you do?", ['Get mad', 'Hasty +4'],
     ['Get sad',
      'Lonely +4'], ['Woo-hoo! Water fight', 'Impish +4; Jolly +4; Naive +4']],

    ['Have you ever wanted to communicate with aliens from another planet?', ['Yes', 'Naive +4'], ['No', 'Quiet +2']],

    ['Have you ever upset a friend when you were just kidding around?', ['Yes', 'Impish +2; Naive +4'],
     ['No', 'Calm +4']]
]

Group7 = [
    ["Hey, what's that? There's someone behind you! So...did you look just now?", ['Huh? What', 'Relaxed +4'],
     ["No way. I didn't fall for it", 'Lonely +4; Sassy +4'], ['OK, I admit it. You tricked me', 'Docile +4'],
     ["Don't do that! It scared me", 'Timid +4']],

    [
        "Someone who works at a store suggests an item that isn't quite what you're looking for. But you like this person. What do you do?",
        ['Cave in and buy it', 'Timid +2; Rash +2'], ['Say thanks...but say no', 'Calm +4; Lonely +2'],
        ["Say you don't want it", 'Brave +2; Quiet +2']],

    ["You run into a new person that you haven't talked to very much before. What do you do?",
     ['Make an excuse to get away', 'Timid +4'], ['Make small talk', 'Calm +2', 'Say nothing', 'Quirky +2']],

    ["You think you hear someone call your name. But no one's around...so what was it?", ['Someone fooling around',
                                                                                          'Bold +2; Naive +4'],
     ['Just my imagination', 'Relaxed +4', 'A ghost', 'Timid +4']]
]

Group8 = [
    ['Do you find yourself jumping to the wrong conclusion a lot of the time?', ['Yes', 'Hasty +4; Rash +4'], ['No',
                                                                                                               'Docile +2; Quiet +2']],

    ['Do you change the channels often while watching TV?', ['Yes', 'Hasty +4'], ['No', 'Calm +2']],

    ['You find something at a great bargain! What do you do?', ['Buy it right away', 'Hasty +4'],
     ['Think about whether you need it', 'Quiet +2'], ['Demand an even bigger discount', 'Bold +4']],

    ["You're packing your classroom's snacks for a picnic when you get hungry. What do you do?",
     ['Hold myself back and pack it all up', 'Hardy +4'], ["What snacks? They're in my belly", 'Rash +4'],
     ['Eat just a tiny bit', 'Hasty +4']]
]

Group9 = [
    ['Are you a rebel at heart?', ['Totally', 'Sassy +4'], ['Of course not', 'Calm +2']],

    ['When walking in a group, do you tend to be the one at the front?', ['Of course', 'Lonely +2; Sassy +4'], ['No',
                                                                                                                'Calm +4; Quirky +2']],

    ['Do you think that you might be a genius?', ['Certainly', 'Jolly +2; Naive +2; Sassy +4'], ['Well, not really..',
                                                                                                 'Hardy +2']],

    ['Would you feel comfortable stating your opinion to a very important person?', ['Of course',
                                                                                     'Bold +2; Brave +4; Sassy +4'],
     ['Not really', 'Timid +2']]

]

Group10 = [
    ['Are you a city person or a country person?', ['I like the city', 'Lonely +4; Sassy +2'], ['I like the country',
                                                                                                'Calm +4'],
     ['I like them both', 'Quirky +4']],

    ["You're about to take the last cookie when your friend wolfs it down! What do you do?",
     ['I weep for my lost cookie', 'Lonely +4'], ['I unleash my cookie fury', 'Jolly +4; Relaxed +4'],
     ["Whatever. It's just a cookie", 'Calm +4']],

    [
        "You've spent forever stacking dominoes... One more and you're done... OH, NO! You knocked them over! What do you do?",
        ['I unleash my full fury', 'Docile +4'], ['I set up the dominoes again..', 'Bold +4; Calm +4'],
        ["I'm too crushed to start again", 'Hardy +4']],

    ["You don't get bothered by noise and ruckus nearby, do you?", ['Yes', 'Bold +4; Relaxed +2'], ['Not at all',
                                                                                                    'Hasty +2; Lonely +4']]

]

Group11 = [
    ["You've just stuffed yourself with a good meal when a great dessert arrives. What do you do?",
     ['Yum! I love dessert the most!', 'Bold +4; Jolly +4; Relaxed +2'],
     ["Turn it down. It's too fattening", 'Hardy +2'], ["Eat it. Who cares if I'm stuffed", 'Hasty +4; Rash +2']],

    ['You have a really important test tomorrow! What do you do?', ['Study all night long', 'Hardy +4'],
     ["Wing it! I'm sure it will be fine", 'Relaxed +4'], ['Test?! I think I have a fever..', 'Naive +4']],

    ["You're eating at a restaurant when you abruptly realize that everyone's gone! What do you do?",
     ['Alone?! I look for an employee', 'Docile +4; Lonely +4'],
     ["Who's worried? I keep eating", 'Jolly +4; Relaxed +4'], ['I swipe food from other tables', 'Bold +4']],

    ['Do you find yourself humming or singing often?', ['All the time', 'Jolly +2; Relaxed +4'], ['Never', 'Quiet +2']]
]

Group12 = [
    ["The phone's ringing! What do you do?", ['Answer right away', 'Hasty +4; Lonely +4'],
     ['Wait a bit before answering', 'Quiet +2'], ['Ignore it and let it ring', 'Timid +2']],

    ['Your friends seem to be having a fun chat out of earshot. What do you do?',
     ['Join them and chat along', 'Naive +4'], ["Nothing...I'm not interested", 'Lonely +4'],
     ['Eavesdrop from a distance', 'Timid +2']],

    ['Do you like being the center of attention?', ['Yes', 'Lonely +4; Sassy +4'], ['No', 'Relaxed +2']],

    ["You're told to wait in a big, empty room. What do you do?", ['Wait quietly', 'Docile +4'],
     ['Search for something to do', 'Naive +4'], ['Wander outside', 'Rash +4'],
     ['Cradle my knees and sit in the corner', 'Lonely +4']]
]

Group13 = [
    ["Do you have lots of stuff you bought, thinking it was all cool, but don't use anymore?",
     ['Yes', 'Hasty +2; Quirky +4; Rash +2'], ['No', 'Quiet +2']],

    ['Have you had any hobbies for a long time?', ['Yes', 'Hardy +4'], ['No', 'Hasty +2; Quirky +4']],

    ['Do you often cancel plans to meet others at the last second?', ['Yes', 'Quirky +4; Rash +4'], ['No', 'Calm +2']],

    ['Do you like to do things according to plan?', ['Of course', 'Hardy +4'],
     ["I'm not good at planning", 'Quirky +4; Rash +2'], ['Plans? Who needs plans', 'Relaxed +4']]
]

Group14 = [
    ['Do you think that lies are sometimes necessary?', ['Yes', 'Bold +4; Quiet +4'], ['No', 'Brave +4'],
     ["I don't know",
      'Docile +4']],

    ['You spot a deserted ship on the high seas! What do you think the ship holds?', ['Precious loot',
                                                                                      'Jolly +2; Naive +4'],
     ['Ghosts', 'Timid +2'], ['Nothing! The ship is merely a mirage', 'Quiet +4']],

    ['Do you think that anything goes when it comes to winning?', ['Of course', 'Quiet +4; Sassy +4'], ['No way',
                                                                                                        'Brave +4']],

    ['Your friend is crying right in front of you! What made that happen?', ['Someone bullied my friend', 'Hasty +4'],
     ['My friend fell down, no doubt', 'Quiet +4'], ["I wonder if it's my fault", 'Timid +2']]
]

Group15 = [
    ['Your friend says that your shirt is inside out. What do you do?', ['Laugh out loud', 'Rash +4'],
     ["Say that it's the latest fashion", 'Jolly +4'], ['Get embarrassed', 'Docile +4']],

    [
        'You muster your courage and go to a graveyard at night...and see a woman soaked to the skin just standing '
        'there! What do you do?',
        ["So what? It's just a lady", 'Naive +4; Sassy +2'], ['Drop down and play dead', 'Rash +4'],
        ['Run away at full speed', 'Timid +2']],

    ['Do you often forget to lock the door when you go out?', ['No', 'Quiet +2'], ['Yes', 'Bold +2; Rash +4']],

    ['Have you ever accidentally revealed a personal secret that someone shared with you?', ['No', 'Hardy +2'],
     ['Yes', 'Lonely +4; Rash +4']],
]

Group16 = [
    ["You're in class when you realize that you really have to go to the restroom! What do you do?",
     ['Hold on until class ends', 'Timid +2'], ['Sneak out', 'Hasty +2'], ['Ask for permission to leave',
                                                                           'Bold +4; Brave +4']],

    ["You're in a play with friends. What kind of role do you prefer?", ['Just a bit part', 'Quirky +4'],
     ['Starring role',
      'Bold +4'], ['Supporting role', 'Jolly +4']],

    ['You see a cake that is past its expiration date, but only by one day. What do you do?',
     ['Get someone to try it first', 'Bold +4'], ['Think about it briefly, then decide', 'Timid +2'],
     ['Not a problem! Chow time', 'Brave +4; Relaxed +2']],

    ["You attend a fine dinner at a friend's house. How do you behave?", ['Ask to take the leftovers home', 'Bold +4'],
     ['Devour the food heartily', 'Impish +4; Naive +4'], ['Enjoy the meal in polite moderation', 'Hardy +2']]
]

Group17 = ['Are you male or female?', ['Male', 'Timid +1'], ['Female', 'Timid +1']]

selectiongroups = [Group1, Group2, Group3, Group4,
                   Group5, Group6, Group7, Group8,
                   Group9, Group10, Group11, Group12,
                   Group13, Group14, Group15, Group16]


def getQuestions():
    question_pool = sample(selectiongroups, k=8)
    selection = []
    for i in question_pool:
        ch = choice(i)
        selection.append(ch)
    selection.append(Group17)
    return selection


def getNatureText(nature):
    if nature == 'Bold':
        return Bold_text
    if nature == 'Brave':
        return Brave_text
    if nature == 'Calm':
        return Calm_text
    if nature == 'Docile':
        return Docile_text
    if nature == 'Hardy':
        return Hardy_text
    if nature == "Naive":
        return Naive_text
    if nature == 'Hasty':
        return Hasty_text
    if nature == 'Impish':
        return Impish_text
    if nature == 'Jolly':
        return Jolly_text
    if nature == 'Lonely':
        return Lonely_text
    if nature == 'Quiet':
        return Quiet_text
    if nature == 'Quirky':
        return Quirky_text
    if nature == 'Rash':
        return Rash_text
    if nature == 'Relaxed':
        return Relaxed_text
    if nature == 'Sassy':
        return Sassy_text
    if nature == 'Timid':
        return Timid_text


def getPokemon(Gender, Nature):
    if Gender == 'Male':
        Male_PKMN = {'001': 'Lonely', '004': 'Docile',
                     '007': 'Quirky', '025': 'Brave',
                     '052': 'Sassy', '152': 'Calm',
                     '155': 'Timid', '158': 'Jolly',
                     '252': 'Quiet', '255': 'Hardy',
                     '258': 'Rash', '300': 'Hasty',
                     '387': 'Bold', '390': 'Naive',
                     '393': 'Impish', '446': 'Relaxed'}
        for id, nat in Male_PKMN.items():
            if nat == Nature:
                return id
    if Gender == 'Female':
        Female_PKMN = {'001': 'Docile', '004': 'Brave',
                       '007': 'Bold', '025': 'Hasty',
                       '052': 'Relaxed', '152': 'Quiet',
                       '155': 'Calm', '158': 'Sassy',
                       '252': 'Hardy', '255': 'Rash',
                       '258': 'Lonely', '300': 'Naive',
                       '387': 'Timid', '390': 'Impish',
                       '393': 'Quirky', '446': 'Jolly'}
        for id, nat in Female_PKMN.items():
            if nat == Nature:
                return id
