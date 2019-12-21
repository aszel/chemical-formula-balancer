# Chemnical stuff balancer

## Task

- Read the given xml file
- Extract ListOfSpecies
- Extract ListOfReactions
- For each reaction
  - get reaction_id
  - get listOfReactants
  - get listOfProducts

    example reaction
    <reaction fast="false" lowerFluxBound="cobra_0_bound" upperFluxBound="cobra_default_ub" id="R_AICARTf" metaid="R_AICARTf" name="AICAR transformylase" reversible="false" sboTerm="SBO:0000375">
        <listOfReactants>
            <speciesReference constant="true" sboTerm="SBO:0000010" species="M_aicar_d" stoichiometry="2"/>
            <speciesReference constant="true" sboTerm="SBO:0000010" species="M_mthf_d" stoichiometry="2"/>
        </listOfReactants>
        <listOfProducts>
            <speciesReference constant="true" sboTerm="SBO:0000011" species="M_faicar_d" stoichiometry="1"/>
            <speciesReference constant="true" sboTerm="SBO:0000011" species="M_thf_d" stoichiometry="1"/>
            <speciesReference constant="true" sboTerm="SBO:0000011" species="M_h_d" stoichiometry="2"/>
        </listOfProducts>
    </reaction>


here comes the math stuff:
- this is the species: M_nadph_c
- this is the stoichiometry: 1
- this is the chemicalFormula': C21H26N7O17P3
- first: write function to split chemicalFormula into something like C21 H26 N7 O17 P3 -> {'element', 'coefficient'}

second:
Now we have...
-  {'c', '21'}, {'h', '26'},{...}
This must be multibplied by the stoichiometry coefficient and we get (in case it is 2)
- {'c', '42'}, {'h', '52'},{...}

But we have 2 reactants
# so must combine them
# so have something like this:
#    {'c', '42'}, {'h', '52'},{...} // reactant 1
#    {'c', '42'}, {'h', '52'},{...} // reactant 2

# result would be
# {'c', '84'}, {'h', '104'},{...}
# hint: for elements just in one but not the other keep them as is -> basically merge


# DO the SAME SHIT with products
# we end up with something like:
# {'c', '84'}, {'h', '104'},{...}


# and now compare the results!
# DONE
