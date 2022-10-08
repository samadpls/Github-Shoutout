import streamlit as st
import requests,random,time
from deta import Deta
Key="d0ioznr7_BVwahBf955uXB5p76Y3R4py3RxC8Adhw" # Project key
deta = Deta(Key)
    # Base key
db= deta.Base("usernames")    

st.set_page_config(page_title="Github Shoutout",page_icon="images/githublogo.png",layout="centered",initial_sidebar_state="auto") # setting the page config    

def verifying(username):
    if username:
        try:
            api_url = f"https://api.github.com/users/{username}" # api url
            response = requests.get(api_url) # get response
            data =  response.json() # parse data as json

            if db.get(username):
                st.warning("Username already exists")                    
            elif data["followers"]!=0 or data["following"]!=0: # if followers or following is not zero    
                db.put({"key":username.lower()}) # add entryin database with key lowercase username
                st.success("Username stored in database.") 
            else:
                st.error("Sorry, you don't have followers")
        except Exception as e: # if username is not valid
            print(e)
            st.error("Invalid github username")

def random_username(): 
    names = db.fetch().items
    github_username=list(names[random.randint(0,len(names)-1)].values())[0]
    try:
        api_url = f"https://api.github.com/users/{github_username}" # api url
        response = requests.get(api_url)
        data =  response.json()
        acc_link=data['html_url'] 
        st.markdown(f"""<div id='container'><img id='pfp' src="https://github.com/{github_username}.png" alt="github profile pic"/> 
            <h3>Name:&nbsp;&nbsp; {data['name']}</h3>
            <p id="bio">Bio:&nbsp;&nbsp; {data['bio']}</p>
            <p id="ff">Followers: &nbsp;&nbsp; {data["followers"]} &nbsp;&nbsp; &nbsp;&nbsp;| &nbsp;&nbsp;  Following: &nbsp;&nbsp; {data["following"]}</p>
            <table>
            <tr>
            <th>Stats</th>
            <th>Streak Color</th>
            <th>Languages</th>
            </tr>
            <tr>
            <td><img src='http://github-profile-summary-cards.vercel.app/api/cards/stats?username={github_username}&theme=github_dark' width=200px height=100px></td>
            <td><img src='https://streak-stats.demolab.com?user={github_username}&theme=github-dark&hide_border=true&border_radius=32&date_format=j%20M%5B%20Y%5D&ring=888888' width=180px height=100px></td>
            <td><img src='http://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username={github_username}&theme=github_dark' width= 200px height=100px></td>
            </tr>
            </table><br><br>
            <a target="_blank" href="{acc_link}">
                <button id='btn'>
                    Follow {github_username} on GitHub
                </button><br><br>
            </a></div>""",unsafe_allow_html=True)  #displaying the data
#         
    except Exception as e:
        st.error("Something went wrong, try again later")   



def main():
    st.markdown("""<a href='https://github.com/samadpls/Github-Shoutout'><img src='https://img.shields.io/github/stars/samadpls/Github-Shoutout?style=social'></a>""",unsafe_allow_html=True) 
    img , heading =  st.columns([1,8]) # using columns to display the heading and image
    with img:
        st.image("images/githublogo.png",width=70) # github logo
    with heading:
        st.markdown('# Shoutout to Github User')  # heading
    st.markdown("`Click on the button to see the profile`") # description

    
    if st.button("See Profile"):
        with st.spinner('Wait for it...'):
            time.sleep(2)
        random_username()
        
    
    #New username
    with st.expander("Add your profile  :"): # sub header
        text = st.empty()
        username=text.text_input("Enter your github username",max_chars=20) 
    st.markdown(""" `
    Made with 🤍 by samadpls
    `
    """) # footer

    verifying(username.strip())

if __name__=="__main__":
    with open('styles.css') as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True) # loading the css file
    main()
    
