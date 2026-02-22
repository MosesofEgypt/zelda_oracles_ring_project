RING_TEXT_NAMES_INDEX = 0x40
RING_TEXT_DESCS_INDEX = 0x80
RING_TEXT_SNIPS_INDEX = 0xC2
RING_TEXT_GROUP       = 0x30

RING_TEXT_SNIPS = [
    dict(id=id, text=text)
    for id, text in [
        ("GREEN", "Green"),
        ("BLUE", "Blue"),
        ("GOLD", "Gold"),
        ("RED", "Red"),
        ("_CURSE_RING", " Curse Ring"),
        ("EFFECT_UP", "effect {{TXT_UP}}"),
        ("ARMOR_RING", "Armor Ring"),
        ("POWER_RING", "Power Ring"),
        ("ARMOR_RING_L", "{ARMOR_RING} L-"),
        ("POWER_RING_L", "{POWER_RING} L-"),
        ("HEART_RING_L", "Heart Ring L-"),
        ("LIGHT_RING_L", "Light Ring L-"),
        ("RANG_RING_L", "Rang Ring L-"),
        ("TINT_RING", " Tint Ring"),
        ("LUCK_RING", " Luck Ring"),
        ("HOLY_RING", " Holy Ring"),
        ("JOY_RING", " Joy Ring"),
        ("LIKE", "Like"),
        ("_MOVEMENT", " movement"),
        ("ATK", "ATK: "),
        ("DEF", "DEF: "),
        ("RANG_RING_DESC", "Boomerang dmg.{{TXT_UP}}"),
        ("LUCK_RING_DESC", (" dmg. -50%{{TXT_NEWL}}"
                            "dodge chance {{LUCK_RING_VAL}}%")),
        ("HOLY_RING_DESC", (" immune{{TXT_NEWL}}"
                            "{DEF}{{HOLY_RING_VAL}}%")),
        ("JOY_RING_DESC", "Find x2"),
        ("S_RING", "'s Ring"),
        ("GASHA", "Gasha"),
        ("CAN_STACK", "{{TXT_NEWL}}Can stack"),
        ("FREE_HAND_PUNCH", "Free hand punch"),
        ("BECOME_", "Become "),
        ("LIGHT_RING_DESC", "Fire beam at {{TXT_HEART}}-"),
        ("SECRET_EFFECTS", "{{TXT_NEWL}}[secret combos]"),
        ("HEART_RECOVERY", "{{TXT_HEART}} recovery {{TXT_UP}}{{TXT_UP}}"),
        ]
    ]
