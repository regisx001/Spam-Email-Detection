# Spam Email Detection — Naive Bayes (Machine Learning)

This repository contains an implementation of an email spam detection pipeline using the Naive Bayes classifier. The project demonstrates data loading, preprocessing, feature extraction, model training, and evaluation. The implementation is provided in a Jupyter notebook for clarity and reproducibility.

## Dataset

Source: Kaggle — "Spam Email Classification"
URL: https://www.kaggle.com/datasets/ashfakyeafi/spam-email-classification

The dataset contains emails labeled as spam or ham (not spam). The CSV file `data/email.csv` is expected to follow the same structure as the Kaggle dataset.

## What is implemented

- **Data Loading**: Load and explore the dataset to understand its structure.
- **Data Preprocessing**: Clean and normalize email text (lowercasing, removing punctuation, filtering stopwords).
- **Feature Extraction**: Create a vocabulary and vectorize messages using token counts.
- **Model Training**: Train a Multinomial Naive Bayes classifier using the vectorized data.
- **Model Evaluation**: Evaluate the classifier using metrics like accuracy, precision, recall, and F1-score.
- **Testing**: Test the classifier with sample messages to predict whether they are spam or ham.

## Repository Structure

- `spam-detection.ipynb` — Jupyter notebook containing the full implementation, including code, explanations, and outputs.
- `data/email.csv` — Dataset file (not included in the repository; download from Kaggle).
- `README.md` — Project documentation (this file).

## Quickstart

1. Clone the repository and open `spam-detection.ipynb` in Jupyter or VS Code.
2. Install dependencies (recommended to use a virtual environment):

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If `requirements.txt` is not present, install the essentials:

```bash
pip install numpy pandas scikit-learn nltk jupyter
```

3. Run the notebook cells sequentially to execute the pipeline.

## Methodology

### Naive Bayes Classifier

The Naive Bayes classifier is based on Bayes' theorem and assumes independence between features. For this project:

- **Preprocessing**: Emails are cleaned and tokenized to remove noise.
- **Feature Extraction**: Token counts are used to represent messages numerically.
- **Training**: The classifier learns the probability of each word given the spam and ham classes.
- **Prediction**: For a new message, the classifier calculates the posterior probability for each class and predicts the class with the highest probability.

### Evaluation Metrics

- **Accuracy**: Overall correctness of predictions.
- **Precision**: Proportion of predicted spam messages that are actually spam.
- **Recall**: Proportion of actual spam messages that are correctly identified.
- **F1-Score**: Harmonic mean of precision and recall.

## Next Steps / Improvements

- Add `requirements.txt` for dependency management.
- Implement a script-based workflow (`train.py`, `predict.py`) for CLI usage.
- Enhance preprocessing with techniques like lemmatization and bigram features.
- Experiment with other classifiers (e.g., Logistic Regression, SVM).
- Build a web-based demo using Flask or FastAPI.

## License

This repository uses the Kaggle dataset, which may have its own license. Check the dataset page for details. The code in this repository is provided under the MIT License unless otherwise specified.

## Contact

If you have questions, open an issue or contact the repository owner.

---

Updated: October 21, 2025
