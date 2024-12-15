from django.shortcuts import render
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Formula
import re

def formula_editor(request):
    """
    Handles the formula editing view.

    This view processes POST requests to retrieve a formula from the request
    data and renders the 'editor.html' template with the formula and its LaTeX
    representation.

    Args:
        request: The HTTP request object containing method and POST data.

    Returns:
        HttpResponse: The rendered 'editor.html' template with context data.
    """
    formula = ""
    latex = ""
    if request.method == "POST":
        formula = request.POST.get("formula", "")
        latex = formula
    return render(request, "editor.html", {"formula": formula, "latex": latex})

def latex_tokenizer(text):
    """
    Tokenizes a given LaTeX string into a list of tokens.

    This function uses regular expressions to identify and extract LaTeX commands,
    numbers, operators, and other symbols from the input text.

    Parameters:
        text (str): The LaTeX string to be tokenized.

    Returns:
        list: A list of tokens extracted from the input text.
    """
    tokens = re.findall(r'\\[a-zA-Z]+|\d+|[+\-*/^=(),;]+|[a-zA-Z]+', text)
    return tokens

def cosine_similarity_latex(formula1, formula2):
    """
    Calculates the cosine similarity between two LaTeX formulas.

    This function uses a CountVectorizer with a custom LaTeX tokenizer to
    transform the input formulas into vector representations and then computes
    the cosine similarity between these vectors.

    Parameters:
        formula1 (str): The first LaTeX formula.
        formula2 (str): The second LaTeX formula.

    Returns:
        float: The cosine similarity score between the two formulas.
    """
    vectorizer = CountVectorizer(tokenizer=latex_tokenizer).fit_transform([formula1, formula2])
    return cosine_similarity(vectorizer[0], vectorizer[1])[0][0]

def comparator(request):
    """
    Handles the comparison of a given LaTeX formula against stored formulas.

    This view function processes a POST request containing a LaTeX formula,
    calculates the cosine similarity between the provided formula and each
    stored formula in the database, and identifies matches with a similarity
    score above 0.5. The matched formulas and their similarity scores are
    rendered in the 'comparator.html' template.

    Parameters:
        request (HttpRequest): The HTTP request object containing the formula.

    Returns:
        HttpResponse: The rendered 'comparator.html' template with the input
        formula and matched formulas with their similarity scores.
    """
    formula = ""
    matched_formulas = []
    similarity_scores = []

    if request.method == "POST":
        formula = request.POST.get("formula", "").strip()

        if formula:
            stored_formulas = Formula.objects.all()
            
            for formula_from_db in stored_formulas:
                similarity = cosine_similarity_latex(formula, formula_from_db.formula_text)
                
                if similarity > 0.7:
                    matched_formulas.append(formula_from_db)
                    similarity_scores.append(similarity)
    
    matched_formulas_with_scores = zip(matched_formulas, similarity_scores)
    
    matched_formulas_with_scores_list = list(matched_formulas_with_scores)
    sorted_matched_formulas_with_scores = sorted(matched_formulas_with_scores_list, key=lambda x: x[1], reverse=True)
    
    if not matched_formulas:
        sorted_matched_formulas_with_scores = 0

    return render(request, "comparator.html", {
        "formula": formula, 
        "matched_formulas_with_scores": sorted_matched_formulas_with_scores,
    })