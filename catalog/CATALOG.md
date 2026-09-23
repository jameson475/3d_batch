# 3D object generation — combined record

Objects defined: **100** · run: **12** · succeeded: **3**  
Tokens: 50,794 in / 45,485 out · Total cost (incl. retries): **$1.0878**  
Avg per object: $0.0907, 3,790 output tokens, 33.2s, 418 lines of code  
Projected cost for 100 objects at this average: **$9.07**

## By batch

| batch | defined | ok | total cost | avg cost | avg out tokens | avg lines | avg time |
|---|---|---|---|---|---|---|---|
| batch_01 | 10 | 2 | $0.7957 | $0.3979 | 16,700 | 462 | 146.0s |
| batch_02 | 10 | 0 | $0.0000 | $0.0000 | 0 | 0 | 0.0s |
| batch_03 | 10 | 0 | $0.0000 | $0.0000 | 0 | 0 | 0.0s |
| batch_04 | 10 | 0 | $0.0000 | $0.0000 | 0 | 0 | 0.0s |
| batch_05 | 10 | 0 | $0.0000 | $0.0000 | 0 | 0 | 0.0s |
| batch_06 | 10 | 0 | $0.0000 | $0.0000 | 0 | 0 | 0.0s |
| batch_07 | 10 | 0 | $0.0000 | $0.0000 | 0 | 0 | 0.0s |
| batch_08 | 10 | 1 | $0.2921 | $0.0292 | 1,208 | 329 | 10.7s |
| batch_09 | 10 | 0 | $0.0000 | $0.0000 | 0 | 0 | 0.0s |
| batch_10 | 10 | 0 | $0.0000 | $0.0000 | 0 | 0 | 0.0s |

## By category

| category | defined | ok | total cost | avg cost | avg out tokens | avg lines | avg time |
|---|---|---|---|---|---|---|---|
| architecture | 10 | 0 | $0.0000 | $0.0000 | 0 | 0 | 0.0s |
| character | 10 | 0 | $0.0000 | $0.0000 | 0 | 0 | 0.0s |
| food | 10 | 0 | $0.0000 | $0.0000 | 0 | 0 | 0.0s |
| furniture | 10 | 2 | $0.6614 | $0.3307 | 13,678 | 383 | 120.2s |
| indoor_scene | 10 | 0 | $0.0000 | $0.0000 | 0 | 0 | 0.0s |
| mechanical | 10 | 0 | $0.0000 | $0.0000 | 0 | 0 | 0.0s |
| nature | 10 | 0 | $0.0000 | $0.0000 | 0 | 0 | 0.0s |
| product | 20 | 1 | $0.4265 | $0.1422 | 6,043 | 488 | 52.8s |
| vehicle | 10 | 0 | $0.0000 | $0.0000 | 0 | 0 | 0.0s |

## All objects

