# [Team Code for Impact - Hack n Lead](https://womenplusplus.ch/hacknlead)

## Description
See the `docs` folder for a full description of our product.

### Context

How do you measure impact? This is a problem many non-profits, especially non-profits in the social sphere, face every day. In an age where data-driven decisions are the gold standard for decision-making, how do you measure your success when financial returns do not necessarily factor into the equation? Non-profits face increasing pressure to demonstrate the impact they have in order to receive support from the government, sponsors, and the community at large. So how can this be done? That is the question you will seek to answer as part of the women++ challenge for Hack’n’Lead.
 
### Challenge Description

The aim of this challenge is for you to create a software solution to support non-profit organizations in defining and tracking their impact.
While your solution ideally is built in a way that allows sufficient customization to cater to a diverse range of organizations, we are conscious of the fact that this is an ambitious goal to begin with. Therefore, it may help you to narrow down your target audience both geographically as well as by topic. So you may for instance want to develop an impact tracker app for non-profits dedicated to increasing diversity in the Swiss tech industry.

### Solution - ImpactDash

Based on the above needs, objectives and the characteristics of the persona, we decided to create a comprehensive solution:

1. We have identified the indicators that can most effectively show the impact of activities.
2. We propose the data needed for the indicators and have prepared questionnaires for this purpose.
3. We created a dashboard for organisations to track and analyse the information collected.

## Technical info

The application is built using Streamlit. To generate your own dashboard:
1. Fork the repo
2. Create your environment using conda or venv
3. run `pip3 install -r requirements.txt`
4. The data used in the dashboard are gathered via a Google Survey. 
	A template of the google survey can be found in the `docs`
5. Save the results of the survey as a .csv to the `data` folder.
6. Follow the directions [here](https://docs.streamlit.io/library/get-started/create-an-app) to deploy your app

To see our dashboard, click on the Streamlit link to deploy the application

Link to [Streamlit app](https://impact-hack-n-lead-2023.streamlit.app/)

Link to [Figma](https://www.figma.com/file/JB0Vxd091qpjainY9I4umJ/Wow-Design-System?type=design&node-id=2403-111&mode=design)   
