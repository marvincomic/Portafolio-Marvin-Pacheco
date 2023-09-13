import streamlit as st
st.set_page_config(page_title='Template' ,layout="wide",page_icon='👧🏻')

# Import necessary libraries
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, LLMPredictor, ServiceContext, LangchainEmbedding
# Llamaindex also works with langchain framework to implement embeddings to configure the Falcon-7B-Instruct model from Hugging Face 
from langchain.llms import HuggingFaceEndpoint
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain import HuggingFaceHub
from llama_index.prompts.prompts import SimpleInputPrompt


# Store the conversation history in a List
conversation_history = []

# load the file
documents = SimpleDirectoryReader(input_files=["data.txt"]).load_data()

PROMPT_QUESTION = """
    Your name is IBM Skills Network. You are providing the answer to the question based on the given context. Briefly introduce yourself first when you answer for the first time.
    Your conversation with the human is recorded in the chat history below. After the self-introduction, you don't need to repeat mentioning your name or introducing yourself actively. If the recruiter asks about the skills or experiences you have with url links, answer it with the link.
    
    History:
    "{history}"
    
    Now continue the conversation with the human. If you do not know the answer, politely ask for more information.
    Human: {input}
    Assistant:"""

# This will wrap the default prompts that are internal to llama-index
query_wrapper_prompt = SimpleInputPrompt(f"{PROMPT_QUESTION}<|USER|>{query_str}<|ASSISTANT|>")


llm = HuggingFaceEndpoint(
                endpoint_url= "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct" ,
                huggingfacehub_api_token="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", # Replace with your own API key or use ours: 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
                task="text-generation",
                temperature=0.7,
                model_kwargs = {
                    "max_new_tokens":250 # define the maximum number of tokens the model may produce in its answer. Int (0-250)       
                }
            )
    # LLMPredictor: to generate the text response (Completion)
llm_predictor = LLMPredictor(
        llm=llm,
        system_prompt=system_prompt, # added in llama-index by myself
        query_wrapper_prompt=query_wrapper_prompt # added in llama-index by myself
)
                                 
# Hugging Face models can be supported by using LangchainEmbedding to convert text to embedding vector	
embed_model = LangchainEmbedding(HuggingFaceEmbeddings())
# ServiceContext: to encapsulate the resources used to create indexes and run queries    
service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor, 
        embed_model=embed_model
)      
# build index
index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)


def ask_bot(input_text):
    # update conversation history
    global conversation_history
    history_string = "\n".join(conversation_history)
    print(f"history_string: {history_string}")  
    # query LlamaIndex and Falcon-7B-Instruct for the AI's response
    output = index.as_query_engine().query(PROMPT_QUESTION.format(history=history_string, input=input_text))
    print(f"output: {output}")   
    # update conversation history with user input and AI's response
    conversation_history.append(input_text)
    conversation_history.append(output.response)
    return output.response

# get the user's input by calling the get_text function
def get_text():
    input_text = st.text_input("You can send your questions and hit Enter to know more about me:)", key="input")
    return input_text

#st.markdown("Chat With Me Now")
user_input = get_text()

if user_input:
  #text = st.text_area('Enter your questions')
    st.info(ask_bot(user_input))


import requests
from streamlit_lottie import st_lottie

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
    
def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
        
local_css("style/style.css")

# Load animation assets
lottie_gif = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_x17ybolp.json")


python_lottie = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_2znxgjyt.json")
java_lottie = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_zh6xtlj9.json")
my_sql_lottie = load_lottieurl("https://assets4.lottiefiles.com/private_files/lf30_w11f2rwn.json")
git_lottie = load_lottieurl("https://assets9.lottiefiles.com/private_files/lf30_03cuemhb.json")
github_lottie = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_6HFXXE.json")
docker_lottie = load_lottieurl("https://assets4.lottiefiles.com/private_files/lf30_35uv2spq.json")
figma_lottie = load_lottieurl("https://lottie.host/5b6292ef-a82f-4367-a66a-2f130beb5ee8/03Xm3bsVnM.json")
js_lottie = load_lottieurl("https://lottie.host/fc1ad1cd-012a-4da2-8a11-0f00da670fb9/GqPujskDlr.json")