| id | batch | category | status | out tokens | cost | lines | meshes | anim | UI | geometries |
|---|---|---|---|---|---|---|---|---|---|---|
| 001_armchair | batch_01 | furniture | ok | 15,273 | $0.3693 | 437 | 6 | y | n | Box Circle Cylinder Sphere |
| 002_desk_lamp | batch_01 | product | ok | 18,128 | $0.4265 | 488 | 1 | y | y | Box Cylinder Lathe Plane Torus Tube |
| 003_espresso_machine | batch_01 | product | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 004_vintage_car | batch_01 | vehicle | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 005_lighthouse | batch_01 | architecture | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 006_bonsai | batch_01 | nature | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 007_robot_arm | batch_01 | mechanical | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 008_ramen_bowl | batch_01 | food | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 009_office_corridor | batch_01 | indoor_scene | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 010_original_mascot | batch_01 | character | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 011_bookshelf | batch_02 | furniture | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 012_headphones | batch_02 | product | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 013_bicycle | batch_02 | vehicle | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 014_torii_gate | batch_02 | architecture | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 015_monstera | batch_02 | nature | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 016_wall_clock_gears | batch_02 | mechanical | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 017_birthday_cake | batch_02 | food | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 018_grocery_aisle | batch_02 | indoor_scene | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 019_explorer_robot | batch_02 | character | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 020_chess_set | batch_02 | product | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 021_office_chair | batch_03 | furniture | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 022_film_camera | batch_03 | product | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 023_game_controller | batch_03 | product | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 024_sailboat | batch_03 | vehicle | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 025_windmill | batch_03 | architecture | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 026_cactus_terrarium | batch_03 | nature | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 027_steam_engine | batch_03 | mechanical | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 028_sushi_platter | batch_03 | food | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 029_hospital_lobby | batch_03 | indoor_scene | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 030_original_dragon | batch_03 | character | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 031_bunk_bed | batch_04 | furniture | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 032_electric_kettle | batch_04 | product | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 033_smartwatch | batch_04 | product | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 034_forklift | batch_04 | vehicle | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 035_greenhouse | batch_04 | architecture | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 036_coral_reef | batch_04 | nature | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 037_typewriter | batch_04 | mechanical | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 038_pancake_stack | batch_04 | food | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 039_subway_platform | batch_04 | indoor_scene | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 040_original_owl | batch_04 | character | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 041_rocking_chair | batch_05 | furniture | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 042_quadcopter_drone | batch_05 | product | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 043_mechanical_keyboard | batch_05 | product | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 044_steam_locomotive | batch_05 | vehicle | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 045_log_cabin | batch_05 | architecture | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 046_maple_tree_autumn | batch_05 | nature | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 047_newtons_cradle | batch_05 | mechanical | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 048_pizza | batch_05 | food | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 049_library_reading_room | batch_05 | indoor_scene | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 050_original_snail_courier | batch_05 | character | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 051_kitchen_island | batch_06 | furniture | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 052_robot_vacuum | batch_06 | product | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 053_acoustic_guitar | batch_06 | product | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 054_biplane | batch_06 | vehicle | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 055_suspension_bridge | batch_06 | architecture | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 056_mushroom_log | batch_06 | nature | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 057_orrery | batch_06 | mechanical | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 058_burger_meal | batch_06 | food | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 059_airport_gate | batch_06 | indoor_scene | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 060_original_penguin_chef | batch_06 | character | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 061_study_desk | batch_07 | furniture | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 062_backpack | batch_07 | product | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 063_table_fan | batch_07 | product | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 064_delivery_scooter | batch_07 | vehicle | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 065_pagoda | batch_07 | architecture | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 066_waterfall | batch_07 | nature | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 067_tower_crane | batch_07 | mechanical | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 068_fruit_bowl | batch_07 | food | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 069_parking_garage | batch_07 | indoor_scene | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 070_original_jellyfish | batch_07 | character | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 071_velvet_sofa | batch_08 | furniture | ok | 12,084 | $0.2921 | 329 | 3 | y | n | Box Cylinder Plane |
| 072_stand_mixer | batch_08 | product | error: [Errno 2] No such file or directory: 'claude' | 0 | $0.0000 | 0 |  |  |  |  |
| 073_tube_radio | batch_08 | product | error: [Errno 2] No such file or directory: 'claude' | 0 | $0.0000 | 0 |  |  |  |  |
| 074_hot_air_balloon | batch_08 | vehicle | error: [Errno 2] No such file or directory: 'claude' | 0 | $0.0000 | 0 |  |  |  |  |
| 075_garden_gazebo | batch_08 | architecture | error: [Errno 2] No such file or directory: 'claude' | 0 | $0.0000 | 0 |  |  |  |  |
| 076_bamboo_grove | batch_08 | nature | error: [Errno 2] No such file or directory: 'claude' | 0 | $0.0000 | 0 |  |  |  |  |
| 077_wind_turbine | batch_08 | mechanical | error: [Errno 2] No such file or directory: 'claude' | 0 | $0.0000 | 0 |  |  |  |  |
| 078_dumplings_steamer | batch_08 | food | error: [Errno 2] No such file or directory: 'claude' | 0 | $0.0000 | 0 |  |  |  |  |
| 079_museum_gallery | batch_08 | indoor_scene | error: [Errno 2] No such file or directory: 'claude' | 0 | $0.0000 | 0 |  |  |  |  |
| 080_original_hedgehog_gardener | batch_08 | character | error: [Errno 2] No such file or directory: 'claude' | 0 | $0.0000 | 0 |  |  |  |  |
| 081_wardrobe | batch_09 | furniture | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 082_running_shoe | batch_09 | product | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 083_rotary_phone | batch_09 | product | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 084_research_submarine | batch_09 | vehicle | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 085_glass_house | batch_09 | architecture | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 086_desert_arch | batch_09 | nature | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 087_oil_pumpjack | batch_09 | mechanical | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 088_ice_cream_sundae | batch_09 | food | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 089_classroom | batch_09 | indoor_scene | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 090_original_hamster_astronaut | batch_09 | character | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 091_vanity_dresser | batch_10 | furniture | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 092_camping_lantern | batch_10 | product | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 093_skateboard | batch_10 | product | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 094_fire_truck | batch_10 | vehicle | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 095_castle_gatehouse | batch_10 | architecture | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 096_lotus_pond | batch_10 | nature | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 097_music_box | batch_10 | mechanical | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 098_taco_plate | batch_10 | food | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 099_mall_atrium | batch_10 | indoor_scene | not_run | 0 | $0.0000 | 0 |  |  |  |  |
| 100_original_sloth | batch_10 | character | not_run | 0 | $0.0000 | 0 |  |  |  |  |
