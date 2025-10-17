# Spam Email Detection — Naive Bayes (Machine Learning)

This repository contains a simple, reproducible implementation of an email spam detection pipeline using the Naive Bayes classifier. The project uses the "Spam Email Classification" dataset from Kaggle and demonstrates data loading, preprocessing, model training, evaluation, and basic model export.

## Dataset

Source: Kaggle — "Spam Email Classification"
URL: https://www.kaggle.com/datasets/ashfakyeafi/spam-email-classification

The dataset is a collection of emails labeled as spam or ham (not spam). The CSV included in this repository (`data/email.csv`) is expected to follow the same structure as the Kaggle dataset.

## What is implemented

- Data loading and exploratory checks
- Text preprocessing (lowercasing, tokenization / simple cleanup)
- Feature extraction using TF-IDF (or CountVectorizer)
- Training a Multinomial Naive Bayes classifier
- Model evaluation using accuracy, precision, recall, F1, and confusion matrix
- Saving the trained model and vectorizer for later inference

## Repository structure

- `spam-detection.ipynb` — Jupyter notebook that walks through the end-to-end pipeline with code, visualizations and explanations. This is the recommended place to start.
- `data/email.csv` — dataset file (not tracked here if large). Should match the Kaggle dataset format (columns like `label` and `text` or `message`).
- `README.md` — this file

## Quickstart (recommended)

1. Clone the repository and open `spam-detection.ipynb` in Jupyter or VS Code to view the planned pipeline and notes.

## Model status and approach

This repository documents a planned Naive Bayes-based spam detection pipeline but does not include a trained model yet. The intended approach is:

- Preprocessing: clean and normalize email text (lowercasing, removing punctuation, basic tokenization).
- Feature extraction: represent text as token-count vectors or TF-IDF features.
- Classifier: Multinomial Naive Bayes, which models each class (spam/ham) by the distribution of token frequencies and uses Bayes' rule to compute the posterior probability of class membership for new messages.
- Evaluation: use accuracy, precision, recall and F1-score; inspect confusion matrix to evaluate false positives and false negatives.

The notebook contains examples and guidance to implement these steps when you're ready to train models.

## Assumptions and dataset specifics

- The CSV file `data/email.csv` contains at least a text column and a label column. Common column names in similar datasets are `text`/`message` and `label` (label values like `spam`/`ham` or `1`/`0`).
- If your column names differ, update the notebook or script accordingly.

## Reproducibility

- Set a random seed before training to ensure reproducible splits and model behavior (e.g., `random_state=42`).
- Save fitted `TfidfVectorizer` and the trained `MultinomialNB` model with `joblib.dump` so you can run inference later without retraining.

## Evaluation metrics to watch

- Accuracy
- Precision (spam detection: precision tells how many predicted spam messages were actually spam — important for avoiding false positives)
- Recall (how many actual spam messages were detected — important for catching spam)
- F1-score (harmonic mean of precision and recall)
- Confusion matrix (TP, FP, TN, FN)

## Implementation notes

The notebook outlines step-by-step code to implement the planned pipeline. If you want a script-based workflow instead of a notebook, you can extract the same steps into `train.py` and `predict.py` later. For reproducibility, set a random seed for data splits and persist the fitted feature extractor and classifier.

## Next steps / improvements

- Add `requirements.txt` and script(s) to train and run the model from the command line
- Implement and persist the vectorizer and Multinomial Naive Bayes model
- Improve preprocessing with stopword removal and lemmatization
- Experiment with other models and hyperparameter tuning
- Add tests and a small demo (web or CLI) for manual review

## License

This repository uses the Kaggle dataset which may have its own license — check the dataset page for licensing details. The code in this repository is provided under the MIT License unless otherwise specified.

## Contact

If you have questions, open an issue or contact the repository owner.

---

Updated: October 17, 2025
