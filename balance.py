import os
import xml.etree.ElementTree as ET

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
        return species

    def create_chemical_formula_model(self, species):
        # TODO - implement
        # each chemicalFormula -> C21H26N7O17P3
        # must be turned into a dictionary {'element', 'coefficient'}
        pass

b = Balancer()
full_file_name = b.get_full_file_name()

model = b.get_model_node(full_file_name)

reactions = b.get_reactions(model)
for reaction_id, (list_of_reactants, list_of_products) in reactions.items():
    dict_reactants = b.get_species_references(list_of_reactants)
    dict_products = b.get_species_references(list_of_products)
    print(dict_reactants)
    print(dict_products)

species = b.get_species(model)
print(species)
