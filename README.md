# Chemnical stuff balancer

## Task

- Read the given xml file
- Extract ListOfSpecies
- Extract ListOfReactions
- For each reaction in ListOfReactions
  - get id attribute -> reaction_id
  - get name attribute -> reaction_attribute
  - get listOfReactants -> list_of_reactants
  - get listOfProducts -> list_of_products  
  - For each reactant in list_of_reactants (called speciesReference)
    - get attribute species (Example: "M_nadph_c")
    -
