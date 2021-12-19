# ws_b0t
v.0.0.2
#  main functionality
The main functionality is implemented with buttons. At the first start, you will be asked to choose from several options for ad aggregators, then the functionality of the buttons is the same for all aggregator options.

# Directly buttons
- The button "Create link ...", is responsible for creating and validating the link, and further parsing on this link. If the format of the link is invalid, detailed instructions will be sent in response. If the link is valid, it is parsed and new product cards from the selected site come, with a (adjustable) delay, in response. The action of this button is canceled by clicking on the "Return to aggregators" button;
- The button "My links ...", is responsible for displaying valid links from the database (currently Sqlite is used);
- The "Delete links ..." button is responsible for deleting links from the database (while all links have been deleted at once);
- The "Return to aggregators" button is responsible for returning to the main keyboard with the selection of an aggregator.

