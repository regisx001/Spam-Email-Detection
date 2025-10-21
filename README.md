# Spam Email Detection using Naive Bayes

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68%2B-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org)

<img width="1906" height="900" alt="Screenshot from 2025-10-21 22-55-53" src="https://github.com/user-attachments/assets/78badcbc-4b8f-4897-8fb8-6bbbb7a9b874" />
A comprehensive spam email detection system built with **Multinomial Naive Bayes** classifier, featuring both interactive Jupyter notebook implementation and production-ready REST API. This project demonstrates the complete machine learning pipeline from data preprocessing to model deployment.


## Project Overview

This repository implements an end-to-end spam detection solution that can:

- Train a custom Naive Bayes classifier from scratch
- Evaluate model performance with comprehensive metrics
- Serve predictions through a REST API
- Handle both single and batch email classifications

### Technical Highlights

- **Algorithm**: Multinomial Naive Bayes with Laplace smoothing
- **Features**: Bag-of-words with stopword filtering and length-based pruning
- **Evaluation**: Precision, Recall, F1-Score, and Confusion Matrix analysis
- **Deployment**: FastAPI-based REST API with automatic documentation
- **Storage**: Pickle-based model persistence for production use

## Dataset

**Source**: [Kaggle - Spam Email Classification](https://www.kaggle.com/datasets/ashfakyeafi/spam-email-classification)

The dataset contains labeled email messages classified as:

- **Ham**: Legitimate emails
- **Spam**: Unwanted/promotional emails

Expected format: CSV file with `Category` and `Message` columns.

## Repository Structure

```
spam-detection/
├── spam-detection.ipynb      # Complete ML pipeline with explanations
├── api.py                    # FastAPI REST API implementation
├── requirements.txt          # Python dependencies
├── data/
│   └── email.csv             # Training dataset (download from Kaggle)
├── models/
│   └── spam_classifier_model.pkl  # Trained model (generated)
└── README.md                 # This file
```

## Quick Start

### Option 1: Jupyter Notebook (Recommended for Learning)

1. **Clone and Setup**

   ```bash
   git clone https://github.com/regisx001/Spam-Email-Detection.git
   cd spam-detection
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Download Dataset**

   - Download from [Kaggle](https://www.kaggle.com/datasets/ashfakyeafi/spam-email-classification)
   - Place as `data/email.csv`

3. **Run Notebook**
   ```bash
   jupyter notebook spam-detection.ipynb
   ```

### Option 2: API Server (Production Ready)

1. **Complete Setup Above** (Steps 1-2)

2. **Train Model** (run notebook once to generate model file)

3. **Start API Server**

   ```bash
   python api.py
   # Or manually: uvicorn api:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access API**
   - **API**: http://localhost:8000
   - **Documentation**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/health

## API Documentation

### Endpoints

| Method | Endpoint         | Description                             |
| ------ | ---------------- | --------------------------------------- |
| `GET`  | `/`              | API information and available endpoints |
| `GET`  | `/health`        | Health check and model status           |
| `GET`  | `/model-info`    | Model statistics and configuration      |
| `POST` | `/predict`       | Classify single email message           |
| `POST` | `/predict-batch` | Classify multiple emails at once        |

### Usage Examples

#### Single Prediction

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"message": "FREE! Win money now! Limited offer!"}'
```

#### Batch Prediction

```bash
curl -X POST "http://localhost:8000/predict-batch" \
     -H "Content-Type: application/json" \
     -d '["FREE money!", "Hello friend, how are you?", "WINNER! Call now!"]'
```

#### Python Client Example

```python
import requests

