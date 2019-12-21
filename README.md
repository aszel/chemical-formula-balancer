# Chemical formula balancer

## Introduction

This script compares the components of a list of reactions. Each reaction consists
of a list of reactants (input) and a list of products (output). These reactants / products
will be combined and compared. The output should be equal to the input. If not the input must be
edited.

## Requirements

See Pipfile:
- python_version = "3.7"

## Usage

    ---  That's how I run it ---
    pipenv run python balance.py
    --- or ---
    python balance.py

## Task

- Read the given xml file
- Extract ListOfSpecies
- Extract ListOfReactions
- For each reaction
  - get reaction_id
  - get listOfReactants
  - get listOfProducts

```xml
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
```
## What is to do?

### First

- this is the species: M_nadph_c
- this is the stoichiometry: 1
- this is the chemicalFormula': C21H26N7O17P3
- first: write function to split chemicalFormula into something like C21 H26 N7 O17 P3 -> {'element', 'coefficient'}

### Second

Now we have...
-  {'c', '21'}, {'h', '26'},{...}
This must be multibplied by the stoichiometry coefficient and we get (in case it is 2)
- {'c', '42'}, {'h', '52'},{...}

But we have 2 reactants
So must combine them. So have something like this:
- reactant 1: {'c', '42'}, {'h', '52'},{...}
- reactant 2: {'c', '42'}, {'h', '52'},{...}

Result would be:
- {'c', '84'}, {'h', '104'},{...}
- hint: for elements just in one but not the other keep them as is -> basically merge

### Third

Do the same stuff with products.
We end up with something like:
- {'c', '84'}, {'h', '104'},{...}

### Fourth

Compare the results. Mark the differences. Done. Happy times.
