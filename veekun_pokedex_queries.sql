-- all moves learned from breeding
SELECT
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
ORDER BY p."order", mn.name;

-- all information about breeding
SELECT
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
ORDER BY egp.name, psn.name;

-- effort values
SELECT
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
ORDER BY p."order", sn.name;

-- pokedex numbers
SELECT
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
ORDER BY ps."order";
