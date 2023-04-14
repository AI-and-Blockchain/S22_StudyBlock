from nlp import Model

my_model = Model('trialdata.csv')
my_model.train_model()
my_model.add_trial('test trial', 'hello')
my_model.search('Chemotherapy trials for woman older than 30')
