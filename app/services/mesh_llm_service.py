import os

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


class MeshLLMService:


    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv(
                "MESH_API_KEY"
            ),
            base_url="https://api.meshapi.ai/v1"
        )


        self.model = (
            "tencent/hy3"
        )


    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ):

        response = (
            self.client.chat.completions.create(

                model=self.model,

                messages=[

                    {
                        "role": "system",
                        "content": system_prompt,
                    },

                    {
                        "role": "user",
                        "content": user_prompt,
                    }

                ],

                temperature=0.4,

            )
        )


        return (
            response
            .choices[0]
            .message
            .content
        )


mesh_llm_service = MeshLLMService()