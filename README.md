## Training and Running CoreML Models using GitHub Actions

Apple's [CoreML](https://developer.apple.com/documentation/coreml]) provides a way to run model predictions on iOS and OSX. Some parts of the libarary, such as the [model conversion tools](https://developer.apple.com/documentation/coreml/converting_trained_models_to_core_ml), can be run on non-Apple platforms, but the [prediction methods](https://developer.apple.com/documentation/coreml/mlmodel#2880473) will fail unless run on an iPhone (iOS) or Mac (OSX). This can present a problem for datascientists and developers without access to an Apple device.

Fortunately, [GitHub Actions](https://github.com/features/actions) provides macOS as a [virtual machine type](https://help.github.com/en/articles/workflow-syntax-for-github-actions#jobsjob_idruns-on) for running jobs. This makes it possible for developers to run CoreML predictions from inside a GitHub Actions workflow.

#### Training the model

First, we'll train an extremely simple [sklearn](https://scikit-learn.org/stable/) model and export it to CoreML: see [train.py](train.py) for details, or clone this repository and run:

```bash
pip install -r requirements.txt
python train.py 
```

This ingests known square footage and listing prices of some Seattle-area homes from [prices.csv](prices.csv), fits a linear regression, and exports [pricing.mlmodel](pricing.mlmodel).

#### Running a prediction

On iOS or OSX only, we can run [predict.py](predict.py), which ingests a list of square-footage values from [input.csv](input.csv) and uses [pricing.mlmodel](pricing.mlmodel) to generate and save a list of predicted prices as [output.csv](output.csv).

```bash
pip install coremltools
python predict.py
```

#### Setting up GitHub Actions

We can now [configure a sequence of actions](https://developer.github.com/actions/creating-github-actions/) to be triggered when specific files are pushed to our repository. We'll set up two separate workflows, both stored in [/.github/workflows](/.github/workflows):

- [train.yml](/.github/workflows/train.yml) will be executed whenever prices.csv or train.py changes, and will run train.py to generate a new pricing.mlmodel

- [predict.yml](/.github/workflows/predict.yml) will be executed whenever input.csv, predict.py, or pricing.mlmodel changes. It will run predict.py to generate a new output.csv

In addition, either job will be run if the job configuration file itself is changed, e.g.: 

```bash
on: 
  push:
    paths:
    - .github/workflows/predict.yml
    - input.csv
    - predict.py
    - pricing.mlmodel
```

Let's examine each section of the jobs/build section of predict.yml to better understand what's going on:

```bash
runs-on: macOS-latest
strategy:
  max-parallel: 1
  matrix:
    python-version: [3.6]
```

Here, we specify that this job will run in the latest OSX container, with Python 3.6 installed.

```bash
steps:
- uses: actions/checkout@v1
- name: Set up Python ${{ matrix.python-version }}
  uses: actions/setup-python@v1
  with:
    python-version: ${{ matrix.python-version }}
```

Our first steps check out the current repo and set up the specified Python.

```bash
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install coremltools
- name: Run predictions
  run: python predict.py
```

Next, we install our dependencies and run the prediction script.

```bash
- name: Commit changed output
  env:
    GITHUB_ACTOR: ${{ secrets.GITHUB_ACTOR }}
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    GITHUB_REPOSITORY: ${{ secrets.GITHUB_REPOSITORY }}
  run: |
    git remote set-url origin "https://$GITHUB_ACTOR:$GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY.git"
    git commit -m "updated predictions" output.csv
    git push origin HEAD:master
```

Lastly, we commit our changed file(s) back to the repo. This requires some backflips using [runtime variables](https://developer.github.com/actions/creating-github-actions/accessing-the-runtime-environment/), as our code inside the workflow has been automatically checked out on a [detached branch](http://marklodato.github.io/visual-git-guide/index-en.html#detached).

#### Try it yourself

Make sure you are signed up for the [GitHub actions](https://github.com/features/actions) Beta, then clone this repository and commit a change to the input.csv file. Click the "Actions" tab at the top of your repo to examine the run, then check to see if output.csv has changed.

Enjoy!  