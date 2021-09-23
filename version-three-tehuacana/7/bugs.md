#

Our output list of players in JSONs did not represent turn order starting with the current player's turn.

We simply used our internet representation of players (a list that already represented turn order correctly) to create JSON player lists. There was no unit test for this as the bug was in our test fixture.

[Bug Fix](https://github.ccs.neu.edu/CS4500-F20/newdiana/commit/f69b1dd0b81b6078b974d933459bd8c18e256629)

#

Our tie-breaking for the xtree output move nullified the clockwise search order specified in the assignment.

We added an additional sorting parameter to ensure the clockwise search order was respected. There was no unit test for this as the bug was in our test fixture.

[Bug Fix](https://github.ccs.neu.edu/CS4500-F20/newdiana/commit/939d8c60719f2d68c2290534683c2901a4cdeb21)

#

Our JSON -> Python code did not handle the case where the JSON had players with penguins located on holes in the game board, causing us to accidentally submit invalid tests.

We fixed our invalid tests and throw an exception if an invalid JSON is being read. There was no unit test for this as the bug was in our test fixture.

[Bug Fix](https://github.ccs.neu.edu/CS4500-F20/newdiana/commit/2eac460508b5fbdc2131614417ba1f208baedcf8)

#

Our maximin algorithm in Strategy searched at depths different from the n passed into it, in addition to handling the passing of turns improperly.

These two bugs manifested as a joint issue, and were fixed at the same time: The minimax implementation was adjusted to properly consider search depth, and the passing of turns was made manual such that the strategy could understand when passing happened and adjust appropriately.

[Unit Test(s)](https://github.ccs.neu.edu/CS4500-F20/newdiana/commit/b89449b35b5dd8c4bec1348b7dc35fac70698545),
[Bug Fix](https://github.ccs.neu.edu/CS4500-F20/newdiana/commit/af799e51e1489ae09425d351cbd096e3e6043d76)
