# RL + RL: Reinforcement Learning and Rocket League
#
### This repository holds my resources, work, and exploration related to the use of reinforcement learning as a system to play Rocket League.
#
## Background & Motivation:  
From the time I could walk and kick a ball, I was on a junior-league soccer team. Having spent much of my childhood on a farm, I was comfortable operating machinery, equipment, and vehicles at a young age. My love of motorsports and soccer, undoubtedly, stems from my upbringing, fueled my involvement in Autocross racing at BMWCCA events, drifting, and branching out into other competitive sports, particularly BJJ and Judo.

Fast forward to the present time, my list of hobbies and passions has grown to include Machine Learning and Video Games. This repo is where the intersection of those two topics started for me, the home of my third Capstone project for the 2020-2021 Galvanize Data Science Immersive.
#
## What's the BIG idea?
Rocket League has been a supreme form of stress relief for me. On a larger scale, alongside regular exercise, light-moderate gaming has proven to provide excellent cognitive and social benefits. Personally, I learn most effectively through visual and kinestic means. In other words, by watching and doing, I am able to acquire new understanding, skills, behaviors, and values. One of my dreams is to create a bot in Rocket League that will play the game just a little bit better than everyone else in the lobby. My aim is not to have a bot that plays vastly superior to human reaction and planning. Instead, I envision a case where a player sees the bot drive up the wall, jump off, and perform a technical aerial. Then, because that player saw it happen, and thus knows it is possible, the player will extend beyond their comfort zone and attempt the very same move.
#
## Why Rocket League?
### Looking at it from the perspective of a player:
##### _(Part of the following is an excerpt from my [Capstone 1 proposal](https://github.com/bdotbull/rl-stats-eda/blob/main/proposal/proposal.md))_  
Quite simply, I love the game. Rocket League's major appeal to me, as a player, is its core pillar of being easy to pick up while maintaining itself as a bona fide eSport with an incredible skill ceiling. Hastily writing the game off as merely "soccer but with cars having rocket engines on the back" does a disservice to the beautiful complexity that emerges in higher brackets of play. A single match is 5 minutes, the average professional player likely has over 5000 hours of play, and new mechanics are being discovered to this day.  
### Looking at it as an environment for AI:  
##### _(The following is an excerpt from my [Capstone 3 propsal](https://github.com/bdotbull/rl_cap3/blob/main/proposals/P1_RL%2BML.md))_  
Using reinforcement learning to make a bot is "the holy grail for many ML enthusiasts in the RLBot community"[*](https://github.com/RLBot/RLBot/wiki/Machine-Learning-FAQ). Due to the multifaceted nature of teaching an AI how to _understand_ the game of RL, I will focus on a single piece of the puzzle:  
**Where should I <sub><sup>_(the bot)_</sub></sup> be in order to be part of an effective play?**

Examples of an effectively play include:
- Making a good touch on the ball by way of...
    - passing toward a teammate
    - clearing to an open area of the field
- Being in a favorable position by way of...
    - sitting in net to block a shot
    - moving to get boost pads
    - rotating out, away from the play *

##### * The concept of "rotating play" is fundamental to success in Rocket League.  The nuance and complexity involved in determining when to leave the play, where to go next, and how fast to get there are all integral to Rocket League's astronomic skill ceiling and competitive play
#
#
## Repo Directory Info
[Bullish](https://github.com/bdotbull/rl_cap3/tree/main/Bullish) contains everything related to my first RLBot, built using GoslingUtils. It is an "always towards ball agent" which, as the name implies, chases the ball endlessly. I used this bot as a tool to learn about the engine powering Rocket League, the available information in the game's GameTickPacket, and how everything comes together to create an autonomous agent in the game.

[rlah](https://github.com/bdotbull/rl_cap3/tree/main/rlah) contains everything related to when I went "back to basics" on the subject of reinforcement learning. This is where I created a simple soccer game which serves as an environment in which a Q-Learning agent can learn and be rewarded. The game may also be played by a human.

#
#
### Info on my Capstone projects:
- [Capstone 1](https://github.com/bdotbull/rl-stats-eda) -
Statistical analysis on over 5,000 Rocket League games to determine if a particular mechanic affects game balance.
- [Capstone 2](https://github.com/bdotbull/capst2ne) -
A simple CNN image classifier. The network looks at a screenshot of Rocket League and outputs the name of the car the player is using. Trained on the three most popular vehicle bodies used in the game.
- [Capstone 3](https://github.com/bdotbull/rl_cap3) -
RLBot/Q-Learning environment. Project started with building an autonomous agent to play Rocket League. I wanted to learn more about reinforcement learning, so I built a simplified soccer game along the way.