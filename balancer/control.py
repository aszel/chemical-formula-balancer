import balance

class Controller:

    bal = ""
    file = ""
    output = []

    def __init__(self):
        file_name = "test-data.xml"
        #file_name = "test-data-2.xml"
        #file_name = "Supporting Information File S1_Jcurcas_model.xml"
        self.bal = balance.Balancer(file_name)

    def start(self):
        species, species_without_chemical_formula = self.bal.get_species()
        reactions = self.bal.get_reactions()

        # print
        headline = "reaction id;differences"
        #output.append(headline)
        for reaction_id, (reactants_dict, products_dict) in reactions.items():

            reactants = self.bal.remove_unusable_elements(reactants_dict, species_without_chemical_formula, species)
            reactants_formula = self.bal.get_combined_chemical_formula(species, reactants)

            products = self.bal.remove_unusable_elements(products_dict, species_without_chemical_formula, species)
            products_formula = self.bal.get_combined_chemical_formula(species, products)

            self.bal.print_status(reaction_id, reactants, products, reactants_formula, products_formula)

        self.bal.print_summary(reactions, species_without_chemical_formula)

    def write_output_file(self):
        reactants_only, products_only, differences, equals = self.bal.compare(reactants_formula, products_formula)

# DO NOT DELETE - this is for testing
#b.calculate_chemical_formula(species, "M_aicar_d", 2)
#test_formula_list = [{'C': 2, 'H': 1, 'N': 8}, {'C': 3, 'H': 2, 'X': 8}]
#combined_formulas = b.combine_chemical_formulas(test_formula_list)
#print(combined_formulas)
#some_bad_reactants_dict = {'test_1': '2', 'test_2': '1.1'}
#some_bad_species_dict = {'M_Biomass_c': ''}
#result = b.remove_unusable_elements(some_bad_reactants_dict, some_bad_species_dict)
#print(result)
