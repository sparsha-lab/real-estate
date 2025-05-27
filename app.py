from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load the pre-trained model and label encoder
with open("house.lr-model.pkl", "rb") as file:
    house_model = pickle.load(file)

with open("lb-housing.pkl", "rb") as file:
    lb_housing = pickle.load(file)

# Prediction function
def predict_house(Square_Feet=143.2, Num_Bedrooms=2, Num_Bathrooms=3, Num_Floors=3,
       Year_Built=1997,Has_Garden=1, Has_Pool=0, Garage_Size=45, Location_Score=8.6,
       Distance_to_Center=5.7):
    lst=[]
    lst=lst+[Square_Feet]
    lst=lst+[Num_Bedrooms]
    lst=lst+[Num_Bathrooms]
    lst=lst+[Num_Floors]
    lst=lst+[Year_Built]
    if Has_Garden==0:
        lst=lst+[0]
    elif Has_Garden==1:
        lst=lst+[1]


    if Has_Pool==0:
        lst=lst+[0]
    elif Has_Pool==1:
        lst=lst+[1]
        
    lst=lst+[Garage_Size]
    lst=lst+[Location_Score]
    lst=lst+[Distance_to_Center]
    result=house_model.predict([lst])
    return result
# Return the first (and only) prediction

# Routes
@app.route("/", methods=["GET"])
def index():
    return render_template("home.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        # 🔧 FIXED: Corrected field name from "Square_feet" → "square_feet"
        Square_Feet = float(request.form.get("square_feet"))
        Num_Bedrooms = int(request.form.get("bedrooms"))
        Num_Bathrooms = int(request.form.get("bathrooms"))
        Num_Floors = int(request.form.get("floors"))
        Year_Built = int(request.form.get("year_built"))

        # Convert garden and pool inputs to binary (1 for Yes, 0 for No)
        garden = request.form.get("garden")
        Has_Garden = 1 if garden == "Yes" else 0

        pool = request.form.get("pool")
        Has_Pool = 1 if pool == "Yes" else 0

        Garage_Size = float(request.form.get("garage_size"))
        Location_Score = float(request.form.get("location_score"))
        Distance_to_Center = float(request.form.get("distance_to_center"))

        # Get the prediction using the predict_house function
        result = predict_house(
            Square_Feet=Square_Feet,
            Num_Bedrooms=Num_Bedrooms,
            Num_Bathrooms=Num_Bathrooms,
            Num_Floors=Num_Floors,
            Year_Built=Year_Built,
            Has_Garden=Has_Garden,
            Has_Pool=Has_Pool,
            Garage_Size=Garage_Size,
            Location_Score=Location_Score,
            Distance_to_Center=Distance_to_Center,
        )
        formatted_result = f"{result[0]:,.2f}"

        # Render the predict page and pass the result to display it
        return render_template("predict.html", prediction=formatted_result)

    # If GET request, just render the predict page without a prediction
    return render_template("predict.html")


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
