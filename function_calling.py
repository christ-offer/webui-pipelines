from blueprints.function_calling_blueprint import Pipeline as FunctionCallingBlueprint
import requests
from typing import Optional, List, Dict

class Pipeline(FunctionCallingBlueprint):
    class Valves(FunctionCallingBlueprint.Valves):
        # Add your custom valves here
        pass

    class Tools:
        def __init__(self, pipeline) -> None:
            self.pipeline = pipeline

        def query_wikidata(self, query: str) -> Optional[List[Dict]]:
            """
            Query Wikidata using a SPARQL query.

            :param query: The SPARQL query to execute.
            :return: A list of dictionaries representing the results, or None if there are no results.
            """

            url = "https://query.wikidata.org/sparql"
            headers = {"Accept": "application/json"}
            data = {"query": query}
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()  # Raises an HTTPError for bad responses

            results = response.json()["results"]["bindings"]
            if results:
                return results
            else:
                return None

    def __init__(self):
        super().__init__()

        # Optionally, you can set the id and name of the pipeline.
        # Best practice is to not specify the id so that it can be automatically inferred from the filename, so that users can install multiple versions of the same pipeline.
        # The identifier must be unique across all pipelines.
        # The identifier must be an alphanumeric string that can include underscores or hyphens. It cannot contain spaces, special characters, slashes, or backslashes.
        # self.id = "my_tools_pipeline"
        self.name = "My Tools Pipeline"
        self.valves = self.Valves(
            **{
                **self.valves.model_dump(),
                "pipelines": ["*"],  # Connect to all pipelines
            },
        )
        self.tools = self.Tools(self)
