import os
import xml.etree.ElementTree as ET
import re

class Balancer:

    #file_name = "Supporting Information File S1_Jcurcas_model.xml"
    file_name = "test-data.xml"
    node_name_list_of_species = "listOfSpecies"
    node_name_list_of_reactions = "listOfReactions"
    node_name_reactants = "listOfReactants"
    node_name_products = "listOfProducts"
    node_name_species_ref = "speciesReference"
    node_name_species = "species"
    reaction_attribute_id = "id"
    species_ref_attribute_id = "species"
    species_ref_attribute_coefficient = "stoichiometry"
    species_attribute_id = "id"
    species_attribute_chemical_formula = "chemicalFormula"

    def get_full_file_name(self):
        full_file_name = os.path.abspath(os.path.join("data", self.file_name))
        return full_file_name

    def get_model_node(self, full_file_name):
        tree = ET.parse(full_file_name)
        root = tree.getroot()
        model = root.find("model")
        return model

    def get_reactions(self, model_node):
        reactions = {}
        list_of_reactions = model_node.find(self.node_name_list_of_reactions)
        for reaction in list_of_reactions:
            reaction_list_tuple = self.get_reaction_content(reaction)
            (reaction_id, list_of_reactants, list_of_products) = reaction_list_tuple
            reactions.update({reaction_id : (list_of_reactants, list_of_products)})
        return reactions

    def get_reaction_content(self, parent_node):
        reaction_attributes = parent_node.attrib
        reaction_id = reaction_attributes.get(self.reaction_attribute_id)
        list_of_reactants = parent_node.findall(self.node_name_reactants)
        list_of_products = parent_node.findall(self.node_name_products)
        return reaction_id, list_of_reactants, list_of_products

    def get_species_references(self, list):
        dict = {}
        for list_element in list:
            list_of_species_refs = list_element.findall(self.node_name_species_ref)
            for species_reference in list_of_species_refs:
                species_reference_attributes = species_reference.attrib
                id = species_reference_attributes.get(self.species_ref_attribute_id)
                coefficient = species_reference_attributes.get(self.species_ref_attribute_coefficient)
                dict.update({id : coefficient})
        return dict

    def get_species(self, model_node):
        species = {}
        list_of_species = model_node.find(self.node_name_list_of_species)
        for s in list_of_species:
            species_attributes = s.attrib
            id = species_attributes.get(self.species_attribute_id)
            chemical_formula = species_attributes.get(self.species_attribute_chemical_formula)
            species.update({id : chemical_formula})

        updated_species = self.create_chemical_formula_model(species)
        return updated_species

    """
    Turn a chemicalFormula string like "C21H26N7O17P3"
    in a dictionary like this: {'C', '21'},{'H', '26'}...
    """
    def create_chemical_formula_model(self, species):
        for id, chemical_formula_string in species.items():
            my_dict = self.build_dictionary_of_string(id, chemical_formula_string)
            species[id] = my_dict
        return species

    def build_dictionary_of_string(self, id, chemical_formula_string):
        chemical_formula_list = (re.findall(r'[A-Za-z]|-?\d+\.\d+|\d+', chemical_formula_string))
        my_dict = {}
        key, value = "", ""
        for element in chemical_formula_list:
            if self.is_integer(element):
                value = element
                my_dict.update({key: value})
                # flush key and value
                key, value = "", ""
            else:
                key = element

            # Catch the last element without a number.
            # If element has no following number then it gets the value 1
            if key and not value:
                my_dict.update({key: 1})

        return my_dict

    def is_integer(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False


b = Balancer()
full_file_name = b.get_full_file_name()

model = b.get_model_node(full_file_name)

species = b.get_species(model)
print(species)

reactions = b.get_reactions(model)
for reaction_id, (list_of_reactants, list_of_products) in reactions.items():
    print("------------")
    print("Reaction  -> ", reaction_id)
    dict_reactants = b.get_species_references(list_of_reactants)
    dict_products = b.get_species_references(list_of_products)
    print("Reactants -> ", dict_reactants)
    print("Products  -> ", dict_products)
