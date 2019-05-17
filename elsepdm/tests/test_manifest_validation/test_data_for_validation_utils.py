from rest_framework.exceptions import ErrorDetail

error_dict = {
   'product': [
      ErrorDetail(string='This field may not be blank.',
                  code='blank')
   ],
   'config': {
      'components': [
         {
            'structures': [
               {
                  'elements': [
                     ErrorDetail(string='This field is required.',
                                 code='required')
                  ],
                  'name': [
                     ErrorDetail(string='This field is required.',
                                 code='required')
                  ]
               }
            ],
            'name': [
               ErrorDetail(string='This field is required.',
                           code='required')
            ]
         },
         {
            'structures': [
               {
                  'elements': [
                     {
                        'path': [
                           ErrorDetail(string='This field is required.',
                                       code='required')
                        ],
                        'active_color': [
                           ErrorDetail(string='This field is required.',
                                       code='required')
                        ]
                     },
                     {

                     },
                     {

                     }
                  ]
               }
            ]
         },
         {
            'structures': [
               {
                  'name': [
                     ErrorDetail(string='This field is required.',
                                 code='required')
                  ]
               },
               {
                  'elements': [
                     {
                        'path': [
                           ErrorDetail(string='This field is required.',
                                       code='required')
                        ]
                     },
                     {

                     },
                     {
                        'active_color': [
                           ErrorDetail(string='This field is required.',
                                       code='required')
                        ]
                     }
                  ]
               }
            ]
         },
         {

         },
         {

         },
         {
            'structures': [
               ErrorDetail(string='This field is required.',
                           code='required')
            ]
         },
         {

         },
         {

         }
      ],
      'available_configurations': {
         0: {
            '21': [
               ErrorDetail(string='This field may not be blank.',
                           code='blank')
            ]
         }
      }
   }
}

available_configurations_correct = [
            {
                "1": "1",
                "2": "1",
                "3": "0",
            }
        ]

available_configurations_incorrect = [
            {
                "1": "1",
                "2": "5",
                "3": "0",
            }
        ]

components = [
      {
        "name": "upper",
        "component": "1",
        "structures": [
          {
            "name": "upper",
            "structure": "1",
            "elements": [
              {
                "materials": [
                    "metal",
                    "smooth_calfskin",
                ],
                "path": "body",
                "element": "1",
                "active_color": "mat_shoemaster_boxgrain"
              }
            ]
          }
        ]
      },
      {
        "name": "butterfly",
        "component": "2",
        "structures": [
          {
            "name": "butterfly",
            "structure": "1",
            "elements": [
              {
                "materials": [
                    "metal",
                    "smooth_calfskin",
                ],
                "path": "butterfly",
                "element": "1",
                "active_color": "mat_metal_F5B64C"
              }
            ]
          }
        ]
      },
      {
        "name": "star",
        "component": "3",
        "structures": [
          {
            "name": "star",
            "structure": "1",
            "elements": [
              {
                "materials": [
                    "metal",
                    "smooth_calfskin",
                ],
                "path": "star",
                "element": "1",
                "active_color": "mat_metal_F5B64C"
              }
            ]
          }
        ]
      },
    ]

default_configuration_path = "1,1:3,0:2,1"
element_materials_correct = {'smooth_calfskin', 'metal'}

materials_correct = {
            "suede":
            [
                "mat_suede_A6123E",
                "mat_suede_232A3C",
                "mat_suede_CBBB9F",
                "mat_suede_F75D00",
                "mat_suede_302F2E"
            ],
            "drummed_leather":
            [
                "mat_drummed-leather_crismon"
            ],
            "shiny_grained_leather":
            [
                "mat_shiny-grained-calfskin_orange"
            ],
            "nappa_subset":
            [
                "mat_nappa_191A1B",
                "mat_nappa_1B2028",
                "mat_nappa_F6F5F2",
                "mat_nappa_AA0028"
            ],
            "nappa":
            [
                "mat_nappa_191A1B",
                "mat_nappa_1B2028",
                "mat_nappa_F6F5F2",
                "mat_nappa_AA0028",
                "mat_nappa_E62900",
                "mat_nappa_B482AD"
            ],
            "smooth_calfskin":
            [
                "mat_smooth-calfskin_C9C9C9",
                "mat_smooth-calfskin_FFB8F5"
            ],
            "cotton":
            [
                "mat_cotton_DEDCDF",
                "mat_cotton_302F2E",
                "mat_cotton_C40A34",
                "mat_cotton_A5A1A1",
                "mat_cotton_FF7400",
                "mat_cotton_AC7BA8",
                "mat_cotton_354153"
            ],
            "metal":
            [
                "mat_metal_945F17",
                "mat_metal_424242"
            ],
            "logo":
            [
                "mat_transparent-logo_silver",
                "mat_transparent-logo_gold"
            ]
        }

collect_element_materials_correct = ["metal", "smooth_calfskin"]
collect_element_materials_incorrect = ["incorrect", "material"]

collect_component_structures_correct = {
    "1": ["1"],
    "2": ["1"],
    "3": ["1"],
}
