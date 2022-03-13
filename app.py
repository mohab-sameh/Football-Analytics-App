import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots



st.title('Internationa Football matches')
df = pd.read_csv("assets//datasets//international-football-results//results.csv")


st.subheader('Comparing 2 teams')
teams_to_compare = st.multiselect('Pick your teams', df['home_team'].unique())


comparison = df[(df['home_team'].isin(teams_to_compare)) & (df['away_team'].isin(teams_to_compare)) ]  
comparison = comparison.reset_index(drop=True)
st.write(comparison)
st.write('Number of matches: ', len(comparison))



#stop app if no comparison exists
if len(comparison['home_score']) == 0:
    st.stop()


st.subheader('Highest intensity of play')
out_c = comparison.iloc[np.argmax(np.array(comparison['home_score']+comparison['away_score']))]
st.write(out_c)





team1_w = 0
team2_w = 0
teams_draw=0
team1_cum=[]
team2_cum=[]

for i in range(len(comparison)):
    if comparison['home_team'][i]==teams_to_compare[0]:
        if comparison['home_score'][i]>comparison['away_score'][i]:
            team1_w+=1
            team1_cum.append(1)
            team2_cum.append(0)
        elif comparison['home_score'][i]<comparison['away_score'][i]:
            team2_w+=1
            team1_cum.append(0)
            team2_cum.append(1)
        else:
            teams_draw+=1
            team1_cum.append(0)
            team2_cum.append(0)
    else:
        if comparison['home_score'][i]<comparison['away_score'][i]:
            team1_w+=1
            team1_cum.append(1)
            team2_cum.append(0)
        elif comparison['home_score'][i]>comparison['away_score'][i]:
            team2_w+=1
            team1_cum.append(0)
            team2_cum.append(1)
        else:
            teams_draw+=1
            team1_cum.append(0)
            team2_cum.append(0)
            
            
            
comparison_labels = ['Team 1 wins','Team 2 wins','Draws']
comparison_values = [team1_w, team2_w, teams_draw]
fig5 = go.Figure(data=[go.Pie(labels=comparison_labels, values=comparison_values)])
st.plotly_chart(fig5)





st.subheader('Cumulative wins of two teams')
 
fig6 = go.Figure()
 
fig6.add_trace(go.Scatter(x=list(df['date']), y=np.cumsum(np.array(team1_cum)), name='team 1'))
fig6.add_trace(go.Scatter(x=list(df['date']), y=np.cumsum(np.array(team2_cum)), name='team 2'))
 
 
# Add range slider
     
fig6.update_layout(
    xaxis=go.layout.XAxis(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)
 
st.plotly_chart(fig6)




st.subheader('Frequency of city of matches')
 
cities = comparison.groupby('city').count()['country'].index.values
occurrences = comparison.groupby('city').count()['country'].values
occurrences.sort()
 
 
fig7 = go.Figure(go.Bar(
            x=occurrences,
            y=cities,
            orientation='h'))
 
 
st.plotly_chart(fig7)





st.subheader('Tournament information')
if len(comparison['home_score']) == 0:
    st.text("non monsieur")
comparison['challenge']=np.array(comparison['home_score']+comparison['away_score'])
fig8 = px.scatter(comparison, x="home_score", y="away_score",
             size="challenge", color="tournament",
                 hover_name="home_team")
 
st.plotly_chart(fig8) 




tour = st.selectbox('Select a tournament', comparison['tournament'].unique())
 
comparison_t = comparison[comparison['tournament']==tour] 
per = len(comparison_t)/len(comparison)
 
st.write(f"{round(per*100,2)}% of matches between the 2 teams have been played as {tour} matches")