from constant import *

st.sidebar.markdown(info['Photo'],unsafe_allow_html=True)

def gradient(color1, color2, color3, content1, content2):
    st.markdown(f'<h1 style="text-align:center;background-image: linear-gradient(to right,{color1}, {color2});font-size:60px;border-radius:2%;">'
                f'<span style="color:{color3};">{content1}</span><br>'
                f'<span style="color:white;font-size:17px;">{content2}</span></h1>', 
                unsafe_allow_html=True)

with st.container():
    col1,col2 = st.columns([8,3])

with col1:
    gradient('#FFD4DD','#000395','e0fbfc',"Hi, I'm Cognitive Class👋", "https://cognitiveclass.ai/")
    st.write("")
    st.write(info['About'])
    
with col2:
    st_lottie(lottie_gif, height=280, key="data")

with st.container():
    st.subheader('⚒️ Skills')
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        st_lottie(python_lottie, height=70,width=70, key="python", speed=2.5)
    with col2:
        st_lottie(java_lottie, height=70,width=70, key="java", speed=4)
    with col3:
        st_lottie(my_sql_lottie,height=70,width=70, key="mysql", speed=2.5)
    with col4:
        st_lottie(git_lottie,height=70,width=70, key="git", speed=2.5)
    with col1:
        st_lottie(github_lottie,height=50,width=50, key="github", speed=2.5)
    with col2:
        st_lottie(docker_lottie,height=70,width=70, key="docker", speed=2.5)
    with col3:
        st_lottie(figma_lottie,height=50,width=50, key="figma", speed=2.5)
    with col4:
        st_lottie(js_lottie,height=50,width=50, key="js", speed=1)


from streamlit_timeline import timeline

with st.container():
    st.markdown("""""")
    st.subheader('📌 Career Snapshot')
    # Load data
    with open('example.json', "r") as f:
        data = f.read()
    # Render timeline
    timeline(data, height=400)

import streamlit.components.v1 as components
    
with st.container():
    st.markdown("""""")
    st.subheader("📊 Tableau")
    col1,col2 = st.columns([0.95, 0.05])
    with col1:
        with st.expander('See the work'):
            components.html(
                """
                <!DOCTYPE html>
                <html>  
                    <title>Basic HTML</title>  
                    <body style="width:130%">  
                        <div class='tableauPlaceholder' id='viz1684205791200' style='position: static'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Su&#47;SunnybrookTeam&#47;Overview&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='SunnybrookTeam&#47;Overview' /><param name='tabs' value='yes' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Su&#47;SunnybrookTeam&#47;Overview&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1684205791200');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.minWidth='1350px';vizElement.style.maxWidth='100%';vizElement.style.minHeight='1550px';vizElement.style.maxHeight=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.minWidth='1350px';vizElement.style.maxWidth='100%';vizElement.style.minHeight='1550px';vizElement.style.maxHeight=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.minHeight='5750px';vizElement.style.maxHeight=(divElement.offsetWidth*1.77)+'px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
                    </body>  
                </HTML>
                """
            , height=400, scrolling=True
            )
    st.markdown(""" <a href={}> <em>🔗 access to the link </a>""".format(info['Tableau']), unsafe_allow_html=True)

with st.container():
    st.markdown("""""")
    st.subheader('✍️ Medium')
    page = requests.get(info['Medium'])
    col1,col2 = st.columns([0.95, 0.05])
    with col1:
        with st.expander('Display my latest posts'):
            components.html(embed_rss['rss'],height=400)
            
        st.markdown(""" <a href={}> <em>🔗 access to the link </a>""".format(info['Medium']), unsafe_allow_html=True)

