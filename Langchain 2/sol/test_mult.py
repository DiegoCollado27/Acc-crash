class MultiRag_creator:
    """ This class is used to create a MultiRag object that can be used to run the RAG model on a given input text.

    Args:
        custom_prompt (str): The custom prompt that the user wants to use.
        model (str): The model that the user wants to use. The default model is "gpt-4-turbo".
        api_key (str): The api key that the user wants to use. The default api key is None.

    Attributes: 
        model (str): The model that the user wants to use. The default model is "gpt-4-turbo".
        api_key (str): The api key that the user wants to use. The default api key is None.
        prompt (str): The custom prompt that the user wants to use.
        chat_chain (ChatPromptTemplate The chat chain that the user wants to use.
        llm (ChatOpenAI): The ChatOpenAI object that the user wants to use.

    """
    def __init__(self,custom_prompt=None, model="gpt-4-turbo", api_key=None):
        if model == "gpt-4-turbo":
            self.model = "gpt-4-turbo"
        
        if api_key == None:
            self.api_key = os.getenv("API_KEY")
        if custom_prompt != None:
            self.prompt = custom_prompt
            self.chat_chain = ChatPromptTemplate.from_template(self.prompt)
        
        self.llm = ChatOpenAI(model=self.model, api_key=self.api_key, temperature=1.5)

        self.chat_chain = ChatPromptTemplate.from_template(template="""
        Could you help me with a programming question? Your goal is to simply rephrase that question. Please respond using the new phrasing of the question, and make sure your response is clear and concise.
        Example 1:
        User: I need to figure out how to iterate over a list in Python
        Assistant: How can I loop through each element in a Python list
                                                             
        Example 2:
        User: What's the best method to connect to a database using Java?
        Assistant: Could you explain how to establish a connection to a database in Java     

        This is the question to rephrase:  {question}                                                
""")
        
    def create_rag(self):
        """ This function is used to create a MultiRag object that can be used to run the RAG model on a given input text."""
        self.chain = self.chat_chain | self.llm | StrOutputParser()

    def run_rag(self, input_text):
        """ This function is used to rewrite a question on a given input text."""
        return self.chain.invoke(input_text)
    
    def sim_search_rag(self,query, iters=1):
        """ This function creates a list of vectordb prompts"""
        self.create_rag()
        self.rag_list = []
        for i in range(iters):
            previous_output = self.rag_list
            self.rag_list.append(self.run_rag(query + str(previous_output)))

        return self.rag_list
    
    def beautify_response(self, question, context, llm_prompt=None):
        """ This function is used to beautify the response from the VectorStore using an llm."""
        # Create the prompt chain based on whether a custom prompt is provided
        if llm_prompt is None:
            self.llm_prompt_chain = ChatPromptTemplate.from_template(
                """You will be given a context that is useful for answering a question. You need to provide a response to a question basing exclusively on the context given.
                Question: {question}
                Context: {context}""")
        else:
            
            self.llm_prompt_chain = ChatPromptTemplate.from_template(llm_prompt)

        # Invoke the prompt template with provided question and context
        prompt_result = self.llm_prompt_chain.invoke({"question": question, "context": context})

       
        self.llm_chain =  self.llm | StrOutputParser()

        # Execute the chain
        return self.llm_chain.invoke(prompt_result)