# Single prediction
response = requests.post(
    "http://localhost:8000/predict",
    json={"message": "Congratulations! You won $1000!"}
)
result = response.json()
print(f"Prediction: {result['prediction']} (confidence: {result['confidence']:.3f})")
```

## Model Architecture

### Preprocessing Pipeline

1. **Text Normalization**: Lowercase conversion
2. **Punctuation Removal**: RegEx-based cleaning
3. **Tokenization**: Whitespace-based word splitting
4. **Stopword Filtering**: English stopwords removal
5. **Length Filtering**: Remove words ≤ 3 characters

### Feature Engineering

- **Vocabulary**: Unique words from training corpus
- **Vectorization**: Bag-of-words representation
- **Dimensionality**: ~6,000-8,000 features (dataset dependent)

### Classification Algorithm

- **Model**: Multinomial Naive Bayes
- **Smoothing**: Laplace (add-1) smoothing
- **Training**: Maximum likelihood estimation of word probabilities
- **Prediction**: Posterior probability comparison using Bayes' rule

## Performance Metrics

The model is evaluated using standard classification metrics:

- **Accuracy**: Overall prediction correctness
- **Precision**: Spam detection accuracy (minimize false positives)
- **Recall**: Spam capture rate (minimize false negatives)
- **F1-Score**: Harmonic mean of precision and recall
- **Confusion Matrix**: Detailed prediction breakdown

Typical performance (dataset dependent):

- Accuracy: ~95-98%
- Precision: ~92-96%
- Recall: ~85-92%
- F1-Score: ~88-94%

## Testing

Run the test suite to validate API functionality:

```bash
python test_api.py
```

This will test:

- API health and model loading
- Individual message classification
- Batch processing capabilities
- Error handling and edge cases

## Configuration

### Environment Variables

```bash
# Optional: Customize API settings
export API_HOST=0.0.0.0
export API_PORT=8000
export MODEL_PATH=models/spam_classifier_model.pkl
```

### Model Parameters

Modify in notebook for experimentation:

- `min_word_length`: Minimum word length (default: 3)
- `smoothing_factor`: Laplace smoothing parameter (default: 1)
- `train_test_split`: Data split ratio (default: 0.8/0.2)

## Future Improvements

### Short Term

- [ ] **Enhanced Preprocessing**
  - Stemming/Lemmatization integration
  - N-gram features (bigrams, trigrams)
  - TF-IDF weighting scheme
- [ ] **Model Improvements**
  - Cross-validation implementation
  - Hyperparameter optimization
  - Feature selection techniques

### Medium Term

- [ ] **Alternative Algorithms**
  - Logistic Regression comparison
  - Support Vector Machine implementation
  - Ensemble methods (Random Forest, Gradient Boosting)
- [ ] **Production Features**
  - Model versioning and A/B testing
  - Performance monitoring and alerting
  - Automated model retraining pipeline

### Long Term

- [ ] **Advanced Features**
  - Deep learning approaches (LSTM, BERT)
  - Multi-language support
  - Real-time stream processing
- [ ] **Integration & Deployment**
  - Docker containerization
  - Kubernetes orchestration
  - CI/CD pipeline with automated testing
- [ ] **User Interface**
  - Web-based GUI for easy testing
  - Admin dashboard for model monitoring
  - Email client plugin integration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Dataset License**: The Kaggle dataset may have its own license terms. Please check the [dataset page](https://www.kaggle.com/datasets/ashfakyeafi/spam-email-classification) for specific licensing information.

## Contact & Support

- **Repository**: [https://github.com/regisx001/Spam-Email-Detection](https://github.com/regisx001/Spam-Email-Detection)
- **Issues**: [Report bugs or request features](https://github.com/regisx001/Spam-Email-Detection/issues)
- **Discussions**: [Community discussions and Q&A](https://github.com/regisx001/Spam-Email-Detection/discussions)

## Acknowledgments

- **Dataset**: Thanks to [Ashfak Yeafi](https://www.kaggle.com/ashfakyeafi) for the spam email dataset
- **Inspiration**: Classical machine learning approaches for text classification
- **Tools**: Built with Python, FastAPI, NumPy, Pandas, and NLTK

---

**If you find this project helpful, please give it a star!**

_Last updated: October 21, 2025_
