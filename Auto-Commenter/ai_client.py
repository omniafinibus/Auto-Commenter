from ollama import Client
import logging as log

class AiClient:
    def __init__(self, model, host):
        self.model = model
        self.client = Client(host=host, headers={"x-some-header": "some-value"})

    def get_response(self, language, code):
        return self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": self.get_message(language, code),
                },
            ],
            stream=False,
            options={
                "temperature":0.3
            }
        )

    def get_message(self, language, code):
        log.debug(f"Creating message for the language: {language}")
        return "".join(
            [
                "The following code needs to be commented. It is "
                + str(language)
                + " code.\n",
                "**Do not change any functionality, syntax or variable names** and add comments to the full file. Only add comments!\n",
                "In case there is a discrepancy or issue in the code, do not change it, instead, say so in a comment at the top of the file.\n",
                "The code:\n",
                str(code),
                "\nI repeat, do not change any functionality and comment on the complete file. Print the updated code in 1 single code block enveloped in \"```\" in the response\n"
                
            ]
        )
