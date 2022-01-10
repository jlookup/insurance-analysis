# insurance-analysis
An app for tracking healthcare events and insurance costs.
Used to compare my Insurance options with my employer for 2022.

Built as an exercise in test-driven development


## Modes of Use

### Track
Use to keep tabs on your healthcare costs and insurance plan status. 
Saves your plan definition and history to peristent storage to be accessed and updated each time you launch the app.


### Compare
Use to compare multiple plan options and their costs.
Loads several plan definitions and a calendar of potential healthcare services, and compares the costs between plans.


## Plan Definitions
Plan definitions are loaded via a .yml file. By default the app will look in the root directory for 'plan.yml' when launched in Track mode or 'plan-comparison.yml' when launched in Compare mode, but you can specify a different file with the ```-p | --plan-definition``` option flag when launching the app. 

Below is the format for the plan definition. Notice each expense category has either a 'payment', 'copay', or 'coinsurance' element. 

```name: 'Test Plan'
deductable: 6350
out_of_pocket_max: 6850
categories:
  premium:
    name: 'premium'
    payment: 200
  pcp:
    name: 'pcp'
    copay: 25
    deductable_applies: False
  specialist: 
    name: 'specialist'
    coinsurance: 0.2 
    deductable_applies: True
  prescription: 
    name: 'prescription'
    copay: 45
    deductable_applies: False
  test: 
    name: 'test'
    coinsurance: 0.2 
    deductable_applies: True```

To compare plans, include all plan definitions in one file, separated by three dashes `---`