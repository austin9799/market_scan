import re
from google import genai
from google.genai import types


class LLMHandler:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._setup()
    
    def _setup(self) -> None:
        self.client = genai.Client(api_key=self.api_key)

    def get_analysis(self, sys_prompt: str, prompt: str = None):
        try:

            parts, chunks = [], []

            if prompt:
                parts.append(types.Part.from_text(text = prompt))

            contents = [
                types.Content(
                    role="user",
                    parts=parts,
                ),
            ]

            tools = [
                types.Tool(google_search=types.GoogleSearch())
            ]

            generate_content_config = types.GenerateContentConfig(
                tools=tools,
                response_mime_type="text/plain",
                system_instruction=sys_prompt
            )

            content_stream = self.client.models.generate_content_stream(
                model="gemini-2.0-flash",
                contents=contents,
                config=generate_content_config,
            )

            for chunk in content_stream:
                chunks.append(chunk)

            if chunks:
                parsed_response = self.format_google_search_analysis(chunks)
            else:
                parsed_response = None
            
            return parsed_response
        except Exception as e:
            return "We Are Facing An Issue, Please Try Again!!"
        
    def format_google_search_analysis(self, chunks: list):
            cited_response = ""

            for chunk in chunks:
                cited_response = cited_response + chunk.text

            grounding_metadata = chunks[-1].candidates[0].grounding_metadata

            if grounding_metadata is not None:
                grounding_chunks = chunks[-1].candidates[0].grounding_metadata.grounding_chunks
                grounding_supports = chunks[-1].candidates[0].grounding_metadata.grounding_supports

            if grounding_metadata is not None and grounding_supports:
                cited_response = self.cite_response(cited_response, grounding_supports)

                if grounding_chunks is not None:
                    cited_response = self.add_clickable_citations(cited_response, grounding_chunks)
                    cited_response += "\nSources:<br/>"
                    for i, chunk in enumerate(grounding_chunks):
                        cited_response += f"{i+1}.\t[{chunk.web.title}]({chunk.web.uri})\n <br/>"

            return cited_response
    
    def add_clickable_citations(self, response: str, grounding_chunk_list):
        def replace_citation(match):
            citation_index = int(match.group(1)) - 1  
            if 0 <= citation_index < len(grounding_chunk_list):
                grounding_chunk = grounding_chunk_list[citation_index]
                if grounding_chunk.web and grounding_chunk.web.uri:
                    uri = grounding_chunk.web.uri
                    return f"[{match.group(1)}]({uri})"  
            return match.group(0)  

        modified_text = re.sub(r'\[(\d+)\]', replace_citation, response)
        return modified_text

    def cite_response(self, response: str, grounding_details):
        cited_response = response

        for i, detail in enumerate(grounding_details):
            text = detail.segment.text
            grounding_chunk_indices = [int(index) + 1 for index in detail.grounding_chunk_indices]
            grounding_chunk_index_str = ", ".join([f"[[{index}]]" for index in grounding_chunk_indices])

            cited_response = cited_response.replace(text, text + " " + grounding_chunk_index_str)

        return cited_response
        
            