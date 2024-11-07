from langchain_core.pydantic_v1 import BaseModel
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

class DateExtractionChain(object):

    class Dates(BaseModel):
        date: str = Field(description="Date of the question on the format '''Year-Month-Day'''", default=None)

    def __init__(self, date:str, day:str, llm:BaseModel, llm_kwds:dict = {}):
        self.llm = llm(**llm_kwds)
        self.date = date
        self.day = day
        self.parser = JsonOutputParser(pydantic_object=self.Dates)
        self.prompt = PromptTemplate(
            template="Given the user input below and todays date '" + self.date + "' \
                and the day of week is '" + self.day + "', extract the date of request.\
                date dictionary:\n{format_instructions}\n{input}\n",
            input_variables=["input"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )
    
    def init_chain(self):
        return self.prompt | self.llm | self.parser

class ChainClassifier(object):
    """
    A classifier for categorizing text using a language model.

    Attributes:
        llm (LanguageModel): The shared language model used for classification.
        classes (list): A list of class labels.
        descriptions (str): A string containing descriptions for each class.
        classifier: The initialized classifier object.
    """
    def __init__(self, classes:list, descriptions:str, llm:BaseModel, llm_kwds:dict = {}):
        self.llm = llm(**llm_kwds)
        self.classes = classes
        self.descriptions = descriptions
        self.classifier = self.init_chain()


    
    def init_chain(self):
        classes = ", ".join([f"`{item}`" for item in self.classes[:-1]]) + f", or `{self.classes[-1]}`"
        return (PromptTemplate.from_template(
                "Given the user input below, classify it as either being about \
                    " + classes + ".\
                    based on the following description: " + self.descriptions + ". \
                    Do not respond with more than one word.\
                    <input>\
                    {input}\
                    </input>\
                    Classification:"
                )
                | self.llm
                | StrOutputParser()
            )