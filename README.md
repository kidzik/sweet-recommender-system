# Sweet Recommender System

## Data

**Data and analysis available at https://github.com/kidzik/sweetrs-analysis**

BibTeX

```
@article{kidzinski2017sweetrs,
  title={SweetRS: Dataset for a recommender systems of sweets},
  author={Kidzi{\'n}ski, {\L}ukasz},
  journal={arXiv preprint arXiv:1709.03496},
  year={2017}
}
```

## Website

Available at http://sweetrs.org/

## About

The main goal of this project is to create collaborative-filtering dataset
and test various algorithms of recommendation.

In order to install it, make sure you have installed:
- django >= 1.2
- python >= 2.5

Using debian packages simply run:
$ apt-get install python-django

After cloning the repository type
$ cd sweet-recommender-system/src/sweetrs
$ python manage.py syncdb
$ python manage.py runserver

and enjoy your recommendation system on
http://localhost:8000

Feel free to contribute with adding new recommendation algorithms.
