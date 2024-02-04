# wfmarketlister
Script that will gather the prices (in-game currency) of various digital items for the video game "Warframe" from a public market API

For more context, the website I made this script for is a third-party free service that allows players to list their items for "Platinum", an in-game currency obtainable by spending real money on the popular video game "Warframe".
Warframe.market is often used as a central place to contact other players to trade platinum for in-game items. Using this script, the back-end API will be consumed and report the lowest prices for each good on the marketplace, 
which can be limited based on various categories, defined by user input out of a list of options during run-time. In the game, certain items are often sold as "sets", comprised of different parts to assemble the item. The script
provides the difference value between purchasing the set versus purchasing each individual piece. As a result, users of the script may identify items that may be purchased individually and subseqently sold as a set to profit from the difference.

I enjoy playing the game and often use the marketplace to purchase items from other players. I wanted to find the cheapest items from specific categories, and thought making a script for the public API would be fun.

Further updates to the script that can improve it's functionality include:
* Threading of requests
* Indexing values, allowing users to force-update the database whenever the game updates and adds new content (writing to a local MySQL file would work), resulting in improved performance
* UI that displays the items in a more user-friendly way

https://warframe.market - Front End
https://warframe.market/api_docs - API Documentation
