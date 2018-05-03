# FaaS Composition Patterns

Companion examples to this conference talk:
https://kccnceu18.sched.com/event/Dqvm/function-composition-in-a-serverless-world-erwin-van-eyk-timirah-james-platform9-intermediate-skill-level

## Deploying

### Setup

You'll need a Kubernetes cluster setup, Fission installed, and Fission
Workflows installed.

### Install demo

```
fission env create --name python --image fission/python-env

fission spec apply
```

This will deploy all of the demo functions and triggers.

## Run the demo

Demo the vision function:

On a picture of text:

```
curl -X POST -d "url=https://raw.githubusercontent.com/fission/faas-composition-patterns/master/test-images/ocrtest.png" http://$FISSION_ROUTER/vision
Hej Verden!
```

On a picture of a cat:

```
curl -X POST -d "url=https://raw.githubusercontent.com/fission/faas-composition-patterns/master/test-images/cat.jpg" http://$FISSION_ROUTER/vision
cat
```

Run the translation function:

```
curl -X POST -d "text=Hej&to=en" http://$FISSION_ROUTER/translation
Hello
```

Now run any of the combined functions:

Using the _compiled_ function, Identify the cat picture and translate the label to Spanish:

```
curl -X POST -d "url=https://raw.githubusercontent.com/fission/faas-composition-patterns/master/test-images/cat.jpg&lang=es" http://$FISSION_ROUTER/compiled
gato
```

Using the _coordinator_, OCR a picture of text and translate it to English:

```
curl -X POST -d "url=https://raw.githubusercontent.com/fission/faas-composition-patterns/master/test-images/ocrtest.png&lang=en" http://$FISSION_ROUTER/coordinator
Hello World!
```

[There's a workflow function sample too under functions/workflow, but it's not tested yet]
