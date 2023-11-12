import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import random
import sys
import glob

from PIL import Image
image_path = "womanplusplus_logo.png"
image = Image.open(image_path)

st.set_page_config(
    page_title="Women++ Dashboard",
    page_icon=image,
    layout="wide",
)

title_container = st.container()
col1, col2 = st.columns([1, 20])
with title_container:
    with col1:
        st.image(image, width=80)
    with col2:
        st.markdown('<h1 style="color: #15065B;">Women++ ImpactDash</h1>',
                    unsafe_allow_html=True)

# dashboard title
#st.title("Women++ ImpactDash")

#read in data and combine into one df
csvs = glob.glob('data/*.csv')
dfs = [pd.read_csv(csv) for csv in csvs]
df_all = pd.concat(dfs)


#preprocessing - rename columns
df_all.columns=['user_id',
            'event',
            'nps',
            'transition',
            'connection',
            'volunteering',
            'soft_skills',
            'confidence',
            'comm_partner',
            'other']

def find_count_norm(df:pd.DataFrame, column:str)->pd.DataFrame:
    """
    filters a dataframe on the columnn name, where the column name is one of the questions in the survey
    then finds the count and normalized count for the response

    df: pandas DataFrame
    column: column name in the dataframe, must be one of the questions
    """
    filtered_df = df.copy()

    # df with just the question
    filtered_df = filtered_df[['user_id', 'event', column]]

    # get the list of events in the df

    events = filtered_df['event'].unique().tolist()

    new_df = pd.DataFrame()
    for event in events:
        test1=filtered_df[filtered_df['event']==event]
        #print(test1.head(3))

        q_name=test1.columns[1]

        norm = (test1[column].value_counts(normalize=True)*100).astype(int).reset_index()

        norm = (test1[column].value_counts(normalize=True)*100).astype(int).reset_index()
        #print(norm)
        
        count = test1[column].value_counts().reset_index()
        #print(count)
        count['event']=event

        df_temp=norm.merge(count, on=column, how='inner')
        #print(df_temp)

        new_df=pd.concat([new_df, df_temp], ignore_index=True)

    return new_df

#create event_list
event_list = df_all.event.unique().tolist()
if len(event_list)>1:
    event_list.append('all')
event_list=set(event_list)



# nps question
st.header("How likely would you recommend this event to someone")


nps_df = find_count_norm(df_all,'nps')


# create a dropdown menu to select the event
col1,col2=st.columns([10,20])
with col1:
    event = st.selectbox(
            "Select event",
            event_list,
        )

#st.dataframe(nps_df.head(3))

# if all is selected in the dropdown menu, create a streamlit figure which shows both bootcamp and hackathon data in one figure, with score on x-axis and count on y-axis and event as color
if event == 'all':
    fig = px.bar(nps_df, x=nps_df.columns[0], y='proportion', color='event')
    st.plotly_chart(fig)
else:
    fig = px.bar(nps_df, x=nps_df.columns[0], y='proportion')
    st.plotly_chart(fig)

if event != 'all':
    ### net promoter score
    st.subheader('Net promoter score')

    def nps_scores(x):
        if x>=9:
            return "Promote"
        elif x>=7:
            return "Passive"
        else:
            return "Detractor"

    def nps_value(dataframe,column):
        promo = dataframe.copy()
        promo = promo[promo['event']==column]
        # st.dataframe(promo)
        # promo['normed'] = (promo['count']/promo['count'].sum())*100
        promo['score']=promo['proportion'].apply(nps_scores)
        #st.dataframe(promo)
        net_score=promo.score.value_counts(normalize=True)*100
        net_score = net_score.to_frame().reset_index()
        #st.dataframe(net_score)
        net_value = net_score.loc[net_score['score']=='Promote', 'proportion'].item()- net_score.loc[net_score['score']=='Detractor', 'proportion'].item()
        #st.write(net_value)
        net_value = int(net_value)
        return net_value
        #return promo

    column_name=event

    net_promoter_score = nps_value(nps_df,column_name)
    #st.dataframe(nps_df.head())
    st.write(net_promoter_score)

    if net_promoter_score<=0:
        st.write('Most participants would not recommend this event.')
    else:
        st.write('Most participants would recommend this event.')



### transition question

st.header("How helpful was this event on your transition into the tech industry")

transition_df = find_count_norm(df_all,'transition')


# create a dropdown menu to select the event
col1,col2=st.columns([10,20])
with col1:
    event = st.selectbox(
            "Select event",
            event_list,
            key='q2'
        )

#st.dataframe(transition_df.head(3))

# if all is selected in the dropdown menu, create a streamlit figure which shows both bootcamp and hackathon data in one figure, with score on x-axis and count on y-axis and event as color
if event == 'all':
    fig = px.bar(transition_df, x=transition_df.columns[0], y='proportion', color='event')
    st.plotly_chart(fig)
else:
    fig = px.bar(transition_df, x=transition_df.columns[0], y='proportion')
    st.plotly_chart(fig)



### connection question

st.header("I made a connection with participants/recruiters/mentors that can help me transition into the tech sector")

connection_df = find_count_norm(df_all,'connection')


# create a dropdown menu to select the event
col1,col2=st.columns([10,20])
with col1:
    event = st.selectbox(
            "Select event",
            event_list,
            key='q3'
        )


# if all is selected in the dropdown menu, create a streamlit figure which shows both bootcamp and hackathon data in one figure, with score on x-axis and count on y-axis and event as color
if event == 'all':
    fig = px.bar(connection_df, x=connection_df.columns[0], y='proportion', color='event')
    st.plotly_chart(fig)
