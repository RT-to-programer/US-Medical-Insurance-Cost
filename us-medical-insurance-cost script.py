import csv
from decimal import *
from tkinter import *
from collections import Counter

#Make lists of all 7 colums
ages = []
sexes = []
bmis = []
children = []
smokers = []
regions = []
charges = []

#Patient class

#Reader function
def list_colum_data(lst, colum, csv_file):
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            lst.append(row[colum])
        
    return lst
        
        
#check average function
def check_average(lst):
    getcontext().prec = 6
    lst_average = sum(map(Decimal, lst)) / Decimal(len(lst))
    print(f"The average of {'lst'}: {lst_average}")
    return lst_average

#Put each colum of data into a list (use Reader function)
list_colum_data(ages, 'age', 'insurance.csv')
list_colum_data(sexes, 'sex', 'insurance.csv')
list_colum_data(bmis, 'bmi', 'insurance.csv')
list_colum_data(children, 'children', 'insurance.csv')
list_colum_data(smokers, 'smoker', 'insurance.csv')
list_colum_data(regions, 'region', 'insurance.csv')
list_colum_data(charges, 'charges', 'insurance.csv')

#Patient information class
class Patients:
    
    def __init__(self, ages, sexes, bmis, children, smokers, region, charges):
        self.ages = ages
        self.sexes = sexes
        self.bmis = bmis
        self.children = children
        self.smokers = smokers
        self.regions = regions
        self.charges = charges
        
    def all_patients_dict(self):
        all_patients_dict = {}
        all_patients_dict['ages'] = self.ages
        all_patients_dict['sexes'] = self.sexes
        all_patients_dict['bmis'] = self.bmis
        all_patients_dict['children'] = self.children
        all_patients_dict['smokers'] = self.smokers
        all_patients_dict['regions'] = self.regions
        all_patients_dict['charges'] = self.charges
        return all_patients_dict
    
    def singe_patient_inspector(self, n):
        out = []
        for key in self.all_patients_dict().keys():
            out.append(self.all_patients_dict()[key][n])
        return f'Patient {n+1}, Age: {out[0]}, Sex: {out[1]}, BMI: {out[2]}, Children: {out[3]}, Smoker: {out[4]}, Region: {out[5]}, Charge: {out[6]}'
        
    
    def check_average(self):
        root = Tk()
        root.title("Check average")

        # Add a grid
        mainframe = Frame(root)
        mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
        mainframe.columnconfigure(0, weight = 1)
        mainframe.rowconfigure(0, weight = 1)
        mainframe.pack(pady = 100, padx = 100)

        # Create a Tkinter variable
        tkvar = StringVar(root)

        # Dictionary with options
        choices = { 'Age','BMI','Children', 'Charge'}
        tkvar.set('Age') # set the default option

        popupMenu = OptionMenu(mainframe, tkvar, *choices)
        Label(mainframe, text="Choose a colum").grid(row = 1, column = 1)
        popupMenu.grid(row = 2, column =1)

        # on change dropdown value
        def change_dropdown(*args):
            print(tkvar.get())

        # link function to change dropdown
        tkvar.trace('w', change_dropdown)

        root.mainloop()
        if tkvar.get() == 'Age':
            getcontext().prec = 5
            average = sum(map(Decimal, self.ages)) / Decimal(str(len(self.ages)))
            return average
        elif tkvar.get() == 'BMI':
            getcontext().prec = 5
            average = sum(map(Decimal, self.bmis)) / Decimal(str(len(self.bmis)))
            return average
        elif tkvar.get() == 'Children':
            getcontext().prec = 5
            average = sum(map(Decimal, self.children)) / Decimal(str(len(self.children)))
            return average
        else:
            getcontext().prec = 5
            average = sum(map(Decimal, self.charges)) / Decimal(str(len(self.charges)))
            return average 
        
    def smoker_ratio(self):
        getcontext().prec = 5
        counter_dict = Counter(self.smokers)
        average_smoker = Decimal(str(Counter(self.smokers)['yes']))/Decimal(str(len(self.smokers)))
        average_nonsmoker = Decimal(str(Counter(self.smokers)['no']))/Decimal(str(len(self.smokers)))
        return f"Smoker ratio: {average_smoker}, Non-smoker ratio: {average_nonsmoker}"
    
    def sex_analysis(self):
        counter_dict = Counter(self.sexes)
        male, female = Counter(self.sexes)['male'], Counter(self.sexes)['female']
        
        #Lists required for analysis
        age_sex = list(zip(self.ages, self.sexes))
        sex_smoker = list(zip(self.sexes, self.smokers))
        sex_region = list(zip(self.sexes, self.regions))
        
        #Age and sex analysis
        male_age = []
        female_age = []
        for i in age_sex:
            if i[1] == 'male':
                male_age.append(i[0])
            else:
                female_age.append(i[0])
        male_average_age, female_average_age = (check_average(male_age), check_average(female_age))
        
        #Smoker and sex analysis 
        male_smoker = 0
        female_smoker = 0
        for i in sex_smoker:
            if i[0] == 'male' and i[1] == 'yes':
                male_smoker += 1
            elif i[0] == 'female' and i[1] == 'yes':
                female_smoker += 1
        
        #Regions and sex analysis        
        region_sex_dict = {}
        for i in sex_region:
            if i[1] == 'northeast' and i[1] not in region_sex_dict.keys():
                if i[0] == 'male':
                    region_sex_dict[i[1]] = {'male':1, 'female':0}
                else:
                    region_sex_dict[i[1]] = {'male':0, 'female':1}
                
            elif i[1] == 'northwest' and i[1] not in region_sex_dict.keys():
                region_sex_dict[i[1]] = 1
                if i[0] == 'male':
                    region_sex_dict[i[1]] = {'male':1, 'female':0}
                else:
                    region_sex_dict[i[1]] = {'male':0, 'female':1}
            elif i[1] == 'southeast' and i[1] not in region_sex_dict.keys():
                region_sex_dict[i[1]] = 1
                if i[0] == 'male':
                    region_sex_dict[i[1]] = {'male':1, 'female':0}
                else:
                    region_sex_dict[i[1]] = {'male':0, 'female':1}
            elif i[1] == 'southwest' and i[1] not in region_sex_dict.keys():
                region_sex_dict[i[1]] = 1
                if i[0] == 'male':
                    region_sex_dict[i[1]] = {'male':1, 'female':0}
                else:
                    region_sex_dict[i[1]] = {'male':0, 'female':1}
            else:
                if i[0] == 'male':
                    region_sex_dict[i[1]]['male'] += 1
                else:
                    region_sex_dict[i[1]]['female'] += 1
                    
        out = f"Male: Number {male}, Average age: {male_average_age}, Smokers: {male_smoker} \nFemale: Number {female}, Average age: {female_average_age}, Smokers: {female_smoker}, regions: {region_sex_dict}"
        return out
        
    def charge_analysis(self):
        #Average charge: gender, children, smoker/non-smoker, regions
        l = list(zip(self.charges, self.sexes, self.children, self.smokers, self.regions))
        
        #gender
        male_cost = []
        female_cost = []
        for i in l:
            if i[1] == 'male':
                male_cost.append(i[0])
            else:
                female_cost.append(i[0])
        gender_average_cost = (check_average(male_cost), check_average(female_cost))
        
        #children <2, >2, >5
        less_than_2 = []
        more_than_2 = []
        more_than_5 = []
        for i in l:
            if int(i[2]) <2:
                less_than_2.append(i[0])
            elif 2 <= int(i[2]) < 5:
                more_than_2.append(i[0])
            elif int(i[2]) >= 5:
                more_than_5.append(i[0])
        children_average_cost = (check_average(less_than_2), check_average(more_than_2), check_average(more_than_5))
        
        #smoker/non-smoker
        smoker_charge = []
        non_smoker_charge = []
        for i in l:
            if i[3] == 'yes':
                smoker_charge.append(Decimal(i[0]))
            elif i[3] == 'no':
                non_smoker_charge.append(Decimal(i[0]))
        
        mean_smoker_charge = check_average(smoker_charge)
        mean_non_smoker_charge = check_average(non_smoker_charge)
        
        smoker_variance = (sum(map(lambda x: (x-mean_smoker_charge)**2, smoker_charge)) / len(smoker_charge) - 1)
        non_smoker_variance = (sum(map(lambda x: (x-mean_non_smoker_charge)**2, non_smoker_charge)) / len(non_smoker_charge) - 1)
        smoker_sd = smoker_variance.sqrt()
        non_smoker_sd = non_smoker_variance.sqrt()
        
        #regions
        region_charge_dict = {'northeast': [], 'northwest': [], 'southeast': [], 'southwest': []}

        for i in l:
            if i[4] == 'northeast':
                region_charge_dict['northeast'].append(i[0])
            elif i[4] == 'northwest':    
                region_charge_dict['northwest'].append(i[0])
            elif i[4] == 'southeast':
                region_charge_dict['southeast'].append(i[0])
            else:
                region_charge_dict['southwest'].append(i[0])
                
        means = list(map(check_average, region_charge_dict.values()))
        region_charge_dict['northeast'] = means[0]
        region_charge_dict['northwest'] = means[1]
        region_charge_dict['southeast'] = means[2]
        region_charge_dict['southwest'] = means[3]
        
        return f"Average charge: male {gender_average_cost[0]}/ female {gender_average_cost[1]}, Charge with childrens: <2 {children_average_cost[0]}/ 2 to 5 {children_average_cost[1]}/ >5 {children_average_cost[2]} , 95% of smokers' charges are {mean_smoker_charge - smoker_sd * 3} - {mean_smoker_charge + smoker_sd *3}/ 95% of non-smokers' charge are {mean_non_smoker_charge - non_smoker_sd * 3} - {mean_non_smoker_charge + non_smoker_sd * 3}, {region_charge_dict}"
        
    def __repr__(self):
        n = 0
        out = ''
        while n < 1338:
            out += f"Patient{n}: Age: {self.ages[n]}, Sex: {self.sexes[n]}, BMI: {self.bmis[n]}, Children: {self.children[n]}, Smoker: {self.smokers}, Region: {self.regions}, Charge: {self.charges}, "
            n += 1
        return out