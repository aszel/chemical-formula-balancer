import balance

class Main:

    def main():
        file_name = "test-data.xml"
        #file_name = "Supporting Information File S1_Jcurcas_model.xml"

        b = balance.Balancer(file_name)
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

            b.print_status(reaction_id, reactants_dict_updated, products_dict_updated,
                combined_reactants_formula, combined_products_formula)

        b.print_summary(reactions, species_without_chemical_formula)

    if __name__ == "__main__":
        main()




# DO NOT DELETE - this is for testing
#b.calculate_chemical_formula(species, "M_aicar_d", 2)
#test_formula_list = [{'C': 2, 'H': 1, 'N': 8}, {'C': 3, 'H': 2, 'X': 8}]
#combined_formulas = b.combine_chemical_formulas(test_formula_list)
#print(combined_formulas)
#some_bad_reactants_dict = {'test_1': '2', 'test_2': '1.1'}
#some_bad_species_dict = {'M_Biomass_c': ''}
#result = b.remove_unusable_elements(some_bad_reactants_dict, some_bad_species_dict)
#print(result)
