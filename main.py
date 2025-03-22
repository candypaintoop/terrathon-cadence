import pickle

with open('model_pkl', 'rb') as file:
    model = pickle.load(file)


predictions = model.predict([[29.030026760569317,44.05951886973143,6.721410369152325,5.976468928278917,9.5,6.393439995825869,3.4496929600700956,114.19272681347245]])
print(predictions)
