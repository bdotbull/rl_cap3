# RL **+** ML
Not all double commits are [bad](https://www.reddit.com/r/RocketLeague/comments/8l0hvp/whats_a_double_commit/).
#
#
## Motivation **+** Project Description
#
It is no secret I have a passion for Rocket League and machine learning. With my next project, I aim to gain a much deeper understanding of both RL+ML and further advance toward my ultimate goal of an advanced Rocket League bot. Using reinforcement learning to make a bot is "the holy grail for many ML enthusiasts in the RLBot community"[*](https://github.com/RLBot/RLBot/wiki/Machine-Learning-FAQ). Due to the multifaceted nature of teaching an AI how to _understand_ the game of RL, I will focus on a single piece of the puzzle:  
**Where should I <sub><sup>_(the bot)_</sub></sup> be in order to be part of an effective play?**

Examples of an effectively play include:
- Making a good touch on the ball by way of...
    - passing toward a teammate
    - clearing to an open area of the field
- Being in a favorable position by way of...
    - sitting in net to block a shot
    - moving to get boost pads
    - rotating out, away from the play*

##### * The concept of "rotating play" is fundamental to success in Rocket League.  The nuance and complexity involved in determining when to leave the play, where to go next, and how fast to get there are all integral to Rocket League's astronomic skill ceiling and competitive play.
#
## Approach **+** Data
#
This section is very much a formative one. The more I research and the further I get into [this deeplizard series](https://www.youtube.com/playlist?list=PLZbbT5o_s2xoWNVdDudn51XM8lOuZ_Njv) on reinforcement learning, the better my predictions become for what I _actually_ need to do.    
In essence, I will need to build a system to determine how "valuable" an arbritrary position on the field is, given _some_ information. Then I will need to teach an agent how to map that state to an action.

Alternatively, I could do something more simple, like train a neural network on professional players' positions and have it predict what the bot's next move should be. Something along the lines of "given the position of the 5 other players on the field and the position of the ball, where should the 6th player be".

The [RLBot](https://github.com/RLBot) <sub><sup>([wiki](https://github.com/RLBot/RLBot/wiki))</sub></sup> community has been an invaluable source of knowledge and inspiration.  

As for the data specifically, I have scraped over 50,000 replay files from professional lobbies (at least one player in the match is a pro;  most of the time, pros stick together, so the replays are almost exclusively professional players). I will use a tool called [carball](https://github.com/SaltieRL/carball) to decompile the replays. This will allow me to gain access to the game tick packets (see a snippet of one packet [here](https://github.com/RLBot/RLBotPythonExample/wiki/Input-and-Output-Data)).

There is a great series of [notes](https://samuelpmish.github.io/notes/) I may reference for information on the finer details of object interaction, notably:
- [How to Analyze Drivable Paths](https://samuelpmish.github.io/notes/RocketLeague/path_analysis/)
- [How the Car Handles (Ground)](https://samuelpmish.github.io/notes/)
- [How the Car Handles (Aerial)](https://samuelpmish.github.io/notes/RocketLeague/aerial_control/)
- [How the Car and Ball Interact](https://samuelpmish.github.io/notes/RocketLeague/car_ball_interaction/)

**TL,DR:** I have access to the tools I need, I have loads of replay files for data, but I am actively researching my exact process for a solution.  Basically, I have a good amount of pieces to a puzzle, a general idea of what the finished product looks like, but I'm still figuring out how everything fits together.
#
## Interactivity **+** Insight
#
Ideally, if I have a trained model which operates on information provided by the standard GameTickPacket, I could contribute to the RLBot community in a substantial way.  The goal would be to make something which other people can use in their system, but even if it required my system as a whole, other people may gain insight from the project overall.