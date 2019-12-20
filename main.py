import os
import xml.etree.ElementTree as ET

file_name = "Supporting Information File S1_Jcurcas_model.xml"
full_file_name = os.path.abspath(os.path.join("data", file_name))

string = f"Reading file: {full_file_name}"
print(string)

tree = ET.parse(full_file_name)
root = tree.getroot()
model = root.find("model")

# list of species
# species (ID, chemicalFormula)
list_of_species = model.find("listOfSpecies")
for species in list_of_species:
    #print(species.attrib)
    pass


# list of reactions
# ID, ListOfReactants, ListOfProducts
list_of_reactions = model.find("listOfReactions")
for reaction in list_of_reactions:
    reaction_attributes = reaction.attrib
    reaction_id = reaction_attributes.get("id")

    list_of_reactants = reaction.findall("listOfReactants")
    for reactant in list_of_reactants:
        species_list = reactant.findall("speciesReference")
        for species_reference in species_list:
            print(species_reference)
            species_ref_attr = species_reference.attrib
            species = species_ref_attr.get("species")
            stoichiometry = species_ref_attr.get("stoichiometry")
            print(species)
            print(stoichiometry)




### example reaction
#            <reaction fast="false" lowerFluxBound="cobra_0_bound" upperFluxBound="cobra_default_ub" id="R_AICARTf" metaid="R_AICARTf" name="AICAR transformylase" reversible="false" sboTerm="SBO:0000375">
#                <listOfReactants>
#                    <speciesReference constant="true" sboTerm="SBO:0000010" species="M_aicar_d" stoichiometry="2"/>
#                    <speciesReference constant="true" sboTerm="SBO:0000010" species="M_mthf_d" stoichiometry="2"/>
#                </listOfReactants>
#                <listOfProducts>
#                    <speciesReference constant="true" sboTerm="SBO:0000011" species="M_faicar_d" stoichiometry="1"/>
#                    <speciesReference constant="true" sboTerm="SBO:0000011" species="M_thf_d" stoichiometry="1"/>
#                    <speciesReference constant="true" sboTerm="SBO:0000011" species="M_h_d" stoichiometry="2"/>
#                </listOfProducts>
#            </reaction>


# TODO - implement
# #get chemical formula by species
# getChemFormulaBySpecies(M_nadph_c)
#    return C21H26N7O17P3


# here comes the math stuff
# this is the species: M_nadph_c
# this is the stoichiometry: 1
# this is the chemicalFormula': C21H26N7O17P3
# first: write function to split chemicalFormula into something like C21 H26 N7 O17 P3 -> {'element', 'coefficient'}

# second: we have now
# {'c', '21'}, {'h', '26'},{...}
# this must be multibplied by the stoichiometry coefficient
# and we get (in case it is 2)
# {'c', '42'}, {'h', '52'},{...}


# but we have 2 reactants
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
