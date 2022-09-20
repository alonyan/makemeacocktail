import os
import logging

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
logging.basicConfig(filename='logfile.log', level=logging.INFO)


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        cocktail = request.form["cocktail"]
        app.logger.info(cocktail)
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_prompt(cocktail),
            temperature=1,
            max_tokens=150
        )
        app.logger.info(response)
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(cocktail):
    return """Create a cocktail recipe based on a list of ingredients. Try to be creative and come up with new cocktails and interesting names.

Ingredients: Gin, Watermelon
Recipe: Waterloo Sunset: 7 leaves mint, .5 oz sugar syrup, 1 oz Szechuan Peppercorn–Infused Plymouth Gin, 1 oz Beefeater London Dry Gin, .5 oz Dolin Blanc Vermough, 1.5 oz watermelon juice, 0.75 oz lime juice. Muddle mint, shake with all remaining ingredients. Double rocks glass with large rock, Mint sprig.
Ingredients: Taquila, Lime
Recipe: Margarita : 2 oz Taquila, 1 oz lime, 1 oz cointreau. Shaken, up, in a coup with salted rim.
Ingredients: Rye, dry vermouth, maraschino
Recipe: Brooklyn: 2 oz rye, 1 oz dry vermouth, 1/4 oz maraschino, 1/4 oz Amaro Averna, 2 ds orange bitters. Stirred, up, coupe, cherry.
Ingredients: Rum, curacao, lime
Recipe: Mai tai: 1.5 oz white rum, 0.75 oz curacao, 0.75 oz lime juice, 0.5 oz orgeat. Shaken, low ball, crushed ice. Dark rum float, mint sprig.
Ingredients: Rum
Recipe: 12 Mile limit: 1 oz rum, 0.5 oz rye, 0.5 oz cognac, 0.5 oz lemon juice, 0.5 oz grenadine. Shaken up in Nick and nora.
Ingredients: Lime, gin, campari
Recipe: Jungle rose: 1 oz Gin, 1 oz Campari, 1 oz passionfruit syrup, 1 oz lime juice, 0.5 oz grenadine. Shaken open pour into highball. Straw.
Ingredients: {}
Recipe:""".format(
        cocktail.capitalize()
    )
