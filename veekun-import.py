#!/usr/bin/env python2
# coding: UTF-8

import sqlite3, json, collections
from collections import OrderedDict

def searchPokemonByName(name, pokemonData):
    for i, item in enumerate(pokemonData):
        if 'name' in item and item['name'] == name:
            return {'index': i, 'pokemon': item}
    return False

def searchPokemonByIdentifier(identifier, pokemonData):
    for i, item in enumerate(pokemonData):
        if 'identifier' in item and item['identifier'] == identifier:
            return {'index': i, 'pokemon': item}
    return False

def searchPokemon(name, identifier, pokemonData):
    for i, item in enumerate(pokemonData):
        if 'identifier' in item and item['identifier'] == identifier:
            return {'index': i, 'pokemon': item}
    for i, item in enumerate(pokemonData):
        if 'name' in item and item['name'] == name:
            return {'index': i, 'pokemon': item}
    return False

def prependIdentifier(pokemon, identifier):
    newPokemon = OrderedDict()
    newPokemon['identifier'] = identifier
    for i, row in enumerate(pokemon):
        newPokemon[row] = pokemon[row]
    return newPokemon

def enhancePokemonInformation(conn, pokemonData):

    cur = conn.execute(
        """SELECT
            egp.name AS egg_group_name
            , p.identifier
            , psn.name AS pokemon
            , psn.genus
            , pcn.name AS color
            , ps.gender_rate
            , ps.capture_rate
            , ps.base_happiness
            , ps.is_baby
            , ps.hatch_counter
            , ps.has_gender_differences
            , grp.name AS growth_rate
            , p.height
            , p.weight
            , p.base_experience
            FROM pokemon_species AS ps
            LEFT JOIN pokemon AS p ON ps.id = p.id
            LEFT JOIN pokemon_egg_groups AS peg ON ps.id = peg.species_id
            LEFT JOIN egg_group_prose AS egp ON peg.egg_group_id = egp.egg_group_id
            LEFT JOIN pokemon_species_names AS psn ON ps.id = psn.pokemon_species_id
            LEFT JOIN growth_rate_prose AS grp ON ps.growth_rate_id = grp.growth_rate_id
            LEFT JOIN pokemon_color_names AS pcn ON ps.color_id = pcn.pokemon_color_id
            WHERE psn.local_language_id = 9 -- english
            AND egp.local_language_id = 9 -- english
            AND grp.local_language_id = 9 -- english
            AND pcn.local_language_id = 9 -- english
            ORDER BY egp.name, psn.name
        ;""")

    for i, row in enumerate(cur):

        entry = searchPokemonByName(row['pokemon'], pokemonData)

        if 'identifier' in row and entry == False:
            entry = searchPokemonByIdentifier(row['identifier'], pokemonData)

        if entry:

            pokemon = entry['pokemon']

            if 'identifier' not in pokemon:
                pokemon = prependIdentifier(pokemon, row['identifier'])

            pokemon['genus'] = row['genus']
            pokemon['color'] = row['color']
            pokemon['genderRate'] = row['gender_rate']
            pokemon['captureRate'] = row['capture_rate']
            pokemon['baseHappiness'] = row['base_happiness']
            pokemon['baseHappiness'] = row['base_happiness']
            pokemon['isBaby'] = row['is_baby']
            pokemon['hatchCounter'] = row['hatch_counter']
            pokemon['hasGenderDifferences'] = row['has_gender_differences']
            pokemon['growthRate'] = row['growth_rate']
            pokemon['height'] = row['height']
            pokemon['weight'] = row['weight']
            pokemon['baseExperience'] = row['base_experience']

            if 'eggGroups' not in pokemon:
                pokemon['eggGroups'] = []

            if row['egg_group_name'] not in pokemon['eggGroups']:
                pokemon['eggGroups'].append(row['egg_group_name'])

            pokemonData[entry['index']] = pokemon
    return


