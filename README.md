# Blockchiain_assigment2
Source: 
Chat GPT 5. 
https://www.geeksforgeeks.org/python/create-simple-blockchain-using-python
https://www.youtube.com/watch?v=G5M4bsxR-7E
https://www.youtube.com/watch?v=alNU9AVWkQk

How to run:
- You will need to install the require library for this. To do that copy and paste the text below into your terminal: 
    - pip install -r requirements.txt 
- After installing successfully.

- To run:
    - Go to terminal and paste in "uvicorn main:app --reload" 
    - It will take a few seconds to run, then this will show up http://127.0.0.1:8000/docs. 
    - Copy and paste the link on to your browsers or you can  click the link (don't worry the link is safe!!). 
    - Note: uvicorn must be running in order for you to access the link and test out the features.

How to test:
- When you the link above. It will direct you to a page of all the feature.
- At the bottom. Click on the /load API endpoint, then on the left side click "Try it Out"
    - Run the existing blockchain that I've created
- After that you can try out all the different features.
- Remember if you have made any changes such as adding new block or creating new transactions remember to save it 
    - Use the /save endpoint. 
    - Else if you rerun the API, without using the /save endpoint, no changes will be updated.