else:
    fig = px.bar(connection_df, x=connection_df.columns[0], y='proportion')
    st.plotly_chart(fig)


### volunteering question
st.header("How likely would you volunteer for a women++ event in the future")

volunteering_df = find_count_norm(df_all,'volunteering')


# create a dropdown menu to select the event
col1,col2=st.columns([10,20])
with col1:
    event = st.selectbox(
            "Select event",
            event_list,
            key='q4'
        )


# if all is selected in the dropdown menu, create a streamlit figure which shows both bootcamp and hackathon data in one figure, with score on x-axis and count on y-axis and event as color
if event == 'all':
    fig = px.bar(volunteering_df, x=volunteering_df.columns[0], y='proportion', color='event')
    st.plotly_chart(fig)
else:
    fig = px.bar(volunteering_df, x=volunteering_df.columns[0], y='proportion')
    st.plotly_chart(fig)


### confidence question
st.header("How much did the event boost your confidence in your ability to successfully transition into the tech industry")

confidence_df = find_count_norm(df_all,'confidence')


# create a dropdown menu to select the event
col1,col2=st.columns([10,20])
with col1:
    event = st.selectbox(
            "Select event",
            event_list,
            key='q5'
        )


# if all is selected in the dropdown menu, create a streamlit figure which shows both bootcamp and hackathon data in one figure, with score on x-axis and count on y-axis and event as color
if event == 'all':
    fig = px.bar(confidence_df, x=confidence_df.columns[0], y='proportion', color='event')
    st.plotly_chart(fig)
else:
    fig = px.bar(confidence_df, x=confidence_df.columns[0], y='proportion')
    st.plotly_chart(fig)





# # create a new chart which shows the bar charts for both events side by side
# fig = px.bar(df_all_grouped, x='score', y='count', color='event', facet_col='event')
# st.plotly_chart(fig)

# # create a new chart which shows bars with events stacked for each score
# fig = px.bar(df_all_grouped, x='score', y='count', color='event', barmode='stack')
# st.plotly_chart(fig)

# # create a new chart which shows the bar charts for both events with bars side by side for each event and each score <---------
# fig = px.bar(df_all_grouped, x='score', y='count', color='event', barmode='group')
# st.plotly_chart(fig)

# # create a new chart which shows the bar charts for both events: each score showing the count for each event
# fig = px.bar(df_all_grouped, x='event', y='count', color='score')
# st.plotly_chart(fig)

# # create a new chart which shows all the data in a heatmap
# fig = px.density_heatmap(df_all, x='event', y='score')
# st.plotly_chart(fig)

# # Question: 'How did you hear about this event?' (multiple choice: Facebook, Instagram, LinkedIn, Twitter)
# # Create a new dataframe with 200 rows of data, 100 rows for event bootcamp and 100 rows for hack event, where the column multi_choice has a list of 1 to 4 options randomly selected from the 4 options
# # data = []
# # for i in range(1, 101):
# #     data.append({'user_id': i, 'event': 'bootcamp', 'multi_choice': random.sample(['Facebook', 'Instagram', 'LinkedIn', 'Twitter'], random.randint(1, 4))})
# # for i in range(1, 101):
# #     data.append({'user_id': i, 'event': 'hack', 'multi_choice': random.sample(['Facebook', 'Instagram', 'LinkedIn', 'Twitter'], random.randint(1, 4))})
# # df_multi_choice = pd.DataFrame(data)
# # # save df_multi_choice to csv file
# # df_multi_choice.to_csv('multi_choice.csv', index=False)

# # load data from csv file 'multi_choice.csv' in a dataframe 'df_multi_choice'
# df_multi_choice = pd.read_csv('multi_choice.csv')

# # create a donut chart with the dataframe 'df_multi_choice' by aggregating by platform and according to the event selected
# # create a new dataframe 'df_multi_choice_event' with data from the selected event
# df_multi_choice_event = df_multi_choice[df_multi_choice['event'] == event]

# # count the number of times each platform is selected within each list in the column 'multi_choice'
# df_multi_choice_event['Facebook'] = df_multi_choice_event['multi_choice'].apply(lambda x: x.count('Facebook'))
# df_multi_choice_event['Instagram'] = df_multi_choice_event['multi_choice'].apply(lambda x: x.count('Instagram'))
# df_multi_choice_event['LinkedIn'] = df_multi_choice_event['multi_choice'].apply(lambda x: x.count('LinkedIn'))
# df_multi_choice_event['Twitter'] = df_multi_choice_event['multi_choice'].apply(lambda x: x.count('Twitter'))

# # create a new dataframe 'df_multi_choice_event_grouped' by grouping dataframe by platform
# df_multi_choice_event_grouped = df_multi_choice_event.groupby(['event']).sum().reset_index()

# # drop columns user_id and multi_choice from dataframe 'df_multi_choice_event_grouped'
# df_multi_choice_event_grouped = df_multi_choice_event_grouped.drop(columns=['user_id', 'multi_choice'])

# print(df_multi_choice_event_grouped)

# # create a bar chart with the dataframe 'df_multi_choice_event_grouped'
# fig = px.bar(df_multi_choice_event_grouped, x='event', y=['Facebook', 'Instagram', 'LinkedIn', 'Twitter'])
# st.plotly_chart(fig)



# # create a donut graph with the dataframe 'df_multi_choice_event_grouped' where the values are the sum of the number of times each platform is selected
# fig = px.pie(df_multi_choice_event_grouped, values=[10, 20, 30, 40], names=['Facebook', 'Instagram', 'LinkedIn', 'Twitter'], hole=.3)
# st.plotly_chart(fig)
# """





