# Chemical formula balancer

## Introduction

This script compares the components of a list of reactions. Each reaction consists
of a list of reactants (input) and a list of products (output). These reactants / products
will be combined and compared. The output should be equal to the input. If not the input must be
edited.

## Next steps

* input file which stays untouched
* output 1: log file = output of program steps
* condensed version of a log file which holds differences only

### Format

* Reaction-ID xyz
* Product Z +1
* Reactant O +1  H +2

## Requirements

See Pipfile:
- python_version = "3.7"

## Usage

    ---  That's how I run it ---
    pipenv run python balance.py
    --- or ---
    python balance.py

## Input example

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
