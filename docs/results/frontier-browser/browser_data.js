window.BROWSER_DATA = {
  "project": "EA Lab A8 Mario PCG",
  "cases": [
    {
      "id": "core_3obj_seed7",
      "title": "core baseline",
      "algorithm": "nsga2",
      "objective_mode": "core_3obj",
      "config": {
        "population_size": 30,
        "mutation_rate": 0.2,
        "generations": 12,
        "seed": 7,
        "num_segments": 8,
        "segment_width": 14,
        "target_difficulty": 0.55,
        "target_emptiness": 0.45
      },
      "evaluation": {
        "difficulty_score": 0.175,
        "difficulty_error": 0.37500000000000006,
        "structural_diversity": 0.625,
        "emptiness_error": 0.3362723214285714,
        "emptiness": 0.7862723214285714,
        "difficulty_curve_error": 1.0,
        "family_balance": 0.5249999999999999
      },
      "constraints": {
        "is_feasible": true,
        "start_ok": true,
        "goal_ok": true,
        "reachable": true,
        "illegal_overlap": false,
        "max_gap_ok": true,
        "enemy_rules_ok": true,
        "pipe_rules_ok": true,
        "placement_rules_ok": true,
        "violation_count": 0,
        "violations": []
      },
      "best_level": {
        "png_path": "assets/core_3obj_seed7/best_level.png",
        "ascii_path": "assets/core_3obj_seed7/best_level.txt",
        "ascii_text": "................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n..............................................................?.............?...........................?.......\n.......o........................................................................................................\n..BBBBBBBBBB.....................?..?..........?..?.........BBBBBB........BBBBBB.........?..?.........BBBBBB....\n....PP...PP.........?...........................................................................................\n....PP...PP..................BBBBBBBBBBBB..BBBBBBBBBBBB...PP............PP...........BBBBBBBBBBBB...PP..........\n....PP...PP...............................................PPBBBBBBBB....PPBBBBBBBB..................PPBBBBBBBB..\n....PP...PP...............................................PP............PP..........................PP..........\n.S..PP...PP......E.....E.......E......E......E......E.....PP....E..E....PP....E..E.....E......E.....PP....E..EG.\n################################################################################################################\n################################################################################################################\n",
        "chromosome": [
          14,
          9,
          11,
          11,
          17,
          17,
          11,
          17
        ],
        "segment_metadata": [
          {
            "segment_id": 14,
            "family": "pipe_pressure",
            "variant": "double_pipe_bridge",
            "difficulty_tier": 3
          },
          {
            "segment_id": 9,
            "family": "mixed_challenge",
            "variant": "dual_enemy_reward",
            "difficulty_tier": 3
          },
          {
            "segment_id": 11,
            "family": "enemy_pressure",
            "variant": "double_enemy_bridges",
            "difficulty_tier": 3
          },
          {
            "segment_id": 11,
            "family": "enemy_pressure",
            "variant": "double_enemy_bridges",
            "difficulty_tier": 3
          },
          {
            "segment_id": 17,
            "family": "mixed_challenge",
            "variant": "pipe_enemy_stack",
            "difficulty_tier": 3
          },
          {
            "segment_id": 17,
            "family": "mixed_challenge",
            "variant": "pipe_enemy_stack",
            "difficulty_tier": 3
          },
          {
            "segment_id": 11,
            "family": "enemy_pressure",
            "variant": "double_enemy_bridges",
            "difficulty_tier": 3
          },
          {
            "segment_id": 17,
            "family": "mixed_challenge",
            "variant": "pipe_enemy_stack",
            "difficulty_tier": 3
          }
        ]
      },
      "logs": [
        {
          "generation": 0,
          "feasible_ratio": 0.06666666666666667,
          "first_front_size": 1,
          "first_front_hv": 0.20171526227678568,
          "first_front_spread": 0.0,
          "best_difficulty_error": 0.45000000000000007,
          "best_structural_diversity": 0.5625,
          "best_emptiness_error": 0.3479910714285714,
          "best_emptiness": 0.7979910714285714,
          "best_difficulty_curve_error": 1.125,
          "best_family_balance": 0.675
        },
        {
          "generation": 1,
          "feasible_ratio": 0.13333333333333333,
          "first_front_size": 3,
          "first_front_hv": 0.2250275530133928,
          "first_front_spread": 0.03592522717904257,
          "best_difficulty_error": 0.45000000000000007,
          "best_structural_diversity": 0.5625,
          "best_emptiness_error": 0.3479910714285714,
          "best_emptiness": 0.7979910714285714,
          "best_difficulty_curve_error": 1.125,
          "best_family_balance": 0.675
        },
        {
          "generation": 2,
          "feasible_ratio": 0.4,
          "first_front_size": 4,
          "first_front_hv": 0.22509905133928565,
          "first_front_spread": 0.03280199718178979,
          "best_difficulty_error": 0.45000000000000007,
          "best_structural_diversity": 0.5625,
          "best_emptiness_error": 0.3457589285714286,
          "best_emptiness": 0.7957589285714286,
          "best_difficulty_curve_error": 0.6964285714285714,
          "best_family_balance": 0.63
        },
        {
          "generation": 3,
          "feasible_ratio": 0.9666666666666667,
          "first_front_size": 8,
          "first_front_hv": 0.2287709263392857,
          "first_front_spread": 0.032895247854109765,
          "best_difficulty_error": 0.42500000000000004,
          "best_structural_diversity": 0.5,
          "best_emptiness_error": 0.3580357142857143,
          "best_emptiness": 0.8080357142857143,
          "best_difficulty_curve_error": 0.9464285714285714,
          "best_family_balance": 0.7124999999999999
        },
        {
          "generation": 4,
          "feasible_ratio": 1.0,
          "first_front_size": 8,
          "first_front_hv": 0.2306604875837054,
          "first_front_spread": 0.05250978294616941,
          "best_difficulty_error": 0.42500000000000004,
          "best_structural_diversity": 0.5,
          "best_emptiness_error": 0.3580357142857143,
          "best_emptiness": 0.8080357142857143,
          "best_difficulty_curve_error": 0.9464285714285714,
          "best_family_balance": 0.7124999999999999
        },
        {
          "generation": 5,
          "feasible_ratio": 1.0,
          "first_front_size": 4,
          "first_front_hv": 0.23552900041852676,
          "first_front_spread": 0.053394675789815486,
          "best_difficulty_error": 0.4125000000000001,
          "best_structural_diversity": 0.5,
          "best_emptiness_error": 0.3541294642857143,
          "best_emptiness": 0.8041294642857143,
          "best_difficulty_curve_error": 0.6428571428571428,
          "best_family_balance": 0.475
        },
        {
          "generation": 6,
          "feasible_ratio": 1.0,
          "first_front_size": 10,
          "first_front_hv": 0.24635410853794643,
          "first_front_spread": 0.03543548702165378,
          "best_difficulty_error": 0.4,
          "best_structural_diversity": 0.5625,
          "best_emptiness_error": 0.3485491071428571,
          "best_emptiness": 0.7985491071428571,
          "best_difficulty_curve_error": 0.8571428571428571,
          "best_family_balance": 0.475
        },
        {
          "generation": 7,
          "feasible_ratio": 1.0,
          "first_front_size": 5,
          "first_front_hv": 0.2515885707310268,
          "first_front_spread": 0.04042124244134218,
          "best_difficulty_error": 0.38750000000000007,
          "best_structural_diversity": 0.5625,
          "best_emptiness_error": 0.35859375,
          "best_emptiness": 0.80859375,
          "best_difficulty_curve_error": 0.6964285714285714,
          "best_family_balance": 0.5249999999999999
        },
        {
          "generation": 8,
          "feasible_ratio": 1.0,
          "first_front_size": 9,
          "first_front_hv": 0.24623526436941962,
          "first_front_spread": 0.02543153195394287,
          "best_difficulty_error": 0.38750000000000007,
          "best_structural_diversity": 0.5625,
          "best_emptiness_error": 0.35859375,
          "best_emptiness": 0.80859375,
          "best_difficulty_curve_error": 0.6964285714285714,
          "best_family_balance": 0.5249999999999999
        },
        {
          "generation": 9,
          "feasible_ratio": 1.0,
          "first_front_size": 19,
          "first_front_hv": 0.25809674944196426,
          "first_front_spread": 0.02901477763350991,
          "best_difficulty_error": 0.37500000000000006,
          "best_structural_diversity": 0.5,
          "best_emptiness_error": 0.34296875,
          "best_emptiness": 0.79296875,
          "best_difficulty_curve_error": 0.8214285714285714,
          "best_family_balance": 0.5249999999999999
        },
        {
          "generation": 10,
          "feasible_ratio": 1.0,
          "first_front_size": 30,
          "first_front_hv": 0.26470947265624994,
          "first_front_spread": 0.02187187302394631,
          "best_difficulty_error": 0.37500000000000006,
          "best_structural_diversity": 0.625,
          "best_emptiness_error": 0.3362723214285714,
          "best_emptiness": 0.7862723214285714,
          "best_difficulty_curve_error": 1.0,
          "best_family_balance": 0.5249999999999999
        },
        {
          "generation": 11,
          "feasible_ratio": 1.0,
          "first_front_size": 7,
          "first_front_hv": 0.2649972098214285,
          "first_front_spread": 0.029918173624112997,
          "best_difficulty_error": 0.37500000000000006,
          "best_structural_diversity": 0.625,
          "best_emptiness_error": 0.3362723214285714,
          "best_emptiness": 0.7862723214285714,
          "best_difficulty_curve_error": 1.0,
          "best_family_balance": 0.5249999999999999
        }
      ],
      "frontier": [
        {
          "rank": 1,
          "png_path": "assets/core_3obj_seed7/frontier_levels/frontier_01.png",
          "ascii_path": "assets/core_3obj_seed7/frontier_levels/frontier_01.txt",
          "ascii_text": "................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n..............................................................?.............?...........................?.......\n.......o........................................................................................................\n..BBBBBBBBBB.....................?..?..........?..?.........BBBBBB........BBBBBB.........?..?.........BBBBBB....\n....PP...PP.........?...........................................................................................\n....PP...PP..................BBBBBBBBBBBB..BBBBBBBBBBBB...PP............PP...........BBBBBBBBBBBB...PP..........\n....PP...PP...............................................PPBBBBBBBB....PPBBBBBBBB..................PPBBBBBBBB..\n....PP...PP...............................................PP............PP..........................PP..........\n.S..PP...PP......E.....E.......E......E......E......E.....PP....E..E....PP....E..E.....E......E.....PP....E..EG.\n################################################################################################################\n################################################################################################################\n",
          "evaluation": {
            "difficulty_curve_error": 1.0,
            "difficulty_error": 0.37500000000000006,
            "difficulty_score": 0.175,
            "emptiness": 0.7862723214285714,
            "emptiness_error": 0.3362723214285714,
            "family_balance": 0.5249999999999999,
            "structural_diversity": 0.625
          },
          "constraints": {
            "enemy_rules_ok": true,
            "goal_ok": true,
            "illegal_overlap": false,
            "is_feasible": true,
            "max_gap_ok": true,
            "pipe_rules_ok": true,
            "placement_rules_ok": true,
            "reachable": true,
            "start_ok": true,
            "violation_count": 0,
            "violations": []
          },
          "chromosome": [
            14,
            9,
            11,
            11,
            17,
            17,
            11,
            17
          ],
          "segment_metadata": [
            {
              "difficulty_tier": 3,
              "family": "pipe_pressure",
              "segment_id": 14,
              "variant": "double_pipe_bridge"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 9,
              "variant": "dual_enemy_reward"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            }
          ]
        },
        {
          "rank": 2,
          "png_path": "assets/core_3obj_seed7/frontier_levels/frontier_02.png",
          "ascii_path": "assets/core_3obj_seed7/frontier_levels/frontier_02.txt",
          "ascii_text": "................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n..............................................................?.........................................?.......\n.......o.....................................................................o..................................\n..BBBBBBBBBB.......?..?...........oo...........?..?.........BBBBBB......BBBBBBBBBB........oo..........BBBBBB....\n....PP...PP....................BBBBBBBB...................................PP...PP......BBBBBBBB.................\n....PP...PP....BBBBBBBBBBBB................BBBBBBBBBBBB...PP..............PP...PP...................PP..........\n....PP...PP...............................................PPBBBBBBBB......PP...PP...................PPBBBBBBBB..\n....PP...PP.................BBBBBB..BBBBBB................PP..............PP...PP...BBBBBB..BBBBBB..PP..........\n.S..PP...PP......E......E....................E......E.....PP....E..E......PP...PP...................PP....E..EG.\n################################################################################################################\n################################################################################################################\n",
          "evaluation": {
            "difficulty_curve_error": 1.0,
            "difficulty_error": 0.45000000000000007,
            "difficulty_score": 0.09999999999999999,
            "emptiness": 0.7689732142857143,
            "emptiness_error": 0.3189732142857143,
            "family_balance": 1.0,
            "structural_diversity": 0.625
          },
          "constraints": {
            "enemy_rules_ok": true,
            "goal_ok": true,
            "illegal_overlap": false,
            "is_feasible": true,
            "max_gap_ok": true,
            "pipe_rules_ok": true,
            "placement_rules_ok": true,
            "reachable": true,
            "start_ok": true,
            "violation_count": 0,
            "violations": []
          },
          "chromosome": [
            14,
            11,
            12,
            11,
            17,
            14,
            12,
            17
          ],
          "segment_metadata": [
            {
              "difficulty_tier": 3,
              "family": "pipe_pressure",
              "segment_id": 14,
              "variant": "double_pipe_bridge"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            },
            {
              "difficulty_tier": 3,
              "family": "gap_jump",
              "segment_id": 12,
              "variant": "ceiling_gap_reward"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            },
            {
              "difficulty_tier": 3,
              "family": "pipe_pressure",
              "segment_id": 14,
              "variant": "double_pipe_bridge"
            },
            {
              "difficulty_tier": 3,
              "family": "gap_jump",
              "segment_id": 12,
              "variant": "ceiling_gap_reward"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            }
          ]
        },
        {
          "rank": 3,
          "png_path": "assets/core_3obj_seed7/frontier_levels/frontier_03.png",
          "ascii_path": "assets/core_3obj_seed7/frontier_levels/frontier_03.txt",
          "ascii_text": "................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n..............................................................?.............?...................................\n.......o.................................................................................................o......\n..BBBBBBBBBB.......?..?...........oo...........?..?.........BBBBBB........BBBBBB..........oo........BBBBBBBBBB..\n....PP...PP....................BBBBBBBB................................................BBBBBBBB.......PP...PP...\n....PP...PP....BBBBBBBBBBBB................BBBBBBBBBBBB...PP............PP............................PP...PP...\n....PP...PP...............................................PPBBBBBBBB....PPBBBBBBBB....................PP...PP...\n....PP...PP.................BBBBBB..BBBBBB................PP............PP..........BBBBBB..BBBBBB....PP...PP...\n.S..PP...PP......E......E....................E......E.....PP....E..E....PP....E..E....................PP...PP.G.\n################################################################################################################\n################################################################################################################\n",
          "evaluation": {
            "difficulty_curve_error": 1.0,
            "difficulty_error": 0.45000000000000007,
            "difficulty_score": 0.09999999999999999,
            "emptiness": 0.7689732142857143,
            "emptiness_error": 0.3189732142857143,
            "family_balance": 0.95,
            "structural_diversity": 0.625
          },
          "constraints": {
            "enemy_rules_ok": true,
            "goal_ok": true,
            "illegal_overlap": false,
            "is_feasible": true,
            "max_gap_ok": true,
            "pipe_rules_ok": true,
            "placement_rules_ok": true,
            "reachable": true,
            "start_ok": true,
            "violation_count": 0,
            "violations": []
          },
          "chromosome": [
            14,
            11,
            12,
            11,
            17,
            17,
            12,
            14
          ],
          "segment_metadata": [
            {
              "difficulty_tier": 3,
              "family": "pipe_pressure",
              "segment_id": 14,
              "variant": "double_pipe_bridge"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            },
            {
              "difficulty_tier": 3,
              "family": "gap_jump",
              "segment_id": 12,
              "variant": "ceiling_gap_reward"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            },
            {
              "difficulty_tier": 3,
              "family": "gap_jump",
              "segment_id": 12,
              "variant": "ceiling_gap_reward"
            },
            {
              "difficulty_tier": 3,
              "family": "pipe_pressure",
              "segment_id": 14,
              "variant": "double_pipe_bridge"
            }
          ]
        },
        {
          "rank": 4,
          "png_path": "assets/core_3obj_seed7/frontier_levels/frontier_04.png",
          "ascii_path": "assets/core_3obj_seed7/frontier_levels/frontier_04.txt",
          "ascii_text": "................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n..............................................................?.............?...........................?.......\n.......o........................................................................................................\n..BBBBBBBBBB.......?..?...........oo...........?..?.........BBBBBB........BBBBBB.........?..?.........BBBBBB....\n....PP...PP....................BBBBBBBB.........................................................................\n....PP...PP....BBBBBBBBBBBB................BBBBBBBBBBBB...PP............PP...........BBBBBBBBBBBB...PP..........\n....PP...PP...............................................PPBBBBBBBB....PPBBBBBBBB..................PPBBBBBBBB..\n....PP...PP.................BBBBBB..BBBBBB................PP............PP..........................PP..........\n.S..PP...PP......E......E....................E......E.....PP....E..E....PP....E..E.....E......E.....PP....E..EG.\n################################################################################################################\n################################################################################################################\n",
          "evaluation": {
            "difficulty_curve_error": 1.0,
            "difficulty_error": 0.4,
            "difficulty_score": 0.15,
            "emptiness": 0.7756696428571429,
            "emptiness_error": 0.3256696428571429,
            "family_balance": 0.475,
            "structural_diversity": 0.625
          },
          "constraints": {
            "enemy_rules_ok": true,
            "goal_ok": true,
            "illegal_overlap": false,
            "is_feasible": true,
            "max_gap_ok": true,
            "pipe_rules_ok": true,
            "placement_rules_ok": true,
            "reachable": true,
            "start_ok": true,
            "violation_count": 0,
            "violations": []
          },
          "chromosome": [
            14,
            11,
            12,
            11,
            17,
            17,
            11,
            17
          ],
          "segment_metadata": [
            {
              "difficulty_tier": 3,
              "family": "pipe_pressure",
              "segment_id": 14,
              "variant": "double_pipe_bridge"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            },
            {
              "difficulty_tier": 3,
              "family": "gap_jump",
              "segment_id": 12,
              "variant": "ceiling_gap_reward"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            }
          ]
        },
        {
          "rank": 5,
          "png_path": "assets/core_3obj_seed7/frontier_levels/frontier_05.png",
          "ascii_path": "assets/core_3obj_seed7/frontier_levels/frontier_05.txt",
          "ascii_text": "................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n..............................................................?.........................................?.......\n.......o.....................................................................o..................................\n..BBBBBBBBBB.......?..?...........oo...........?..?.........BBBBBB......BBBBBBBBBB.......?..?.........BBBBBB....\n....PP...PP....................BBBBBBBB...................................PP...PP...............................\n....PP...PP....BBBBBBBBBBBB................BBBBBBBBBBBB...PP..............PP...PP....BBBBBBBBBBBB...PP..........\n....PP...PP...............................................PPBBBBBBBB......PP...PP...................PPBBBBBBBB..\n....PP...PP.................BBBBBB..BBBBBB................PP..............PP...PP...................PP..........\n.S..PP...PP......E......E....................E......E.....PP....E..E......PP...PP......E......E.....PP....E..EG.\n################################################################################################################\n################################################################################################################\n",
          "evaluation": {
            "difficulty_curve_error": 1.0,
            "difficulty_error": 0.42500000000000004,
            "difficulty_score": 0.125,
            "emptiness": 0.7723214285714286,
            "emptiness_error": 0.3223214285714286,
            "family_balance": 0.75,
            "structural_diversity": 0.625
          },
          "constraints": {
            "enemy_rules_ok": true,
            "goal_ok": true,
            "illegal_overlap": false,
            "is_feasible": true,
            "max_gap_ok": true,
            "pipe_rules_ok": true,
            "placement_rules_ok": true,
            "reachable": true,
            "start_ok": true,
            "violation_count": 0,
            "violations": []
          },
          "chromosome": [
            14,
            11,
            12,
            11,
            17,
            14,
            11,
            17
          ],
          "segment_metadata": [
            {
              "difficulty_tier": 3,
              "family": "pipe_pressure",
              "segment_id": 14,
              "variant": "double_pipe_bridge"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            },
            {
              "difficulty_tier": 3,
              "family": "gap_jump",
              "segment_id": 12,
              "variant": "ceiling_gap_reward"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            },
            {
              "difficulty_tier": 3,
              "family": "pipe_pressure",
              "segment_id": 14,
              "variant": "double_pipe_bridge"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            }
          ]
        }
      ],
      "final_front_hv": 0.2649972098214285,
      "final_front_spread": 0.029918173624112997,
      "final_front_size": 7
    },
    {
      "id": "family_4obj_seed27",
      "title": "family showcase",
      "algorithm": "nsga2",
      "objective_mode": "family_4obj",
      "config": {
        "population_size": 30,
        "mutation_rate": 0.2,
        "generations": 12,
        "seed": 27,
        "num_segments": 8,
        "segment_width": 14,
        "target_difficulty": 0.55,
        "target_emptiness": 0.45
      },
      "evaluation": {
        "difficulty_score": 0.049999999999999996,
        "difficulty_error": 0.5,
        "structural_diversity": 0.625,
        "emptiness_error": 0.3368303571428571,
        "emptiness": 0.7868303571428571,
        "difficulty_curve_error": 0.8571428571428572,
        "family_balance": 1.0
      },
      "constraints": {
        "is_feasible": true,
        "start_ok": true,
        "goal_ok": true,
        "reachable": true,
        "illegal_overlap": false,
        "max_gap_ok": true,
        "enemy_rules_ok": true,
        "pipe_rules_ok": true,
        "placement_rules_ok": true,
        "violation_count": 0,
        "violations": []
      },
      "best_level": {
        "png_path": "assets/family_4obj_seed27/best_level.png",
        "ascii_path": "assets/family_4obj_seed27/best_level.txt",
        "ascii_text": "................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n..........................................................................o.o.o.................................\n......o........................................................o.........????????..........o....................\n....BBBBBB.......................?..?...........oo........BBBBBBBBBB..................BBBBBBBBBB.......?..?.....\n.............................................BBBBBBBB.......PP...PP.....................PP...PP.................\n.............................BBBBBBBBBBBB...................PP...PP....BBBBBBBBBBBB.....PP...PP....BBBBBBBBBBBB.\n..BBBBBBBBBB................................................PP...PP.....................PP...PP.................\n..........................................BBBBBB..BBBBBB....PP...PP.....................PP...PP.................\n.S.............................E......E.....................PP...PP.....................PP...PP......E......E.G.\n################################################################################################################\n################################################################################################################\n",
        "chromosome": [
          10,
          8,
          11,
          12,
          14,
          16,
          14,
          11
        ],
        "segment_metadata": [
          {
            "segment_id": 10,
            "family": "reward_relief",
            "variant": "double_shelf_coin",
            "difficulty_tier": 1
          },
          {
            "segment_id": 8,
            "family": "gap_jump",
            "variant": "full_gap_lane",
            "difficulty_tier": 3
          },
          {
            "segment_id": 11,
            "family": "enemy_pressure",
            "variant": "double_enemy_bridges",
            "difficulty_tier": 3
          },
          {
            "segment_id": 12,
            "family": "gap_jump",
            "variant": "ceiling_gap_reward",
            "difficulty_tier": 3
          },
          {
            "segment_id": 14,
            "family": "pipe_pressure",
            "variant": "double_pipe_bridge",
            "difficulty_tier": 3
          },
          {
            "segment_id": 16,
            "family": "reward_relief",
            "variant": "question_arc",
            "difficulty_tier": 1
          },
          {
            "segment_id": 14,
            "family": "pipe_pressure",
            "variant": "double_pipe_bridge",
            "difficulty_tier": 3
          },
          {
            "segment_id": 11,
            "family": "enemy_pressure",
            "variant": "double_enemy_bridges",
            "difficulty_tier": 3
          }
        ]
      },
      "logs": [
        {
          "generation": 0,
          "feasible_ratio": 0.06666666666666667,
          "first_front_size": 2,
          "first_front_hv": 0.16363113839285715,
          "first_front_spread": 0.16898604051150232,
          "best_difficulty_error": 0.525,
          "best_structural_diversity": 0.5,
          "best_emptiness_error": 0.3915178571428571,
          "best_emptiness": 0.8415178571428571,
          "best_difficulty_curve_error": 0.8035714285714286,
          "best_family_balance": 0.55
        },
        {
          "generation": 1,
          "feasible_ratio": 0.16666666666666666,
          "first_front_size": 4,
          "first_front_hv": 0.30024135044642847,
          "first_front_spread": 0.22545389923524264,
          "best_difficulty_error": 0.5,
          "best_structural_diversity": 0.5625,
          "best_emptiness_error": 0.3714285714285714,
          "best_emptiness": 0.8214285714285714,
          "best_difficulty_curve_error": 0.4464285714285715,
          "best_family_balance": 0.5225
        },
        {
          "generation": 2,
          "feasible_ratio": 0.4,
          "first_front_size": 6,
          "first_front_hv": 0.30625837053571425,
          "first_front_spread": 0.14035302209135136,
          "best_difficulty_error": 0.5,
          "best_structural_diversity": 0.5625,
          "best_emptiness_error": 0.3714285714285714,
          "best_emptiness": 0.8214285714285714,
          "best_difficulty_curve_error": 0.4464285714285715,
          "best_family_balance": 0.5225
        },
        {
          "generation": 3,
          "feasible_ratio": 1.0,
          "first_front_size": 6,
          "first_front_hv": 0.22819190848214282,
          "first_front_spread": 0.14237769835021616,
          "best_difficulty_error": 0.47500000000000003,
          "best_structural_diversity": 0.625,
          "best_emptiness_error": 0.3770089285714286,
          "best_emptiness": 0.8270089285714286,
          "best_difficulty_curve_error": 0.7857142857142857,
          "best_family_balance": 0.6649999999999999
        },
        {
          "generation": 4,
          "feasible_ratio": 1.0,
          "first_front_size": 11,
          "first_front_hv": 0.24101049107142858,
          "first_front_spread": 0.131490739072692,
          "best_difficulty_error": 0.45000000000000007,
          "best_structural_diversity": 0.5625,
          "best_emptiness_error": 0.3825892857142857,
          "best_emptiness": 0.8325892857142857,
          "best_difficulty_curve_error": 0.5892857142857143,
          "best_family_balance": 0.6649999999999999
        },
        {
          "generation": 5,
          "feasible_ratio": 1.0,
          "first_front_size": 23,
          "first_front_hv": 0.24441367187500002,
          "first_front_spread": 0.12363734356331686,
          "best_difficulty_error": 0.45000000000000007,
          "best_structural_diversity": 0.5625,
          "best_emptiness_error": 0.3825892857142857,
          "best_emptiness": 0.8325892857142857,
          "best_difficulty_curve_error": 0.5892857142857143,
          "best_family_balance": 0.6649999999999999
        },
        {
          "generation": 6,
          "feasible_ratio": 1.0,
          "first_front_size": 5,
          "first_front_hv": 0.27512346540178567,
          "first_front_spread": 0.13531587749644755,
          "best_difficulty_error": 0.45000000000000007,
          "best_structural_diversity": 0.625,
          "best_emptiness_error": 0.3613839285714286,
          "best_emptiness": 0.8113839285714286,
          "best_difficulty_curve_error": 0.5892857142857143,
          "best_family_balance": 0.75
        },
        {
          "generation": 7,
          "feasible_ratio": 1.0,
          "first_front_size": 7,
          "first_front_hv": 0.27857282366071423,
          "first_front_spread": 0.11343878557338707,
          "best_difficulty_error": 0.45000000000000007,
          "best_structural_diversity": 0.625,
          "best_emptiness_error": 0.3613839285714286,
          "best_emptiness": 0.8113839285714286,
          "best_difficulty_curve_error": 0.5892857142857143,
          "best_family_balance": 0.75
        },
        {
          "generation": 8,
          "feasible_ratio": 1.0,
          "first_front_size": 19,
          "first_front_hv": 0.1442527901785714,
          "first_front_spread": 0.1432443274392283,
          "best_difficulty_error": 0.43750000000000006,
          "best_structural_diversity": 0.625,
          "best_emptiness_error": 0.3619419642857143,
          "best_emptiness": 0.8119419642857143,
          "best_difficulty_curve_error": 0.4464285714285714,
          "best_family_balance": 0.35999999999999993
        },
        {
          "generation": 9,
          "feasible_ratio": 1.0,
          "first_front_size": 29,
          "first_front_hv": 0.2924358258928571,
          "first_front_spread": 0.1489035243444454,
          "best_difficulty_error": 0.42500000000000004,
          "best_structural_diversity": 0.625,
          "best_emptiness_error": 0.3524553571428571,
          "best_emptiness": 0.8024553571428571,
          "best_difficulty_curve_error": 0.8392857142857143,
          "best_family_balance": 0.5
        },
        {
          "generation": 10,
          "feasible_ratio": 1.0,
          "first_front_size": 30,
          "first_front_hv": 0.36497433035714283,
          "first_front_spread": 0.13996533873008019,
          "best_difficulty_error": 0.42500000000000004,
          "best_structural_diversity": 0.625,
          "best_emptiness_error": 0.3524553571428571,
          "best_emptiness": 0.8024553571428571,
          "best_difficulty_curve_error": 0.8392857142857143,
          "best_family_balance": 0.5
        },
        {
          "generation": 11,
          "feasible_ratio": 1.0,
          "first_front_size": 30,
          "first_front_hv": 0.38393159179687497,
          "first_front_spread": 0.17027191811849066,
          "best_difficulty_error": 0.42500000000000004,
          "best_structural_diversity": 0.625,
          "best_emptiness_error": 0.3373883928571429,
          "best_emptiness": 0.7873883928571429,
          "best_difficulty_curve_error": 0.75,
          "best_family_balance": 0.5225
        }
      ],
      "frontier": [
        {
          "rank": 1,
          "png_path": "assets/family_4obj_seed27/frontier_levels/frontier_01.png",
          "ascii_path": "assets/family_4obj_seed27/frontier_levels/frontier_01.txt",
          "ascii_text": "................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n..........................................................................o.o.o.................................\n......o........................................................o.........????????..........o....................\n....BBBBBB.......................?..?...........oo........BBBBBBBBBB..................BBBBBBBBBB.......?..?.....\n.............................................BBBBBBBB.......PP...PP.....................PP...PP.................\n.............................BBBBBBBBBBBB...................PP...PP....BBBBBBBBBBBB.....PP...PP....BBBBBBBBBBBB.\n..BBBBBBBBBB................................................PP...PP.....................PP...PP.................\n..........................................BBBBBB..BBBBBB....PP...PP.....................PP...PP.................\n.S.............................E......E.....................PP...PP.....................PP...PP......E......E.G.\n################################################################################################################\n################################################################################################################\n",
          "evaluation": {
            "difficulty_curve_error": 0.8571428571428572,
            "difficulty_error": 0.5,
            "difficulty_score": 0.049999999999999996,
            "emptiness": 0.7868303571428571,
            "emptiness_error": 0.3368303571428571,
            "family_balance": 1.0,
            "structural_diversity": 0.625
          },
          "constraints": {
            "enemy_rules_ok": true,
            "goal_ok": true,
            "illegal_overlap": false,
            "is_feasible": true,
            "max_gap_ok": true,
            "pipe_rules_ok": true,
            "placement_rules_ok": true,
            "reachable": true,
            "start_ok": true,
            "violation_count": 0,
            "violations": []
          },
          "chromosome": [
            10,
            8,
            11,
            12,
            14,
            16,
            14,
            11
          ],
          "segment_metadata": [
            {
              "difficulty_tier": 1,
              "family": "reward_relief",
              "segment_id": 10,
              "variant": "double_shelf_coin"
            },
            {
              "difficulty_tier": 3,
              "family": "gap_jump",
              "segment_id": 8,
              "variant": "full_gap_lane"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            },
            {
              "difficulty_tier": 3,
              "family": "gap_jump",
              "segment_id": 12,
              "variant": "ceiling_gap_reward"
            },
            {
              "difficulty_tier": 3,
              "family": "pipe_pressure",
              "segment_id": 14,
              "variant": "double_pipe_bridge"
            },
            {
              "difficulty_tier": 1,
              "family": "reward_relief",
              "segment_id": 16,
              "variant": "question_arc"
            },
            {
              "difficulty_tier": 3,
              "family": "pipe_pressure",
              "segment_id": 14,
              "variant": "double_pipe_bridge"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            }
          ]
        },
        {
          "rank": 2,
          "png_path": "assets/family_4obj_seed27/frontier_levels/frontier_02.png",
          "ascii_path": "assets/family_4obj_seed27/frontier_levels/frontier_02.txt",
          "ascii_text": "................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n..................o.o.o...................................................o.o.o.................................\n......o..........????????..........o...........................o.........????????..........o....................\n....BBBBBB....................BBBBBBBBBB........oo........BBBBBBBBBB..................BBBBBBBBBB.......?..?.....\n................................PP...PP......BBBBBBBB.......PP...PP.....................PP...PP.................\n...............BBBBBBBBBBBB.....PP...PP.....................PP...PP....BBBBBBBBBBBB.....PP...PP....BBBBBBBBBBBB.\n..BBBBBBBBBB....................PP...PP.....................PP...PP.....................PP...PP.................\n................................PP...PP...BBBBBB..BBBBBB....PP...PP.....................PP...PP.................\n.S..............................PP...PP.....................PP...PP.....................PP...PP......E......E.G.\n################################################################################################################\n################################################################################################################\n",
          "evaluation": {
            "difficulty_curve_error": 0.6785714285714286,
            "difficulty_error": 0.525,
            "difficulty_score": 0.024999999999999998,
            "emptiness": 0.765625,
            "emptiness_error": 0.315625,
            "family_balance": 0.475,
            "structural_diversity": 0.625
          },
          "constraints": {
            "enemy_rules_ok": true,
            "goal_ok": true,
            "illegal_overlap": false,
            "is_feasible": true,
            "max_gap_ok": true,
            "pipe_rules_ok": true,
            "placement_rules_ok": true,
            "reachable": true,
            "start_ok": true,
            "violation_count": 0,
            "violations": []
          },
          "chromosome": [
            10,
            16,
            14,
            12,
            14,
            16,
            14,
            11
          ],
          "segment_metadata": [
            {
              "difficulty_tier": 1,
              "family": "reward_relief",
              "segment_id": 10,
              "variant": "double_shelf_coin"
            },
            {
              "difficulty_tier": 1,
              "family": "reward_relief",
              "segment_id": 16,
              "variant": "question_arc"
            },
            {
              "difficulty_tier": 3,
              "family": "pipe_pressure",
              "segment_id": 14,
              "variant": "double_pipe_bridge"
            },
            {
              "difficulty_tier": 3,
              "family": "gap_jump",
              "segment_id": 12,
              "variant": "ceiling_gap_reward"
            },
            {
              "difficulty_tier": 3,
              "family": "pipe_pressure",
              "segment_id": 14,
              "variant": "double_pipe_bridge"
            },
            {
              "difficulty_tier": 1,
              "family": "reward_relief",
              "segment_id": 16,
              "variant": "question_arc"
            },
            {
              "difficulty_tier": 3,
              "family": "pipe_pressure",
              "segment_id": 14,
              "variant": "double_pipe_bridge"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            }
          ]
        },
        {
          "rank": 3,
          "png_path": "assets/family_4obj_seed27/frontier_levels/frontier_03.png",
          "ascii_path": "assets/family_4obj_seed27/frontier_levels/frontier_03.txt",
          "ascii_text": "................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n....................?.......................................................?...................................\n......o....................................................................................o....................\n....BBBBBB........BBBBBB.........?..?...........oo........................BBBBBB......BBBBBBBBBB.......?..?.....\n.............................................BBBBBBBB.........?.........................PP...PP.................\n................PP...........BBBBBBBBBBBB...............................PP..............PP...PP....BBBBBBBBBBBB.\n..BBBBBBBBBB....PPBBBBBBBB..............................................PPBBBBBBBB......PP...PP.................\n................PP........................BBBBBB..BBBBBB................PP..............PP...PP.................\n.S..............PP....E..E.....E......E....................E.....E......PP....E..E......PP...PP......E......E.G.\n################################################################################################################\n################################################################################################################\n",
          "evaluation": {
            "difficulty_curve_error": 0.75,
            "difficulty_error": 0.42500000000000004,
            "difficulty_score": 0.125,
            "emptiness": 0.7873883928571429,
            "emptiness_error": 0.3373883928571429,
            "family_balance": 0.5225,
            "structural_diversity": 0.625
          },
          "constraints": {
            "enemy_rules_ok": true,
            "goal_ok": true,
            "illegal_overlap": false,
            "is_feasible": true,
            "max_gap_ok": true,
            "pipe_rules_ok": true,
            "placement_rules_ok": true,
            "reachable": true,
            "start_ok": true,
            "violation_count": 0,
            "violations": []
          },
          "chromosome": [
            10,
            17,
            11,
            12,
            9,
            17,
            14,
            11
          ],
          "segment_metadata": [
            {
              "difficulty_tier": 1,
              "family": "reward_relief",
              "segment_id": 10,
              "variant": "double_shelf_coin"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            },
            {
              "difficulty_tier": 3,
              "family": "gap_jump",
              "segment_id": 12,
              "variant": "ceiling_gap_reward"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 9,
              "variant": "dual_enemy_reward"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            },
            {
              "difficulty_tier": 3,
              "family": "pipe_pressure",
              "segment_id": 14,
              "variant": "double_pipe_bridge"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            }
          ]
        },
        {
          "rank": 4,
          "png_path": "assets/family_4obj_seed27/frontier_levels/frontier_04.png",
          "ascii_path": "assets/family_4obj_seed27/frontier_levels/frontier_04.txt",
          "ascii_text": "................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n..................................?.........................................?...................................\n...........................................................................................o....................\n................................BBBBBB.......................?..?.........BBBBBB......BBBBBBBBBB.......?..?.....\n........................................................................................PP...PP.................\n....................PP........PP.........................BBBBBBBBBBBB...PP..............PP...PP....BBBBBBBBBBBB.\n....................PP........PPBBBBBBBB................................PPBBBBBBBB......PP...PP.................\n....................PP........PP........................................PP..............PP...PP.................\n.S..................PP........PP....E..E...................E......E.....PP....E..E......PP...PP......E......E.G.\n################################################################################################################\n################################################################################################################\n",
          "evaluation": {
            "difficulty_curve_error": 0.5892857142857143,
            "difficulty_error": 0.45000000000000007,
            "difficulty_score": 0.09999999999999999,
            "emptiness": 0.8063616071428571,
            "emptiness_error": 0.3563616071428571,
            "family_balance": 1.0,
            "structural_diversity": 0.625
          },
          "constraints": {
            "enemy_rules_ok": true,
            "goal_ok": true,
            "illegal_overlap": false,
            "is_feasible": true,
            "max_gap_ok": true,
            "pipe_rules_ok": true,
            "placement_rules_ok": true,
            "reachable": true,
            "start_ok": true,
            "violation_count": 0,
            "violations": []
          },
          "chromosome": [
            0,
            7,
            17,
            0,
            11,
            17,
            14,
            11
          ],
          "segment_metadata": [
            {
              "difficulty_tier": 1,
              "family": "flat_safe",
              "segment_id": 0,
              "variant": "plain_run"
            },
            {
              "difficulty_tier": 2,
              "family": "pipe_pressure",
              "segment_id": 7,
              "variant": "center_pipe"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            },
            {
              "difficulty_tier": 1,
              "family": "flat_safe",
              "segment_id": 0,
              "variant": "plain_run"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            },
            {
              "difficulty_tier": 3,
              "family": "pipe_pressure",
              "segment_id": 14,
              "variant": "double_pipe_bridge"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            }
          ]
        },
        {
          "rank": 5,
          "png_path": "assets/family_4obj_seed27/frontier_levels/frontier_05.png",
          "ascii_path": "assets/family_4obj_seed27/frontier_levels/frontier_05.txt",
          "ascii_text": "................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n..........................................................................o.o.o.................................\n...............................................................o.........????????..........o....................\n.....?..?........................?..?...........oo........BBBBBBBBBB..................BBBBBBBBBB.......?..?.....\n.............................................BBBBBBBB.......PP...PP.....................PP...PP.................\n.BBBBBBBBBBBB................BBBBBBBBBBBB...................PP...PP....BBBBBBBBBBBB.....PP...PP....BBBBBBBBBBBB.\n............................................................PP...PP.....................PP...PP.................\n..........................................BBBBBB..BBBBBB....PP...PP.....................PP...PP.................\n.S.E......E....................E......E.....................PP...PP.....................PP...PP......E......E.G.\n################################################################################################################\n################################################################################################################\n",
          "evaluation": {
            "difficulty_curve_error": 1.1071428571428572,
            "difficulty_error": 0.47500000000000003,
            "difficulty_score": 0.075,
            "emptiness": 0.7873883928571429,
            "emptiness_error": 0.3373883928571429,
            "family_balance": 0.75,
            "structural_diversity": 0.625
          },
          "constraints": {
            "enemy_rules_ok": true,
            "goal_ok": true,
            "illegal_overlap": false,
            "is_feasible": true,
            "max_gap_ok": true,
            "pipe_rules_ok": true,
            "placement_rules_ok": true,
            "reachable": true,
            "start_ok": true,
            "violation_count": 0,
            "violations": []
          },
          "chromosome": [
            11,
            8,
            11,
            12,
            14,
            16,
            14,
            11
          ],
          "segment_metadata": [
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            },
            {
              "difficulty_tier": 3,
              "family": "gap_jump",
              "segment_id": 8,
              "variant": "full_gap_lane"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            },
            {
              "difficulty_tier": 3,
              "family": "gap_jump",
              "segment_id": 12,
              "variant": "ceiling_gap_reward"
            },
            {
              "difficulty_tier": 3,
              "family": "pipe_pressure",
              "segment_id": 14,
              "variant": "double_pipe_bridge"
            },
            {
              "difficulty_tier": 1,
              "family": "reward_relief",
              "segment_id": 16,
              "variant": "question_arc"
            },
            {
              "difficulty_tier": 3,
              "family": "pipe_pressure",
              "segment_id": 14,
              "variant": "double_pipe_bridge"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            }
          ]
        }
      ],
      "final_front_hv": 0.38393159179687497,
      "final_front_spread": 0.17027191811849066,
      "final_front_size": 30
    },
    {
      "id": "curve_4obj_seed27",
      "title": "curve showcase",
      "algorithm": "nsga2",
      "objective_mode": "curve_4obj",
      "config": {
        "population_size": 30,
        "mutation_rate": 0.2,
        "generations": 12,
        "seed": 27,
        "num_segments": 8,
        "segment_width": 14,
        "target_difficulty": 0.55,
        "target_emptiness": 0.45
      },
      "evaluation": {
        "difficulty_score": 0.049999999999999996,
        "difficulty_error": 0.5,
        "structural_diversity": 0.625,
        "emptiness_error": 0.3396205357142857,
        "emptiness": 0.7896205357142857,
        "difficulty_curve_error": 0.3928571428571429,
        "family_balance": 0.45
      },
      "constraints": {
        "is_feasible": true,
        "start_ok": true,
        "goal_ok": true,
        "reachable": true,
        "illegal_overlap": false,
        "max_gap_ok": true,
        "enemy_rules_ok": true,
        "pipe_rules_ok": true,
        "placement_rules_ok": true,
        "violation_count": 0,
        "violations": []
      },
      "best_level": {
        "png_path": "assets/curve_4obj_seed27/best_level.png",
        "ascii_path": "assets/curve_4obj_seed27/best_level.txt",
        "ascii_text": "................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n..................o.o.o.......................o.o.o...........?.................................................\n......o..........????????....................????????......................................o....................\n....BBBBBB..................................................BBBBBB....................BBBBBBBBBB.......?..?.....\n........................................................................................PP...PP.................\n...............BBBBBBBBBBBB.......PP.......BBBBBBBBBBBB...PP................PP..........PP...PP....BBBBBBBBBBBB.\n..BBBBBBBBBB......................PP......................PPBBBBBBBB........PP..........PP...PP.................\n..................................PP......................PP................PP..........PP...PP.................\n.S................................PP......................PP....E..E........PP..........PP...PP......E......E.G.\n################################################################################################################\n################################################################################################################\n",
        "chromosome": [
          10,
          16,
          7,
          16,
          17,
          7,
          14,
          11
        ],
        "segment_metadata": [
          {
            "segment_id": 10,
            "family": "reward_relief",
            "variant": "double_shelf_coin",
            "difficulty_tier": 1
          },
          {
            "segment_id": 16,
            "family": "reward_relief",
            "variant": "question_arc",
            "difficulty_tier": 1
          },
          {
            "segment_id": 7,
            "family": "pipe_pressure",
            "variant": "center_pipe",
            "difficulty_tier": 2
          },
          {
            "segment_id": 16,
            "family": "reward_relief",
            "variant": "question_arc",
            "difficulty_tier": 1
          },
          {
            "segment_id": 17,
            "family": "mixed_challenge",
            "variant": "pipe_enemy_stack",
            "difficulty_tier": 3
          },
          {
            "segment_id": 7,
            "family": "pipe_pressure",
            "variant": "center_pipe",
            "difficulty_tier": 2
          },
          {
            "segment_id": 14,
            "family": "pipe_pressure",
            "variant": "double_pipe_bridge",
            "difficulty_tier": 3
          },
          {
            "segment_id": 11,
            "family": "enemy_pressure",
            "variant": "double_enemy_bridges",
            "difficulty_tier": 3
          }
        ]
      },
      "logs": [
        {
          "generation": 0,
          "feasible_ratio": 0.06666666666666667,
          "first_front_size": 1,
          "first_front_hv": 0.06375239158163266,
          "first_front_spread": 0.0,
          "best_difficulty_error": 0.525,
          "best_structural_diversity": 0.5,
          "best_emptiness_error": 0.3915178571428571,
          "best_emptiness": 0.8415178571428571,
          "best_difficulty_curve_error": 0.8035714285714286,
          "best_family_balance": 0.55
        },
        {
          "generation": 1,
          "feasible_ratio": 0.16666666666666666,
          "first_front_size": 3,
          "first_front_hv": 0.07401137994260208,
          "first_front_spread": 0.14073297112869682,
          "best_difficulty_error": 0.5,
          "best_structural_diversity": 0.5625,
          "best_emptiness_error": 0.3714285714285714,
          "best_emptiness": 0.8214285714285714,
          "best_difficulty_curve_error": 0.4464285714285715,
          "best_family_balance": 0.5225
        },
        {
          "generation": 2,
          "feasible_ratio": 0.4,
          "first_front_size": 1,
          "first_front_hv": 0.17845882493622453,
          "first_front_spread": 0.0,
          "best_difficulty_error": 0.5,
          "best_structural_diversity": 0.625,
          "best_emptiness_error": 0.3552455357142857,
          "best_emptiness": 0.8052455357142857,
          "best_difficulty_curve_error": 0.4464285714285714,
          "best_family_balance": 0.4675
        },
        {
          "generation": 3,
          "feasible_ratio": 1.0,
          "first_front_size": 3,
          "first_front_hv": 0.17923110650510207,
          "first_front_spread": 0.11905546587359607,
          "best_difficulty_error": 0.5,
          "best_structural_diversity": 0.625,
          "best_emptiness_error": 0.3552455357142857,
          "best_emptiness": 0.8052455357142857,
          "best_difficulty_curve_error": 0.4464285714285714,
          "best_family_balance": 0.4675
        },
        {
          "generation": 4,
          "feasible_ratio": 1.0,
          "first_front_size": 7,
          "first_front_hv": 0.18244579081632656,
          "first_front_spread": 0.07260104486325455,
          "best_difficulty_error": 0.47500000000000003,
          "best_structural_diversity": 0.5625,
          "best_emptiness_error": 0.3669642857142857,
          "best_emptiness": 0.8169642857142857,
          "best_difficulty_curve_error": 0.4642857142857143,
          "best_family_balance": 0.7
        },
        {
          "generation": 5,
          "feasible_ratio": 1.0,
          "first_front_size": 13,
          "first_front_hv": 0.18485979352678575,
          "first_front_spread": 0.07508785988241497,
          "best_difficulty_error": 0.47500000000000003,
          "best_structural_diversity": 0.5625,
          "best_emptiness_error": 0.3669642857142857,
          "best_emptiness": 0.8169642857142857,
          "best_difficulty_curve_error": 0.4642857142857143,
          "best_family_balance": 0.7
        },
        {
          "generation": 6,
          "feasible_ratio": 1.0,
          "first_front_size": 5,
          "first_front_hv": 0.18634207589285717,
          "first_front_spread": 0.038623513940106886,
          "best_difficulty_error": 0.47500000000000003,
          "best_structural_diversity": 0.5625,
          "best_emptiness_error": 0.3669642857142857,
          "best_emptiness": 0.8169642857142857,
          "best_difficulty_curve_error": 0.4642857142857143,
          "best_family_balance": 0.7
        },
        {
          "generation": 7,
          "feasible_ratio": 1.0,
          "first_front_size": 8,
          "first_front_hv": 0.0703127491230867,
          "first_front_spread": 0.09466036476143333,
          "best_difficulty_error": 0.45000000000000007,
          "best_structural_diversity": 0.5,
          "best_emptiness_error": 0.3658482142857143,
          "best_emptiness": 0.8158482142857143,
          "best_difficulty_curve_error": 0.8214285714285715,
          "best_family_balance": 0.6649999999999999
        },
        {
          "generation": 8,
          "feasible_ratio": 1.0,
          "first_front_size": 15,
          "first_front_hv": 0.09298075773278058,
          "first_front_spread": 0.09598032061207126,
          "best_difficulty_error": 0.42500000000000004,
          "best_structural_diversity": 0.625,
          "best_emptiness_error": 0.3357142857142857,
          "best_emptiness": 0.7857142857142857,
          "best_difficulty_curve_error": 0.7857142857142857,
          "best_family_balance": 0.75
        },
        {
          "generation": 9,
          "feasible_ratio": 1.0,
          "first_front_size": 27,
          "first_front_hv": 0.17702726403061222,
          "first_front_spread": 0.09152509782163218,
          "best_difficulty_error": 0.42500000000000004,
          "best_structural_diversity": 0.625,
          "best_emptiness_error": 0.3357142857142857,
          "best_emptiness": 0.7857142857142857,
          "best_difficulty_curve_error": 0.7857142857142857,
          "best_family_balance": 0.75
        },
        {
          "generation": 10,
          "feasible_ratio": 1.0,
          "first_front_size": 30,
          "first_front_hv": 0.17634964923469387,
          "first_front_spread": 0.08051770601522217,
          "best_difficulty_error": 0.42500000000000004,
          "best_structural_diversity": 0.625,
          "best_emptiness_error": 0.3357142857142857,
          "best_emptiness": 0.7857142857142857,
          "best_difficulty_curve_error": 0.7857142857142857,
          "best_family_balance": 0.75
        },
        {
          "generation": 11,
          "feasible_ratio": 1.0,
          "first_front_size": 30,
          "first_front_hv": 0.2509956951530612,
          "first_front_spread": 0.09215064364765503,
          "best_difficulty_error": 0.42500000000000004,
          "best_structural_diversity": 0.625,
          "best_emptiness_error": 0.3357142857142857,
          "best_emptiness": 0.7857142857142857,
          "best_difficulty_curve_error": 0.7857142857142857,
          "best_family_balance": 0.75
        }
      ],
      "frontier": [
        {
          "rank": 1,
          "png_path": "assets/curve_4obj_seed27/frontier_levels/frontier_01.png",
          "ascii_path": "assets/curve_4obj_seed27/frontier_levels/frontier_01.txt",
          "ascii_text": "................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n..................o.o.o.......................o.o.o...........?.................................................\n......o..........????????....................????????......................................o....................\n....BBBBBB..................................................BBBBBB....................BBBBBBBBBB.......?..?.....\n........................................................................................PP...PP.................\n...............BBBBBBBBBBBB.......PP.......BBBBBBBBBBBB...PP................PP..........PP...PP....BBBBBBBBBBBB.\n..BBBBBBBBBB......................PP......................PPBBBBBBBB........PP..........PP...PP.................\n..................................PP......................PP................PP..........PP...PP.................\n.S................................PP......................PP....E..E........PP..........PP...PP......E......E.G.\n################################################################################################################\n################################################################################################################\n",
          "evaluation": {
            "difficulty_curve_error": 0.3928571428571429,
            "difficulty_error": 0.5,
            "difficulty_score": 0.049999999999999996,
            "emptiness": 0.7896205357142857,
            "emptiness_error": 0.3396205357142857,
            "family_balance": 0.45,
            "structural_diversity": 0.625
          },
          "constraints": {
            "enemy_rules_ok": true,
            "goal_ok": true,
            "illegal_overlap": false,
            "is_feasible": true,
            "max_gap_ok": true,
            "pipe_rules_ok": true,
            "placement_rules_ok": true,
            "reachable": true,
            "start_ok": true,
            "violation_count": 0,
            "violations": []
          },
          "chromosome": [
            10,
            16,
            7,
            16,
            17,
            7,
            14,
            11
          ],
          "segment_metadata": [
            {
              "difficulty_tier": 1,
              "family": "reward_relief",
              "segment_id": 10,
              "variant": "double_shelf_coin"
            },
            {
              "difficulty_tier": 1,
              "family": "reward_relief",
              "segment_id": 16,
              "variant": "question_arc"
            },
            {
              "difficulty_tier": 2,
              "family": "pipe_pressure",
              "segment_id": 7,
              "variant": "center_pipe"
            },
            {
              "difficulty_tier": 1,
              "family": "reward_relief",
              "segment_id": 16,
              "variant": "question_arc"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            },
            {
              "difficulty_tier": 2,
              "family": "pipe_pressure",
              "segment_id": 7,
              "variant": "center_pipe"
            },
            {
              "difficulty_tier": 3,
              "family": "pipe_pressure",
              "segment_id": 14,
              "variant": "double_pipe_bridge"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            }
          ]
        },
        {
          "rank": 2,
          "png_path": "assets/curve_4obj_seed27/frontier_levels/frontier_02.png",
          "ascii_path": "assets/curve_4obj_seed27/frontier_levels/frontier_02.txt",
          "ascii_text": "................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n......?.......................................o.o.o...........?.................................................\n.............................................????????......................................o....................\n....BBBBBB.......................?..?.......................BBBBBB.........?..?.......BBBBBBBBBB.......?..?.....\n........................................................................................PP...PP.................\n..PP..............######.....BBBBBBBBBBBB..BBBBBBBBBBBB...PP...........BBBBBBBBBBBB.....PP...PP....BBBBBBBBBBBB.\n..PPBBBBBBBB..............................................PPBBBBBBBB....................PP...PP.................\n..PP......................................................PP............................PP...PP.................\n.SPP....E..E...................E......E...................PP....E..E.....E......E.......PP...PP......E......E.G.\n################################################################################################################\n################################################################################################################\n",
          "evaluation": {
            "difficulty_curve_error": 0.7857142857142857,
            "difficulty_error": 0.42500000000000004,
            "difficulty_score": 0.125,
            "emptiness": 0.7857142857142857,
            "emptiness_error": 0.3357142857142857,
            "family_balance": 0.75,
            "structural_diversity": 0.625
          },
          "constraints": {
            "enemy_rules_ok": true,
            "goal_ok": true,
            "illegal_overlap": false,
            "is_feasible": true,
            "max_gap_ok": true,
            "pipe_rules_ok": true,
            "placement_rules_ok": true,
            "reachable": true,
            "start_ok": true,
            "violation_count": 0,
            "violations": []
          },
          "chromosome": [
            17,
            5,
            11,
            16,
            17,
            11,
            14,
            11
          ],
          "segment_metadata": [
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            },
            {
              "difficulty_tier": 1,
              "family": "reward_relief",
              "segment_id": 5,
              "variant": "mid_platform"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            },
            {
              "difficulty_tier": 1,
              "family": "reward_relief",
              "segment_id": 16,
              "variant": "question_arc"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            },
            {
              "difficulty_tier": 3,
              "family": "pipe_pressure",
              "segment_id": 14,
              "variant": "double_pipe_bridge"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            }
          ]
        },
        {
          "rank": 3,
          "png_path": "assets/curve_4obj_seed27/frontier_levels/frontier_03.png",
          "ascii_path": "assets/curve_4obj_seed27/frontier_levels/frontier_03.txt",
          "ascii_text": "................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n..................o.o.o.......................................?.................................................\n......o..........????????..................................................................o....................\n....BBBBBB..................................................BBBBBB....................BBBBBBBBBB.......?..?.....\n........................................................................................PP...PP.................\n...............BBBBBBBBBBBB.......PP......................PP................PP..........PP...PP....BBBBBBBBBBBB.\n..BBBBBBBBBB......................PP......................PPBBBBBBBB........PP..........PP...PP.................\n..................................PP......................PP................PP..........PP...PP.................\n.S................................PP.............E........PP....E..E........PP..........PP...PP......E......E.G.\n################################################################################################################\n################################################################################################################\n",
          "evaluation": {
            "difficulty_curve_error": 0.3035714285714286,
            "difficulty_error": 0.48750000000000004,
            "difficulty_score": 0.0625,
            "emptiness": 0.8018973214285714,
            "emptiness_error": 0.3518973214285714,
            "family_balance": 0.675,
            "structural_diversity": 0.625
          },
          "constraints": {
            "enemy_rules_ok": true,
            "goal_ok": true,
            "illegal_overlap": false,
            "is_feasible": true,
            "max_gap_ok": true,
            "pipe_rules_ok": true,
            "placement_rules_ok": true,
            "reachable": true,
            "start_ok": true,
            "violation_count": 0,
            "violations": []
          },
          "chromosome": [
            10,
            16,
            7,
            4,
            17,
            7,
            14,
            11
          ],
          "segment_metadata": [
            {
              "difficulty_tier": 1,
              "family": "reward_relief",
              "segment_id": 10,
              "variant": "double_shelf_coin"
            },
            {
              "difficulty_tier": 1,
              "family": "reward_relief",
              "segment_id": 16,
              "variant": "question_arc"
            },
            {
              "difficulty_tier": 2,
              "family": "pipe_pressure",
              "segment_id": 7,
              "variant": "center_pipe"
            },
            {
              "difficulty_tier": 2,
              "family": "enemy_pressure",
              "segment_id": 4,
              "variant": "single_patrol"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            },
            {
              "difficulty_tier": 2,
              "family": "pipe_pressure",
              "segment_id": 7,
              "variant": "center_pipe"
            },
            {
              "difficulty_tier": 3,
              "family": "pipe_pressure",
              "segment_id": 14,
              "variant": "double_pipe_bridge"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            }
          ]
        },
        {
          "rank": 4,
          "png_path": "assets/curve_4obj_seed27/frontier_levels/frontier_04.png",
          "ascii_path": "assets/curve_4obj_seed27/frontier_levels/frontier_04.txt",
          "ascii_text": "................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n..................o.o.o.......................o.o.o...........?.................................................\n......o..........????????....................????????...........................................................\n....BBBBBB..................................................BBBBBB.....................................?..?.....\n..........................................................................................?.....................\n...............BBBBBBBBBBBB.......PP.......BBBBBBBBBBBB...PP................PP.....................BBBBBBBBBBBB.\n..BBBBBBBBBB......................PP......................PPBBBBBBBB........PP..................................\n..................................PP......................PP................PP..................................\n.S................................PP......................PP....E..E........PP.........E.....E.......E......E.G.\n################################################################################################################\n################################################################################################################\n",
          "evaluation": {
            "difficulty_curve_error": 0.3928571428571429,
            "difficulty_error": 0.47500000000000003,
            "difficulty_score": 0.075,
            "emptiness": 0.8052455357142857,
            "emptiness_error": 0.3552455357142857,
            "family_balance": 0.7124999999999999,
            "structural_diversity": 0.625
          },
          "constraints": {
            "enemy_rules_ok": true,
            "goal_ok": true,
            "illegal_overlap": false,
            "is_feasible": true,
            "max_gap_ok": true,
            "pipe_rules_ok": true,
            "placement_rules_ok": true,
            "reachable": true,
            "start_ok": true,
            "violation_count": 0,
            "violations": []
          },
          "chromosome": [
            10,
            16,
            7,
            16,
            17,
            7,
            9,
            11
          ],
          "segment_metadata": [
            {
              "difficulty_tier": 1,
              "family": "reward_relief",
              "segment_id": 10,
              "variant": "double_shelf_coin"
            },
            {
              "difficulty_tier": 1,
              "family": "reward_relief",
              "segment_id": 16,
              "variant": "question_arc"
            },
            {
              "difficulty_tier": 2,
              "family": "pipe_pressure",
              "segment_id": 7,
              "variant": "center_pipe"
            },
            {
              "difficulty_tier": 1,
              "family": "reward_relief",
              "segment_id": 16,
              "variant": "question_arc"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            },
            {
              "difficulty_tier": 2,
              "family": "pipe_pressure",
              "segment_id": 7,
              "variant": "center_pipe"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 9,
              "variant": "dual_enemy_reward"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            }
          ]
        },
        {
          "rank": 5,
          "png_path": "assets/curve_4obj_seed27/frontier_levels/frontier_05.png",
          "ascii_path": "assets/curve_4obj_seed27/frontier_levels/frontier_05.txt",
          "ascii_text": "................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n................................................................................................................\n..................o.o.o...........?...........o.o.o...........?...........o.o.o.................................\n......o..........????????....................????????....................????????..........o....................\n....BBBBBB......................BBBBBB......................BBBBBB....................BBBBBBBBBB.......?..?.....\n........................................................................................PP...PP.................\n...............BBBBBBBBBBBB...PP...........BBBBBBBBBBBB...PP...........BBBBBBBBBBBB.....PP...PP....BBBBBBBBBBBB.\n..BBBBBBBBBB..................PPBBBBBBBB..................PPBBBBBBBB....................PP...PP.................\n..............................PP..........................PP............................PP...PP.................\n.S............................PP....E..E..................PP....E..E....................PP...PP......E......E.G.\n################################################################################################################\n################################################################################################################\n",
          "evaluation": {
            "difficulty_curve_error": 0.6428571428571429,
            "difficulty_error": 0.47500000000000003,
            "difficulty_score": 0.075,
            "emptiness": 0.7717633928571429,
            "emptiness_error": 0.3217633928571429,
            "family_balance": 0.475,
            "structural_diversity": 0.625
          },
          "constraints": {
            "enemy_rules_ok": true,
            "goal_ok": true,
            "illegal_overlap": false,
            "is_feasible": true,
            "max_gap_ok": true,
            "pipe_rules_ok": true,
            "placement_rules_ok": true,
            "reachable": true,
            "start_ok": true,
            "violation_count": 0,
            "violations": []
          },
          "chromosome": [
            10,
            16,
            17,
            16,
            17,
            16,
            14,
            11
          ],
          "segment_metadata": [
            {
              "difficulty_tier": 1,
              "family": "reward_relief",
              "segment_id": 10,
              "variant": "double_shelf_coin"
            },
            {
              "difficulty_tier": 1,
              "family": "reward_relief",
              "segment_id": 16,
              "variant": "question_arc"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            },
            {
              "difficulty_tier": 1,
              "family": "reward_relief",
              "segment_id": 16,
              "variant": "question_arc"
            },
            {
              "difficulty_tier": 3,
              "family": "mixed_challenge",
              "segment_id": 17,
              "variant": "pipe_enemy_stack"
            },
            {
              "difficulty_tier": 1,
              "family": "reward_relief",
              "segment_id": 16,
              "variant": "question_arc"
            },
            {
              "difficulty_tier": 3,
              "family": "pipe_pressure",
              "segment_id": 14,
              "variant": "double_pipe_bridge"
            },
            {
              "difficulty_tier": 3,
              "family": "enemy_pressure",
              "segment_id": 11,
              "variant": "double_enemy_bridges"
            }
          ]
        }
      ],
      "final_front_hv": 0.2509956951530612,
      "final_front_spread": 0.09215064364765503,
      "final_front_size": 30
    }
  ],
  "compare_summary": [
    {
      "title": "core baseline",
      "objective_mode": "core_3obj",
      "difficulty_error": 0.37500000000000006,
      "emptiness_error": 0.3362723214285714,
      "difficulty_curve_error": 1.0,
      "family_balance": 0.5249999999999999,
      "front_hv": 0.2649972098214285,
      "front_spread": 0.029918173624112997,
      "front_size": 7
    },
    {
      "title": "family showcase",
      "objective_mode": "family_4obj",
      "difficulty_error": 0.5,
      "emptiness_error": 0.3368303571428571,
      "difficulty_curve_error": 0.8571428571428572,
      "family_balance": 1.0,
      "front_hv": 0.38393159179687497,
      "front_spread": 0.17027191811849066,
      "front_size": 30
    },
    {
      "title": "curve showcase",
      "objective_mode": "curve_4obj",
      "difficulty_error": 0.5,
      "emptiness_error": 0.3396205357142857,
      "difficulty_curve_error": 0.3928571428571429,
      "family_balance": 0.45,
      "front_hv": 0.2509956951530612,
      "front_spread": 0.09215064364765503,
      "front_size": 30
    }
  ]
};
