# map-image-bot
Personal use discord bot to track map track discord embeds from [Maunz](https://github.com/Vauff/Maunz-Discord) and pull useful statistics
## Capabilities
* Read and output raw csv of embed information from Maunz for a specific server at a specific timeframe.
* Translate raw data into useful statistics (e.g. duration of map played, players present during the map etc.).
* Calculate popularity of maps within a server and sort by most popular maps calculated from personally derived algorithm.
  - "Popularity" is a combination of duration of the map and the number of players present at that session.
  - Also prints server specific statistics, such as average players, average duration of map played, number of sessions, and number of unique maps played.
  - Output csv is accompanied by raw data to reuse existing data.
* Filter for embeds without valid embedded map image and create a prioritised list of maps that require a map image to be made.
  - Maps in this list are also unbound to map versions; e.g. data *ze_map_v1* and *ze_map_v2* will be combined together into *ze_map* when calculating statistics.
