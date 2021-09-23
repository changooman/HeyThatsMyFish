## Self-Evaluation Form for Milestone 1

### General

We will run self-evaluations for each milestone this semester.  The
graders will evaluate them for accuracy and completeness.

Every self-evaluation will go out into your Enterprise GitHub repo
within a short time afrer the milestone deadline, and you will have 24
hours to answer the questions and push back a completed form.

This one is a practice run to make sure you get


### Specifics


- does your analysis cover the following ideas:

  - the need for an explicit Interface specification between the (remote) AI
    players and the game system?

    - Yes - we stated that the Game Runner will enforce a specific protocol that will used by AI players. (2nd paragraph)

  - the need for a referee sub-system for managing individual games

    - Yes - our Game Runner manages individual games and is responsible for all referee duties. (2nd paragraph)

  - the need for a tournament management sub-system for grouping
    players into games and dispatching to referee components

    - Yes - our Tournament Manager groups players into different games and launches each fish game using a Game Runner instance. (3rd paragraph)

- does your building plan identify concrete milestones with demo prototypes:

  - for running individual games

    - Yes - our 2nd milestone states that at that point, all necessary components to run an individual game will be completed and a demonstration would be possible at that time. To complete a game in a timely manner, we would need to develop a test AI, which we failed to mention.

  - for running complete tournaments on a single computer

    - Yes - our 3rd milestone states that we'd be able to show tournament progression as games are played.

  - for running remote tournaments on a network

    - Yes - our final milestone demonstrates  a complete tournament being played out over a network using all of our components.

- for the English of your memo, you may wish to check the following:

  - is each paragraph dedicated to a single topic? does it come with a
    thesis statement that specifies the topic?

    - Yes - each of our paragraphs introduces the component that will be discussed. Each paragraph generally explains an individual component.

  - do sentences make a point? do they run on?

    - Yes. No.

  - do sentences connect via old words/new words so that readers keep reading?

    - Yes.


  - are all sentences complete? Are they missing verbs? Objects? Other
    essential words?

    - Yes. No. No.

  - did you make sure that the spelling is correct? ("It's" is *not* a
    possesive; it's short for "it is". "There" is different from
    "their", a word that is too popular for your generation.)

    - Yes.

The ideal feedback are pointers to specific senetences in your memo.
For PDF, the paragraph/sentence number suffices.

For **code repos**, we will expect GitHub line-specific links.
