
# Capitals Game

**Capitals Game** is a terminal-based capitals game.

## Description

The **Capitals Game** is a world capitals guessing game fully in the terminal. The game supports sovereign states as well as some recognized dependencies. The capitals and states/dependencies are all in English and as such responses are to be provided in English.

The game currently supports **198** sovereign states and **7** dependencies. This listing is provided with guidance by the United Nations listing of entities.

## Features

### Notes
The game supports entities that have several multiple capitals. In that case requires a single response.

The game provides a forgiving and similarity heuristics allowing for *slight misspellings* of capitals.

The game translates any character outside the ASCII 128 character set into the valid characters needed for comparison. As such: `é` -> `e` (i.e. *Cameroon's* capital *Yaoundé*). A user need not enter these special characters.

The game can be terminated early with `CRTL-C` so that a user need not cycle through the entire capitals list.

The game has an inbuilt validation step to ensure that the capitals belong to allowed regions. As a user you can edit the validation or regions as needed.

### Flags 

- *Alphabetize* - the game supports alphabetical mode for the entities
- *Dependencies* - the game supports several territories and free associating entities, however, these are disabled by default
- *Timing* - the game supports a time taken for each response
- *Regions* - the game supports the **inclusion** and **exclusion** of regions for capitals
- *Full Results* - the game will show a table of correctly and incorrectly guessed capitals at the end for review
- *Infinite* - the game supports an infinite mode in which the game continues indefinitely until the user quits
- *Spelling* - the game supports stringent spelling check

## Regions

The game supports the following regions and sub-regions:

	 - africa
	 - americas
		 - north_america
			 - caribbean
			 - central_america
		 - south_america
	 - asia
		 - middle_east
		 - southeast_asia
	 - europe
	 - oceania

A user can filter the set of entities by using the `-r/--regions` and `-e/--exlude-regions` flags to obtain a subset they wish to play.

## Usage

To run the game:

```
./capitals_game.py [args]
```

The game supports the following command line arguments:
```
  -h, --help            show this help message and exit
  -a, --alphabetize     Alphabetize Countries (default: False)
  -d, --dependencies    Include Dependencies (default: False)
  -e, --exclude-regions Exclude selected regions (default: None)
  -f, --full-results    Show Full Results (default: False)
  -i, --infinite        Infinite mode, cycle indefinitely (default: False)
  -r, --regions         Show Only Countries from selected regions (default:
                        None)
  -s, --spelling        Require correct spellings (default: False)
  -t, --timing          Show Timing per Question (default: False)
  ```

You can press `CRTL-C` at anytime during the game to exit and see your results.

## Dependencies

The game is built on **Python 3** and requires the following additional dependencies:
- `colorama`
- `unidecode`

## Citation

If you wish to reference the **Capitals Game** please provide the recommended citation that includes:
- **Author**: *Pratheek Nagaraj*
- **Title**: *Capitals Game*
- **GitHub**: [github.com/pratheeknagaraj/capitals-game](https://github.com/pratheeknagaraj/capitals-game)

Below is an example TeX friendly citation:

```
@misc{pnagaraj_capitals-game_2020,
  author = {Pratheek Nagaraj},
  title = {Capitals Game},
  year = {2020},
  howpublished = {\url{https://github.com/pratheeknagaraj/capitals-game}}
}
```

## License

Copyright (c) 2020 Pratheek Nagaraj. Released under GNU GENERAL PUBLIC LICENSE V3. See [LICENSE][license] for details.

[license]: LICENSE

