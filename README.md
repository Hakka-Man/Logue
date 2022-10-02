# hackmit2022

Setup guide:

1. Install pytorch
   conda install pytorch torchvision torchaudio -c pytorch

2. Install other dependencies
   pip install soundfile transformers datasets sounddevice scipy

3. Install Streamlit
   conda install streamlit
   
4. Install Phoenimizer
   pip install phoenimzer
   
5. Install espeak
   brew install espeak
   

Stutters are roughly 1% of the world’s population, around 70 million people. Depending on the condition’s severity, stuttering can significantly hamper one’s ability to do presentations, talk to strangers, or even just chat with friends, leading to psychological and self-esteem issues. As a stutterer myself, I want to leverage the power of AI and NLP to provide support for the stutterer community. 

Currently, there isn’t any concrete cure for stuttering. Conventional speech therapists are often hard to access and expensive. Some private institutions have also released heftily priced programs to “solve stuttering”. We offer a simple way for stutterers to train in an intelligent way.

In the first step, the user would read and record a curated text that would allow our program to analyze the phonemes that the stutterers are struggling with. We use a transformer-based ASR approach to convert the user’s speech into phonemes.  Then we use a vectorization algorithm to compare the user’s speech with the ground truth. (the phonemes of the text prompt).

After figuring out the weaknesses of the user, we would show that information to the user and generate a personalized practice text with Spacy NLP methods. The text would contain words with the phonemes that the user is struggling with. The sentences don’t have to mean anything semantically, but we made the text grammatically correct to make it a realistic practice material. The users would be able to practice and analyze their results with our program. 