with st.container():
    col1,col2,col3 = st.columns([0.475, 0.475, 0.05])
        
    with col1:
        st.write("---")
        st.subheader("💬 See how my coworker describe me:")
        components.html(
        """
        <!DOCTYPE html>
        <html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {box-sizing: border-box;}
            .mySlides {display: none;}
            img {vertical-align: middle;}

            /* Slideshow container */
            .slideshow-container {
            position: relative;
            margin: auto;
            width: 100%;
            }

            /* The dots/bullets/indicators */
            .dot {
            height: 15px;
            width: 15px;
            margin: 0 2px;
            background-color: #6F6F6F;
            border-radius: 50%;
            display: inline-block;
            transition: background-color 0.6s ease;
            }

            .active {
            background-color: #eaeaea;
            }

            /* Fading animation */
            .fade {
            animation-name: fade;
            animation-duration: 1s;
            }

            @keyframes fade {
            from {opacity: .4} 
            to {opacity: 1}
            }

            /* On smaller screens, decrease text size */
            @media only screen and (max-width: 300px) {
            .text {font-size: 11px}
            }
            </style>
        </head>
        <body>
            <div class="slideshow-container">
                <div class="mySlides fade">
                <img src="https://user-images.githubusercontent.com/90204593/238169843-12872392-f2f1-40a6-a353-c06a2fa602c5.png" style="width:100%">
                </div>

                <div class="mySlides fade">
                <img src="https://user-images.githubusercontent.com/90204593/238171251-5f4c5597-84d4-4b4b-803c-afe74e739070.png" style="width:100%">
                </div>

                <div class="mySlides fade">
                <img src="https://user-images.githubusercontent.com/90204593/238171242-53f7ceb3-1a71-4726-a7f5-67721419fef8.png" style="width:100%">
                </div>

            </div>
            <br>

            <div style="text-align:center">
                <span class="dot"></span> 
                <span class="dot"></span> 
                <span class="dot"></span> 
            </div>

            <script>
            let slideIndex = 0;
            showSlides();

            function showSlides() {
            let i;
            let slides = document.getElementsByClassName("mySlides");
            let dots = document.getElementsByClassName("dot");
            for (i = 0; i < slides.length; i++) {
                slides[i].style.display = "none";  
            }
            slideIndex++;
            if (slideIndex > slides.length) {slideIndex = 1}    
            for (i = 0; i < dots.length; i++) {
                dots[i].className = dots[i].className.replace("active", "");
            }
            slides[slideIndex-1].style.display = "block";  
            dots[slideIndex-1].className += " active";
            }

            var interval = setInterval(showSlides, 1200); // Change image every 1.2 seconds

            function pauseSlides(event)
            {
                clearInterval(interval); // Clear the interval we set earlier
            }
            function resumeSlides(event)
            {
                interval = setInterval(showSlides, 1200);
            }
            // Set up event listeners for the mySlides
            var mySlides = document.getElementsByClassName("mySlides");
            for (i = 0; i < mySlides.length; i++) {
            mySlides[i].onmouseover = pauseSlides;
            mySlides[i].onmouseout = resumeSlides;
            }
            </script>

            </body>
            </html> 

            """,
                height=270,
    )

    with col2:
        st.write("---")
        st.subheader("📨 Get in touch with me!")

        contact_form = """
        <form action="https://formsubmit.co/email@gmail.com" method="POST">
            <input type="hidden" name="_captcha value="false">
            <input type="text" name="name" placeholder="Your name" required>
            <input type="email" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Your message here" required></textarea>
            <button type="submit">Send</button>
        </form>
        """
        st.markdown(contact_form, unsafe_allow_html=True)

footer="""
<div class="footer">
<p>Developed with Streamlit by <a href="https://cognitiveclass.ai/" target="_blank">IBM Skills Network</a></p></div>
""".format(foot['url'])
st.markdown(footer,unsafe_allow_html=True)