def addEffortValues(conn, pokemonData):

    cur = conn.execute(
        """SELECT
            psn.name AS pokemon
            , sn.name AS stat_name
            , pst.effort
            , p.identifier
            , p.is_default
            FROM pokemon_stats pst
            LEFT JOIN pokemon AS p ON pst.pokemon_id = p.id
            LEFT JOIN pokemon_species AS ps ON p.species_id = ps.id
            LEFT JOIN pokemon_species_names AS psn ON ps.id = psn.pokemon_species_id
            LEFT JOIN stat_names AS sn ON pst.stat_id = sn.stat_id
            WHERE sn.local_language_id = 9 -- english
            AND psn.local_language_id = 9 -- english
            AND pst.effort > 0
            ORDER BY p."order", sn.name
        ;""")

    for i, row in enumerate(cur):

        entry = searchPokemon(row['pokemon'], row['identifier'], pokemonData)

        if entry:
            pokemon = entry['pokemon']

            if 'effortValues' not in pokemon:
                pokemon['effortValues'] = []

            effortValue = row['stat_name'] + ' (' + str(row['effort']) + ')'

            if effortValue not in pokemon['effortValues']:
                pokemon['effortValues'].append(effortValue)

            pokemonData[entry['index']] = pokemon

    return


def addEggMoves(conn, pokemonData):

    cur = conn.execute(
        """SELECT
            psn.name AS pokemon
            , mn.name AS move
            , p.identifier
            FROM pokemon_moves AS pm
            LEFT JOIN moves AS m ON pm.move_id = m.id
            LEFT JOIN move_names AS mn ON m.id = mn.move_id
            LEFT JOIN pokemon AS p ON pm.pokemon_id = p.id
            LEFT JOIN pokemon_species_names AS psn ON p.species_id = psn.pokemon_species_id
            WHERE pm.pokemon_move_method_id = 2 -- egg
            AND pm.version_group_id = 15 -- X/Y
            AND mn.local_language_id = 9 -- english
            AND psn.local_language_id = 9 -- english
            ORDER BY p."order", mn.name
        ;""")

    for i, row in enumerate(cur):

        entry = searchPokemon(row['pokemon'], row['identifier'], pokemonData)

        if entry:
            pokemon = entry['pokemon']

            if 'eggMoves' not in pokemon:
                pokemon['eggMoves'] = []

            if row[1] not in pokemon['eggMoves']:
                pokemon['eggMoves'].append(row[1])

            pokemonData[entry['index']] = pokemon

    return

def addPokedexNumbers(conn, pokemonData):

    cur = conn.execute(
        """SELECT
            psn.name AS pokemon
            , pdp.name AS pokedex
            , pdn.pokedex_number
            , ps.identifier
            FROM pokemon_dex_numbers AS pdn
            LEFT JOIN pokemon_species AS ps ON pdn.species_id = ps.id
            LEFT JOIN pokedex_prose AS pdp ON pdn.pokedex_id = pdp.pokedex_id
            LEFT JOIN pokemon_species_names AS psn ON ps.id = psn.pokemon_species_id
            AND psn.local_language_id = 9 -- english
            AND pdp.local_language_id = 9 -- english
            WHERE pdn.pokedex_id IN (1, 12, 13, 14) -- only national and all three kalos dexes
            ORDER BY ps."order"
        ;""")

    for i, row in enumerate(cur):

        entry = searchPokemon(row['pokemon'], row['identifier'], pokemonData)

        if entry:
            pokemon = entry['pokemon']

            if 'pokedexNumbers' not in pokemon:
                pokemon['pokedexNumbers'] = []

            effortValue = row['pokedex'] + ' (' + str(row['pokedex_number']) + ')'

            if effortValue not in pokemon['pokedexNumbers']:
                pokemon['pokedexNumbers'].append(effortValue)

            pokemonData[entry['index']] = pokemon

    return


pokedexDatabase = "pokedex/data/pokedex.sqlite"
pokemonData = []

conn = sqlite3.connect(pokedexDatabase)
conn.row_factory = sqlite3.Row

with open('pokemon.poke') as data_file:
    pokemonData = json.load(data_file, object_pairs_hook=collections.OrderedDict)

if pokemonData != []:

    enhancePokemonInformation(conn, pokemonData)
    addEggMoves(conn, pokemonData)
    addEffortValues(conn, pokemonData)
    addPokedexNumbers(conn, pokemonData)

    pokemonJson = json.dumps(pokemonData, ensure_ascii=False).encode('utf8')

    with open('pokemon.poke', 'w') as save_file:
    # with open('pokemonUpdated.poke', 'w') as save_file:
        save_file.write(pokemonJson)

conn.close()