RING_TEXT_STRINGS = [
    dict(name=name, desc=desc)
    for name, desc in [
        # NOTE: names cannot go over 15 characters, or they won't render
        #       properly in the appraisal textbox Vasu says their name in
        ("Vasu{S_RING}", ("Press {{TXT_COLOR}}\x01Ring Box{{TXT_COLOR}}\x00{{TXT_NEWL}}"
                          "to swap rings")),
        ("{POWER_RING_L}1",
         ("{ATK}{{TXT_UP}}{{TXT_NEWL}}"
          "{DEF}{{TXT_DOWN}}")),
        ("{POWER_RING_L}2",
         ("{ATK}{{TXT_UP}}{{TXT_UP}}{{TXT_NEWL}}"
          "{DEF}{{TXT_DOWN}}")),
        ("{POWER_RING_L}3",
         ("{ATK}{{TXT_UP}}{{TXT_UP}}{{TXT_UP}}{{TXT_NEWL}}"
          "{DEF}{{TXT_DOWN}}")),
        ("{ARMOR_RING_L}1",
         ("{DEF}{{TXT_UP}}{{TXT_NEWL}}"
          "{ATK}{{TXT_DOWN}}")),
        ("{ARMOR_RING_L}2",
         ("{DEF}{{TXT_UP}}{{TXT_UP}}{{TXT_NEWL}}"
          "{ATK}{{TXT_DOWN}}")),
        ("{ARMOR_RING_L}3",
         ("{DEF}{{TXT_UP}}{{TXT_UP}}{{TXT_UP}}{{TXT_NEWL}}"
          "{ATK}{{TXT_DOWN}}")),
        ("{RED} Ring",  "{ATK}{{RED_RING_VAL}}%"),
        ("{BLUE} Ring", "{DEF}{{BLUE_RING_VAL}}%"),
        ("{GREEN} Ring", ("{ATK}{{GREEN_RING_VAL1}}%{{TXT_NEWL}}"
                          "{DEF}{{GREEN_RING_VAL2}}%")),
        ("{RED}{_CURSE_RING}", ("{ATK}{{CURSE_RING_VAL1}}%{{TXT_NEWL}}"
                                "{{TXT_HEART}} cap of {{CURSE_RING_VAL2}}")),
        ("Expert{S_RING}", ("{FREE_HAND_PUNCH}"
                            "{SECRET_EFFECTS}")),
        ("Blast Ring", ("Blast size/dmg.{{TXT_UP}}"
                        "{SECRET_EFFECTS}")),
        ("{RANG_RING_L}1", ("{RANG_RING_DESC}"
                            "{SECRET_EFFECTS}")),
        ("GBA Time Ring", ("Invin. time +60%"
                           "{CAN_STACK}")),
        ("Maple{S_RING}", "Maple meetings {{TXT_UP}}"),
        ("Steadfast Ring", ("Knockback {{TXT_DOWN}}"
                            "{SECRET_EFFECTS}")),
        ("Mystic Ring", ("Mystic seed{{TXT_NEWL}}"
                         "{EFFECT_UP}{{TXT_UP}}")),
        ("Toss Ring", ("Throw dist. {{TXT_UP}}"
                       "{SECRET_EFFECTS}")),
        ("{HEART_RING_L}1", ("{HEART_RECOVERY}"
                             "{CAN_STACK}")),
        ("{HEART_RING_L}2", ("{HEART_RECOVERY}{{TXT_UP}}"
                             "{CAN_STACK}")),
        ("Swimmer{S_RING}", ("Swim speed {{TXT_UP}}"
                             "{SECRET_EFFECTS}")),
        ("Charge Ring", ("Charge time -75%"
                         "{SECRET_EFFECTS}")),
        ("{LIGHT_RING_L}1", ("{LIGHT_RING_DESC}{{LIGHT_RING_L1_VAL}}"
                             "{SECRET_EFFECTS}")),
        ("{LIGHT_RING_L}2", ("{LIGHT_RING_DESC}{{LIGHT_RING_L2_VAL}}"
                             "{SECRET_EFFECTS}")),
        ("Bomber{S_RING}", ("Can set 4 {{TXT_COLOR}}\x01Bombs{{TXT_COLOR}}\x00"
                            "{SECRET_EFFECTS}")),
        ("{GREEN}{LUCK_RING}", "Trap{LUCK_RING_DESC}"),
        ("{BLUE}{LUCK_RING}", "Fall{LUCK_RING_DESC}"),
        ("Alchemy Ring", ("Turn Rupees into{{TXT_NEWL}}"
                          "{{TXT_COLOR}}\x01Bombs{{TXT_COLOR}}\x00 and Seeds")),
        ("{RED}{LUCK_RING}",   "Spike{LUCK_RING_DESC}"),
        ("{GREEN}{HOLY_RING}", "Elec. zap{HOLY_RING_DESC}"),
        ("{BLUE}{HOLY_RING}",  "Zora fire{HOLY_RING_DESC}"),
        ("{RED}{HOLY_RING}",   "Wisp jinx{HOLY_RING_DESC}"),
        ("Haste Ring", ("Faster{_MOVEMENT}"
                        "{SECRET_EFFECTS}")),
        ("Roc{S_RING}", ("Feather {EFFECT_UP}"
                         "{SECRET_EFFECTS}")),
        ("Hiker{S_RING}", ("Normal{_MOVEMENT}{{TXT_NEWL}}"
                           "on all surfaces")),
        ("{RED}{JOY_RING}", ("{JOY_RING_DESC} Rupees"
                             "{CAN_STACK}")),
        ("{BLUE}{JOY_RING}", ("{JOY_RING_DESC} Hearts"
                              "{CAN_STACK}")),
        ("{GOLD}{JOY_RING}", ("{JOY_RING_DESC} Items"
                              "{SECRET_EFFECTS}")),
        ("{GREEN}{JOY_RING}", ("{JOY_RING_DESC} Ore"
                               "{SECRET_EFFECTS}")),
        ("Discovery Ring", ("Item discovery {{TXT_UP}}"
                            "{SECRET_EFFECTS}")),
        ("{RANG_RING_L}2", ("{RANG_RING_DESC}{{TXT_UP}}"
                            "{SECRET_EFFECTS}")),
        ("Octo Ring", ("Become an{{TXT_NEWL}}"
                       "Octorok")),
        ("Moblin Ring", ("Become a{{TXT_NEWL}}"
                         "Moblin")),
        ("{LIKE} {LIKE} Ring", ("Become a{{TXT_NEWL}}"
                                "{LIKE} {LIKE}")),
        ("Subrosian Ring", ("Become a{{TXT_NEWL}}"
                           "Subrosian")),
        ("First Gen Ring", ("{BECOME_}{{TXT_NEWL}}"
                            "something")),
        ("Spin Ring", ("Dbl. Spin Attack"
                       "{SECRET_EFFECTS}")),
        ("Bombproof Ring", ("Own Bomb is safe"
                            "{SECRET_EFFECTS}")),
        ("Energy Ring", ("Chrg. fires beam"
                         "{SECRET_EFFECTS}")),
        ("{BLUE}{_CURSE_RING}", ("Dmg. taken/dealt{{TXT_NEWL}}"
                                 "reduced to {{TXT_HEART}}/4")),
        ("GBA Nature Ring", ("Invin. time +60%"
                             "{CAN_STACK}")),
        ("{RED}{TINT_RING}", ("1K beasts slain{{TXT_NEWL}}"
                               "{BECOME_}{RED}")),
        ("{GREEN}{TINT_RING}", ("10K Rupees found{{TXT_NEWL}}"
                                 "{BECOME_}{GREEN}")),
        ("Victory Ring", ("Sword & Shield{{TXT_NEWL}}"
                          "level {{TXT_UP}}")),
        ("{GOLD}{TINT_RING}", ("100 signs broken{{TXT_NEWL}}"
                               "{BECOME_}{GOLD}")),
        ("{BLUE}{TINT_RING}", ("100 rings found{{TXT_NEWL}}"
                                "{BECOME_}{BLUE}")),
        ("GBC {TINT_RING}",  ("This is now a{{TXT_NEWL}}"
                              "Game Boy Color!")),
        ("{GASHA} Ring", ("Grow {GASHA}{{TXT_NEWL}}"
                          "trees quickly")),
        ("Peace Ring", ("Defuse held Bomb"
                        "{SECRET_EFFECTS}")),
        ("Zora{S_RING}", ("Dive for ever"
                          "{SECRET_EFFECTS}")),
        ("Fist Ring", "{FREE_HAND_PUNCH}"
                      "{SECRET_EFFECTS}"),
        ("{GOLD} Ring", ("{ATK}{{GOLD_RING_VAL1}}%  {{TXT_TIMES}}2 if{{TXT_NEWL}}"
                         "{DEF}{{GOLD_RING_VAL2}}%  {{TXT_HEART}} < {{GOLD_RING_VAL3}}")),
        ("Fairy{S_RING}", ("Revives you{{TXT_NEWL}}"
                           "but breaks")),
        ]
    ]


# the banks that the patches should apply to
PATCH_BANKS = dict(
    TEXT_SNIPS0     = 63,
    TEXT_SNIPS1     = 63,
    TEXT_SNIPS2     = 63,
    )
AGES_PATCH_BANKS = dict()
SEAS_PATCH_BANKS = dict()

PADDING_REPLACE_MAP  = {
    name: b'\x00\x00' for name in set([
        *PATCH_BANKS, *AGES_PATCH_BANKS, *SEAS_PATCH_BANKS
        ])
    }

globals().update({name: name for name in PADDING_REPLACE_MAP})
