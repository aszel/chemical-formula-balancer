import os
import xml.etree.ElementTree as ET
import re

class Balancer:

    file_name = "Supporting Information File S1_Jcurcas_model.xml"
    #file_name = "test-data.xml"
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
        species_without_chemical_formula = {}
        list_of_species = model_node.find(self.node_name_list_of_species)
        for s in list_of_species:
            species_attributes = s.attrib
            id = species_attributes.get(self.species_attribute_id)
            chemical_formula = species_attributes.get(self.species_attribute_chemical_formula)
            if chemical_formula:
                species.update({id : chemical_formula})
            else:
                species_without_chemical_formula.update({id : chemical_formula})

        updated_species = self.create_chemical_formula_model(species)
        return (updated_species, species_without_chemical_formula)

    def create_chemical_formula_model(self, species):
        for id, chemical_formula_string in species.items():
            my_dict = self.build_dictionary_of_string(id, chemical_formula_string)
            species[id] = my_dict
        return species

    def build_dictionary_of_string(self, id, chemical_formula_string):
        my_dict = {}
        chemical_formula_list = (re.findall(r'[A-Za-z]|-?\d+\.\d+|\d+', chemical_formula_string))
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
                my_dict.update({key: '1'})

        return my_dict

    def is_integer(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def species_exists(self, id, species):
        if id in species:
            return True
        else:
            return False

    def get_combined_chemical_formula(self, species_dict, dict_elements):
        my_formulas_list = []
        for id, coefficient in dict_elements.items():
            calculated_formula = self.calculate_chemical_formula(species_dict, id, coefficient)
            my_formulas_list.append(calculated_formula)
        my_dict = self.combine_chemical_formulas(my_formulas_list)
        return my_dict

    def calculate_chemical_formula(self, species_dict, id, coefficient):
        my_dict = {}
        specie_chem_form = species_dict.get(id)
        for element, amount in specie_chem_form.items():
            updated_amount = int(amount) * int(coefficient)
            my_dict.update({element : updated_amount})
        #print("formula: ", specie_chem_form, " updated formula: ", my_dict)
        return my_dict

    def combine_chemical_formulas(self, formulas_list):
        my_dict = {}
        for formula in formulas_list:
            for key, value in formula.items():
                if not key in my_dict:
                    my_dict.update({key : value})
                else:
                    existing_value = my_dict.get(key)
                    new_value = int(existing_value) + int(value)
                    my_dict.update({key : new_value})
        return my_dict

    def compare(self, d1, d2):
        d1_keys = set(d1.keys())
        d2_keys = set(d2.keys())
        intersect_keys = d1_keys.intersection(d2_keys)
        added = d1_keys - d2_keys
        removed = d2_keys - d1_keys
        modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
        same = set(o for o in intersect_keys if d1[o] == d2[o])
        return added, removed, modified, same

    """
    function takes a list of reactants/products and removes those which yield
    a none-integer value as coefficient or their referrenced species has no
    chemical formula
    """
    def remove_unusable_elements(self, elements_dict, species_without_chemical_formula, species):
        my_dict = {}
        for id, coefficient in elements_dict.items():
            if not id in species_without_chemical_formula and self.is_integer(coefficient) and self.species_exists(id, species):
                my_dict.update({id : coefficient})
        return my_dict


b = Balancer()
full_file_name = b.get_full_file_name()
model = b.get_model_node(full_file_name)
species, species_without_chemical_formula = b.get_species(model)

reactions = b.get_reactions(model)
for reaction_id, (list_of_reactants, list_of_products) in reactions.items():
    dict_reactants = b.get_species_references(list_of_reactants)
    reactants_dict_updated = b.remove_unusable_elements(dict_reactants, species_without_chemical_formula, species)

    products_dict = b.get_species_references(list_of_products)
    products_dict_updated = b.remove_unusable_elements(products_dict, species_without_chemical_formula, species)

    combined_reactants_formula = b.get_combined_chemical_formula(species, reactants_dict_updated)
    combined_products_formula = b.get_combined_chemical_formula(species, products_dict_updated)

    print("------------")
    print("Reaction ID                       -> ", reaction_id)
    print("Reactants [speciesId,coefficient] -> ", reactants_dict_updated)
    print("Products  [speciesId,coefficient] -> ", products_dict_updated)
    print("Reactants chem. formulas combined -> ", combined_reactants_formula)
    print("Products chem. formulas combined  -> ", combined_products_formula)
    added, removed, modified, same = b.compare(combined_reactants_formula, combined_products_formula)
    if len(added) == 0:
        added = ""
    if len(removed) == 0:
        removed = ""
    if len(modified) == 0:
        modified = ""
    if len(same) == 0:
        same = ""
    print("Comparison")
    print("Elemements in Reactants only      -> ", added)
    print("Elemements in Products only       -> ", removed)
    print("Differences                       -> ", modified)
    print("Equal elements                    -> ", same)

print("------------")
print("Summary")
print("Number of reactions: ", len(reactions))
print("Skipped species without chemical formula: ", species_without_chemical_formula)




# DO NOT DELETE - this is for testing
#b.calculate_chemical_formula(species, "M_aicar_d", 2)
#test_formula_list = [{'C': 2, 'H': 1, 'N': 8}, {'C': 3, 'H': 2, 'X': 8}]
#combined_formulas = b.combine_chemical_formulas(test_formula_list)
#print(combined_formulas)
#some_bad_reactants_dict = {'test_1': '2', 'test_2': '1.1'}
#some_bad_species_dict = {'M_Biomass_c': ''}
#result = b.remove_unusable_elements(some_bad_reactants_dict, some_bad_species_dict)
#print(result)
