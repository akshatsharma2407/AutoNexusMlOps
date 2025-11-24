AutoNexus | AI Powered Car Market Place
==============================

This repo will be used for end to end mlops cycle, from experiment tracking, data pipeline to CI/CD, docker and aws service.

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

## Project Workflow

![AutoNexus MLOps Workflow](https://github.com/akshatsharma2407/my_portfolio/blob/main/images/flowdiag.png)

---

## Application Screenshots

<table>
  <tr>
    <td align="center">
      <strong>Home Page</strong><br/>
      <img src="https://github.com/akshatsharma2407/my_portfolio/blob/main/images/main_page1.png" alt="AutoNexus Home Page" width="400"/>
    </td>
    <td align="center">
      <strong>Prediction/Blogs & Insights</strong><br/>
      <img src="https://github.com/akshatsharma2407/my_portfolio/blob/main/images/main_page2.png" alt="AutoNexus Dashboard" width="400"/>
    </td>
  </tr>
  <tr>
    <td align="center">
      <strong>Price Prediction Form</strong><br/>
      <img src="https://github.com/akshatsharma2407/my_portfolio/blob/main/images/prediction.png" alt="Price Prediction Page" width="400"/>
    </td>
  </tr>
</table>

---

## DVC Pipeline

![DVC Pipeline workflow on Dagshub](https://github.com/akshatsharma2407/my_portfolio/blob/main/images/dvc_pipeline.png)

---

## Experiment Tracking – DagsHub & MLflow

![DagsHub MLflow Tracking](https://github.com/akshatsharma2407/my_portfolio/blob/main/images/mlflow_ui.png)

---

## Optuna Dashboard

![Optuna for HyperParameter tuning & tracking results](https://github.com/akshatsharma2407/my_portfolio/blob/main/images/optuna.png)

---
